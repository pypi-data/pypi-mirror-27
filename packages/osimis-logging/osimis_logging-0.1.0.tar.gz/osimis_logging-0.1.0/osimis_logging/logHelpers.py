import json, logging, sys, random, uuid, os
from copy import deepcopy

class LogContext():
    def __init__(self, contextualLogger, contextString):
        self._contextualLogger = contextualLogger
        self._contextString = contextString

    def __enter__(self):
        return self._contextualLogger._contexts.append(self._contextString)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._contextualLogger._contexts.pop()


class ContextualLogger:
    """ logger with a hierarchical context.  (check sample code at the end of the file).

    This is not thread safe !!

    Example:
        2017-02-06 22:39:51,318 - TEST - INFO | message
        2017-02-06 22:39:51,318 - TEST - INFO | TUTU | message
        2017-02-06 22:39:51,318 - TEST - INFO | TUTU | TATA | message
        2017-02-06 22:39:51,318 - TEST - INFO | TUTU | TATA | 11376257 | message
        2017-02-06 22:39:51,318 - TEST - INFO | message
    """

    def __init__(self, logger, context = None):
        self._contexts = []
        self._logger = logger
        self._context = context

        if context is None:
            self._context = '{i:06}'.format(i = random.randint(0, 999999))
        else:
            self._context = context

    def context(self, contextString = None):
        """creates a LogContext to use in a 'with' statement"""
        if contextString is None:
            contextString = uuid.uuid4().hex.upper()[:8]
        return LogContext(self, contextString)

    def info(self, msg, *args, **kwargs):
        if os.linesep in msg:
            splitMessages = msg.splitlines(keepends = False)
            for split in splitMessages:
                self.info(split, *args, **kwargs)
        else:
            self._logger.info(msg, extra = {'context' : self._getLogContextsString()}, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self._logger.critical(msg, extra = {'context' : self._getLogContextsString()}, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._logger.warning(msg, extra = {'context' : self._getLogContextsString()}, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._logger.error(msg, extra = {'context' : self._getLogContextsString()}, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        self._logger.exception(msg, extra = {'context' : self._getLogContextsString()}, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self._logger.debug(msg, extra = {'context' : self._getLogContextsString()}, *args, **kwargs)

    def _getLogContextsString(self):
        if len(self._contexts) == 0:
            return ''
        return ' ' + ' | '.join(self._contexts) + ' |'


class ContextualNullLogger(ContextualLogger):
    """ Null logger that will avoid you to test if you have defined a logger.
    # instead of writing
    if self._logger:
        self._logger.info('toto')

    # use
    self._logger = LogHelpers.getNullLogger()
    # so you can write
    self._logger.info('toto')
    """

    def __init__(self):
        ContextualLogger.__init__(self, None)

    def info(self, msg, *args, **kwargs):
        pass

    def critical(self, msg, *args, **kwargs):
        pass

    def warning(self, msg, *args, **kwargs):
        pass

    def error(self, msg, *args, **kwargs):
        pass

    def debug(self, msg, *args, **kwargs):
        pass

    def exception(self, msg, *args, **kwargs):
        pass


class LogHelpers:

    loggingLevel = logging.INFO
    loggers = {}
    logConsoleHandler = None
    logFileHandler = None
    _isConfigured = False

    @staticmethod
    def configureLogging(loggingLevel = logging.DEBUG, enableStdOutLogging = True, logFileName = None):
        """configures logging at the app level.  This configuration will be applied to all loggers created afterwards"""

        LogHelpers.loggingLevel = loggingLevel
        logFormatter = logging.Formatter('%(asctime)s - %(name)+10s - %(levelname)+10s |%(context)s %(message)s')

        if enableStdOutLogging and LogHelpers.logConsoleHandler is None:
            LogHelpers.logConsoleHandler = logging.StreamHandler(stream=sys.stdout)
            LogHelpers.logConsoleHandler.setLevel(loggingLevel)
            LogHelpers.logConsoleHandler.setFormatter(logFormatter)

        if logFileName is not None and LogHelpers.logFileHandler is None:
            LogHelpers.logFileHandler = logging.FileHandler(logFileName)
            LogHelpers.logFileHandler.setLevel(loggingLevel)
            LogHelpers.logFileHandler.setFormatter(logFormatter)

        #if some loggers have already been created before the configuration, reconfigure them
        if len(LogHelpers.loggers) > 0:
            for loggerName, logger in LogHelpers.loggers.items():
                LogHelpers._configureLogger(logger)
        LogHelpers._isConfigured = True

    @staticmethod
    def clearLoggingConfiguration():
        LogHelpers.logConsoleHandler = None
        LogHelpers.logFileHandler = None

    @staticmethod
    def _configureLogger(logger):
        logger._logger.setLevel(LogHelpers.loggingLevel)
        if LogHelpers.logConsoleHandler is not None and LogHelpers.logConsoleHandler not in logger._logger.handlers:
            logger._logger.addHandler(LogHelpers.logConsoleHandler)
        if LogHelpers.logFileHandler is not None and LogHelpers.logFileHandler not in logger._logger.handlers:
            logger._logger.addHandler(LogHelpers.logFileHandler)

    @staticmethod
    def getLogger(loggerName):
        if loggerName in LogHelpers.loggers:
            return LogHelpers.loggers[loggerName]

        # creates a new logger and configure it directly
        logger = logging.getLogger(loggerName)
        logger.propagate = False #don't propagate to default logger

        contextualLogger = ContextualLogger(logger)
        LogHelpers.loggers[loggerName] = contextualLogger

        if LogHelpers._isConfigured:
            LogHelpers._configureLogger(contextualLogger)

        return contextualLogger

    @staticmethod
    def getNullLogger():
        return ContextualNullLogger()


    @staticmethod
    def summarizeObjectForLogging(data, maxChildStringSize = 100, maxParentStringSize = 200):
        """removes long strings from an object so we can display it in the logs

        :param data: the object to summarize
        :return: a copy of the object where long strings have been pruned
        """
        if data is None:
            return data
        if isinstance(data, str):  # if the parent is a string
            if len(data) > maxParentStringSize:
                return data[:maxParentStringSize] + ' ...'
            else:
                return data
        if isinstance(data, list) or isinstance(data, dict):
            data = deepcopy(data)
        return LogHelpers._summarizeObjectForLogging(data, maxChildStringSize)

    @staticmethod
    def _summarizeObjectForLogging(data, maxStringSize):
        if isinstance(data, str):
            if len(data) > maxStringSize:
                return data[:maxStringSize] + ' ...'
        elif isinstance(data, dict):
            for k, v in data.items():
                data[k] = LogHelpers._summarizeObjectForLogging(v, maxStringSize)
        elif isinstance(data, list):
            for i in range(0, len(data)):
                data[i] = LogHelpers.summarizeObjectForLogging(data[i], maxStringSize)
        return data

    @staticmethod
    def getDataStringForLogging(data, prettyJsonPrint = False):
        if data is None:
            dataString = 'None'
        elif isinstance(data, dict) or isinstance(data, list):
            if prettyJsonPrint:
                dataString = json.dumps(LogHelpers.summarizeObjectForLogging(data), indent=4)
            else:
                dataString = str(LogHelpers.summarizeObjectForLogging(data))
        else:
            dataString = 'binary data: {0} bytes'.format(len(data))
        return dataString


if __name__ == "__main__":
    LogHelpers.configureLogging()

    logger = LogHelpers.getLogger('TEST')
    logger.critical('criticalmessage')

    with logger.context('TUTU'):
        logger.info('info message')
        with logger.context('TATA'):
            logger.debug('debug message')
            with logger.context():
                logger.error('error message')

    logger.warning('warning message')

    # same test with the null logger
    logger = LogHelpers.getNullLogger()
    logger.critical('criticalmessage')

    with logger.context('TUTU'):
        logger.info('info message')
        with logger.context('TATA'):
            logger.debug('debug message')
            with logger.context():
                logger.error('error message')


# output:
# 2017-02-06 22:58:08,444 -       TEST -   CRITICAL | criticalmessage
# 2017-02-06 22:58:08,444 -       TEST -       INFO | TUTU | info message
# 2017-02-06 22:58:08,444 -       TEST -      DEBUG | TUTU | TATA | debug message
# 2017-02-06 22:58:08,444 -       TEST -      ERROR | TUTU | TATA | 40E4BFB3 | error message
# 2017-02-06 22:58:08,444 -       TEST -    WARNING | warning message
