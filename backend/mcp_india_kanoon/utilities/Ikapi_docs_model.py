from __future__ import annotations

from typing import Any, List

from pydantic import BaseModel


class Cover(BaseModel):
    tid: int
    title: str


class IkapiDocModel(BaseModel):
    tid: int
    publishdate: str
    title: str
    doc: str
    numcites: int
    numcitedby: int
    docid: int
    docsource: str
    covers: List[Cover]
    citetid: int
    divtype: str
    courtcopy: bool
    query_alert: Any
    agreement: bool
