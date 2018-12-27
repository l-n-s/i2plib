import asyncio
import logging

import i2plib

BUFFER_SIZE = 65536

PK_B64 = "5pJLIgm7KCqk-d0As66OdeMRj4moqtD97wOluQh5SXWCbeMfp7cr8cgHU~5rrcN6V~QcIJuqjDpYWojBdjYrc7fAA3iwWpN4fzI05yvE48oOOOLqBq7SvkpyzIhjc0hv81XQIu0LWzXXS~-B61wurJhte-LisF571BzefV5xoaRN8y3A0RidaJyuzVufPP4cKY5NeSsmTY36QRl54PG7iWJSXnLROROlg6qsjoeIV9lyNFY6ZsQKTQzEIInCZaARmNfoJP-MAsOMoj-CRDU2MXhYT~DKdI-rWH579A3wuoEjmlHtHyms7xvwUkb6kIx5UJHZmzF2Hyv3xVrpu0HSkZfUIbzz1lAc4IZ-8jnBjt2RIRpYMNnwZW09HjJXQDd7K-QvpxpK-cqNJcmWehGP7OxLt9Jj6h~8aUFHIJtFI77Zmp~YGf7cO9vCZexeLn7iByqDtfhzTP62IPu0~MJafA4efU83A-DXo8PJhOhl7rYRzH7bWRzB1rhBI~w~TsVOBQAEAAcAAL0me7gfS2H-OZ3FAsPtbUFCFpTcvfLAzBmNxxYU5TflB4KcxNe2isp2UjM7YLCuZg6OCaBSEnoag-ABpJPkY0WIjkqbFzOlowH2oVwevFHrZCFwvf1XVXsyWdupACHmmRHFCHKHMKzolO3Cye0RMH0wIEyMRyIszSThft~keXWyuEwBM4Vros-OKrKN-mBrHNbzQzTiGLS0dVMzdPvG6Pq4t1~wCWqAXrO8n7xU-xQECEpl053Ml5AJyUaCoVj3xqCd4nbrH2~kLmvd9r2nnd-Ig19BFHNALadSYbcH9JEdJZPY~7c505W1xhsrM2PcNnE4hm8DF4R~AddaILD7b2d1l~kehRZpUKdCL~THPTM20kTyN2PFqghIA4Ng-tVmXw=="
PK_B64_CLIENT = "Fyax0ON9-Djvy5G7z7ZRyyu7vjK9-dcg4ei94Lnfd1IEI8DqQj3PTytWql-rltRmeMg9pRAm3XqpTNcGR0a26KR3cFNIwRgCKCQ3BOU8bNZQXpaWEpfhoOGKd5Nt9~qI6M3kFcbv8WWVtlPCNEnzjPbXhr0XLuttYFdOPuCDlzxXEHe8NVMTAhXKiuBox7c8zRB~WT6AMJxedf9u3nXLQOYV~ZT-4-xoHcbp1zwbRnvYJ0yjBNprmaac5xo1Zu~k9q93ug3S08FwwjioDswTl9ZyEJkrxTtaUdH~OwCKRVmXhP-HIKMXeBdDRrPFGBKPe-igAyuIdD5zYlgJwxkYsZAvU8XeQRpck7krFhLSgGez8zlpgZi7oUdbYMC6BpqZpDLppWCl9bOz5tX55gd3nbWEYb0DDlVyCAhBkfznUvmOlHmdcAHGS-B7e4WTi0yRb76hRrecHiX2tqDI7UGTAlTIx0TGW3Pa7gMImb5bV5n5TsYw7qBJABgMPSP6MkjtAAAAfn2Z9dSDlwpIVfjzxqhq7lY9So5O0PYFIFYshZhNim7R6nXJbn-QX9DoZ7JGEx9uXndWu6tEApY6q1OGAeXhjEnHagF1o13GpqZ4wgYuOehaq1fmJyFoeYQToHiBsXyo1FE1GeGV8JYJLOWHLKuxay9Nh84yyJ6XJGgylElqnl4WGiwqc0qsAk7l209agFggMCyqCx~nSFMtfGZ2pKp-i7H3HQC9BM0SednWiVsgRPGG20Z-WoQtHTvj5~VUhIbXpa1BGj~sOydi27A3xQPQYtEXhhfWKRGs7pAaobfaUeSnQ12a09LXO8U53eGPioVdSbTMOTqkuWhGEuXebx9DxV3hUdopRSpKSnCT6U9Fc5GpqRKk"
NAMING_REPLY = "5pJLIgm7KCqk-d0As66OdeMRj4moqtD97wOluQh5SXWCbeMfp7cr8cgHU~5rrcN6V~QcIJuqjDpYWojBdjYrc7fAA3iwWpN4fzI05yvE48oOOOLqBq7SvkpyzIhjc0hv81XQIu0LWzXXS~-B61wurJhte-LisF571BzefV5xoaRN8y3A0RidaJyuzVufPP4cKY5NeSsmTY36QRl54PG7iWJSXnLROROlg6qsjoeIV9lyNFY6ZsQKTQzEIInCZaARmNfoJP-MAsOMoj-CRDU2MXhYT~DKdI-rWH579A3wuoEjmlHtHyms7xvwUkb6kIx5UJHZmzF2Hyv3xVrpu0HSkZfUIbzz1lAc4IZ-8jnBjt2RIRpYMNnwZW09HjJXQDd7K-QvpxpK-cqNJcmWehGP7OxLt9Jj6h~8aUFHIJtFI77Zmp~YGf7cO9vCZexeLn7iByqDtfhzTP62IPu0~MJafA4efU83A-DXo8PJhOhl7rYRzH7bWRzB1rhBI~w~TsVOBQAEAAcAAA=="
CLIENT_DESTINATION = "m6ha8qpiaEuH4OR4MQl2wvAl09sZCHBqi~cOuCBKfLE4F9gkxgYqNPvXU8QQXQ0XHTze~HTA2hNu8mgtCyyMKII4IEyF2CkbhjVF0yYEKDuTAmd-L6NXqj6Wa64X0GdvwdwOHknBNcw7pU8tUbgIu09T-~K6EGzshgmerg03fey1TPC8Q8bbemho-GGZqRyUvWe2U2HmXSis-OyJOGOJChkEfd40lizrEiKtkj8jOLQXxgN2A1oxAtyzN2hkzqK-WwYk8CaNW-SR~nZBFPSDL8KsWWapiSDXG7z8tCjnVana6psk4jms186vuy3Yp302MfLt~hza-5V2622aJENP2ipvfp7O2iaGuaRNTymYn6IDRgD7pM7GIXvtCTCW2GRAKGqf8bjm6GCQu0s0OZuU5M7qoTnJ83SY3sjWd8EBEjFT6NeSu14wdej11Q8itSLP7XOwYFCNNj2jEmKTPcn4I9QkBYy1Zd1P44EUpEuHXn5OWwF-M7sQBx4vn5chzFCuAAAA"
DEST_B32 = "bxwnysaa2nwykldz4ekz6u243x5ctqlcot5acmzj2huylvwr7eyq.b32.i2p"

async def fake_sam_server_handler(reader, writer):
    while True:
        data = await reader.read(BUFFER_SIZE)
        if not data: break
        if data.startswith(b"HELLO VERSION"):
            writer.write(b"HELLO REPLY RESULT=OK VERSION=3.1\n")
        elif data.startswith(b"SESSION CREATE STYLE=STREAM ID=ppserver"):
            writer.write("SESSION STATUS RESULT=OK DESTINATION={}\n".format(
                PK_B64).encode())
        elif data.startswith(b"SESSION CREATE STYLE=STREAM ID=ppclient"):
            writer.write("SESSION STATUS RESULT=OK DESTINATION={}\n".format(
                PK_B64_CLIENT).encode())
        elif data.startswith(b"NAMING LOOKUP NAME"):
            writer.write("NAMING REPLY RESULT=OK NAME=ME VALUE={}\n".format(
                NAMING_REPLY).encode())
        elif data.startswith(b"STREAM ACCEPT"):
            writer.write(b"STREAM STATUS RESULT=OK\n")
            await asyncio.sleep(0.1)
            writer.write("{}\n".format(CLIENT_DESTINATION).encode())
            await asyncio.sleep(0.1)
            writer.write(b"PING")
        elif data.startswith(b"STREAM CONNECT"):
            writer.write(b"STREAM STATUS RESULT=OK\n")
        elif data.startswith(b"PING"):
            writer.write(b"PONG")

    writer.close()

async def coroutines_test(sam_address, loop):
    _, server_session_writer = await i2plib.create_session("ppserver",
        sam_address=sam_address, loop=loop, destination=PK_B64)
    server_reader, server_writer = await i2plib.stream_accept("ppserver", 
        sam_address=sam_address, loop=loop)

    _, client_session_writer = await i2plib.create_session("ppclient", 
        sam_address=sam_address, loop=loop)
    client_reader, client_writer = await i2plib.stream_connect("ppclient",
            DEST_B32, sam_address=sam_address, loop=loop)

    client_writer.write(b"PING")
    incoming = await server_reader.read(BUFFER_SIZE)
    dest, request = incoming.split(b"\n", 1)
    remote_destination = i2plib.Destination(dest.decode())
    if not request:
        request = await server_reader.read(BUFFER_SIZE)
    assert request == b"PING"
    server_writer.write(b"PONG")
    response = await client_reader.read(BUFFER_SIZE)
    assert response == b"PONG"

    client_writer.close()
    server_writer.close()
    server_session_writer.close()
    client_session_writer.close()

async def context_managers_test(sam_address, loop):
    async def server(sam_address, loop, ready):
        async with i2plib.Session("ppserver", sam_address=sam_address, loop=loop, destination=PK_B64):
            ready.release()
            async with i2plib.StreamAcceptor("ppserver", sam_address=sam_address, loop=loop) as s:
                incoming = await s.read(BUFFER_SIZE)
                dest, request = incoming.split(b"\n", 1)
                remote_destination = i2plib.Destination(dest.decode())
                if not request:
                    request = await s.read(BUFFER_SIZE)
                assert request == b"PING"
                s.write(b"PONG")

    ready = asyncio.Lock(loop=loop)
    await ready.acquire()
    server_task = asyncio.ensure_future(server(sam_address, loop, ready), loop=loop)
    await ready.acquire()

    async with i2plib.Session("ppclient", sam_address=sam_address, loop=loop):
        async with i2plib.StreamConnection("ppclient", DEST_B32, sam_address=sam_address, loop=loop) as c:
            c.write(b"PING")
            response = await c.read(BUFFER_SIZE)
            assert response == b"PONG"

    await server_task

async def main(sam_address, loop):
    sam_server = await asyncio.start_server(
        fake_sam_server_handler, *sam_address, loop=loop)

    await coroutines_test(sam_address, loop)
    await context_managers_test(sam_address, loop)

    sam_server.close()
    await sam_server.wait_closed()

    for t in asyncio.Task.all_tasks(loop=loop):
        if t != asyncio.Task.current_task(loop=loop):
            await t

if __name__ == "__main__":
    sam_address = ("127.0.0.1", 19132)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(sam_address, loop))
    loop.stop()
    loop.close()
