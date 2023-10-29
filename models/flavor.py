from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Flavor(Base):
    __tablename__ = 'flavors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    plants = relationship('Plant', back_populates='flavor')
