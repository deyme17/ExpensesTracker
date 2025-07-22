from sqlalchemy.orm import Session
from typing import Optional

from app.database.repositories.base_repository import BaseRepository
from app.database.orm_models.user import UserORM
from app.models.user import User


class UserRepository(BaseRepository[UserORM]):
    def __init__(self, session: Session):
        super().__init__(session, UserORM)

    def save_user(self, user: User) -> None:
        if not user:
            return
        orm_user = UserORM(
            user_id=user.user_id,
            name=user.name, 
            email=user.email,
            encrypted_token=user._encrypted_token      
        )
        self.session.merge(orm_user)
        self.session.commit()

    def get_user(self, user_id: str) -> Optional[User]:
        orm_user = self.session.query(UserORM).filter(UserORM.user_id == user_id).first()
        if orm_user:
            return User(
                user_id=orm_user.user_id,
                name=orm_user.name, 
                email=orm_user.email,
                encrypted_token=orm_user.encrypted_token   
            )
        return None
    
    def clear_user(self, user_id: str) -> None:
        orm = self.session.query(UserORM).filter(UserORM.user_id == user_id).first()
        if orm:
            self.session.delete(orm)
            self.session.commit()