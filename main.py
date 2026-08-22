from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="Task 2 - Projects & Tasks API",
    description="REST API for managing projects and tasks"
)

projects = []
tasks = []


class Project(BaseModel):
    name: str
    description: Optional[str] = ""


class Task(BaseModel):
    title: str
    project_id: int
    status: str = "todo"


# ---------------- PROJECT ENDPOINTS ----------------

@app.post("/projects", status_code=201)
def create_project(project: Project):
    new_project = {
        "id": len(projects) + 1,
        "name": project.name,
        "description": project.description
    }
    projects.append(new_project)
    return new_project


@app.get("/projects")
def get_projects():
    return projects


@app.get("/projects/{project_id}")
def get_project(project_id: int):
    for project in projects:
        if project["id"] == project_id:
            return project

    raise HTTPException(
        status_code=404,
        detail="Project not found"
    )


@app.put("/projects/{project_id}")
def update_project(project_id: int, project: Project):
    for index, existing_project in enumerate(projects):
        if existing_project["id"] == project_id:
            updated_project = {
                "id": project_id,
                "name": project.name,
                "description": project.description
            }
            projects[index] = updated_project
            return updated_project

    raise HTTPException(
        status_code=404,
        detail="Project not found"
    )


@app.delete("/projects/{project_id}")
def delete_project(project_id: int):
    for project in projects:
        if project["id"] == project_id:
            projects.remove(project)
            return {
                "message": "Project deleted successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Project not found"
    )


# ---------------- TASK ENDPOINTS ----------------

@app.post("/tasks", status_code=201)
def create_task(task: Task):
    valid_project = any(
        project["id"] == task.project_id
        for project in projects
    )

    if not valid_project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    if task.status not in ["todo", "in-progress", "done"]:
        raise HTTPException(
            status_code=400,
            detail="Status must be todo, in-progress, or done"
        )

    new_task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "project_id": task.project_id,
        "status": task.status
    }

    tasks.append(new_task)
    return new_task


@app.get("/tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    if task.status not in ["todo", "in-progress", "done"]:
        raise HTTPException(
            status_code=400,
            detail="Status must be todo, in-progress, or done"
        )

    for index, existing_task in enumerate(tasks):
        if existing_task["id"] == task_id:
            updated_task = {
                "id": task_id,
                "title": task.title,
                "project_id": task.project_id,
                "status": task.status
            }

            tasks[index] = updated_task
            return updated_task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {
                "message": "Task deleted successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )