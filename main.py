import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

load_dotenv()

from app.models import Item, ItemCreate, Config, ReturnUpdate
from app.storage import load_items, save_items, load_config, save_config, next_id
from app.excel_export import export_naver, export_coupang

app = FastAPI(title="SalesAssist")

# ── CORS ──────────────────────────────────────────────────────────────────────
# Allow origins specified via ALLOWED_ORIGINS env var (comma-separated),
# falling back to all origins so the deployed app is reachable from any client.
_raw_origins = os.getenv("ALLOWED_ORIGINS", "*")
_origins = [o.strip() for o in _raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIR = Path(__file__).parent / "frontend"

# ── Static files ──────────────────────────────────────────────────────────────
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


@app.get("/")
def read_index():
    return FileResponse(str(FRONTEND_DIR / "index.html"))


# ── Config API ────────────────────────────────────────────────────────────────
@app.get("/api/config")
def get_config():
    return load_config()


@app.put("/api/config")
def update_config(config: Config):
    save_config(config.model_dump())
    return config


# ── Items API ─────────────────────────────────────────────────────────────────
@app.get("/api/items")
def get_items():
    return load_items()


@app.post("/api/items", status_code=201)
def create_item(item: ItemCreate):
    items = load_items()
    new_item = {"id": next_id(items), **item.model_dump()}
    items.append(new_item)
    save_items(items)
    return new_item


@app.put("/api/items/{item_id}")
def update_item(item_id: int, item: ItemCreate):
    items = load_items()
    for i, existing in enumerate(items):
        if existing["id"] == item_id:
            updated = {"id": item_id, **item.model_dump()}
            # Preserve return checklist managed via PATCH /return endpoint
            updated["return_occurred"] = existing.get("return_occurred", False)
            updated["return_checklist"] = existing.get("return_checklist", {})
            items[i] = updated
            save_items(items)
            return items[i]
    raise HTTPException(status_code=404, detail="Item not found")


@app.patch("/api/items/{item_id}/return")
def update_return(item_id: int, update: ReturnUpdate):
    items = load_items()
    for i, existing in enumerate(items):
        if existing["id"] == item_id:
            existing["return_occurred"] = update.return_occurred
            existing["return_checklist"] = update.return_checklist.model_dump()
            items[i] = existing
            save_items(items)
            return items[i]
    raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/api/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    items = load_items()
    new_items = [it for it in items if it["id"] != item_id]
    if len(new_items) == len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    save_items(new_items)


# ── Export API ────────────────────────────────────────────────────────────────
@app.get("/api/export/naver")
def export_naver_route():
    path = export_naver(load_items(), load_config())
    return FileResponse(path, filename=Path(path).name,
                        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


@app.get("/api/export/coupang")
def export_coupang_route():
    path = export_coupang(load_items(), load_config())
    return FileResponse(path, filename=Path(path).name,
                        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host=host, port=port, reload=False)
