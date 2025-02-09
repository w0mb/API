from src.models.users_model import UsersOrm
from src.repository.baseRep import BaseRepository

class UserRepository(BaseRepository):
    model = UsersOrm