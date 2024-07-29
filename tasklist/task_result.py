from dataclasses import dataclass
from typing import Any, Generic, TypeAlias

from .task_generics import TValue


@dataclass
class TaskSuccess(Generic[TValue]):
    value: TValue


@dataclass
class TaskFailure:
    exception: Exception
    formatted: str


@dataclass
class TaskSkipped:
    reason: str


TaskResult: TypeAlias = TaskSuccess | TaskFailure | TaskSkipped


def get_task_results(object, init = False) -> dict[str, TaskResult]:
    if init:
        task_results = getattr(object, '_task_results', {})
        setattr(object, '_task_results', task_results)
        return task_results

    task_results = getattr(object, '_task_results', None)
    if task_results is None:
        raise RuntimeError(f"Tasks of {object!r} weren't executed yet (did you call `run_tasks`?)")
    
    return task_results


def get_task_results_values(object) -> dict[str, Any]:
    """
    Helper function that returns the values of the task results in the given object.
    If a certain task failed or was skipped, its value will be `None`.
    """
    task_results = get_task_results(object)
    return {task_name: task_result.value if isinstance(task_result, TaskSuccess) else None
            for task_name, task_result in task_results.items()}
