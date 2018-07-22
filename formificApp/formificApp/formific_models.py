from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from models import Base


class User(Base):
    """Define User table"""

    __tablename__ = 'user'
    #__table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))
    artitem = relationship('ArtItem', back_populates='user')

    def __init__(self, name, email):
        self.name = name
        self.email = email

class Medium(Base):
    """Define Medium table

    A medium is a category to which an item belongs.
    """
    __tablename__ = 'medium'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    artitem = relationship('ArtItem', back_populates='medium')

    def __init__(self, name):
        self.name = name

class ArtItem(Base):
    """Define ArtItem table"""

    __tablename__ = 'art_item'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    material = Column(String)
    image_url = Column(String)
    video_url = Column(String)
    year = Column(String)
    medium_id = Column(Integer, ForeignKey('medium.id'))
    medium = relationship('Medium', back_populates='artitem')
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='artitem')

    def __init__(self, name, description, material, image_url, video_url, year, medium, user_id):
        self.name = name
        self.description = description
        self.material = material
        self.image_url = image_url
        self.video_url = video_url
        self.year = year
        self.medium = medium
        self.user_id = user_id

    @property
    def serialize(self):
        """Return JSON for ArtItem data"""
        return {
            'name': self.name,
            'description': self.description,
            'material': self.material,
            'image url': self.image_url,
            'video url': self.video_url,
            'year': self.year,
            'medium_id': self.medium.id
        }