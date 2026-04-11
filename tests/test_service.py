import tempfile
from pathlib import Path
from raraphsopvt.repository import TaskRepository
from raraphsopvt.service import TaskService
from raraphsopvt.schemas import TaskCreate, TaskUpdate


def test_service_crud_business_logic():
    with tempfile.TemporaryDirectory() as tmp_dir:
        db_path = Path(tmp_dir) / "test_service.db"
        repository = TaskRepository(db_path)
        service = TaskService(repository=repository)

        task_create = TaskCreate(title="Build API", description="Create API endpoints for tasks.")
        saved_task = service.create_task(task_create)
        assert saved_task.title == "Build API"
        assert saved_task.completed is False

        task_read = service.get_task(saved_task.id)
        assert task_read.id == saved_task.id

        task_update = TaskUpdate(description="Update the task service and HTTP API.", completed=True)
        updated_task = service.update_task(saved_task.id, task_update)
        assert updated_task.completed is True
        assert "Update the task service" in updated_task.description

        service.delete_task(saved_task.id)
        try:
            service.get_task(saved_task.id)
            assert False, "Task was not deleted"
        except Exception:
            assert True
