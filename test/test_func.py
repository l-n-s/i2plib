import unittest
import asyncio
import os

import i2plib
import i2plib.sam
import i2plib.utils
import i2plib.tunnel

BUFFER_SIZE = 65536
REAL_SAM = os.getenv("REAL_SAM")

SERVER_DEST_B64 = "5pJLIgm7KCqk-d0As66OdeMRj4moqtD97wOluQh5SXWCbeMfp7cr8cgHU~5rrcN6V~QcIJuqjDpYWojBdjYrc7fAA3iwWpN4fzI05yvE48oOOOLqBq7SvkpyzIhjc0hv81XQIu0LWzXXS~-B61wurJhte-LisF571BzefV5xoaRN8y3A0RidaJyuzVufPP4cKY5NeSsmTY36QRl54PG7iWJSXnLROROlg6qsjoeIV9lyNFY6ZsQKTQzEIInCZaARmNfoJP-MAsOMoj-CRDU2MXhYT~DKdI-rWH579A3wuoEjmlHtHyms7xvwUkb6kIx5UJHZmzF2Hyv3xVrpu0HSkZfUIbzz1lAc4IZ-8jnBjt2RIRpYMNnwZW09HjJXQDd7K-QvpxpK-cqNJcmWehGP7OxLt9Jj6h~8aUFHIJtFI77Zmp~YGf7cO9vCZexeLn7iByqDtfhzTP62IPu0~MJafA4efU83A-DXo8PJhOhl7rYRzH7bWRzB1rhBI~w~TsVOBQAEAAcAAL0me7gfS2H-OZ3FAsPtbUFCFpTcvfLAzBmNxxYU5TflB4KcxNe2isp2UjM7YLCuZg6OCaBSEnoag-ABpJPkY0WIjkqbFzOlowH2oVwevFHrZCFwvf1XVXsyWdupACHmmRHFCHKHMKzolO3Cye0RMH0wIEyMRyIszSThft~keXWyuEwBM4Vros-OKrKN-mBrHNbzQzTiGLS0dVMzdPvG6Pq4t1~wCWqAXrO8n7xU-xQECEpl053Ml5AJyUaCoVj3xqCd4nbrH2~kLmvd9r2nnd-Ig19BFHNALadSYbcH9JEdJZPY~7c505W1xhsrM2PcNnE4hm8DF4R~AddaILD7b2d1l~kehRZpUKdCL~THPTM20kTyN2PFqghIA4Ng-tVmXw=="
SERVER_DEST = i2plib.Destination(SERVER_DEST_B64, has_private_key=True)

CLIENT_DEST_B64 = "Fyax0ON9-Djvy5G7z7ZRyyu7vjK9-dcg4ei94Lnfd1IEI8DqQj3PTytWql-rltRmeMg9pRAm3XqpTNcGR0a26KR3cFNIwRgCKCQ3BOU8bNZQXpaWEpfhoOGKd5Nt9~qI6M3kFcbv8WWVtlPCNEnzjPbXhr0XLuttYFdOPuCDlzxXEHe8NVMTAhXKiuBox7c8zRB~WT6AMJxedf9u3nXLQOYV~ZT-4-xoHcbp1zwbRnvYJ0yjBNprmaac5xo1Zu~k9q93ug3S08FwwjioDswTl9ZyEJkrxTtaUdH~OwCKRVmXhP-HIKMXeBdDRrPFGBKPe-igAyuIdD5zYlgJwxkYsZAvU8XeQRpck7krFhLSgGez8zlpgZi7oUdbYMC6BpqZpDLppWCl9bOz5tX55gd3nbWEYb0DDlVyCAhBkfznUvmOlHmdcAHGS-B7e4WTi0yRb76hRrecHiX2tqDI7UGTAlTIx0TGW3Pa7gMImb5bV5n5TsYw7qBJABgMPSP6MkjtAAAAfn2Z9dSDlwpIVfjzxqhq7lY9So5O0PYFIFYshZhNim7R6nXJbn-QX9DoZ7JGEx9uXndWu6tEApY6q1OGAeXhjEnHagF1o13GpqZ4wgYuOehaq1fmJyFoeYQToHiBsXyo1FE1GeGV8JYJLOWHLKuxay9Nh84yyJ6XJGgylElqnl4WGiwqc0qsAk7l209agFggMCyqCx~nSFMtfGZ2pKp-i7H3HQC9BM0SednWiVsgRPGG20Z-WoQtHTvj5~VUhIbXpa1BGj~sOydi27A3xQPQYtEXhhfWKRGs7pAaobfaUeSnQ12a09LXO8U53eGPioVdSbTMOTqkuWhGEuXebx9DxV3hUdopRSpKSnCT6U9Fc5GpqRKk"
CLIENT_DEST = i2plib.Destination(CLIENT_DEST_B64, has_private_key=True)

UNKNOWN_DEST = "zpk544zs7zsh2pluudh4n64tsg7xtjl3vrwjqu6dggouya5qf3cq.b32.i2p"
OFFLINE_DEST = "9ZI1KN~C6ITmw2xGljY1p~36anL3uXpItFUschg0-~-ly4Q0Bh0wtbja6MJNZrAkRrAYUia9e1uugv5U1X9A1Q4Bt3JbrNJ1ouTx~PO4Pv-aWgKaB4rfluN3dPKutpLWRTz6d-rWIC-Wim7Gb8FwauPG29ZVRiWV8tR16ZmKUGNQPaZrL2M5Hy9bgBhkcoPKeNsUl1obc4TBO1sg5rtaxV7qDRUk8cG0kOHrl3u9VIuxAAehhqXYScaIMLfw18GooJZof1IrSQOmCmhiJAk9oEuAh1NAsvZCdVRWe1xRSw~MQRnb6YzdgFERGS0SIqTTBaIk444WEsPFys2ImWUR~e2rp4MTfgZAP3TsS6cdequ5w3lmOu-Ap30Nc7n4yAAR0rYOOT8gRVbE9zLN7VncYRYwkHwNWg~bTMb0yxvDGeXVHRlahAtAJUwaF7VW7oloAmJzbjIgRRfWdp621mAh-IarKzieCS1HxrwtaW3dtBJ8SdICWZ663-YAsXkOL67RBQAEAAcAAA=="


SESSION_DEST_MAP = {
    "ppserver": SERVER_DEST_B64, "ppclient": CLIENT_DEST_B64, 
    "failedaccept": SERVER_DEST_B64, 
    "unknowntest": CLIENT_DEST_B64, 
    "offlinetest": CLIENT_DEST_B64
}

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
                if msg["NAME"] == SERVER_DEST.base32 + ".b32.i2p":
                    writer.write("NAMING REPLY RESULT=OK NAME=ME VALUE={}\n".format(
                        SERVER_DEST.base64).encode())
                elif msg["NAME"] == UNKNOWN_DEST:
                    writer.write("NAMING REPLY RESULT=INVALID_KEY NAME={}\n".format(
                        UNKNOWN_DEST).encode())
            elif msg.cmd == "DEST" and msg.action == "GENERATE":
                writer.write("DEST REPLY PUB={} PRIV={}\n".format(
                    CLIENT_DEST.base64, CLIENT_DEST.private_key.base64).encode())
            elif msg.cmd == "SESSION" and msg.action == "CREATE":
                session = msg["ID"]
                if session == "duplicatedid":
                    writer.write("SESSION STATUS RESULT=DUPLICATED_ID\n".encode())
                else:
                    writer.write("SESSION STATUS RESULT=OK DESTINATION={}\n".format(
                        SESSION_DEST_MAP[session]).encode())
            elif msg.cmd == "STREAM" and msg.action == "ACCEPT":
                session = msg["ID"]
                if session == "ppserver":
                    writer.write(b"STREAM STATUS RESULT=OK\n")
                    await asyncio.sleep(0.1)
                    writer.write("{}\n".format(CLIENT_DEST.base64).encode())
                    await asyncio.sleep(0.01)
                    data_transfer = True
                    writer.write(b"PING")
                    await asyncio.sleep(0.01)
                    writer.close()
                elif session == "failedaccept":
                    writer.write(b"STREAM STATUS RESULT=I2P_ERROR\n")
            elif msg.cmd == "STREAM" and msg.action == "CONNECT":
                session = msg["ID"]
                if session == "ppclient":
                    writer.write(b"STREAM STATUS RESULT=OK\n")
                    data_transfer = True
                elif session == "offlinetest":
                    writer.write(b"STREAM STATUS RESULT=CANT_REACH_PEER\n")
        else:
            if data == b"PING":
                writer.write(b"PONG")

    writer.close()

class TestFuncPingPong(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        if REAL_SAM:
            self.sam_address = i2plib.utils.get_sam_address()
        else:
            self.sam_address = ("127.0.0.1", 19132)

    def runner(self, coro, *args, **kwargs):
        async def _runner(coro, *args, **kwargs):
            if not REAL_SAM:
                sam_server = await asyncio.start_server(
                    fake_sam_server_handler, *self.sam_address, loop=self.loop)

            await coro(*args, **kwargs)

            if not REAL_SAM:
                sam_server.close()
                await sam_server.wait_closed()

            for t in asyncio.Task.all_tasks(loop=self.loop):
                if t != asyncio.Task.current_task(loop=self.loop):
                    await t

        self.loop.run_until_complete(_runner(coro, *args, **kwargs))

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

        self.runner(coroutines_test)

    def test_context_managers_ping_pong(self):
        async def context_managers_test():
            async def server(sam_address, loop, ready):
                async with i2plib.Session("ppserver", sam_address=sam_address, loop=loop, destination=SERVER_DEST):
                    ready.release()
                    async with i2plib.StreamAcceptor("ppserver", sam_address=sam_address, loop=loop) as s:
                        incoming = await s.read(BUFFER_SIZE)
                        dest, request = incoming.split(b"\n", 1)
                        remote_destination = i2plib.Destination(dest.decode())
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

        self.runner(context_managers_test)

    def test_create_session_with_base64_destination(self):
        async def coro():
            _, session_writer = await i2plib.create_session("ppserver", 
                destination=SERVER_DEST_B64,
                sam_address=self.sam_address, loop=self.loop)
            session_writer.close()

        self.runner(coro)

    @unittest.skipIf(REAL_SAM, "real SAM will not fail")
    def test_duplicated_id(self):
        async def coro():
            with self.assertRaises(i2plib.DuplicatedId):
                _, client_session_writer = await i2plib.create_session("duplicatedid", 
                    sam_address=self.sam_address, loop=self.loop)

        self.runner(coro)

    @unittest.skipIf(REAL_SAM, "real SAM will not fail")
    def test_fail_accept(self):
        async def coro():
            _, client_session_writer = await i2plib.create_session("failedaccept", 
                sam_address=self.sam_address, loop=self.loop)
            with self.assertRaises(i2plib.I2PError):
                server_reader, server_writer = await i2plib.stream_accept("failedaccept", 
                    sam_address=self.sam_address, loop=self.loop)

            client_session_writer.close()

        self.runner(coro)

    def test_unknown_dest(self):
        async def coro():
            _, client_session_writer = await i2plib.create_session("unknowntest", 
                sam_address=self.sam_address, loop=self.loop)
            with self.assertRaises(i2plib.InvalidKey):
                client_reader, client_writer = await i2plib.stream_connect("unknowntest",
                        UNKNOWN_DEST, sam_address=self.sam_address, loop=self.loop)
                client_writer.close()

            client_session_writer.close()

        self.runner(coro)

    def test_offline_dest(self):
        async def coro():
            _, client_session_writer = await i2plib.create_session("offlinetest", 
                sam_address=self.sam_address, loop=self.loop)
            with self.assertRaises(i2plib.CantReachPeer):
                client_reader, client_writer = await i2plib.stream_connect("offlinetest",
                        OFFLINE_DEST, sam_address=self.sam_address, loop=self.loop)
                client_writer.close()

            client_session_writer.close()

        self.runner(coro)

    @unittest.skipIf(REAL_SAM, "real SAM returns a real destination")
    def test_dest_generate(self):
        async def coro():
            dest = await i2plib.new_destination(sam_address=self.sam_address, loop=self.loop)
            self.assertEqual(dest.base32, CLIENT_DEST.base32)

        self.runner(coro)

    def test_ping_pong_tunnel(self):
        async def coro():
            async def pong_handler(reader, writer):
                data = await reader.read(4096)
                writer.write(b"PONG")
                writer.close()

            server_local_address = ("127.0.0.1", i2plib.utils.get_free_port())
            client_local_address = ("127.0.0.1", i2plib.utils.get_free_port())
            pong_server = await asyncio.start_server(
                pong_handler, *server_local_address, loop=self.loop)

            s_tunnel = i2plib.ServerTunnel(server_local_address, loop=self.loop, 
                    session_name="ppserver",
                    destination=SERVER_DEST, sam_address=self.sam_address)
            c_tunnel = i2plib.ClientTunnel(SERVER_DEST.base64, client_local_address,
                    session_name="ppclient",
                    loop=self.loop, 
                    destination=CLIENT_DEST, sam_address=self.sam_address)

            await s_tunnel.run()
            await c_tunnel.run()
            await asyncio.sleep(0.1)

            reader, writer = await asyncio.open_connection(*client_local_address)
            writer.write(b"PING")
            data = await reader.read(4096)
            writer.close()

            pong_server.close()
            await pong_server.wait_closed()
            c_tunnel.stop()
            s_tunnel.stop()
            await asyncio.sleep(0.1)

        self.runner(coro)


    def tearDown(self):
        self.loop.stop()
        self.loop.close()

