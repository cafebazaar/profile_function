import six

METRIC_PROFILE_NAMESPACE = 'functions_profile'

METRIC_MODE_TIME = "time"


class ProfileFunction(object):
    def __init__(self, statsd, namespace=METRIC_PROFILE_NAMESPACE):
        self.statsd = statsd
        self.namespace = namespace

    @staticmethod
    def get_function_path(func, group, block):
        """
        extract a function path

        args:
            func: a function to extract it's path and function name separated with dot character given as a parameter
            group: metric grouping scope
            block: specific block of the function (could be None)
        returns:
            function path separated with dot character param
        """

        function_name = func if isinstance(
            func, six.string_types) else func.__name__
        path = group + "." + function_name
        if block is not None:
            path += '.' + block

        return path

    def get_profiling_metric_name(self, func, group, block=None):
        """
        returns metric name to save in graphite

        Args:
            func: function to find metric name for profiling
            group: scope to group the function in stats
            block: specific block of the function (could be None)

        Returns:
            metric name to save it it graphite
        """
        path = self.get_function_path(func, group, block=block)
        return format("{}.{}.{}".format(self.namespace, METRIC_MODE_TIME, path))

    def profile_block(self, func, group, block=None):
        """
        Records timing information for a function or a block inside a function.

        Args:
            func: function to find metric name for profiling
            group: scope to group the function in stats
            block: specific block of the function (could be None)

        Returns:
            timer object
        """
        return self.statsd.timer(self.get_profiling_metric_name(func, group, block=block))

    def profile_function(self, name=None, group="other"):
        """
        decorator to profile function, send how many and how much time a function call takes
        Args:
            name: force function path
            group: group name of a function to profile otherwise the the group name will be 'other'

        Returns:
            profile enabled function to use
        """

        def internal(f):
            def wrapper(*args, **kwargs):
                with self.profile_block(name or f, group):
                    return f(*args, **kwargs)

            return wrapper

        return internal
