# It's All Ghosts - GhostText server for any editor
# Copyright (c) 2017 Dominik George <nik@naturalnet.de>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import asyncio
from contextlib import closing
import json
import os
import socket
import sys
from tempfile import mkstemp

import aiohttp
from aiohttp import web
from xdg import XDG_CONFIG_HOME, XDG_RUNTIME_DIR

# Address to bind on
LISTEN_ADDRESS = '127.0.0.1'

# Editor to spawn
EDITOR = ['uxterm', '-e', 'nano']
# If user's own script exists, call that
USERSCRIPT = os.path.join(XDG_CONFIG_HOME, 'itsallghosts_cmd')
if os.path.exists(USERSCRIPT):
    EDITOR = ['sh', USERSCRIPT]

def free_port():
    """ Get a random free port """

    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.bind(('127.0.0.1', 0))
        return sock.getsockname()[1]

def owner_of_port(port):
    """ Get the owning user id of a TCP connection """
    import psutil

    # Get connection matching port
    conns = psutil.net_connections()
    matches = [conn for conn in conns if conn.laddr.ip == '127.0.0.1' and conn.laddr.port == port]

    if matches:
        # Find user id holding socket with port
        conn = matches[0]
        pid = conn.pid
        process = psutil.Process(pid)
        uid = process.uids().real
        return uid

async def handle_get(request):
    # Determine whether this is WebSockets or not
    try:
        ws = web.WebSocketResponse()
        await ws.prepare(request)
    except:
        # This is not a WebSocket connection

        if os.getuid() == 0:
            # Determine user's port (if running as root, so multi-user mode)
            client_port = request.transport.get_extra_info('peername')[1]
            uid = owner_of_port(client_port)
            # FIXME correctly get user's runtime dir
            port_filen = os.path.join('/run', 'user', str(uid), 'itsallghosts-port')
            with open(port_filen, 'r') as port_fileh:
                port = int(port_fileh.read())
        else:
            port = 4001
        # Assemble initial JSON response
        res = {'ProtocolVersion': 1, 'WebSocketPort': port}
        return web.json_response(res)

    fileh, filen, process = None, None, None

    # Continue WebSockets conversation
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            # Handle editor information
            data = json.loads(msg.data)
            source = (data['url'], data['title'])
            text = data['text']

            # Check if fiel is already known
            if not fileh:
                # Create new tempfile and start subprocess
                fileh, filen = mkstemp(suffix='itsallghosts')

            # Write text to file
            with open(filen, 'w') as fileh2:
                fileh2.write(text)

            # Check if process is already running
            if not process:
                # Start subprocess and wait for termination
                process = await asyncio.create_subprocess_exec(*EDITOR, filen)
                await process.wait()

                # Unset process to detect exit later
                process = None

                # Get contents of file and send text change event
                with open(filen, 'r') as fileh2:
                    text = fileh2.read()
                res = {'text': text}
                await ws.send_str(json.dumps(res))

                # Close WebSocket connection
                await ws.close()

    # Clean up
    if fileh:
        os.close(fileh)
        os.unlink(filen)
    if process:
        process.terminate()

    return ws

def main():
    # Set up the main HTTP server
    http_app = web.Application()
    http_app.router.add_get('/', handle_get)
    port = 4001

    # Randomise port if run as separate user process
    if len(sys.argv) > 1 and sys.argv[1] == '--user':
        port = free_port()

    # Store port in user's run directory
    if os.getuid() != 0:
        port_filen = os.path.join(XDG_RUNTIME_DIR, 'itsallghosts-port')
        with open(port_filen, 'w')as port_fileh:
            port_fileh.write(str(port))

    # Run web server
    web.run_app(http_app, host=LISTEN_ADDRESS, port=port)

if __name__ == '__main__':
    main()
