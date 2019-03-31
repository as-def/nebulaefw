# Main Nebulae Source File
import sys
import os
from subprocess import Popen
import ctcsound
import controlhandler as ch
import conductor
import ui
import fileloader
import time
import logger


debug = False
debug_controls = False

class Nebulae(object):

    def __init__(self):
        print "Nebulae Initializing"
        #self.c = ctcsound.Csound()    # Create an instance of Csound
        self.orc_handle = conductor.Conductor() # Initialize Audio File Tables and Csound Score/Orchestra
        self.currentInstr = "a_granularlooper"
        self.c = None
        self.pt = None 
        self.ui = None
        self.c_handle = None
        self.led_process = None
        self.log = logger.NebLogger()
        self.new_bank = 'factory'
        self.new_instr = 'a_granularlooper'
        self.first_run = True

    def start(self, instr, instr_bank):
        print "Nebulae Starting"
        self.currentInstr = instr
        #self.launch_bootled()
        if self.c is None:
            self.c = ctcsound.Csound()
        self.log.spill_basic_info()
        floader = fileloader.FileLoader()
        floader.reload()
        self.orc_handle.generate_orc(instr, instr_bank)
        configData = self.orc_handle.getConfigDict()
        self.c.setOption("-iadc:hw:0,0")
        self.c.setOption("-odac:hw:0,0")  # Set option for Csound
        if configData.has_key("-B"):
            self.c.setOption("-B"+str(configData.get("-B")[0]))
        else: 
            self.c.setOption("-B512") # Liberal Buffer

        if configData.has_key("-b"):
            self.c.setOption("-b"+str(configData.get("-b")[0]))
        self.c.setOption("--realtime")
        self.c.setOption("-+rtaudio=alsa") # Set option for Csound
        #self.c.setOption("--sched")
        if debug is True:
            self.c.setOption("-m7")
        else:
            self.c.setOption("-m0")  # Set option for Csound
            self.c.setOption("-d")
        self.c.compileOrc(self.orc_handle.curOrc)     # Compile Orchestra from String
        self.c.readScore(self.orc_handle.curSco)     # Read in Score generated from notes 
        self.c.start() # Start Csound
        self.c_handle = ch.ControlHandler(self.c, self.orc_handle.numFiles(), configData, self.new_instr, bank=self.new_bank) # Create handler for all csound comm.
        self.loadUI()
        self.pt = ctcsound.CsoundPerformanceThread(self.c.csound()) # Create CsoundPerformanceThread 
        self.pt.play() # Begin Performing the Score in the perforamnce thread
        self.c_handle.updateAll() # Update all values to ensure their at their initial state.

    def run(self):
        new_instr = None
        request = False
        if self.first_run == False:
            self.c_handle.restoreAltToDefault()
        while (self.pt.status() == 0): # Run a loop to poll for messages, and handle the UI.
            self.ui.update()
            self.c_handle.updateAll()
            if debug_controls == True:
                self.c_handle.printAllControls()
            request = self.ui.getReloadRequest()
            if request == True:
                self.cleanup()
        if request == True:
            self.first_run = False
            print "Received Reload Request from UI"
            print "index of new instr is: " + str(self.c_handle.instr_sel_idx)
            self.new_instr = self.ui.getNewInstr()
            print "new instr: " + self.new_instr
            self.new_bank = self.c_handle.getInstrSelBank() 
            print "new bank: " + self.new_bank
            self.c.cleanup()
            self.ui.reload_flag = False # Clear Reload Flag
            print "Reloading " + self.new_instr + " from " + self.new_bank
            if self.new_bank == "puredata":
                self.start_puredata(self.new_instr)
                self.run_puredata()
            else:
                self.c.reset()
                self.start(self.new_instr, self.new_bank)
                self.run()
        else:
            print "Run Loop Ending."
            self.cleanup()
            print "Goodbye!"
            sys.exit()

    def cleanup(self):
        print "Cleaning Up"
        self.pt.stop()
        self.pt.join()

    def start_puredata(self, patch):
        #self.launch_bootled()
        self.log.spill_basic_info()
        if self.c is not None:
            self.c.cleanup() 
            self.c = None
        self.c_handle = None
        self.currentInstr = patch
        self.newInstr = patch
        floader = fileloader.FileLoader()
        floader.reload()
        self.orc_handle.refreshFileHandler()
        fullPath = "/home/alarm/pd/" + patch + ".pd"
        #cmd = "pd -rt -nogui -verbose -audiobuf 5".split()
        if debug == False:
            cmd = "pd -rt -callback -nogui -audiobuf 5".split()
        else:
            cmd = "pd -rt -callback -nogui -verbose -audiobuf 5".split()
        cmd.append(fullPath)
        self.pt = Popen(cmd)
        print 'sleeping'
        time.sleep(2)
        self.c_handle = ch.ControlHandler(None, self.orc_handle.numFiles(), None, self.new_instr, bank="puredata")
        self.c_handle.enterPureDataMode()
        self.loadUI()
        

    def run_puredata(self):
        new_instr = None
        request = False
        self.c_handle.enterPureDataMode()
        while(request != True):
            self.c_handle.updateAll()
            if debug_controls == True:
                self.c_handle.printAllControls()
            self.ui.update()
            request = self.ui.getReloadRequest()
        if request == True:
            print "Received Reload Request from UI"
            print "index of new instr is: " + str(self.c_handle.instr_sel_idx)
            self.new_instr = self.ui.getNewInstr()
            self.new_bank = self.c_handle.getInstrSelBank() 
            self.ui.reload_flag = False # Clear Reload Flag
            print "Reloading " + self.new_instr + " from " + self.new_bank
            self.cleanup_puredata()
            if self.new_bank == "puredata":
                self.start_puredata(self.new_instr)
                self.run_puredata()
            else:
                self.start(self.new_instr, self.new_bank)
                self.run()
        else:
            print "Run Loop Ending."
            self.cleanup_puredata()
            print "Goodbye!"
            sys.exit()
            
    def cleanup_puredata(self): 
        #self.pt.terminate()
        self.pt.terminate()
        #self.pt.join()
        self.pt.kill()
        #os.system("sudo pkill pd")

    def loadUI(self):
        print "Killing LED program"
        cmd = "sudo pkill -1 -f /home/alarm/QB_Nebulae_V2/Code/nebulae/bootleds.py"
        os.system(cmd)
        #print 'Waiting for LED process parent to terminate'
        #self.led_process.wait()
        #print 'Done waiting'
        #if self.led_process is not None:
        #else:
            #cmd = "sudo pkill -1 -f /home/alarm/QB_Nebulae_V2/Code/nebulae/bootleds.py"
            #os.system(cmd)
        if self.ui is None:
            self.ui = ui.UserInterface(self.c_handle) # Create User Interface
        else:
            self.ui.controlhandler = self.c_handle
            self.ui.clearAllLEDs()
        self.c_handle.setInstrSelBank(self.new_bank)
        self.ui.setCurrentInstr(self.new_instr)

    def launch_bootled(self):
        cmd = "sudo pkill -1 -f /home/alarm/QB_Nebulae_V2/Code/nebulae/bootleds.py"
        os.system(cmd)
        print "Launching LED program"
        fullCmd = "python2 /home/alarm/QB_Nebulae_V2/Code/nebulae/bootleds.py loading"
        self.led_process = Popen(fullCmd, shell=True)
        print 'led process created: ' + str(self.led_process)


### NEBULAE ###
app = Nebulae()

#try: 
app.start("a_granularlooper", "factory")
app.run()

#app.start_puredata("rhythmic_chords_tcp")
#app.run_puredata()
#except (KeyboardInterrupt, SystemExit):
#    print "Keyboard Exit, or System Exit detected."
#    raise
#except Exception as ex:
#    template = "An exception of type {0} occurered. Arguments:\n{1!r}"
#    app.cleanup()
#    print "Program ended"
