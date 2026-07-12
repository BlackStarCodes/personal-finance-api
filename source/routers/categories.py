from fastapi import APIRouter, HTTPException
from ..models.category import CategoryOrm
from ..models.transaction import TransactionOrm
from ..dependencies import session_dependency
from sqlalchemy import select, func, exists, or_
from ..schemas import CategoryCreate, CategoryOut, CategoryUpdate
from ..security import current_user


router = APIRouter()


@router.post('/', response_model=CategoryOut)
async def create_category(
    user: current_user,
    category: CategoryCreate,
    session : session_dependency
):
    category_name = category.name.strip()

    try:
        existing_category = session.scalar(select(CategoryOrm).where(
            CategoryOrm.user_id == user.id,
            func.lower(CategoryOrm.name) == category_name.lower()
        ))
        if existing_category:
            raise HTTPException(status_code=409, detail='This category already exists!')
        
        new_category = CategoryOrm(
            user_id = user.id,
            name = category_name,
            type = category.type
        )
        session.add(new_category)
        session.commit()
        session.refresh(new_category)
        
    except Exception:
        session.rollback()
        raise
    return new_category


@router.get('/', response_model=list[CategoryOut])
async def read_categories(
    user: current_user,
    session: session_dependency
):
    categories = session.scalars(select(CategoryOrm).where(
        CategoryOrm.user_id == user.id
    )).all()

    return categories


@router.get('/{category_id}', response_model=CategoryOut)
async def read_category(
    user: current_user,
    category_id: int,
    session: session_dependency,
):
    category = session.scalar(select(CategoryOrm).where(
        CategoryOrm.id == category_id, 
        CategoryOrm.user_id == user.id))
    
    if not category:
        raise HTTPException(status_code=404, detail="Category Not Found!")
    
    return category


@router.put('/{category_id}', response_model=CategoryOut)
async def update_category(
    user: current_user,
    category: CategoryUpdate,
    category_id: int,
    session: session_dependency
): 
    try:
        db_category = session.scalar(select(CategoryOrm).where(
            CategoryOrm.id == category_id, 
            CategoryOrm.user_id == user.id))
        
        if not db_category:
            raise HTTPException(status_code=404, detail= "Category Not Found!")

        category_name = category.name.strip()

        existing_category = session.scalar(select(CategoryOrm).where(
            CategoryOrm.user_id == user.id,
            func.lower(CategoryOrm.name) == category_name.lower()
        ))

        if existing_category and existing_category.id != category_id:
            raise HTTPException(status_code=409, detail="Category already exists!")
        
        db_category.name = category_name
        db_category.type = category.type

        session.commit()
        session.refresh(db_category)

    except Exception:
        session.rollback()
        raise
    return db_category


@router.delete('/{category_id}')
async def delete_category(
    user: current_user,
    session: session_dependency,
    category_id: int
):
    try:
        category = session.scalar(select(CategoryOrm).where(CategoryOrm.user_id == user.id, CategoryOrm.id == category_id))

        if not category:
            raise HTTPException(status_code=404, detail="Category Not Found")
        
        has_transactions = session.scalar(select(exists().where(
            TransactionOrm.category_id == category.id)))
        
        if has_transactions:
            raise HTTPException(status_code=409, detail="Category cannot be deleted since it contains transactions!")
        
        session.delete(category)
        session.commit()
        
    except Exception:
        session.rollback()
        raise
    return {'message':'Category deleted Successfully'}