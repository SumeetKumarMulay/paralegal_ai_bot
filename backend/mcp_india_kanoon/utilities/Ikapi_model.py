from __future__ import annotations

from typing import List, Optional, Union

from pydantic import BaseModel


class Category(BaseModel):
    value: str
    formInput: str
    selected: Optional[bool] = None


class Cover(BaseModel):
    tid: int
    title: str


class Doc(BaseModel):
    tid: int
    catids: Optional[List[int]]
    doctype: int
    publishdate: str
    authorid: Optional[int]
    bench: Optional[List[int]]
    title: str
    numcites: int
    numcitedby: int
    headline: str
    docsize: int
    fragment: bool
    covers: Optional[List[Cover]] = None
    docsource: str
    author: Optional[str] = None
    authorEncoded: Optional[str] = None
    citation: Optional[str] = None


class IKapiModel(BaseModel):
    categories: List[List[Union[str, List[Category]]]]
    docs: List[Doc]
    found: str
    encodedformInput: str
