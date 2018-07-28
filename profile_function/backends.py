import timeit


class CollectorBackend(object):
    name_separator = None

    def timer(self, name):
        pass


class StatsdBackend(CollectorBackend):
    name_separator = '.'

    def __init__(self, statsd):
        self.statsd = statsd

    def timer(self, name):
        return self.statsd.timer(name)


class TimerContext(object):
    log_format = "{}: elapsed {}"

    def __init__(self, logger, name, log_level):
        self.start = None
        self.name = name
        self.logger = logger
        self.log_level = log_level

    def __enter__(self):
        self.start = timeit.default_timer()

    def __exit__(self, *args):
        self.elapsed = timeit.default_timer() - self.start
        self.logger.log(self.log_level, self.log_format.format(self.name, self.elapsed))


class LoggerBackend(CollectorBackend):
    name_separator = '.'

    def __init__(self, logger, log_level='INFO'):
        self.logger = logger
        self.log_level = log_level

    def timer(self, name):
        return TimerContext(self.logger, name, self.log_level)


class PrometheusBackend(CollectorBackend):
    name_separator = '_'

    def timer(self, name):
        raise NotImplemented("Not implemented yet!")
