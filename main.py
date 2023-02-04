import asyncio
from mega import Mega
from decouple import config
from datetime import datetime
import gzip
import os
import aiohttp


async def upload_to_mega(filename):
    mega = Mega()
    m = mega.login(config("MEGA_EMAIL"), config("MEGA_PASSWORD"))
    m.upload(filename)
    os.remove(filename)


async def create_psql_dump(db: str, filename: str):
    # Restore using: pg_restore -h localhost -U postgres -d testdb -1 file_name.dump

    os.system("pg_dump --file={} --format=custom --dbname={}".format(filename, db))

    compressed_file = "{}.gz".format(str(filename))
    with open(filename, "rb") as f_in:
        with gzip.open(compressed_file, "wb") as f_out:
            for line in f_in:
                f_out.write(line)

    os.remove(filename)


async def send_discord_webhook(project: str):
    embed = {
        "embeds": [{"description": "Database backup for Project `{}` created.".format(project.title()), "color": 6524915}]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(config("WEBHOOK"), json=embed) as resp:
            if resp.status != 204:
                print(f"Error sending embed: {resp.reason}")


async def main():
    quotient_db = config("QUOTIENT")
    filename = "quotient_{}.dump".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    await create_psql_dump(quotient_db, filename)
    await upload_to_mega(filename + ".gz")

    await send_discord_webhook("Quotient")

    pro_db = config("QUOTIENTPRO")
    filename = "quotientpro_{}.dump".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    await create_psql_dump(pro_db, filename)
    await upload_to_mega(filename + ".gz")

    await send_discord_webhook("Quotient Pro")


if __name__ == "__main__":
    asyncio.run(main())
