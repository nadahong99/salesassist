import os

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from app.models import Item, ItemCreate, Config, ReturnUpdate, OrderCreate, Order
from app.storage import load_items, save_items, load_config, save_config, next_id, load_orders, save_orders
from app.excel_export import export_naver, export_coupang

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


# ── Orders API ────────────────────────────────────────────────────────────────
@app.get("/api/orders")
def get_orders():
    return load_orders()


@app.post("/api/orders", status_code=201)
def create_order(order: OrderCreate):
    orders = load_orders()
    new_order = {"id": next_id(orders), **order.model_dump()}
    orders.append(new_order)
    save_orders(orders)
    return new_order


@app.put("/api/orders/{order_id}")
def update_order(order_id: int, order: OrderCreate):
    orders = load_orders()
    for i, existing in enumerate(orders):
        if existing["id"] == order_id:
            updated = {"id": order_id, **order.model_dump()}
            orders[i] = updated
            save_orders(orders)
            return orders[i]
    raise HTTPException(status_code=404, detail="Order not found")


@app.delete("/api/orders/{order_id}", status_code=204)
def delete_order(order_id: int):
    orders = load_orders()
    new_orders = [o for o in orders if o["id"] != order_id]
    if len(new_orders) == len(orders):
        raise HTTPException(status_code=404, detail="Order not found")
    save_orders(new_orders)


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "127.0.0.1")
    uvicorn.run("main:app", host=host, port=port, reload=False)
