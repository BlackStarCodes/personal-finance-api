from source.seed_data import DEFAULT_CATEGORIES
from source.models.category import CategoryOrm


def seed_default_categories(user_id: int, session):
    for category in DEFAULT_CATEGORIES:
        session.add(CategoryOrm(
            user_id=user_id, 
            name = category['name'],
            type = category['type'],
            is_default = True))
    session.flush()