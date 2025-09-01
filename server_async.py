"""
server_async.py - Asyncio TCP Echo Server
-----------------------------------------
Event-loop based echo server using asyncio streams.
Run:
    python3 server_async.py --host 0.0.0.0 --port 5051
"""

import argparse
import asyncio

async def handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter, bufsize: int):
    peer = writer.get_extra_info("peername")
    # print(f"[server-async] connection from {peer}")
    try:
        while True:
            data = await reader.read(bufsize)
            if not data:
                break
            writer.write(data)
            await writer.drain()
    finally:
        writer.close()
        await writer.wait_closed()
        # print(f"[server-async] closed {peer}")

async def main():
    parser = argparse.ArgumentParser(description="Asyncio TCP echo server")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=5051)
    parser.add_argument("--bufsize", type=int, default=4096)
    args = parser.parse_args()

    server = await asyncio.start_server(
        lambda r, w: handle(r, w, args.bufsize),
        host=args.host, port=args.port, reuse_address=True
    )
    addr = ", ".join(str(s.getsockname()) for s in server.sockets)
    print(f"[server-async] listening on {addr}")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
