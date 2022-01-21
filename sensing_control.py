# week 3

from adc import ADC

class Sensing(object):
    def __init__(self,ref = 1000):
        self.chn_0 = ADC("A0")
        self.chn_1 = ADC("A1")
        self.chn_2 = ADC("A2")
        self.ref = ref


    def Sensing(self):
        adc_value_list = []
        adc_value_list.append(self.chn_0.read())
        adc_value_list.append(self.chn_1.read())
        adc_value_list.append(self.chn_2.read())
        return adc_value_list

class ProcessData(object):
    # take arguments for sensitivity and polarity
    def __init__(self, sensitivity, polarity, ref_s = 1000, ref_p = 10):
        print("enter")
    #main processing, sense edge, allign with center

    #return the position

# 
# class Controller(object):
#     def __init__(self):
#  # automatic steering

if __name__=='__main__':
    sense = Sensing()
    print("Welcoem to week 3 coding")
    while (True):
        print(sense.Sensing())

 # sensor control integration
 # camera based driving
