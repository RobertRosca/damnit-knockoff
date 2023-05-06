import asyncio

from pathlib import Path

from damnit_knockoff.db import db_init
from damnit_knockoff.context_reader import MODELS


async def test():
    await db_init(
        state=None,  # type: ignore
        client="beanita",
    )

    for model in MODELS:
        latest = await model.find().sort(-model.run_no).limit(1).first_or_none()  # type: ignore
        res = await model(
            proposal_no=4696,
            run_no=latest.run_no + 1 if latest else 1,
            run_path=Path("/gpfs/exfel/exp/HED/202321/p004696/"),
        ).insert()  # type: ignore

        query_all = await model.find_all().to_list()  # type: ignore
        print(query_all)


if __name__ == "__main__":
    asyncio.run(test())
