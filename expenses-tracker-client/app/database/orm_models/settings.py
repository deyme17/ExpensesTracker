from sqlalchemy import Column, String, UniqueConstraint
from app.database.orm_models.base_orm import Base


class SettingsORM(Base):
    __tablename__ = "settings"

    user_id = Column(String, primary_key=True)
    key = Column(String, primary_key=True)
    value = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "key", name="unique_user_setting"),
    )
