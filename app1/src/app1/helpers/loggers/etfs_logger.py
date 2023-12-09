import logging
import logging.config
import os
import sys

from config.definitions import common

# This code is mainly copied from the python logging module, with minor modifications

# _srcfile is used when walking the stack to check when we've got the first
# caller stack frame.
#
if hasattr(sys, 'frozen'): #support for py2exe
    _srcfile = "logging%s__init__%s" % (os.sep, __file__[-4:])
elif __file__[-4:].lower() in ['.pyc', '.pyo']:
    _srcfile = __file__[:-4] + '.py'
else:
    _srcfile = __file__
_srcfile = os.path.normcase(_srcfile)

class ETFSLogger(logging.Logger):
    """
    Logger wrapper class that logs Activity as well as Performance information
    in two different log files (see config file for log path info)

    Usage:
    Initialise -
    self.etfslogger = etfs_logger.ETFSLogger(__name__)

    Performance logging -
    self.etfslogger.info_performance(<message>)

    Activity logging -
    self.etfslogger.info(<message>)
    self.etfslogger.error(<message>)
    """

    def __init__(self, logger_name=None, logfile_name=None, logfile_performance_name=None):

        if logger_name:
            self._logger_name = logger_name

        if logfile_name:
            self._logfile_name = logfile_name

        if logfile_performance_name:
            self._logfile_performance_name = logfile_performance_name

        logging.Logger.__init__(self, logger_name)

        self.setup_logger()

    def setup_logger(self):
        """
        This method initialises the code to read from the setup file
        It is implicitly called when a method call to get the logger
        is made
        :return: none
        """
        logging.config.fileConfig(common['LOGGING_CONFIG_PATH'],
                                  defaults={'logfilename': self._logfile_name,
                                            'performancelogfilename': self._logfile_performance_name})

    def get_logger(self, name=''):
        """
        This method returns the named logger which is usually a module
            level logger that can subsequently be used to record log entries
            This method is ideally used to call either the root or the child
            named loggers
            :return: Logger ()
        :param name:
        :return:
        """
        if self._logger_name:
            return logging.getLogger(self._logger_name)
        else:
            return logging.getLogger()

    def get_logger_etfs(self):
        """
        This method returns the named logger which is usually a module
            level logger that can subsequently be used to record log entries
            This method is ideally used to call either the root or the child
            named loggers
            :return: Logger ()
        :return:
        """
        return logging.getLogger('Activity')

    def get_logger_performance(self):
        """
        This method reads from the config file and returns the performance
            logger that can subsequently be used to record log entries
        :return: Logger (setup as Performance logger in the ini file)
        """
        return logging.getLogger('Performance')

    def info_performance(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'INFO'.
        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.
        logger.info("Houston, we have a %s", "interesting problem", exc_info=1)
        """
        if common['LOGGING_PERFORMANCE_ENABLED']:
            self._log(self.get_logger_performance(), logging.INFO, msg, args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'INFO'.
        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.
        logger.info("Houston, we have a %s", "interesting problem", exc_info=1)
        """
        if common['LOGGING_ACTIVITY_ENABLED']:
            if self.get_logger_etfs().isEnabledFor(logging.INFO):
                # avoid logging passwords and AWS keys
                if "AWS_ACCESS_KEY_ID" in msg or "AWS_SECRET_ACCESS_KEY" in msg or "PASSWORD" in msg or "DB_SRVR_CONN" in msg:
                    self._log(self.get_logger_etfs(), logging.INFO, "Skipping sensitive data", args, **kwargs)
                else:
                    self._log(self.get_logger_etfs(), logging.INFO, msg, args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'DEBUG'.
        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.
        logger.debug("Houston, we have a %s", "thorny problem", exc_info=1)
        """
        if common['LOGGING_ACTIVITY_ENABLED']:
            if self.get_logger_etfs().isEnabledFor(logging.DEBUG):
                self._log(self.get_logger_etfs(), logging.DEBUG, msg, args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'WARN'.
        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.
        logger.info("Houston, we have a %s", "interesting problem", exc_info=1)
        """
        if common['LOGGING_ACTIVITY_ENABLED']:
            if self.get_logger_etfs().isEnabledFor(logging.WARNING):
                self._log(self.get_logger_etfs(), logging.WARNING, "<<< warning >>> " + str(msg), args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'ERROR'.
        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.
        logger.info("Houston, we have a %s", "interesting problem", exc_info=1)
        """
        if common['LOGGING_ACTIVITY_ENABLED']:
            if self.get_logger_etfs().isEnabledFor(logging.ERROR):
                self._log(self.get_logger_etfs(), logging.ERROR, "<<< Error >>> " + str(msg), args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'CRITICAL'.
        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.
        logger.info("Houston, we have a %s", "interesting problem", exc_info=1)
        """
        if common['LOGGING_ACTIVITY_ENABLED']:
            if self.get_logger_etfs().isEnabledFor(logging.CRITICAL):
                self._log(self.get_logger_etfs(), logging.CRITICAL, "<<< Critical >>> " + str(msg), args,
                          **kwargs)

    def exception(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'ERROR' for Exceptions.
        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.
        logger.info("Houston, we have a %s", "interesting problem", exc_info=1)
        """
        if common['LOGGING_ACTIVITY_ENABLED']:
            if self.get_logger_etfs().isEnabledFor(logging.ERROR):
                if (sys.exc_info()):
                    msg = str(msg) + str(sys.exc_info()[1])
                self._log(self.get_logger_etfs(), logging.ERROR, "<<< Exception >>>" + str(msg), args, sys.exc_info(), **kwargs)

    def _log(self, logger, level, msg, args, exc_info=None, extra=None):
        """
        Low-level logging routine which creates a LogRecord and then calls
        all the handlers of this logger to handle the record.
        """
        # Add wrapping functionality here.
        if _srcfile:
            # IronPython doesn't track Python frames, so findCaller throws an
            # exception on some versions of IronPython. We trap it here so that
            # IronPython can use logging.
            try:
                fn, lno, func = self.findCaller()
            except ValueError:
                fn, lno, func = "(unknown file)", 0, "(unknown function)"
        else:
            fn, lno, func = "(unknown file)", 0, "(unknown function)"
        if exc_info:
            if not isinstance(exc_info, tuple):
                exc_info = sys.exc_info()
        record = self.get_logger_etfs().makeRecord(
            logger.name, level, fn, lno, msg, args, exc_info, func, extra)
        logger.handle(record)

    def findCaller(self):
        """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        """
        f = logging.currentframe()
        # On some versions of IronPython, currentframe() returns None if
        # IronPython isn't run with -X:Frames.
        if f is not None:
            f = f.f_back.f_back
        rv = "(unknown file)", 0, "(unknown function)"
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            # if filename == _srcfile or 'log_decorate.py' in filename:
            if filename == _srcfile in filename:
                f = f.f_back
                continue
            rv = (co.co_filename, f.f_lineno, co.co_name)
            break
        return rv
