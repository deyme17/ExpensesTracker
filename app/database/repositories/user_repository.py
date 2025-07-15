from sqlalchemy.orm import Session
from typing import Optional

from app.database.repositories.base_repository import BaseRepository
from app.database.orm_models.user import UserORM
from app.models.user import User


class UserRepository(BaseRepository[UserORM]):
    def __init__(self, session: Session):
        super().__init__(session, UserORM)