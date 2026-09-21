from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import User, Project, Task
from schemas import (
    UserCreate,
    UserResponse,
    ProjectCreate,
    ProjectResponse,
    TaskCreate,
    TaskResponse,
)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task 3 - Projects & Tasks API",
    description="REST API with PostgreSQL database integration"
)


# =========================================================
# USER ENDPOINTS
# =========================================================

@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(
        name=user.name,
        email=user.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get("/users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserCreate,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    existing_email = (
        db.query(User)
        .filter(
            User.email == user_data.email,
            User.id != user_id
        )
        .first()
    )

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    user.name = user_data.name
    user.email = user_data.email

    db.commit()
    db.refresh(user)

    return user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(user)
    db.commit()

    return {
        "message": "User deleted successfully"
    }


# =========================================================
# PROJECT ENDPOINTS
# =========================================================

@app.post(
    "/projects",
    response_model=ProjectResponse,
    status_code=201
)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.id == project.user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    new_project = Project(
        name=project.name,
        description=project.description,
        user_id=project.user_id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


@app.get(
    "/projects",
    response_model=list[ProjectResponse]
)
def get_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()


@app.get(
    "/projects/{project_id}",
    response_model=ProjectResponse
)
def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):

    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return project


@app.put(
    "/projects/{project_id}",
    response_model=ProjectResponse
)
def update_project(
    project_id: int,
    project_data: ProjectCreate,
    db: Session = Depends(get_db)
):

    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    user = (
        db.query(User)
        .filter(User.id == project_data.user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    project.name = project_data.name
    project.description = project_data.description
    project.user_id = project_data.user_id

    db.commit()
    db.refresh(project)

    return project


@app.delete("/projects/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db)
):

    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    db.delete(project)
    db.commit()

    return {
        "message": "Project deleted successfully"
    }


# =========================================================
# TASK ENDPOINTS
# =========================================================

@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=201
)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):

    project = (
        db.query(Project)
        .filter(Project.id == task.project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    new_task = Task(
        title=task.title,
        project_id=task.project_id,
        status=task.status
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@app.get(
    "/tasks",
    response_model=list[TaskResponse]
)
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()


@app.get(
    "/tasks/{task_id}",
    response_model=TaskResponse
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):

    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


@app.put(
    "/tasks/{task_id}",
    response_model=TaskResponse
)
def update_task(
    task_id: int,
    task_data: TaskCreate,
    db: Session = Depends(get_db)
):

    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    project = (
        db.query(Project)
        .filter(Project.id == task_data.project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    task.title = task_data.title
    task.project_id = task_data.project_id
    task.status = task_data.status

    db.commit()
    db.refresh(task)

    return task


@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):

    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted successfully"
    }