import tempfile
from pathlib import Path
from raraphsopvt.repository import TaskRepository


def test_repository_crud_operations():
    with tempfile.TemporaryDirectory() as tmp_dir:
        db_path = Path(tmp_dir) / "test_tasks.db"
        repository = TaskRepository(db_path)

        task = repository.create_task("Learn Python", "Create a sample project with CRUD operations.")
        assert task.id == 1
        assert task.title == "Learn Python"
        assert task.description.startswith("Create a sample project")
        assert task.completed is False

        fetched = repository.get_task(task.id)
        assert fetched is not None
        assert fetched.title == task.title

        all_tasks = repository.list_tasks()
        assert len(all_tasks) == 1

        updated = repository.update_task(task.id, {"completed": True, "title": "Learn Python Basics"})
        assert updated is not None
        assert updated.completed is True
        assert updated.title == "Learn Python Basics"

        deleted = repository.delete_task(task.id)
        assert deleted is True

        assert repository.get_task(task.id) is None
