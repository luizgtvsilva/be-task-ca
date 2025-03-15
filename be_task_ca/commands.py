from be_task_ca.infrastructure.database.config import engine, Base

from be_task_ca.infrastructure.database.models.user_model import UserModel, CartItemModel
from be_task_ca.infrastructure.database.models.item_model import ItemModel

def create_db_schema():
    Base.metadata.create_all(bind=engine)