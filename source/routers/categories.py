from fastapi import APIRouter, HTTPException
from ..models.category import CategoryOrm
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
    return new_category
