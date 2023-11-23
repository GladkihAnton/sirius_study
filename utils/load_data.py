import asyncio
import json
from pathlib import Path
from argparse import ArgumentParser

from sqlalchemy import insert

from webapp.db.postgres import async_db_connection
from webapp.models.meta import metadata

parser = ArgumentParser()
parser.add_argument('files', metavar='F', type=str, nargs='+', help='files for loading data')
args = parser.parse_args()


async def insert_fixture(filepath: Path):
    with open(filepath, 'r') as f:
        table_data = json.load(f)

    table = metadata.tables[filepath.stem]
    query = insert(table).values(table_data)

    async for session in async_db_connection():
        await session.execute(query)
        await session.commit()

async def main():
    for file in args.files:
        await insert_fixture(Path(file))

if __name__ == '__main__':
    asyncio.run(main())