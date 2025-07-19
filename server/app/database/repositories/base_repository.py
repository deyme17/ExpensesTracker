from typing import Type, TypeVar, Generic, Optional, List
from sqlalchemy.orm import Session
from app.database.db import SessionLocal

ORM_TYPE = TypeVar("T")


class BaseRepository(Generic[ORM_TYPE]):
    def __init__(self, model: Type[ORM_TYPE]):
        self.model = model

    def get_session(self, db: Session = None) -> Session:
        return db or SessionLocal()

    def get_all(self, db: Session = None) -> List[ORM_TYPE]:
        with self.get_session(db) as session:
            return session.query(self.model).all()

    def get_by_id(self, obj_id: str, db: Session = None) -> Optional[ORM_TYPE]:
        with self.get_session(db) as session:
            return session.query(self.model).get(obj_id)

    def create(self, data: dict, db: Session = None) -> ORM_TYPE:
        with self.get_session(db) as session:
            obj = self.model(**data)
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj

    def delete(self, obj_id: str, db: Session = None) -> None:
        with self.get_session(db) as session:
            obj = session.query(self.model).get(obj_id)
            if obj:
                session.delete(obj)
                session.commit()

    def update(self, obj_id: str, data: dict, db: Session = None) -> Optional[ORM_TYPE]:
        with self.get_session(db) as session:
            obj = session.query(self.model).get(obj_id)
            if not obj:
                return None
            for key, value in data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
            session.commit()
            session.refresh(obj)
            return obj
