import asyncio
import logging

import docker
import docker.errors

CONTAINER = 'debian:stable'

client = docker.from_env()

log = logging.getLogger('container')
log.setLevel(logging.INFO)


def prepare():
    try:
        image = client.images.get(CONTAINER)
        log.info("Found Container-Image %s: %s", CONTAINER, image.short_id)
    except docker.errors.ImageNotFound:
        log.info("Pulling Container-Image %s…", CONTAINER)
        client.images.pull(CONTAINER)
        log.info("Pulled Container-Image")


class ContainerPty(object):
    def __init__(self, sock):
        self.sock = sock

    async def recv(self):
        loop = asyncio.get_running_loop()
        msg = await loop.sock_recv(self.sock, 4096)
        return msg.decode('utf-8')

    async def send(self, message):
        loop = asyncio.get_running_loop()
        await loop.sock_sendall(self.sock, message.encode('utf-8'))


async def start_container():
    log.info("Starting Container")
    container = client.containers.run(
        CONTAINER,
        detach=True,
        tty=True,
        stdin_open=True,
        auto_remove=True)

    # container.resize(50, 100)

    log.info("Attaching to Container")
    sock = container.attach_socket(params={
        'stdin': 1,
        'stdout': 1,
        'stderr': 1,
        'stream': 1
    })

    nsock = sock._sock
    nsock.setblocking(False)
    pty = ContainerPty(nsock)
    await pty.send("\n")
    return pty
