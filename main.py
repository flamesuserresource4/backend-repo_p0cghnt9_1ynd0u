import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson.objectid import ObjectId

from database import db, create_document, get_documents
from schemas import Presale, WhitelistEntry

app = FastAPI(title="Crypto Presale API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Crypto Presale Backend Running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

# Basic helper to convert ObjectId
class PresaleOut(BaseModel):
    id: str
    name: str
    symbol: str
    price_usd: float
    soft_cap_usd: float
    hard_cap_usd: float
    token_supply: int
    liquidity_percent: float
    networks: List[str]
    start_at: Optional[str] = None
    end_at: Optional[str] = None
    vesting: Optional[str] = None

@app.post("/api/presales", response_model=dict)
def create_presale(presale: Presale):
    try:
        inserted_id = create_document("presale", presale)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/presales", response_model=List[PresaleOut])
def list_presales():
    try:
        docs = get_documents("presale")
        out = []
        for d in docs:
            out.append(PresaleOut(
                id=str(d.get("_id")),
                name=d.get("name"),
                symbol=d.get("symbol"),
                price_usd=float(d.get("price_usd", 0)),
                soft_cap_usd=float(d.get("soft_cap_usd", 0)),
                hard_cap_usd=float(d.get("hard_cap_usd", 0)),
                token_supply=int(d.get("token_supply", 0)),
                liquidity_percent=float(d.get("liquidity_percent", 0)),
                networks=list(d.get("networks", [])),
                start_at=str(d.get("start_at")) if d.get("start_at") else None,
                end_at=str(d.get("end_at")) if d.get("end_at") else None,
                vesting=d.get("vesting")
            ))
        return out
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/whitelist", response_model=dict)
def add_whitelist(entry: WhitelistEntry):
    try:
        inserted_id = create_document("whitelistentry", entry)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
