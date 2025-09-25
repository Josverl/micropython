# Source: library\espnow.rst:721
# Type: code_block

e = AIOESPNow()
e.active(True)


async def recv_till_halt(e):
    async for mac, msg in e:
        print(mac, msg)
        if msg == b"halt":
            break


asyncio.run(recv_till_halt(e))
