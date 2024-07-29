from typing import Any, Callable, overload

from .task_descriptor import TaskDescriptor
from .task_generics import TClass, TValue


@overload
def task(dependencies: list[str | TaskDescriptor[TClass, Any]]) -> Callable[[Callable[[TClass], TValue]], TaskDescriptor[TClass, TValue]]: ...

@overload
def task(method: Callable[[TClass], TValue]) -> TaskDescriptor[TClass, TValue]: ...

def task(arg: list[str | TaskDescriptor[TClass, Any]] | Callable[[TClass], TValue]) -> Callable[[Callable[[TClass], TValue]], TaskDescriptor[TClass, TValue]] | TaskDescriptor[TClass, TValue]:
    if not isinstance(arg, list):
        return TaskDescriptor[TClass, TValue](arg, [])
        
    def decorator(method: Callable[[TClass], TValue]) -> TaskDescriptor[TClass, TValue]:
        return TaskDescriptor[TClass, TValue](method, arg)
    
    return decorator
