from fastapi import APIRouter, Depends, status
from .schemas import TaskCreate, TaskResponse, TaskUpdate
from .security import get_api_key
from .service import TaskService

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])
service = TaskService()


@router.get("/", response_model=list[TaskResponse], status_code=status.HTTP_200_OK)
def list_tasks(api_key: str = Depends(get_api_key)) -> list[TaskResponse]:
    return service.list_tasks()


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, api_key: str = Depends(get_api_key)) -> TaskResponse:
    return service.create_task(payload)


@router.get("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def retrieve_task(task_id: int, api_key: str = Depends(get_api_key)) -> TaskResponse:
    return service.get_task(task_id)


@router.put("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def update_task(task_id: int, payload: TaskUpdate, api_key: str = Depends(get_api_key)) -> TaskResponse:
    return service.update_task(task_id, payload)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, api_key: str = Depends(get_api_key)) -> None:
    service.delete_task(task_id)
