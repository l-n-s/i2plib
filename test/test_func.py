import unittest
import asyncio

import i2plib
import i2plib.sam

BUFFER_SIZE = 65536

SERVER_DEST_B64 = "5pJLIgm7KCqk-d0As66OdeMRj4moqtD97wOluQh5SXWCbeMfp7cr8cgHU~5rrcN6V~QcIJuqjDpYWojBdjYrc7fAA3iwWpN4fzI05yvE48oOOOLqBq7SvkpyzIhjc0hv81XQIu0LWzXXS~-B61wurJhte-LisF571BzefV5xoaRN8y3A0RidaJyuzVufPP4cKY5NeSsmTY36QRl54PG7iWJSXnLROROlg6qsjoeIV9lyNFY6ZsQKTQzEIInCZaARmNfoJP-MAsOMoj-CRDU2MXhYT~DKdI-rWH579A3wuoEjmlHtHyms7xvwUkb6kIx5UJHZmzF2Hyv3xVrpu0HSkZfUIbzz1lAc4IZ-8jnBjt2RIRpYMNnwZW09HjJXQDd7K-QvpxpK-cqNJcmWehGP7OxLt9Jj6h~8aUFHIJtFI77Zmp~YGf7cO9vCZexeLn7iByqDtfhzTP62IPu0~MJafA4efU83A-DXo8PJhOhl7rYRzH7bWRzB1rhBI~w~TsVOBQAEAAcAAL0me7gfS2H-OZ3FAsPtbUFCFpTcvfLAzBmNxxYU5TflB4KcxNe2isp2UjM7YLCuZg6OCaBSEnoag-ABpJPkY0WIjkqbFzOlowH2oVwevFHrZCFwvf1XVXsyWdupACHmmRHFCHKHMKzolO3Cye0RMH0wIEyMRyIszSThft~keXWyuEwBM4Vros-OKrKN-mBrHNbzQzTiGLS0dVMzdPvG6Pq4t1~wCWqAXrO8n7xU-xQECEpl053Ml5AJyUaCoVj3xqCd4nbrH2~kLmvd9r2nnd-Ig19BFHNALadSYbcH9JEdJZPY~7c505W1xhsrM2PcNnE4hm8DF4R~AddaILD7b2d1l~kehRZpUKdCL~THPTM20kTyN2PFqghIA4Ng-tVmXw=="
CLIENT_DEST_B64 = "Fyax0ON9-Djvy5G7z7ZRyyu7vjK9-dcg4ei94Lnfd1IEI8DqQj3PTytWql-rltRmeMg9pRAm3XqpTNcGR0a26KR3cFNIwRgCKCQ3BOU8bNZQXpaWEpfhoOGKd5Nt9~qI6M3kFcbv8WWVtlPCNEnzjPbXhr0XLuttYFdOPuCDlzxXEHe8NVMTAhXKiuBox7c8zRB~WT6AMJxedf9u3nXLQOYV~ZT-4-xoHcbp1zwbRnvYJ0yjBNprmaac5xo1Zu~k9q93ug3S08FwwjioDswTl9ZyEJkrxTtaUdH~OwCKRVmXhP-HIKMXeBdDRrPFGBKPe-igAyuIdD5zYlgJwxkYsZAvU8XeQRpck7krFhLSgGez8zlpgZi7oUdbYMC6BpqZpDLppWCl9bOz5tX55gd3nbWEYb0DDlVyCAhBkfznUvmOlHmdcAHGS-B7e4WTi0yRb76hRrecHiX2tqDI7UGTAlTIx0TGW3Pa7gMImb5bV5n5TsYw7qBJABgMPSP6MkjtAAAAfn2Z9dSDlwpIVfjzxqhq7lY9So5O0PYFIFYshZhNim7R6nXJbn-QX9DoZ7JGEx9uXndWu6tEApY6q1OGAeXhjEnHagF1o13GpqZ4wgYuOehaq1fmJyFoeYQToHiBsXyo1FE1GeGV8JYJLOWHLKuxay9Nh84yyJ6XJGgylElqnl4WGiwqc0qsAk7l209agFggMCyqCx~nSFMtfGZ2pKp-i7H3HQC9BM0SednWiVsgRPGG20Z-WoQtHTvj5~VUhIbXpa1BGj~sOydi27A3xQPQYtEXhhfWKRGs7pAaobfaUeSnQ12a09LXO8U53eGPioVdSbTMOTqkuWhGEuXebx9DxV3hUdopRSpKSnCT6U9Fc5GpqRKk"

SERVER_DEST = i2plib.Destination(SERVER_DEST_B64, has_private_key=True)
CLIENT_DEST = i2plib.Destination(CLIENT_DEST_B64, has_private_key=True)

SESSION_DEST_MAP = {"ppserver": SERVER_DEST_B64, "ppclient": CLIENT_DEST_B64}

async def fake_sam_server_handler(reader, writer):
    session = None
    data_transfer = False

    while True:
        data = await reader.read(BUFFER_SIZE)
        if not data: break

        if not data_transfer:
            msg = i2plib.sam.Message(data.split(b"\n")[0].decode())

            if msg.cmd == "HELLO":
                writer.write(b"HELLO REPLY RESULT=OK VERSION=3.1\n")
            elif msg.cmd == "NAMING" and msg.action == "LOOKUP":
                writer.write("NAMING REPLY RESULT=OK NAME=ME VALUE={}\n".format(
                    SERVER_DEST.base64).encode())
            elif msg.cmd == "SESSION" and msg.action == "CREATE":
                session = msg["ID"]
                writer.write("SESSION STATUS RESULT=OK DESTINATION={}\n".format(
                    SESSION_DEST_MAP[session]).encode())
            elif msg.cmd == "STREAM" and msg.action == "ACCEPT":
                session = msg["ID"]
                if session == "ppserver":
                    writer.write(b"STREAM STATUS RESULT=OK\n")
                    await asyncio.sleep(0.1)
                    writer.write("{}\n".format(CLIENT_DEST.base64).encode())
                    await asyncio.sleep(0.1)
                    data_transfer = True
                    writer.write(b"PING")
            elif msg.cmd == "STREAM" and msg.action == "CONNECT":
                session = msg["ID"]
                if session == "ppclient":
                    writer.write(b"STREAM STATUS RESULT=OK\n")
                    data_transfer = True
        else:
            if data == b"PING":
                writer.write(b"PONG")

    writer.close()

class TestFuncPingPong(unittest.TestCase):

    def setUp(self):
        self.sam_address = ("127.0.0.1", 19132)
        self.loop = asyncio.new_event_loop()

    async def runner(self, coro, *args, **kwargs):
        sam_server = await asyncio.start_server(
            fake_sam_server_handler, *self.sam_address, loop=self.loop)

        await coro(*args, **kwargs)

        sam_server.close()
        await sam_server.wait_closed()

        for t in asyncio.Task.all_tasks(loop=self.loop):
            if t != asyncio.Task.current_task(loop=self.loop):
                await t

    def test_coroutines_ping_pong(self):
        async def coroutines_test():
            _, server_session_writer = await i2plib.create_session("ppserver",
                sam_address=self.sam_address, loop=self.loop, destination=SERVER_DEST)
            server_reader, server_writer = await i2plib.stream_accept("ppserver", 
                sam_address=self.sam_address, loop=self.loop)

            _, client_session_writer = await i2plib.create_session("ppclient", 
                sam_address=self.sam_address, loop=self.loop)
            client_reader, client_writer = await i2plib.stream_connect("ppclient",
                    SERVER_DEST.base32 + ".b32.i2p", sam_address=self.sam_address, loop=self.loop)

            client_writer.write(b"PING")
            incoming = await server_reader.read(BUFFER_SIZE)
            dest, request = incoming.split(b"\n", 1)
            remote_destination = i2plib.Destination(dest.decode())
            self.assertEqual(remote_destination.base32, CLIENT_DEST.base32)
            if not request:
                request = await server_reader.read(BUFFER_SIZE)
            self.assertEqual(request, b"PING")
            server_writer.write(b"PONG")
            response = await client_reader.read(BUFFER_SIZE)
            self.assertEqual(response, b"PONG")

            client_writer.close()
            server_writer.close()
            server_session_writer.close()
            client_session_writer.close()

        self.loop.run_until_complete(self.runner(coroutines_test))

    def test_context_managers_ping_pong(self):
        async def context_managers_test():
            async def server(sam_address, loop, ready):
                async with i2plib.Session("ppserver", sam_address=sam_address, loop=loop, destination=SERVER_DEST):
                    ready.release()
                    async with i2plib.StreamAcceptor("ppserver", sam_address=sam_address, loop=loop) as s:
                        incoming = await s.read(BUFFER_SIZE)
                        dest, request = incoming.split(b"\n", 1)
                        remote_destination = i2plib.Destination(dest.decode())
                        self.assertEqual(remote_destination.base32, CLIENT_DEST.base32)
                        if not request:
                            request = await s.read(BUFFER_SIZE)
                        self.assertEqual(request, b"PING")
                        s.write(b"PONG")

            ready = asyncio.Lock(loop=self.loop)
            await ready.acquire()
            server_task = asyncio.ensure_future(server(self.sam_address, self.loop, ready), loop=self.loop)
            await ready.acquire()

            async with i2plib.Session("ppclient", sam_address=self.sam_address, loop=self.loop):
                async with i2plib.StreamConnection("ppclient", 
                        SERVER_DEST.base32 + ".b32.i2p", sam_address=self.sam_address, loop=self.loop) as c:
                    c.write(b"PING")
                    response = await c.read(BUFFER_SIZE)
                    self.assertEqual(response, b"PONG")

            await server_task

        self.loop.run_until_complete(self.runner(context_managers_test))

    def tearDown(self):
        self.loop.stop()
        self.loop.close()

