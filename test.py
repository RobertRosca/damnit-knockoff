import asyncio
import random
from pathlib import Path

from damnit_knockoff.context_reader import MODELS
from damnit_knockoff.db import db_init


async def add_or_update(
    model, proposal_no: int, run_no: int, run_path: Path, change=False
):
    m = model.find(model.proposal_no == proposal_no, model.run_no == run_no)
    m = await m.first_or_none()
    changed = m is not None
    if not m:
        m = model(
            proposal_no=proposal_no,
            run_no=run_no,
            run_path=run_path,
        )

    if change:
        m.random = random.randint(0, 100)
        if not m.raw:
            m.raw = True
        else:
            if not m.proc:
                m.proc = True

    if changed:
        await m.save_changes()
    else:
        await m.insert()


async def test():
    await db_init(
        state=None,  # type: ignore
        client="mongo",
    )

    proposal_no = 3360
    run_no = 132
    run_path = Path("/gpfs/exfel/exp/SCS/202301/p003360/raw/r0131")

    await add_or_update(MODELS[2], proposal_no, run_no, run_path, change=True)


if __name__ == "__main__":
    asyncio.run(test())
