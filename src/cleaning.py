import numpy as np

class CleaningData(): 

    def cleaning_function(self, input_):   
        if type(input_) == float or type(input_) == int:
            output = input_
        elif input_.strip() == '-':
            output = np.nan
        else:
            output = input_
        return output

    def cleaning_more_than(self, input_):
        if type(input_) == float or type(input_) == int:
            output = input_
        elif input_.strip() == "> 1000":
            output = np.nan
        else:
            output = input_
        return output    


