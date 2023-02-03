# Enter File/Folder Name
import asyncio
from mega import Mega
from decouple import config
from datetime import datetime
import json


async def upload_to_mega(filename):
    mega = Mega()
    m = mega.login(config("MEGA_EMAIL"), config("MEGA_PASSWORD"))
    m.upload(filename)
    ...


async def create_psql_dump():
    ...


async def main():
    with open("db.json") as f:
        databases = json.load(f)


if __name__ == "__main__":
    asyncio.run(main())
