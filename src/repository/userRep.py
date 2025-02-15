from src.models.users_model import UsersOrm
from src.repository.baseRep import BaseRepository
from src.chemas.chema import User

class UserRepository(BaseRepository):
    model = UsersOrm
    chema = User