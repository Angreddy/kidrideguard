from fastapi import FastAPI
from .database import engine
from .models import Base
from .routers import users, students, routes, assignments, bus

# This line creates tables in PostgreSQL
Base.metadata.create_all(bind=engine)

app = FastAPI(title="School Bus Monitoring API")

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(students.router, prefix="/students", tags=["students"])
app.include_router(routes.router, prefix="/routes", tags=["routes"])
app.include_router(assignments.router, prefix="/assignments", tags=["assignments"])
app.include_router(bus.router, prefix="/bus", tags=["bus"])
