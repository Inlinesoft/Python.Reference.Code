import inspect

class Executor:
    def __init__(self, funcs):
        self.funcs = funcs

    def _execute(self, func, stats):

         
        src = inspect.getsource(func)
        name = func.__name__
        data_point_key = name.replace("calc_", "")

        params = stats.datapoints.filter_to_dict(sig.parameters.keys())

        data_point_value = func(**params)
        stats.datapoints.add_from(data_point_key, data_point_value)
        stats.metacalcs.add(
            params, name, src, data_point_key, data_point_value
        )

    def execute(self, stats):
        for func in self.funcs:
            self._execute(func, stats)
        return stats
