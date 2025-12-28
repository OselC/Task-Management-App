class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:6767@localhost:5432/taskdb"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "super-secret-key"
