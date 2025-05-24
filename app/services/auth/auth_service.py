from abc import ABC, abstractmethod

class BaseAuthService(ABC):
    @abstractmethod
    def login(self, email, password, callback=None): ...
    
    @abstractmethod
    def register(self, email, password, confirm_password, monobank_token, callback=None): ...
    
    @abstractmethod
    def logout(self): ...
    
    @abstractmethod
    def is_authenticated(self): ...
    
    @abstractmethod
    def get_current_user(self): ...
