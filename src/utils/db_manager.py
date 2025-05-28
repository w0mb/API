from src.repository.hotelRep import HotelRepository
from src.repository.roomsRep import RoomRepository
from src.repository.userRep import UserRepository
from src.repository.bookingRep import BookingRepository
from src.repository.comfortRep import ComfortRepository, RoomsComfortRepositiry

class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory
    
    async def __aenter__(self):
        self.session = self.session_factory()
        
        self.hotels = HotelRepository(self.session)
        self.rooms = RoomRepository(self.session)
        self.users = UserRepository(self.session)
        self.bookings = BookingRepository(self.session)
        self.comfort = ComfortRepository(self.session)
        self.rooms_comfort = RoomsComfortRepositiry(self.session)
        
        return self
        
    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()
        
    async def commit(self):
        await self.session.commit()