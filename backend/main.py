from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from . import models, schemas, crud
from .settings import settings

Base.metadata.create_all(bind=engine)

app = FastAPI(title="POS API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/products/{code}", response_model=schemas.ProductOut)
def read_product(code: str, db: Session = Depends(get_db)):
    product = crud.get_product_by_code(db, code)
    if not product:
        raise HTTPException(status_code=404, detail="NOT_FOUND")
    return {
        "code": product.code,
        "name": product.name,
        "unit_price": float(product.unit_price),
    }


@app.post("/orders", response_model=schemas.OrderOut)
def create_order(order_in: schemas.OrderIn, db: Session = Depends(get_db)):
    if not order_in.items:
        raise HTTPException(status_code=400, detail="EMPTY_ITEMS")

    resolved: list[tuple[models.Product, int]] = []
    for item in order_in.items:
        product = crud.get_product_by_code(db, item.productCode)
        if not product:
            raise HTTPException(status_code=400, detail=f"UNKNOWN_CODE:{item.productCode}")
        if item.quantity <= 0:
            raise HTTPException(status_code=400, detail=f"INVALID_QTY:{item.productCode}")
        resolved.append((product, item.quantity))

    order = crud.create_order(db, resolved, settings.TAX_RATE)
    return {
        "subtotal": float(order.subtotal),
        "tax": float(order.tax),
        "total": float(order.total),
    } 