from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)

    description = Column(String, nullable=True)
    start_date = Column(Date, nullable=True)

    places = relationship("Place", back_populates="project", cascade="all, delete-orphan")


class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(Integer, ForeignKey("projects.id"))

    external_id = Column(String, index=True)
    notes = Column(String, nullable=True) # notes for specific places ??

    is_visited = Column(Boolean, default=False)

    project = relationship("Project", back_populates="places")