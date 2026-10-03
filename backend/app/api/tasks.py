from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.task import Task
from app.models.user import User
from app.schemas.task import (
    TaskCreate,
    TaskResponse,
    TaskUpdate,
)


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.get(
    "",
    response_model=list[TaskResponse],
)
def list_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    statement = (
        select(Task)
        .where(Task.user_id == current_user.id)
        .order_by(Task.due_at.asc().nullslast())
    )

    return list(db.scalars(statement).all())


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = Task(
        user_id=current_user.id,
        title=data.title,
        description=data.description,
        status="scheduled" if data.due_at else "draft",
        due_at=data.due_at,
        follow_up_enabled=data.follow_up_enabled,
        follow_up_at=data.follow_up_at,
        retry_enabled=data.retry_enabled,
        max_retries=data.max_retries,
        retry_interval_minutes=data.retry_interval_minutes,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = db.scalar(
        select(Task).where(
            Task.id == task_id,
            Task.user_id == current_user.id,
        )
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
)
def update_task(
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = db.scalar(
        select(Task).where(
            Task.id == task_id,
            Task.user_id == current_user.id,
        )
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    updates = data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(task, field, value)

    task.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(task)

    return task


@router.post(
    "/{task_id}/complete",
    response_model=TaskResponse,
)
def complete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = db.scalar(
        select(Task).where(
            Task.id == task_id,
            Task.user_id == current_user.id,
        )
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    task.status = "completed"
    task.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(task)

    return task


@router.post(
    "/{task_id}/snooze",
    response_model=TaskResponse,
)
def snooze_task(
    task_id: int,
    until: datetime,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = db.scalar(
        select(Task).where(
            Task.id == task_id,
            Task.user_id == current_user.id,
        )
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    task.status = "snoozed"
    task.due_at = until
    task.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(task)

    return task


@router.post(
    "/{task_id}/cancel",
    response_model=TaskResponse,
)
def cancel_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = db.scalar(
        select(Task).where(
            Task.id == task_id,
            Task.user_id == current_user.id,
        )
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    task.status = "cancelled"
    task.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(task)

    return task