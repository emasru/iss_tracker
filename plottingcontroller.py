# -*- coding: utf-8 -*-
def mathplotlib_import_error():
	print("Library mathplotlib not found")

try:
    import matplotlib.pyplot as plt
except Exception: 
	mathplotlib_import_error()
class plot: 
    def __init__(self, data_array = None):
        if data_array is None: 
            return
        self.data = []
        self.timearray = []
        for row in data_array: 
            self.data.append(row[1])
            self.timearray.append(row[0])
        plt.plot(self.timearray, self.data)
        plt.show()
