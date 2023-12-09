import inspect
import traceback
import time
import functools
import sys


def profile(input_capture=False):
    """
       A decorator that wraps the passed in function and logs
       exceptions should one occur

       """

    def decorator(func):

        # functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            arg_names = func.__code__.co_varnames[:func.__code__.co_argcount]
            args = args[:len(arg_names)]
            defaults = func.__defaults__ or ()
            args = args + defaults[len(defaults) - (func.__code__.co_argcount - len(args)):]
            params = list(zip(arg_names, args))
            args = args[len(arg_names):]
            if args: params.append(('args', args))
            if kwargs: params.append(('kwargs', kwargs))
            # print(func.__name__ + ' (' + ', '.join('%s = %r' % p for p in params) + ' )')

            if self.etfs_logger and input_capture:
                self.etfs_logger.info(func.__name__ + ' (' + ', '.join('%s = %r' % p for p in params) + ' )')

            frame = inspect.currentframe()
            stack_trace = traceback.format_stack(frame)

            start = time.time()

            f = func(self, *args, **kwargs)

            end = time.time()

            if self.etfs_logger:
                self.etfs_logger.info_performance("{} ran in {}s".format(stack_trace[:-1][-1], str(round(end - start, 2))))

            else:
                print("{} ran in {}s".format(stack_trace[:-1][-1], str(round(end - start, 2))))

            return f

        return wrapper

    return decorator


def log_exception():
    """
       A decorator that wraps the passed in function and logs
       exceptions should one occur

       """

    def decorator(func):

        functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            try:

                return func(self, *args, **kwargs)

            except Exception:
                # log the exception
                # err = "There was an exception in  "
                # err += func.__name__
                # self.etfs_logger.exception(err)
                # raise
                exc_type, exc_instance, exc_traceback = sys.exc_info()
                formatted_traceback = ''.join(traceback.format_tb(
                    exc_traceback))
                err = "There was an exception in  "
                err += func.__name__
                message = '\n{0}\n{1}:\n{2}'.format(
                    formatted_traceback,
                    exc_type.__name__,
                    exc_instance.args[0],
                    err
                )

                if self.etfs_logger:
                    self.etfs_logger.exception(message)

                raise exc_type(message)

        return wrapper

    return decorator


def caller_name(skip=2):
    """Get a name of a caller in the format module.class.method

       `skip` specifies how many levels of stack to skip while getting caller
       name. skip=1 means "who calls me", skip=2 "who calls my caller" etc.

       An empty string is returned if skipped levels exceed stack height
    """
    stack = inspect.stack()
    start = 0 + skip
    if len(stack) < start + 1:
        return ''
    parentframe = stack[start][0]

    name = []
    module = inspect.getmodule(parentframe)
    # `modname` can be None when frame is executed directly in console
    # TODO(techtonik): consider using __main__
    if module:
        name.append(module.__name__)
    # detect classname
    if 'self' in parentframe.f_locals:
        # I don't know any way to detect call from the object method
        # XXX: there seems to be no way to detect static method call - it will
        #      be just a function call
        name.append(parentframe.f_locals['self'].__class__.__name__)
    codename = parentframe.f_code.co_name
    if codename != '<module>':  # top level usually
        name.append(codename)  # function or a method
    del parentframe
    return ".".join(name)

