from typing import Optional
from sqlmodel import SQLModel, Field

class Profile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    is_current: bool = False
