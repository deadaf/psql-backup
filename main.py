import asyncio
from mega import Mega
from decouple import config
from datetime import datetime
import gzip
import os
import aiohttp
import asyncpg


async def upload_to_mega(filename) -> None:
    """
    Uploads a file to MEGA.nz

    Parameters
    ----------
    filename: Name of the .gz file to upload.
    """
    mega = Mega()
    m = mega.login(config("MEGA_EMAIL"), config("MEGA_PASSWORD"))
    m.upload(filename)
    os.remove(filename)


async def create_psql_dump(db: str, filename: str) -> None:
    """
    Creates a PostgreSQL dump file.

    Parameters
    ----------

    db: URL of the PSQL database.
    filename: Filename for the dump file.
    """
    os.system("pg_dump --file={} --format=custom --dbname={}".format(filename, db))

    compressed_file = "{}.gz".format(str(filename))
    with open(filename, "rb") as f_in:
        with gzip.open(compressed_file, "wb") as f_out:
            for line in f_in:
                f_out.write(line)

    os.remove(filename)


async def send_discord_webhook(project: str) -> None:
    """
    Sends a webhook to Discord

    Parameters
    ----------
    project: Name of the project, just for the embed.
    """

    embed = {
        "embeds": [{"description": "Database backup for Project `{}` created.".format(project.title()), "color": 6524915}]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(config("WEBHOOK"), json=embed) as resp:
            if resp.status != 204:
                print(f"Error sending embed: {resp.reason}")


async def main() -> None:
    async with asyncpg.create_pool(
        host=config("DB_HOST"), port=config("DB_PORT"), user=config("DB_USER"), password=config("DB_PASSWORD")
    ) as conn:
        databases = await conn.fetch(
            "SELECT datname FROM pg_database WHERE datistemplate = false AND datname != 'postgres';"
        )

        for db in databases:  # type: dict
            db_name = db["datname"]
            
            if "test" in db_name:
                continue # ignore test instances.
                
            db_url = "postgresql://{}:{}@{}:{}/{}".format(
                config("DB_USER"), config("DB_PASSWORD"), config("DB_HOST"), config("DB_PORT"), db_name
            )

            filename = "{}_{}.dump".format(db_name, datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
            await create_psql_dump(db_url, filename)
            await upload_to_mega(filename + ".gz")

            await send_discord_webhook(db_name)  # this is optional, I do it to know my program is working.


if __name__ == "__main__":
    asyncio.run(main())
