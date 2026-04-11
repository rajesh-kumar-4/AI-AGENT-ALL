from .exceptions import InvalidDataException, NotFoundException
from .repository import TaskRepository
from .schemas import TaskCreate, TaskUpdate, TaskResponse


class TaskService:
    def __init__(self, repository: TaskRepository | None = None):
        self.repository = repository or TaskRepository()

    def list_tasks(self) -> list[TaskResponse]:
        return [TaskResponse.model_validate(task.to_dict()) for task in self.repository.list_tasks()]

    def create_task(self, payload: TaskCreate) -> TaskResponse:
        if not payload.title.strip():
            raise InvalidDataException("Task title must not be empty.")

        task = self.repository.create_task(payload.title, payload.description)
        return TaskResponse.model_validate(task.to_dict())

    def get_task(self, task_id: int) -> TaskResponse:
        task = self.repository.get_task(task_id)
        if not task:
            raise NotFoundException(f"Task with id {task_id} not found.")
        return TaskResponse.model_validate(task.to_dict())

    def update_task(self, task_id: int, payload: TaskUpdate) -> TaskResponse:
        data = payload.model_dump(exclude_none=True)
        if not data:
            raise InvalidDataException("No update data provided.")

        task = self.repository.update_task(task_id, data)
        if not task:
            raise NotFoundException(f"Task with id {task_id} not found.")

        return TaskResponse.model_validate(task.to_dict())

    def delete_task(self, task_id: int) -> None:
        deleted = self.repository.delete_task(task_id)
        if not deleted:
            raise NotFoundException(f"Task with id {task_id} not found.")
