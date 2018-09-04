import asyncio
import logging

import i2plib

BUFFER_SIZE = 65536

async def irc_bot():
    irc_server, nickname, channel = "irc.ilita.i2p", "aiobot", "0"
    session_name = "ircbot"

    READY = asyncio.Event()
    asyncio.ensure_future(
            i2plib.create_session(session_name, session_ready=READY))
    await READY.wait()

    reader, writer = await i2plib.stream_connect(session_name, irc_server)

    writer.write("NICK {}\n".format(nickname).encode())
    writer.write("USER {} {} {} :{}\n".format(
        nickname, nickname, nickname, nickname).encode())

    while True:
        data = await reader.read(BUFFER_SIZE)
        if not data: break
        lines = data.decode()
        if lines:
            logging.info("Data received: {}".format(lines))
        for line in lines.split("\n"):
            line = line.strip()
            if line:
                if line.startswith('PING :'):
                    writer.write(
                            'PONG :{}\n'.format(line.split(":")[1]).encode())
                elif line[0] == ":":
                    """Server sent some message"""
                    words = line.split()
                    if words[1] == '422' or words[1] == '376':
                        """End of MOTD, joining channel"""
                        writer.write(
                                "JOIN #{}\n".format(channel).encode())
                    if words[1] == 'PRIVMSG':
                        message = line.split(":", 2)[2].strip()
                        if words[2].startswith("#") and \
                                message.startswith("!ping"):
                            writer.write(
                                "PRIVMSG {} :pong\n".format(words[2]).encode())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(irc_bot())
    except KeyboardInterrupt:
        pass
    finally:
        loop.stop()
        loop.close()
