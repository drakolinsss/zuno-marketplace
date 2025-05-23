from pydantic import BaseModel
from datetime import datetime

class MirrorBase(BaseModel):
    onion_link: str
    port: int

class MirrorCreate(MirrorBase):
    pass

class MirrorResponse(MirrorBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
