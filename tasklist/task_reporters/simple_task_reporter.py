from typing import Iterable

from tasklist.task_reporters.base_task_reporter import BaseTaskReporter
from tasklist.task_result import TaskResult, TaskSuccess, TaskFailure


class SimpleTaskReporter(BaseTaskReporter):
    def report_run_start(self, all_tasks: Iterable[str]) -> None:
        all_tasks = list(all_tasks)
        print(f'[*] Starting running tasks ({all_tasks=})')
    
    def report_run_end(self, task_results: dict[str, TaskResult]) -> None:
        print(f'[*] Finished running tasks ({task_results=})')
    
    def report_prepared_tasks(self, tasks: Iterable[str]) -> None:
        tasks = list(tasks)
        print(f'[*] Tasks prepared for execution: {tasks=}')
    
    def report_task_start(self, task: str) -> None:
        print(f'[*] Running task {task!r}...')
    
    def report_task_end(self, task: str, result: TaskFailure | TaskSuccess) -> None:
        print(f'[*] Finished running task {task!r} ({result=})')
    
    def report_task_skipped(self, task: str) -> None:
        print(f'[*] Skipped task {task!r}')
