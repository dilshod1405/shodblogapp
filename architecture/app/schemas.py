from pydantic import BaseModel
from typing import Optional


class ArchitectureBase(BaseModel):
    photo: Optional[str] = None
    file: Optional[str] = None
    description: str


class ArchitectureCreate(ArchitectureBase):
    description: str


class ArchitectureUpdate(ArchitectureBase):
    id: int


class ArchitectureResponse(ArchitectureBase):
    id: int
    photo: Optional[str] = None
    file: Optional[str] = None

    class Config:
        orm_mode = True