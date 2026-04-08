from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from app.models import Item, ItemCreate, Config, Receipt, ReceiptCreate
from app.storage import (
    load_items, save_items, load_config, save_config, next_id,
    load_receipts, save_receipts,
)
from app.excel_export import export_naver, export_coupang, export_receipts

app = FastAPI(title="SalesAssist")

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
            items[i] = {"id": item_id, **item.model_dump()}
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


# ── Receipts API ──────────────────────────────────────────────────────────────
@app.get("/api/receipts")
def get_receipts():
    return load_receipts()


@app.post("/api/receipts", status_code=201)
def create_receipt(receipt: ReceiptCreate):
    receipts = load_receipts()
    new_receipt = {"id": next_id(receipts), **receipt.model_dump()}
    receipts.append(new_receipt)
    save_receipts(receipts)
    return new_receipt


@app.put("/api/receipts/{receipt_id}")
def update_receipt(receipt_id: int, receipt: ReceiptCreate):
    receipts = load_receipts()
    for i, existing in enumerate(receipts):
        if existing["id"] == receipt_id:
            receipts[i] = {"id": receipt_id, **receipt.model_dump()}
            save_receipts(receipts)
            return receipts[i]
    raise HTTPException(status_code=404, detail="Receipt not found")


@app.delete("/api/receipts/{receipt_id}", status_code=204)
def delete_receipt(receipt_id: int):
    receipts = load_receipts()
    new_receipts = [r for r in receipts if r["id"] != receipt_id]
    if len(new_receipts) == len(receipts):
        raise HTTPException(status_code=404, detail="Receipt not found")
    save_receipts(new_receipts)


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


@app.get("/api/export/receipts")
def export_receipts_route():
    path = export_receipts(load_receipts())
    return FileResponse(path, filename=Path(path).name,
                        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
