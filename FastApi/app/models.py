from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # admin, driver, parent

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    grade = Column(String, nullable=False)
    assignments = relationship("Assignment", back_populates="student")

class Route(Base):
    __tablename__ = "routes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    start_location = Column(String, nullable=False)
    end_location = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    assignments = relationship("Assignment", back_populates="route")
    bus_locations = relationship("BusLocation", back_populates="route")

class Assignment(Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=False)
    student = relationship("Student", back_populates="assignments")
    route = relationship("Route", back_populates="assignments")

class BusLocation(Base):
    __tablename__ = "bus_locations"
    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    route = relationship("Route", back_populates="bus_locations")
