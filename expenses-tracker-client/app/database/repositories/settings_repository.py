from sqlalchemy.orm import Session
from app.database.orm_models.settings import SettingsORM


class SettingsRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(self, user_id: str, key: str) -> str | None:
        setting = (
            self.session.query(SettingsORM)
            .filter_by(user_id=user_id, key=key)
            .first()
        )
        return setting.value if setting else None

    def set(self, user_id: str, key: str, value: str) -> None:
        setting = (
            self.session.query(SettingsORM)
            .filter_by(user_id=user_id, key=key)
            .first()
        )
        if setting:
            setting.value = value
        else:
            setting = SettingsORM(user_id=user_id, key=key, value=value)
            self.session.add(setting)

        self.session.commit()

    def delete(self, user_id: str, key: str) -> None:
        self.session.query(SettingsORM).filter_by(user_id=user_id, key=key).delete()
        self.session.commit()

    def get_all_for_user(self, user_id: str) -> dict:
        settings = (
            self.session.query(SettingsORM)
            .filter_by(user_id=user_id)
            .all()
        )
        return {s.key: s.value for s in settings}

# active account methods
    def get_active_account_id(self, user_id: str) -> str | None:
        return self.get(user_id, "active_account_id")
    
    def set_active_account_id(self, user_id: str, account_id: str) -> None:
        self.set(user_id, "active_account_id", account_id)
    
    def clear_active_account(self, user_id: str) -> None:
        self.delete(user_id, "active_account_id")

# current account methods
    def get_current_user_id(self) -> str | None:
        return self.get("system", "current_user_id")
    
    def set_current_user_id(self, user_id: str) -> None:
        self.set("system", "current_user_id", user_id)
    
    def clear_current_user(self) -> None:
        self.delete("system", "current_user_id")