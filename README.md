# psql-backup tool

This is a simple Python application that creates a backup of a PostgreSQL database, compresses it using gzip, and uploads it to MEGA.nz. The application reads the database details from a db.json file that includes the database name and URL. It uses the pg_dump and gzip utilities to create and compress the backup file, respectively.

## Installation & Usage

- Clone this repository using `git clone https://github.com/deadaf/psql-backup.git`
- Install the required packages using `pip install -r requirements.txt` or use `poetry install`.
- Rename `example.db.json` to `db.json` and fill in the database details.
- Rename `.example.env` to `.env` and fill in the MEGA.nz credentials.
- Run the script: `python3 main.py`

## Setting up cron job

- Open the crontab editor: `crontab -e`
- Add the following line to run the script every day at midnight: `0 0 * * * /path/to/python /path/to/postgresql-backup/main.py`

## Restoring a Database Backup

To restore a database from a backup file uploaded on MEGA.nz:

- Download the gzip file from MEGA.nz to your local machine.
- Uncompress the gzip file using `gzip -d <filename>.gz`.
- Restore the database using `pg_restore -h <hostname> -U <username> -d <dbname> -1 <filename>.dump`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please create a pull request or issue on GitHub.
