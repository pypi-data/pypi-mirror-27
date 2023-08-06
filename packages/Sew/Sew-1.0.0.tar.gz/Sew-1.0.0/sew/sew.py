from functools import wraps
import threading

__all__ = [
    "thread",
    "thread_join",
    "thread_daemon",
    "thread_with_return_value",
    "delay",
    "delay_join",
    "delay_daemon",
    "delay_with_return_value"
]


class _FunctionThreadWithReturnValue(threading.Thread):
    """Calls a function and saves the return value."""

    def __init__(self, function, args, kwargs):
        super().__init__()
        self._call = (function, args, kwargs)
        self.return_value = None

    def run(self):
        function, args, kwargs = self._call
        self.return_value = function(*args, **kwargs)


class _DelayedFunctionWithReturnValue(threading.Timer):
    """Calls a function after a certain delay and saves the return value."""

    def __init__(self, seconds, function, args, kwargs):
        super().__init__(seconds, lambda: None)
        # Gives us a reliable timer while still allowing us to store the
        # return value
        self._call = (function, args, kwargs)
        self.return_value = None

    def run(self):
        super().run()
        function, args, kwargs = self._call
        self.return_value = function(*args, **kwargs)


def thread(function):
    """Call `function(*args, **kwargs)` in a separate thread.

    Arguments:
    - function: The callable to run.
    - *args: Positional arguments to `function`.
    - **kwargs: Keyword arguments to `function`.

    Returns:
    - None.
    """
    @wraps(function)
    def call(*args, **kwargs):
        thread = threading.Thread(
            target=function,
            args=args,
            kwargs=kwargs
        )
        thread.start()
    return call


def thread_join(function):
    """Call `function(*args, **kwargs)` in a separate thread and
    join the thread.

    Arguments:
    - function: The callable to run.
    - *args: Positional arguments to `function`.
    - **kwargs: Keyword arguments to `function`.

    Returns:
    - None.
    """
    @wraps(function)
    def call(*args, **kwargs):
        thread = threading.Thread(
            target=function,
            args=args,
            kwargs=kwargs
        )
        thread.start()
        thread.join()
    return call


def thread_daemon(function):
    """Call `function(*args, **kwargs)` in a separate daemon thread.

    Arguments:
    - function: The callable to run.
    - *args: Positional arguments to `function`.
    - **kwargs: Keyword arguments to `function`.

    Returns:
    - None.
    """
    @wraps(function)
    def call(*args, **kwargs):
        thread = threading.Thread(
            target=function,
            args=args,
            kwargs=kwargs
        )
        thread.daemon = True
        thread.start()
    return call


def thread_with_return_value(function):
    """Return `function(*args, **kwargs)` from a separate thread.
    The function call will block due to the use of `join`.

    Arguments:
    - function: The callable to run.
    - *args: Positional arguments to `function`.
    - **kwargs: Keyword arguments to `function`.

    Returns:
    - The return value of `function(*args, **kwargs)`.
    """
    @wraps(function)
    def call(*args, **kwargs):
        thread = _FunctionThreadWithReturnValue(
            function=function,
            args=args,
            kwargs=kwargs
        )
        thread.start()
        thread.join()
        # Wait for the function to fall through to avoid
        # returning `None`
        return thread.return_value
    return call


def delay(seconds):
    """Wait `seconds` seconds before calling `function(*args, **kwargs)`
    in a separate thread.

    Arguments:
    - seconds: An integer or floating point number representing the amount
      of seconds to wait before calling `function(*args, **kwargs)`.
    - function: The callable to run.
    - *args: Positional arguments to `function`.
    - **kwargs: Keyword arguments to `function`.

    Returns:
    - None.
    """
    def wrap(function):
        @wraps(function)
        def call(*args, **kwargs):
            function_timer = threading.Timer(
                seconds,
                function=function,
                args=args,
                kwargs=kwargs
            )
            function_timer.start()
        return call
    return wrap


def delay_join(seconds):
    """Wait `seconds` seconds before calling `function(*args, **kwargs)`
    and joining the thread.

    Arguments:
    - seconds: An integer or floating point number representing the amount
      of seconds to wait before calling `function(*args, **kwargs)`.
    - function: The callable to run.
    - *args: Positional arguments to `function`.
    - **kwargs: Keyword arguments to `function`.

    Returns:
    - None.
    """
    def wrap(function):
        @wraps(function)
        def call(*args, **kwargs):
            function_timer = threading.Timer(
                seconds,
                function=function,
                args=args,
                kwargs=kwargs
            )
            function_timer.start()
            function_timer.join()
        return call
    return wrap


def delay_daemon(seconds):
    """Wait `seconds` seconds before calling `function(*args, **kwargs)`
    in a separate daemon thread.

    Arguments:
    - seconds: An integer or floating point number representing the amount
      of seconds to wait before calling `function(*args, **kwargs)`.
    - function: The callable to run.
    - *args: Positional arguments to `function`.
    - **kwargs: Keyword arguments to `function`.
    
    Returns:
    - None.
    """
    def wrap(function):
        @wraps(function)
        def call(*args, **kwargs):
            function_timer = threading.Timer(
                seconds,
                function=function,
                args=args,
                kwargs=kwargs
            )
            function_timer.daemon = True
            function_timer.start()
        return call
    return wrap


def delay_with_return_value(seconds):
    """Wait `seconds` seconds before returning `function(*args, **kwargs)`
    from a separate thread.

    Arguments:
    - seconds: An integer or floating point number representing the amount
      of seconds to wait before calling `function(*args, **kwargs)`.
    - function: The callable to run.
    - *args: Positional arguments to `function`.
    - **kwargs: Keyword arguments to `function`.

    Returns:
    - `function(*args, **kwargs)`.
    """
    def wrap(function):
        @wraps(function)
        def call(*args, **kwargs):
            function_timer = _DelayedFunctionWithReturnValue(
                seconds=seconds,
                function=function,
                args=args,
                kwargs=kwargs
            )
            function_timer.start()
            function_timer.join()
            return function_timer.return_value
        return call
    return wrap
