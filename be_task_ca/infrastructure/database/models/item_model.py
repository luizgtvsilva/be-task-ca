from sqlalchemy import UUID, Column, String, Float, Integer
import uuid

from be_task_ca.infrastructure.database.config import Base

class ItemModel(Base):
    __tablename__ = "items"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    price = Column(Float)
    quantity = Column(Integer)