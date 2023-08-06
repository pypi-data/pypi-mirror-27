"""
This module contains various decorators to help with common tasks involving
the Python `threading` module.

- `thread`: Call a function in a separate thread.

- `thread_join`: Call a function in a separate thread and join the thread.

- `thread_daemon`: Call a function in a separate thread and return
its return value.

- `delay`: Delay before calling a function.

- `delay_join`: Delay before calling a function and join the thread.

- `delay_daemon`: Delay before calling a function in a daemon thread.

- `delay_with_return_value`: Delay before calling a function and return
its return value.
"""

from .sew import *
