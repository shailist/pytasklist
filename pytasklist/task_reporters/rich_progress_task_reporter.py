from typing import Iterable, Literal
import rich.progress

from .base_task_reporter import BaseTaskReporter
from ..task_result import TaskResult, TaskSuccess, TaskFailure


class CompletedTasksColumn(rich.progress.ProgressColumn):
    """
    Renders completed count/total, e.g. '  10/1000', if the task's total is not `None`.
    """

    def __init__(self):
        super().__init__()

    def render(self, task: rich.progress.Task) -> rich.progress.Text:
        if task.total is None:
            return rich.progress.Text()
        
        completed = int(task.completed)
        total = int(task.total) if task.total is not None else "?"
        total_width = len(str(total))
        return rich.progress.Text(
            f"{completed:{total_width}d}/{total}",
            style="progress.download",
        )


class RichProgressTaskReporter(BaseTaskReporter):
    progress: rich.progress.Progress
    total_task: rich.progress.TaskID
    task_progress: dict[str, rich.progress.TaskID]
    
    def __init__(self) -> None:
        self.progress = rich.progress.Progress(
            rich.progress.TimeElapsedColumn(),
            rich.progress.SpinnerColumn(),
            rich.progress.TextColumn("[progress.description]{task.description}"),
            CompletedTasksColumn(),
            redirect_stdout=False, redirect_stderr=False
        )
        self.total_task = None
        self.task_progress = {}
    
    def report_run_start(self, all_tasks: Iterable[str]) -> None:
        self.total_task = self.progress.add_task('[bold underline magenta]Running tasks:[/]', total=len(all_tasks))
        
        for task in all_tasks:
            self.task_progress[task] = self.progress.add_task('', total=None)
            self._set_task_status(task, 'queued')
        
        self.progress.start()
    
    def report_run_end(self, task_results: dict[str, TaskResult]) -> None:
        self.progress.stop()
    
    def report_prepared_tasks(self, tasks: Iterable[str]) -> None:
        for task in tasks:
            self._set_task_status(task, 'pending')
    
    def report_task_start(self, task: str) -> None:
        self._set_task_status(task, 'executing')
        self.progress.start_task(self.task_progress[task])
    
    def report_task_end(self, task: str, result: TaskSuccess | TaskFailure) -> None:
        task_id = self.task_progress[task]
        self.progress.stop_task(task_id)
        
        match result:
            case TaskSuccess():
                self._set_task_status(task, 'success')
                
            case TaskFailure():
                self._set_task_status(task, 'failure')
            
            case _:
                self._set_task_status(task, 'unknown')
        
        self.progress.advance(self.total_task)
    
    def report_task_skipped(self, task: str) -> None:
        self._set_task_status(task, 'skipped')
        
        self.progress.advance(self.total_task)
    
    def _set_task_status(self, task: str, status: Literal['queued', 'pending', 'executing', 'success', 'failure', 'skipped', 'unknown']) -> None:
        STATUS_SYMBOL = {
            'queued': ' ',
            'pending': ' ',
            'executing': '\N{WHITE HOURGLASS}',
            'success': '\N{CHECK MARK}',
            'failure': '\N{BALLOT X}',
            'skipped': '\N{RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK}',
            'unknown': '?'
        }
        STATUS_COLOR = {
            'queued': 'gray',
            'pending': 'gray',
            'executing': 'yellow',
            'success': 'green',
            'failure': 'red',
            'skipped': 'light gray',
            'unknown': 'gray'
        }
        STATUS_SUFFIX = {
            'queued': 'queued...',
            'pending': 'pending...',
            'executing': 'executing...',
            'success': 'succeeded',
            'failure': 'failed',
            'skipped': 'skipped',
            'unknown': 'unknown result'
        }
        
        symbol = STATUS_SYMBOL[status]
        color = STATUS_COLOR[status]
        suffix = STATUS_SUFFIX[status]
        
        task_id = self.task_progress[task]
        self.progress.update(task_id, description=f'[blue]{task}[/] [bold {color}]{symbol}[/] [{color}]{suffix}[/]')
