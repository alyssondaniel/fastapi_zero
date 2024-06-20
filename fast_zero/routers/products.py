import os
import uuid
from http import HTTPStatus
from typing import Annotated, List

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy import String, cast, select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import Product, ProductImage, User
from fast_zero.schemas import (
    Message,
    ProductImageList,
    ProductList,
    ProductPublic,
    ProductSchema,
    ProductUpdate,
)
from fast_zero.security import get_current_user

router = APIRouter()

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
router = APIRouter(prefix='/products', tags=['products'])


@router.post('/', response_model=ProductPublic)
def create_product(
    product: ProductUpdate,
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


@router.post('/{id}/images', response_model=ProductImageList)
async def upload_images(  # noqa
    id: int,
    session: Session,
    files: Annotated[
        List[UploadFile],
        File(description='Multiple images'),
    ],
    current_user: CurrentUser = None,
):
    list_db_image = []
    if files:
        oldImages = session.scalars(
            select(ProductImage).where(ProductImage.product_id == id)
        ).all()
        for oldImage in oldImages:
            session.delete(oldImage)
            session.commit()
            os.remove(f'{os.getcwd()}/product_images/{oldImage.file_name}')

        for image in files:
            try:
                _, ext = image.content_type.split('/')
                image.filename = f'{uuid.uuid4()}.{ext}'
                file_path = f'{os.getcwd()}/product_images/{image.filename}'
                with open(file_path, 'wb') as f:
                    f.write(image.file.read())
                    f.close()

                db_image: ProductImage = ProductImage(
                    product_id=id,
                    file_name=image.filename,
                    file_type=image.content_type,
                )
                session.add(db_image)
                session.commit()
                list_db_image.append(db_image)
            except Exception as e:
                print(str(e))

    return {'product_images': list_db_image}


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
