from pathlib import Path
from typing import TYPE_CHECKING

import extra_data
from beanie import (
    Document,
    Insert,
    PydanticObjectId,
    Replace,
    SaveChanges,
    Update,
    before_event,
    init_beanie,
)
from pydantic import BaseModel, Extra

if TYPE_CHECKING:
    from starlite import State


class RunBase(BaseModel):
    proposal_no: int
    run_no: int
    run_path: Path


class RunInsert(RunBase, Document):
    _run: extra_data.DataCollection | None = None

    revision_no: int = 0

    @property
    def run(self) -> extra_data.DataCollection:
        """Lazy load runs when needed."""
        if not self._run:
            self._run = extra_data.open_run(self.proposal_no, self.run_no)
        return self._run

    @before_event(Insert, Replace, Update, SaveChanges)
    async def _update_revision(self):
        """Update the revision number and create a new revision when changes are saved."""
        if not self._saved_state:
            return

        if changes := self.get_changes():  # type: ignore
            changed_keys = changes.keys()
            if "revision_no" in changed_keys:
                # We've already changed the revision number, this is a recursive call as
                # part of the current update operation, so we can just return
                return

            previous = {
                k: v for k, v in self.get_saved_state().items() if k in changed_keys
            }
            self.revision_no += 1

            rev = RunRevisions(
                revision_no=self.revision_no,
                parent=self.id,  # type: ignore
                **previous,
            )
            await rev.insert()  # type: ignore

    class Config:
        underscore_attrs_are_private = True
        extra = Extra.allow

    class Settings:
        use_state_management = True
        state_management_save_previous = True
        use_revision = True


class RunRevisions(Document):
    """A document to store revisions of a run."""

    revision_no: int
    parent: PydanticObjectId

    class Config:
        extra = Extra.allow


def get_mongo_db():
    from motor.motor_asyncio import AsyncIOMotorClient as Client

    client = Client("mongodb://localhost:27017/")

    return client.damnit


def get_beanita_db():
    from beanita import Client

    client = Client("beanita")

    return client["damnit"]


async def db_init(
    state: "State" = None,  # type: ignore
    client="beanita",
):
    from damnit_knockoff.context_reader import MODELS

    if client == "beanita":
        db = get_beanita_db()
    else:
        db = get_mongo_db()

    await init_beanie(
        database=db,
        document_models=MODELS,  # type: ignore
    )
