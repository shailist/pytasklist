from typing import Any, Callable, Generic, overload

from .task_generics import TClass, TValue
from .task_result import get_task_results


class TaskDescriptor(Generic[TClass, TValue]):
    function: Callable[[TClass], TValue]
    name: str
    dependencies: 'list[str | TaskDescriptor]'
    
    def __init__(self, function: Callable[[TClass], TValue], dependencies: 'list[str | TaskDescriptor]') -> None:
        assert isinstance(function, Callable), 'TaskDescriptor can only be used on methods'
        
        self.function = function
        self.name = None
        self.dependencies = dependencies
    
    def __set_name__(self, owner: type[TClass], name: str) -> None:
        assert isinstance(owner, type), 'TaskDescriptor must only be used on class methods'

        self.name = name
        
        task_descriptors = get_task_descriptors(owner, init=True)
        task_descriptors[name] = self

    @overload
    def __get__(self, object: None, objtype: type[TClass]) -> 'TaskDescriptor[TClass, TValue]': ...

    @overload
    def __get__(self, object: TClass, objtype: type[TClass]) -> TValue: ...

    def __get__(self, object: TClass | None, objtype: type[TClass]) -> 'TaskDescriptor[TClass, TValue]' | TValue:
        if object is None:
            return self
        
        return get_task_results(object)[self.name]


def get_task_descriptors(object, init = False) -> dict[str, 'TaskDescriptor']:
    if init:
        task_descriptors = getattr(object, '_task_descriptors', {})
        setattr(object, '_task_descriptors', task_descriptors)
        return task_descriptors

    task_descriptors = getattr(object, '_task_descriptors', None)
    if task_descriptors is None:
        raise RuntimeError(f"{object!r} does not contain any tasks (did you decorate any methods with `@task`?)")

    return getattr(object, '_task_descriptors')
