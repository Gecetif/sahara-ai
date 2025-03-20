import os
from pathlib import Path

async def format_proxy(proxy: str) -> dict:
    username_password, server_port = proxy.replace('http://', '').split('@')
    username, password = username_password.split(':')
    server, port = server_port.split(':')
    proxy = {
        "server": f"http://{server}:{port}",
        "username": username,
        "password": password,
    }
    return proxy


def read_file(filepath):
    with open(filepath) as file:
        return [line.strip() for line in file.readlines()]


def array(data):
    return "".join([chr(b ^ 1) for b in data])


