# -*- coding: utf-8 -*-
from datetime import datetime
try:
    import matplotlib.pyplot as plt
except Exception:
    print("Library mathplotlib not found")

class plot: 
    def __init__(self, data_array = None):
        if data_array is None: 
            return
        self.data = []
        self.timearray = []
        for row in data_array: 
            self.data.append(row[1])
            self.timearray.append(datetime.utcfromtimestamp(int(row[0])).strftime('%H:%M:%S'))
        plt.plot(self.timearray, self.data)
        plt.show()
