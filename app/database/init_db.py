from app.database.orm_models.base_orm import Base, engine

def init_db():
    Base.metadata.create_all(bind=engine)