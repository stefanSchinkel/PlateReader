class DataSet(object):
    """Dataset as object"""
    def __init__(self):
        self.row = None
        self.col = None
        self.col_ = None
        self.inner_x = None
        self.inner_y = None
        self.outer_x = None
        self.outer_y = None
        self.labels = []
        self.n_wells = None
        self.data = None

    def __str__(self):
        """Verbose info"""
        return "Dataset with {} wells at {}x{} resolution".format(
                self.n_wells, self.inner_x, self.inner_y)