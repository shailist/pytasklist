from typing import Iterable

from .base_task_reporter import BaseTaskReporter
from ..task_result import TaskResult


class NullTaskReporter(BaseTaskReporter):
    def report_run_start(self, all_tasks: Iterable[str]) -> None:
        pass
    
    def report_run_end(self, task_results: dict[str, TaskResult]) -> None:
        pass
    
    def report_prepared_tasks(self, tasks: Iterable[str]) -> None:
        pass
    
    def report_task_start(self, task: str) -> None:
        pass
    
    def report_task_end(self, task: str, result: TaskResult) -> None:
        pass
    
    def report_task_skipped(self, task: str) -> None:
        pass
