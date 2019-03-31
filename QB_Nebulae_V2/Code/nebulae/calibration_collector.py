import os
import time
import controlhandler
#import leddriver

class CalibrationCollector(object):
    def __init__(self):
        self.ch = controlhandler.ControlHandler(None, 0, None) # Create new Controlhandler.

    def collect(self):
        self.ch.updateAll()
        data = []
        avg = 0
        numSamps = 128
        #name = "start"
        names = ['start', 'size', 'density', 'overlap', 'blend', 'window', 'speed', 'pitch']
        avgs = {}
        for name in names:
            for i in range(0,numSamps):
                self.ch.updateAll()
                val = self.ch.channeldict[name].getRawCVValue()
                data.append(val)
                avg += val
            avg = avg / numSamps
            avgs[name] = avg
        filepath = '/home/alarm/QB_Nebulae_V2/Code/misc/'
        filename = 'calibration_data.txt'
        os.system("sh /home/alarm/QB_Nebulae_V2/Code/scripts/mountfs.sh rw")
        with open(filepath + filename, 'w') as myfile:
            for name in names:
                stuff = [name, str(avgs[name]), '\n']
                line = ','.join(stuff)
                myfile.write(line)
        os.system("sh /home/alarm/QB_Nebulae_V2/Code/scripts/mountfs.sh ro")
            

