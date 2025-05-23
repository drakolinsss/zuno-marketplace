from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime
from enum import Enum

class DisputeStatus(str, Enum):
    OPEN = "open"
    PENDING = "pending"
    RESOLVED = "resolved"

class EscrowStatus(str, Enum):
    PENDING = "pending"
    RELEASED = "released"
    REFUNDED = "refunded"

class EscrowCreate(BaseModel):
    buyer_id: int
    seller_id: int
    product_id: int
    amount: float

    @validator('amount')
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Amount must be greater than 0')
        return v

class EscrowResponse(BaseModel):
    id: int
    buyer_id: int
    seller_id: int
    product_id: int
    amount: float
    status: EscrowStatus
    release_time: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class DisputeCreate(BaseModel):
    escrow_id: int
    complainant_id: int
    description: str

    @validator('description')
    def description_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Description cannot be empty')
        return v

class DisputeResponse(BaseModel):
    id: int
    escrow_id: int
    complainant_id: int
    description: str
    status: DisputeStatus
    resolution: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class DisputeResolve(BaseModel):
    resolution: str
    status: DisputeStatus = DisputeStatus.RESOLVED
    escrow_status: EscrowStatus

    @validator('resolution')
    def resolution_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Resolution cannot be empty')
        return v

    @validator('escrow_status')
    def valid_escrow_status(cls, v):
        if v not in [EscrowStatus.RELEASED, EscrowStatus.REFUNDED]:
            raise ValueError('Escrow status must be either RELEASED or REFUNDED')
        return v
