from Monsoon import LVPM
from Monsoon import sampleEngine
from Monsoon import Operations as op
from Monsoon import HVPM
from Monsoon import pmapi
import usb.core

def testHVPM(serialno=None,Protocol=pmapi.USB_protocol()):
    HVMON = HVPM.Monsoon()
    HVMON.setup_usb(serialno,Protocol)
    print("HVPM Serial Number: " + repr(HVMON.getSerialNumber()))
    HVMON.fillStatusPacket()
    HVMON.setVout(3)
    HVengine = sampleEngine.SampleEngine(HVMON)
    HVengine.ConsoleOutput(False)
    for i in range(10000):
        try:
            HVengine.startSampling(10)
            print(i)
        except usb.core.USBError as e:
            print(e.message)
            if(e.backend_error_code == -116):
                print("Error hit.  Reconnecting")
                HVMON.reconnect()
            else:
                print(e.message)
            
    HVengine.enableCSVOutput("HV Main Example.csv")
    HVengine.ConsoleOutput(True)
    numSamples=sampleEngine.triggers.SAMPLECOUNT_INFINITE #Don't stop based on sample count, continue until the trigger conditions have been satisfied.
    HVengine.setStartTrigger(sampleEngine.triggers.GREATER_THAN,0) #Start when we exceed 0 s
    HVengine.setStopTrigger(sampleEngine.triggers.GREATER_THAN,5) #Stop when we exceed 5 s.
    HVengine.setTriggerChannel(sampleEngine.channels.timeStamp) #Start and stop judged by the timestamp channel.
    HVengine.startSampling(numSamples)
    HVMON.closeDevice();

def testLVPM(serialno=None,Protcol=pmapi.USB_protocol()):
    Mon = LVPM.Monsoon()
    Mon.setup_usb(serialno,Protcol)
    print("LVPM Serial number: " + repr(Mon.getSerialNumber()))
    Mon.fillStatusPacket()
    Mon.setVout(4.5)
    engine = sampleEngine.SampleEngine(Mon)
    engine.enableCSVOutput("Main Example.csv")
    engine.ConsoleOutput(True)
    #test main channels
    numSamples=sampleEngine.triggers.SAMPLECOUNT_INFINITE #Don't stop based on sample count, continue until the trigger conditions have been satisfied.
    engine.setStartTrigger(sampleEngine.triggers.GREATER_THAN,0) #Start when we exceed 0 s
    engine.setStopTrigger(sampleEngine.triggers.GREATER_THAN,5) #Stop when we exceed 5 s.
    engine.setTriggerChannel(sampleEngine.channels.timeStamp) #Start and stop judged by the timestamp channel.
    engine.startSampling(numSamples)


    #Disable Main channels
    engine.disableChannel(sampleEngine.channels.MainCurrent)
    engine.disableChannel(sampleEngine.channels.MainVoltage)

    engine.setStartTrigger(sampleEngine.triggers.GREATER_THAN,5)
    engine.setStopTrigger(sampleEngine.triggers.GREATER_THAN,10)
    engine.setTriggerChannel(sampleEngine.channels.timeStamp)
    #Take measurements from the USB Channel
    Mon.setVout(0)
    #Set USB Passthrough mode to 'on,' since it defaults to 'auto' and will turn off when sampling mode begins.
    Mon.setUSBPassthroughMode(op.USB_Passthrough.On)
    #Enable USB channels
    engine.enableChannel(sampleEngine.channels.USBCurrent)
    engine.enableChannel(sampleEngine.channels.USBVoltage)
    engine.enableCSVOutput("USB Test.csv")
    engine.startSampling(5000)

    #Enable every channel, take measurements
    engine.enableChannel(sampleEngine.channels.MainVoltage)
    engine.enableChannel(sampleEngine.channels.MainCurrent)
    #Enable Aux channel
    engine.enableChannel(sampleEngine.channels.AuxCurrent)
    Mon.setVout(2.5)
    engine.enableCSVOutput("All Test.csv")
    engine.startSampling(5000)

    #Enable every channel, take measurements, and retrieve them as a Python list.
    engine.disableCSVOutput()
    engine.startSampling(5000)
    samples = engine.getSamples()
    Mon.closeDevice();
    
#testLVPM(60001,pmapi.USB_protocol())
testHVPM(60000,pmapi.CPP_Backend_Protocol())
