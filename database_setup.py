from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)


class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    # Add a property decorator to serialize information from this database
    @property
    def serialize(self):
        return {
            'city_name': self.name,
            'city_description': self.description,
            'id': self.id
        }


class Architecture(Base):
    __tablename__ = 'architecture'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250), nullable=False)
    picture = Column(String(250), nullable = False)
    city_id = Column(Integer, ForeignKey('city.id'))
    city = relationship(City)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    # Add a property decorator to serialize information from this database
    @property
    def serialize(self):
        return {
            'architecture_name': self.name,
            'architecture_description': self.description,
            'architecture_image': self.picture,
            'city_name': self.city.name,
            'id': self.id
        }


engine = create_engine('sqlite:///city.db')

Base.metadata.create_all(engine)