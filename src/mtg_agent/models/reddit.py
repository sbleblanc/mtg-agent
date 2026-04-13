from typing import List

from pydantic import BaseModel

class SimplifiedRedditPost(BaseModel):
    title: str
    content: str
    comments: List[str]