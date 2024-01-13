import sqlalchemy
import sqlalchemy.exc
from .exceptions import UserAlreadyExists

class db_handler:
    @staticmethod
    def register(self, *args, **kwargs):
        try: 
            pass
        except sqlalchemy.exc.IntegrityError:
            raise UserAlreadyExists("User already exists!", status_code=422)