
from pathlib import Path

TASK_FILE = Path(__file__).resolve().parent.parent / "task.txt"


def read_task():
    if not TASK_FILE.exists():
        raise FileNotFoundError("task.txt file not found!")

    task = TASK_FILE.read_text(encoding="utf-8").strip()

    if not task:
        raise ValueError("task.txt is empty!")

    return task