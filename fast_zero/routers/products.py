from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import String, cast, select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import Product, User
from fast_zero.schemas import Message, ProductList, ProductPublic, ProductSchema
from fast_zero.security import get_current_user

router = APIRouter()

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
router = APIRouter(prefix='/products', tags=['products'])


@router.post('/', response_model=ProductPublic)
def create_product(
    product: ProductSchema,
    session: Session,
    current_user: CurrentUser = None,
):
    db_product: Product = Product(
        descricao=product.descricao,
        valor=product.valor,
        codigo_barras=product.codigo_barras,
        secao=product.secao,
        categoria=product.categoria,
        estoque_inicial=product.estoque_inicial,
        data_validade=product.data_validade,
    )
    session.add(db_product)
    session.commit()
    session.refresh(db_product)

    return db_product


@router.get('/', response_model=ProductList)
def list_products(  # noqa
    session: Session,
    valor: str = Query(None),
    descricao: str = Query(None),
    categoria: str = Query(None),
    disponivel: bool = Query(False),
    offset: int = Query(None),
    limit: int = Query(None),
    current_user: CurrentUser = None,
):
    query = select(Product)

    if disponivel:
        query = query.filter(Product.estoque_inicial > 0)

    if categoria:
        query = query.filter(Product.categoria == categoria)

    if valor:
        query = query.filter(cast(Product.valor, String) == (f'{valor}'))

    if descricao:
        query = query.filter(Product.descricao.contains(descricao))

    products = session.scalars(query.offset(offset).limit(limit)).all()

    return {'products': products}


@router.get('/{id}', response_model=ProductPublic)
def show_product(  # noqa
    id: int,
    session: Session,
    current_user: CurrentUser = None,
):
    product: Product = session.scalars(
        select(Product).filter(Product.id == id)
    ).first()

    return product


@router.patch('/{product_id}', response_model=ProductPublic)
def patch_product(
    product_id: int,
    session: Session,
    product: ProductSchema,
    current_user: CurrentUser = None,
):
    db_product = session.scalar(select(Product).where(Product.id == product_id))

    if not db_product:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Product not found.'
        )

    for key, value in product.model_dump(exclude_unset=True).items():
        setattr(db_product, key, value)

    session.add(db_product)
    session.commit()
    session.refresh(db_product)

    return db_product


@router.delete('/{product_id}', response_model=Message)
def delete_product(
    product_id: int,
    session: Session,
    current_user: CurrentUser = None,
):
    product = session.scalar(select(Product).where(Product.id == product_id))

    if not product:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Product not found.'
        )

    session.delete(product)
    session.commit()

    return {'message': 'Product has been deleted successfully.'}
