import os

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.excel_export import export_coupang_excel, export_naver_excel
from app.models import AppConfig, ConfigUpdate, Item, ItemCreate, ItemUpdate
from app.storage import load_config, load_items, save_config, save_items

BASE_DIR = os.path.dirname(__file__)
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)

app = FastAPI(title="SalesAssist")

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/", response_class=FileResponse)
def index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


# ---------- Config ----------

@app.get("/api/config", response_model=AppConfig)
def get_config():
    return load_config()


@app.put("/api/config", response_model=AppConfig)
def update_config(body: ConfigUpdate):
    cfg = load_config()
    data = cfg.model_dump()
    updates = body.model_dump(exclude_none=True)
    data.update(updates)
    new_cfg = AppConfig(**data)
    save_config(new_cfg)
    return new_cfg


# ---------- Items ----------

@app.get("/api/items", response_model=list[Item])
def list_items():
    return load_items()


@app.post("/api/items", response_model=Item, status_code=201)
def create_item(body: ItemCreate):
    items = load_items()
    new_id = max((i.id for i in items), default=0) + 1
    new_item = Item(id=new_id, **body.model_dump())
    items.append(new_item)
    save_items(items)
    return new_item


@app.put("/api/items/{item_id}", response_model=Item)
def update_item(item_id: int, body: ItemUpdate):
    items = load_items()
    for idx, item in enumerate(items):
        if item.id == item_id:
            data = item.model_dump()
            updates = body.model_dump(exclude_none=True)
            data.update(updates)
            items[idx] = Item(**data)
            save_items(items)
            return items[idx]
    raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/api/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    items = load_items()
    new_items = [i for i in items if i.id != item_id]
    if len(new_items) == len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    save_items(new_items)


# ---------- Export ----------

@app.get("/api/export/naver")
def export_naver():
    items = load_items()
    cfg = load_config()
    filepath = export_naver_excel(items, cfg, OUTPUT_DIR)
    return FileResponse(
        filepath,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=os.path.basename(filepath),
    )


@app.get("/api/export/coupang")
def export_coupang():
    items = load_items()
    cfg = load_config()
    filepath = export_coupang_excel(items, cfg, OUTPUT_DIR)
    return FileResponse(
        filepath,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=os.path.basename(filepath),
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
