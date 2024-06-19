from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_, func, select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import Order, OrderProduct, Product
from fast_zero.schemas import Message, OrderList, OrderPublic, OrderSchema

router = APIRouter()

Session = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix='/orders', tags=['orders'])


@router.post('/', response_model=OrderPublic)
def create_order(
    order: OrderSchema,
    session: Session,
):
    products = session.scalars(
        select(Product).where(Product.id.in_(order.product_ids))
    ).all()

    db_order: Order = Order(
        state=order.state,
        client_id=order.client_id,
    )
    db_order.products = products
    session.add(db_order)
    session.add_all([db_order] + products)
    session.commit()
    session.refresh(db_order)

    return db_order


@router.get('/', response_model=OrderList)
def list_orders(  # noqa
    session: Session,
    create_at_start: str = Query(None),
    create_at_end: str = Query(None),
    product_secao: str = Query(None),
    order_id: int = Query(None),
    state: str = Query(None),
    client_id: int = Query(None),
    offset: int = Query(None),
    limit: int = Query(None),
):
    query = select(Order)

    if create_at_start and create_at_end:
        query = query.filter(
            and_(func.date(Order.created_at) >= create_at_start),
            func.date(Order.created_at) <= create_at_end,
        )

    if product_secao:
        query = (
            query.join(OrderProduct, OrderProduct.order_id == Order.id)
            .join(Product, Product.id == OrderProduct.product_id)
            .filter(Product.secao == product_secao)
        )

    if order_id:
        query = query.filter(Order.id == order_id)

    if state:
        query = query.filter(Order.state == state)

    if client_id:
        query = query.filter(Order.client_id == client_id)

    orders = session.scalars(query.offset(offset).limit(limit)).all()

    return {'orders': orders}


@router.patch('/{order_id}', response_model=OrderPublic)
def patch_order(order_id: int, session: Session, order: OrderSchema):
    db_order = session.scalar(select(Order).where(Order.id == order_id))

    if not db_order:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Order not found.'
        )

    for key, value in order.model_dump(exclude_unset=True).items():
        setattr(db_order, key, value)

    session.add(db_order)
    session.commit()
    session.refresh(db_order)

    return db_order


@router.delete('/{order_id}', response_model=Message)
def delete_order(order_id: int, session: Session):
    order = session.scalar(select(Order).where(Order.id == order_id))

    if not order:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Order not found.'
        )

    session.delete(order)
    session.commit()

    return {'message': 'Order has been deleted successfully.'}
