from pydantic import BaseModel
from datetime import datetime
from pydantic import BaseModel, constr

# Auth
class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

class UserBase(BaseModel):
    username: str
    role: str

class UserCreate(UserBase):
    password: constr(min_length=8, max_length=72)

class UserOut(UserBase):
    id: int
    class Config:
        orm_mode = True

# Students
class StudentBase(BaseModel):
    name: str
    grade: str

class StudentCreate(StudentBase):
    pass

class StudentOut(StudentBase):
    id: int
    class Config:
        orm_mode = True

# Routes
class RouteBase(BaseModel):
    name: str
    start_location: str
    end_location: str
    capacity: int

class RouteCreate(RouteBase):
    pass

class RouteOut(RouteBase):
    id: int
    class Config:
        orm_mode = True

# Assignments
class AssignmentOut(BaseModel):
    id: int
    student_id: int
    route_id: int
    class Config:
        orm_mode = True

# Bus locations
from pydantic import BaseModel
from datetime import datetime

class BusLocationBase(BaseModel):
    latitude: float
    longitude: float
    timestamp: datetime | None = None

class BusLocationCreate(BusLocationBase):
    pass

class BusLocationOut(BusLocationBase):
    id: int
    route_id: int

    class Config:
        orm_mode = True

# ✅ Add this for listing users 
class UserListOut(BaseModel): 
    id: int 
    username: str 
    role: str 
    class Config: 
        orm_mode = True
