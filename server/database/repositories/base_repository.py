from typing import Type, TypeVar, Generic, Optional, List
from sqlalchemy.orm import Session
from server.database.db import SessionLocal

ORM_TYPE = TypeVar("T")


class BaseRepository(Generic[ORM_TYPE]):
    def __init__(self, model: Type[ORM_TYPE]):
        self.model = model

    def get_session(self) -> Session:
        return SessionLocal()

    def get_all(self) -> List[ORM_TYPE]:
        with self.get_session() as db:
            return db.query(self.model).all()

    def get_by_id(self, obj_id: str) -> Optional[ORM_TYPE]:
        with self.get_session() as db:
            return db.query(self.model).get(obj_id)

    def create(self, data: dict) -> ORM_TYPE:
        with self.get_session() as db:
            obj = self.model(**data)
            db.add(obj)
            db.commit()
            db.refresh(obj)
            return obj

    def delete(self, obj_id: str) -> None:
        with self.get_session() as db:
            obj = db.query(self.model).get(obj_id)
            if obj:
                db.delete(obj)
                db.commit()

    def update(self, obj_id: str, data: dict) -> Optional[ORM_TYPE]:
        with self.get_session() as db:
            obj = db.query(self.model).get(obj_id)
            if not obj:
                return None
            for key, value in data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
            db.commit()
            db.refresh(obj)
            return obj
