# app/models/widget_state.py
from typing import Optional
from sqlmodel import SQLModel, Field
class WidgetState(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    key: str
    state_json: str = "{}"
