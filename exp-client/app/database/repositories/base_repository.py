from sqlalchemy.orm import Session
from typing import Type, TypeVar, Generic, Optional

ORM_TYPE = TypeVar('T')


class BaseRepository(Generic[ORM_TYPE]):
    def __init__(self, session: Session, model: Type[ORM_TYPE]):
        self.session = session
        self.model = model

    def add(self, obj: ORM_TYPE) -> None:
        self.session.add(obj)
        self.session.commit()

    def get_by_id(self, id_value) -> Optional[ORM_TYPE]:
        return self.session.query(self.model).get(id_value)

    def get_all(self) -> list[ORM_TYPE]:
        return self.session.query(self.model).all()

    def update(self, obj: ORM_TYPE) -> None:
        self.session.merge(obj)
        self.session.commit()

    def delete(self, obj: ORM_TYPE) -> None:
        self.session.delete(obj)
        self.session.commit()
