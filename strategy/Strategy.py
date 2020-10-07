import abc


class Strategy(metaclass=abc.ABCMeta):

    def __init__(self):
        self.historical = None
        self.fundamentals = None
        self.period = None
        self.start_date = None
        self.end_date = None
        self.interval = None
        self.indicators = []
        self.kpi = []
        self.fundamentals = False



    def set_data_source_required_parameters(self):
        pass

    def set_date_parameters(self):
        pass



