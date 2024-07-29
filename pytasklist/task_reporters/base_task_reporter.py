from abc import ABCMeta, abstractmethod
from typing import Iterable

from ..task_result import TaskFailure, TaskSuccess, TaskResult


class BaseTaskReporter(metaclass=ABCMeta):
    @abstractmethod
    def report_run_start(self, all_tasks: Iterable[str]) -> None:
        ...
    
    @abstractmethod
    def report_run_end(self, task_results: dict[str, TaskResult]) -> None:
        ...
    
    @abstractmethod
    def report_prepared_tasks(self, tasks: Iterable[str]) -> None:
        ...
    
    @abstractmethod
    def report_task_start(self, task: str) -> None:
        ...
    
    @abstractmethod
    def report_task_end(self, task: str, result: TaskFailure | TaskSuccess) -> None:
        ...
    
    @abstractmethod
    def report_task_skipped(self, task: str) -> None:
        ...
