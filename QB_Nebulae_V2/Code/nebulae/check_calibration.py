#!/bin/python2
import switch
import calibration_collector
import sys
if len(sys.argv) > 1:
    arg = sys.argv[1]
else:
    arg = None
collector = calibration_collector.CalibrationCollector()
pitch_click = switch.Switch(22) # Pitch Encoder Click GPIO
pitch_click.update() 
if pitch_click.state() == True or arg == 'force':
#if 1 >= 0:
    print 'Calibration commencing'
    collector.collect()
else:
    print 'Skipping Calibration'

     


