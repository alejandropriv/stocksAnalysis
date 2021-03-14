import abc
from utilities.Constants import Constants


class KPI(metaclass=abc.ABCMeta):

    class KPIResult:
        def __init__(self, name, result):
            self.name = name
            self.result = result

        def get_result(self):
            return self.result

        def print(self):
            print("Name: {} \n Result: {}".format(self.name, self.result))

    @abc.abstractmethod
    def __init__(self, params=None):
        if params is None:
            params = {}

        self.kpi_name = ""
        self.result = {"name": "", "result": 0}
        self.params = params

    @abc.abstractmethod
    def calculate(self, df, params=None):
        if params is not None:
            self.params = params

    @staticmethod
    def get_reference_days(params):
        if "period" in params.keys():
            period = params["period"]
        else:
            period = Constants.INTERVAL.MONTH

        if period == Constants.INTERVAL.DAY:
            # 252 trading days
            reference_days = 252
        else:
            # 12 months
            reference_days = 12

        return reference_days

