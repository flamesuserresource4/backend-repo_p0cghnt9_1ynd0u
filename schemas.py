"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

# Example schemas (kept for reference)
class User(BaseModel):
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Presale-specific schemas
class Presale(BaseModel):
    name: str = Field(..., description="Token name")
    symbol: str = Field(..., description="Token symbol")
    price_usd: float = Field(..., gt=0, description="Price per token in USD")
    soft_cap_usd: float = Field(..., ge=0)
    hard_cap_usd: float = Field(..., ge=0)
    token_supply: int = Field(..., ge=0)
    liquidity_percent: float = Field(..., ge=0, le=100)
    networks: List[str] = Field(default_factory=lambda: ["ETH", "BSC"]) 
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    vesting: Optional[str] = Field(None, description="Vesting schedule description")

class WhitelistEntry(BaseModel):
    email: EmailStr
    wallet: Optional[str] = Field(None, description="Wallet address")
    network: Optional[str] = Field(None, description="Preferred network")
