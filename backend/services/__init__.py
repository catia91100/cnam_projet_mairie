from models.user_model import User
from sqlalchemy.exc import IntegrityError  # unique et manque une donnée obligatoire

# def insert(entity: dict):
#     try:
#         db = next(get_db())
#         user = User(entity['email'])
#         user._password = entity['password']
#         db.add(user)
#         db.commit()
#     except IntegrityError:
#         db.rollback()
#         raise
#     finally:
#         db.close()
