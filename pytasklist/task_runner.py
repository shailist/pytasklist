from graphlib import TopologicalSorter
from typing import Any
import traceback

from .task_descriptor import TaskDescriptor, get_task_descriptors
from .task_reporters.base_task_reporter import BaseTaskReporter
from .task_reporters.null_task_reporter import NullTaskReporter
from .task_result import TaskFailure, TaskSuccess, TaskSkipped, get_task_results, get_task_results_values


def run_tasks(object, *, task_reporter: BaseTaskReporter | None = None) -> dict[str, Any]:
    if task_reporter is None:
        task_reporter = NullTaskReporter()
    
    task_results = get_task_results(object, init=True)
    task_descriptors = get_task_descriptors(object)
    
    tasks_graph = {
        task_name: {dependency.name if isinstance(dependency, TaskDescriptor) else dependency
                    for dependency in task_descriptor.dependencies}
        for task_name, task_descriptor in task_descriptors.items()
    }
    
    sorter = TopologicalSorter(tasks_graph)
    sorter.prepare()
    
    task_reporter.report_run_start(task_descriptors.keys())
    
    remaining_tasks = {task_name: task_descriptor
                       for task_name, task_descriptor in task_descriptors.items()}
    
    skipped_reason: str = "Dependency didn't succeed"
    
    try:
        while sorter.is_active() and (pending_tasks := sorter.get_ready()):
            task_reporter.report_prepared_tasks(pending_tasks)
            
            for task_name in pending_tasks:
                task_reporter.report_task_start(task_name)
                
                task_descriptor = remaining_tasks[task_name]
                
                try:
                    result = TaskSuccess(value=task_descriptor.function(object))
                    sorter.done(task_name)
                    
                except Exception as exception:
                    result = TaskFailure(exception=exception,
                                        formatted=traceback.format_exception(exception))
                
                task_results[task_name] = result
                
                remaining_tasks.pop(task_name)
                
                task_reporter.report_task_end(task_name, result)
                
    except KeyboardInterrupt:
        skipped_reason = "Cancled by user"
    
    for remaining_task_name in remaining_tasks:
        task_results[remaining_task_name] = TaskSkipped(reason=skipped_reason)
        
        task_reporter.report_task_skipped(remaining_task_name)
    
    task_reporter.report_run_end(task_results)
    
    return task_results
