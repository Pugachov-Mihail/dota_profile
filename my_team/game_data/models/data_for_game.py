from sqlalchemy import Integer, UUID, ForeignKey, Column
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class GamesUser(Base):
    __tablename__ = 'game_user'

    id = Column(Integer, primary_key=True)
    id_game = Column(Integer)
    user = Column(UUID, ForeignKey("users_model.User.id"))





