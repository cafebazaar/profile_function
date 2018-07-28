METRIC_PROFILE_NAMESPACE = 'functions_profile'

METRIC_MODE_TIME = "time"

SEPARATOR = "."


class ProfileFunction(object):
    def __init__(self, backend, namespace=METRIC_PROFILE_NAMESPACE):
        self.backend = backend
        self.namespace = namespace

    @staticmethod
    def get_name(name, group, block, sep=SEPARATOR):
        """
        extract a function path

        args:
            func: a function to extract it's path and function name separated with dot character given as a parameter
            group: metric grouping scope
            block: specific block of the function (could be None)
        returns:
            function path separated with dot character param
        """

        path = group + sep + name
        if block is not None:
            path += sep + block

        return path

    def get_profiling_metric_name(self, name, group, block=None):
        """
        returns metric name to save in graphite

        Args:
            name: function to find metric name for profiling
            group: scope to group the function in stats
            block: specific block of the function (could be None)

        Returns:
            metric name to save it it graphite
        """
        path = self.get_name(name, group, block=block, sep=self.backend.name_separator)
        return format("{}.{}.{}".format(self.namespace, METRIC_MODE_TIME, path))

    def profile_block(self, block_name, group="other", block=None):
        """
        Records timing information for a function or a block inside a function.

        Args:
            block_name: function to find metric name for profiling or the name in string
            group: scope to group the function in stats
            block: specific block of the function (could be None)

        Returns:
            timer object
        """
        return self.backend.timer(self.get_profiling_metric_name(block_name, group, block=block))

    def profile_function(self, name=None, group="other"):
        """
        decorator to profile function, send how many and how much time a function call takes
        Args:
            name: force function path
            group: group name of a function to profile otherwise the the group name will be 'other'

        Returns:
            profile enabled function to use
        """

        def internal(func):
            def wrapper(*args, **kwargs):
                function_name = func if name is not None else func.__name__

                with self.profile_block(function_name, group):
                    return func(*args, **kwargs)

            return wrapper

        return internal


__all__ = (ProfileFunction.__name__,)
