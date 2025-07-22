from typing import Callable, TypeVar, Optional, List, Generic, Type
from sqlalchemy.orm import Session
from contextlib import contextmanager
from app.database.db import SessionLocal

ORM_TYPE = TypeVar("T")
R = TypeVar("R")


class BaseRepository(Generic[ORM_TYPE]):
    def __init__(self, model: Type[ORM_TYPE]):
        self.model = model

    @contextmanager
    def get_session(self, db: Session = None):
        """Context manager for session managing"""
        if db is not None:
            yield db
        else:
            session = SessionLocal()
            try:
                yield session
            finally:
                session.close()
        
    def _with_session(self, func: Callable[[Session], R], db: Session = None) -> R:
        with self.get_session(db) as session:
            return func(session)

    def get_all(self, db: Session = None) -> List[ORM_TYPE]:
        def operation(session: Session):
            return session.query(self.model).all()
        return self._with_session(operation, db)

    def get_by_id(self, obj_id: str, db: Session = None) -> Optional[ORM_TYPE]:
        def operation(session: Session):
            return session.query(self.model).get(obj_id)
        return self._with_session(operation, db)

    def create(self, data: dict, db: Session = None) -> ORM_TYPE:
        def operation(session: Session):
            obj = self.model(**data)
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj
        return self._with_session(operation, db)

    def delete(self, obj_id: str, db: Session = None) -> None:
        def operation(session: Session):
            obj = session.query(self.model).get(obj_id)
            if obj:
                session.delete(obj)
                session.commit()
        return self._with_session(operation, db)

    def update(self, obj_id: str, data: dict, db: Session = None) -> Optional[ORM_TYPE]:
        def operation(session: Session):
            obj = session.query(self.model).get(obj_id)
            if not obj:
                return None
            for key, value in data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
            session.commit()
            session.refresh(obj)
            return obj
        return self._with_session(operation, db)