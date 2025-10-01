from sqlalchemy.orm import Session
from decimal import Decimal
from . import models


def get_product_by_code(db: Session, code: str):
    return db.query(models.Product).filter(models.Product.code == code).first()


def create_order(db: Session, items: list[tuple[models.Product, int]], tax_rate: float):
    subtotal = sum(Decimal(p.unit_price) * q for p, q in items)
    tax = (subtotal * Decimal(str(tax_rate))).quantize(Decimal("0.01"))
    total = (subtotal + tax).quantize(Decimal("0.01"))

    order = models.Order(subtotal=subtotal, tax=tax, total=total)
    db.add(order)
    db.flush()

    for product, quantity in items:
        db.add(models.OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=quantity,
            unit_price=product.unit_price,
        ))

    db.commit()
    db.refresh(order)
    return order 