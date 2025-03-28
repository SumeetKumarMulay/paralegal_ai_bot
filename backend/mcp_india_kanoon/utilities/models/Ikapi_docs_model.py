from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class Cover(BaseModel):
    tid: int
    title: str


class IkapiDocModel(BaseModel):
    tid: Optional[int]
    publishdate: Optional[str] = None
    title: str
    doc: str
    numcites: Optional[int] = None
    numcitedby: Optional[int] = None
    docid: Optional[int] = None
    docsource: Optional[str] = None
    covers: Optional[List[Cover]] = None
    citetid: Optional[int] = None
    divtype: Optional[str] = None
    courtcopy: Optional[bool] = None
    query_alert: Optional[Any] = None
    agreement: Optional[bool] = None
