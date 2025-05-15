import os

class Config:
    SQLALCHEMY_DATABASE_URI = (
        os.getenv('DATABASE_URL') or
      'mysql://catia:Catia1983@localhost/base_mairie'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super_secret_key')