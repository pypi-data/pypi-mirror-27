#!/usr/bin/python

import threading
import time
from Monsoon import HVPM
import struct
import time
import math
from Monsoon.calibrationData import calibrationData
from Monsoon import Operations as ops
from copy import deepcopy
import numpy as np

class channels:
    timeStamp = 0
    MainCurrent = 1
    USBCurrent = 2
    AuxCurrent = 3
    MainVoltage = 4
    USBVoltage = 5

class triggers:

    SAMPLECOUNT_INFINITE = 0xFFFFFFFF
    @staticmethod
    def GREATER_THAN(x,y):
        if(x > y):
            return True
        else:
            return False
    @staticmethod
    def LESS_THAN(x,y):
        if(x < y):
            return True
        else:
            return False

class SampleEngine:
    def __init__(self, Monsoon,bulkProcessRate=128):
        """Declares global variables.
        During testing, we found the garbage collector would slow down sampling enough to cause a lot of dropped samples.
        We've tried to combat this by allocating as much as possible in advance."""
        self.monsoon = Monsoon
        self.__mainCal = calibrationData()
        self.__usbCal = calibrationData()
        self.__auxCal = calibrationData()
        self.__padding = np.zeros((64))
        self.__fineThreshold = Monsoon.fineThreshold
        self.__auxFineThreshold = Monsoon.auxFineThreshold
        self.__ADCRatio = (float)(62.5 / 1e6); #Each tick of the ADC represents this much voltage
        self.__mainVoltageScale = Monsoon.mainvoltageScale
        self.__usbVoltageScale = Monsoon.usbVoltageScale
        self.dropped = 0
        self.bulkProcessRate = 128
        self.__packetSize = 64
        self.__startTime = time.time()
        #Indices
        self.__mainCoarseIndex = 0
        self.__mainFineIndex = 1
        self.__usbCoarseIndex = 2
        self.__usbFineIndex = 3
        self.__auxCoarseIndex = 4
        self.__auxFineIndex = 5
        self.__mainVoltageIndex = 6
        self.__usbVoltageIndex = 7
        self.__timestampIndex = 10
       
        #Output lists
        self.__mainCurrent = []
        self.__usbCurrent = []
        self.__auxCurrent = []
        self.__usbVoltage = []
        self.__mainVoltage = []
        self.__timeStamps = []

        #Output controls
        self.__outputConsoleMeasurements = True
        self.__outputTimeStamp = True
        self.__collectMainMeasurements = True
        self.__collectUSBMeasurements = False
        self.__collectAuxMeasurements = False
        self.__collectMainVoltage = True
        self.__collectUSBVoltage = False
        self.__channels = [self.__outputTimeStamp, self.__collectMainMeasurements,self.__collectUSBMeasurements,self.__collectAuxMeasurements,self.__collectMainVoltage,self.__collectUSBVoltage]
        self.__channelnames = ["Time(ms)","Main(mA)", "USB(mA)", "Aux(mA)", "Main Voltage(V)", "USB Voltage(V)"]
        self.__channelOutputs = [self.__mainCurrent,self.__usbCurrent,self.__auxCurrent,self.__mainVoltage,self.__usbVoltage]
        self.__sampleCount = 0
        self.__CSVOutEnable = False

        #Trigger Settings
        self.__startTriggerSet = False
        self.__stopTriggerSet = False
        self.__triggerChannel = channels.timeStamp
        self.__startTriggerLevel = 0
        self.__startTriggerStyle = np.vectorize(triggers.GREATER_THAN)
        self.__stopTriggerLevel = triggers.SAMPLECOUNT_INFINITE
        self.__stopTriggerStyle = np.vectorize(triggers.GREATER_THAN)
        self.__sampleLimit = 50000

        #output writer
        self.__f = None

        pass

    def setStartTrigger(self,triggerStyle,triggerLevel):
        """Controls the conditions when the sampleEngine starts recording measurements."""
        """triggerLevel: threshold for trigger start."""
        """triggerStyle:  GreaterThan or Lessthan.""" 
        self.__startTriggerLevel = triggerLevel
        self.__startTriggerStyle = np.vectorize(triggerStyle)
        pass

    def setStopTrigger(self,triggerstyle,triggerlevel):
        """Controls the conditions when the sampleEngine stops recording measurements."""
        """triggerLevel: threshold for trigger stop."""
        """triggerStyle:  GreaterThan or Lessthan.""" 
        self.__stopTriggerLevel = triggerlevel
        self.__stopTriggerStyle = np.vectorize(triggerstyle)

    def setTriggerChannel(self, triggerChannel):
        """Sets channel that controls the trigger."""
        self.__triggerChannel = triggerChannel

    def ConsoleOutput(self, boolValue):
        """Enables or disables the display of realtime measurements"""
        self.__outputConsoleMeasurements = boolValue

    def enableChannel(self,channel):
        """Enables a channel.  Takes sampleEngine.channel class value as input."""
        self.__channels[channel] = True 


    def disableChannel(self,channel):
        """Disables a channel.  Takes sampleEngine.channel class value as input."""
        self.__channels[channel] = False

    def enableCSVOutput(self, filename):
        """Opens a file and causes the sampleEngine to periodically output samples when taking measurements
        filename: The file measurements will be output to."""
        self.__f = open(filename,"w")
        self.__CSVOutEnable = True

    def disableCSVOutput(self):
        """Closes the CSV file if open and disables CSV output."""
        if(self.__f is not None):
            self.__f.close()
            self.__f = None
        self.__CSVOutEnable = False
    def __Reset(self):
        self.__startTriggerSet = False
        self.__stopTriggerSet = False;
        self.__sampleCount = 0
        self.__mainCal.clear()
        self.__usbCal.clear()
        self.__auxCal.clear()

        self.__ClearOutput()

    def __ClearOutput(self):
        """Wipes away all of the old output data."""
        self.__mainCurrent = []
        self.__usbCurrent = []
        self.__auxCurrent = []
        self.__usbVoltage = []
        self.__mainVoltage = []
        self.__timeStamps = []
        
    def __isCalibrated(self):
        """Returns true if every channel has sufficient calibration samples."""
        A = self.__mainCal.calibrated()
        B = self.__usbCal.calibrated()
        C = self.__auxCal.calibrated()
        return A and B and C

    def __addMeasurement(self,channel,measurement):
        if(channel == self.__triggerChannel and not self.__startTriggerSet):
            self.__evalStartTrigger(measurement)
        elif(channel == self.__triggerChannel):
            self.__evalStopTrigger(measurement[::self.__granularity])
        if(channel == channels.MainCurrent):
            self.__mainCurrent.append(measurement[::self.__granularity])
        if(channel == channels.USBCurrent):
            self.__usbCurrent.append(measurement[::self.__granularity])
        if(channel == channels.AuxCurrent):
            self.__auxCurrent.append(measurement[::self.__granularity])
        if(channel == channels.USBVoltage):
            self.__usbVoltage.append(measurement[::self.__granularity])
        if(channel == channels.MainVoltage):
            self.__mainVoltage.append(measurement[::self.__granularity])
        if(channel == channels.timeStamp):
            self.__timeStamps.append(measurement[::self.__granularity])

    def __evalStartTrigger(self, measurement):
        self.__startTriggerStyle(measurement,self.__startTriggerLevel)
        self.__startTriggerSet = np.any(self.__startTriggerStyle(measurement,self.__startTriggerLevel))

    def __evalStopTrigger(self,measurement):
        self.__sampleCount
        self.__sampleLimit
        if(self.__sampleCount > self.__sampleLimit and self.__sampleLimit is not triggers.SAMPLECOUNT_INFINITE):
            self.__stopTriggerSet = True
        if(self.__stopTriggerLevel is not triggers.SAMPLECOUNT_INFINITE):
            test = self.__stopTriggerStyle(measurement,self.__stopTriggerLevel)
            if(np.any(test)):
                self.__stopTriggerSet = True

    def __vectorProcess(self,measurements):
        """Translates raw ADC measurements into current values."""
        #Currents
        if(self.__isCalibrated()):
            measurements = np.array(measurements)
            sDebug = ""
            if(self.__channels[channels.MainCurrent]):
            #Main Coarse
                scale = self.monsoon.statusPacket.mainCoarseScale
                zeroOffset = self.monsoon.statusPacket.mainCoarseZeroOffset
                calRef = self.__mainCal.getRefCal(True)
                calZero = self.__mainCal.getZeroCal(True)
                zeroOffset += calZero
                if(calRef - zeroOffset != 0):
                    slope = scale / (calRef - zeroOffset)
                else:
                    slope = 0
                Raw = measurements[:,self.__mainCoarseIndex] - zeroOffset
                mainCoarseCurrents = Raw * slope 
        
                #Main Fine
                scale = self.monsoon.statusPacket.mainFineScale
                zeroOffset = self.monsoon.statusPacket.mainFineZeroOffset
                calRef = self.__mainCal.getRefCal(False)
                calZero = self.__mainCal.getZeroCal(False)
                zeroOffset += calZero
                if(calRef - zeroOffset != 0):
                    slope = scale / (calRef - zeroOffset)
                else:
                    slope = 0
                Raw = measurements[:,self.__mainFineIndex] - zeroOffset
                mainFinecurrents = Raw * slope / 1000
                mainCurrent = np.where(measurements[:,self.__mainFineIndex] < self.__fineThreshold, mainFinecurrents, mainCoarseCurrents)
                self.__addMeasurement(channels.MainCurrent,mainCurrent)
                #self.__mainCurrent.append(mainCurrent)
                sDebug = "Main Current: " + repr(round(mainCurrent[0],2))

            if(self.__channels[channels.USBCurrent]):
                #USB Coarse
                scale = self.monsoon.statusPacket.usbCoarseScale
                zeroOffset = self.monsoon.statusPacket.usbCoarseZeroOffset
                calRef = self.__usbCal.getRefCal(True)
                calZero = self.__usbCal.getZeroCal(True)
                zeroOffset += calZero
                if(calRef - zeroOffset != 0):
                    slope = scale / (calRef - zeroOffset)
                else:
                    slope = 0
                Raw = measurements[:,self.__usbCoarseIndex] - zeroOffset
                usbCoarseCurrents = Raw * slope 

                #USB Fine
                scale = self.monsoon.statusPacket.usbFineScale
                zeroOffset = self.monsoon.statusPacket.usbFineZeroOffset
                calRef = self.__usbCal.getRefCal(False)
                calZero = self.__usbCal.getZeroCal(False)
                zeroOffset += calZero
                if(calRef - zeroOffset != 0):
                    slope = scale / (calRef - zeroOffset)
                else:
                    slope = 0
                Raw = measurements[:,self.__usbFineIndex] - zeroOffset
                usbFineCurrents = Raw * slope/ 1000
                usbCurrent = np.where(measurements[:,self.__usbFineIndex] < self.__fineThreshold, usbFineCurrents, usbCoarseCurrents)
                self.__addMeasurement(channels.USBCurrent,usbCurrent)
                #self.__usbCurrent.append(usbCurrent)
                sDebug = sDebug + " USB Current: " + repr(round(usbCurrent[0], 2))
        
            if(self.__channels[channels.AuxCurrent]):
                #Aux Coarse
                scale = self.monsoon.statusPacket.mainFineScale
                zeroOffset = 0
                calRef = self.__auxCal.getRefCal(True)
                calZero = self.__auxCal.getZeroCal(True)
                zeroOffset += calZero
                if(calRef - zeroOffset != 0):
                    slope = scale / (calRef - zeroOffset)
                else:
                    slope = 0
                Raw = measurements[:,self.__auxCoarseIndex] - zeroOffset
                auxCoarseCurrents = Raw * slope 

                #Aux Fine
                scale = self.monsoon.statusPacket.auxFineScale
                zeroOffset = 0
                calRef = self.__auxCal.getRefCal(False)
                calZero = self.__auxCal.getZeroCal(False)
                zeroOffset += calZero
                if(calRef - zeroOffset != 0):
                    slope = scale / (calRef - zeroOffset)
                else:
                    slope = 0
                Raw = measurements[:,self.__auxFineIndex] - zeroOffset
                auxFineCurrents = Raw * slope / 1000
                auxCurrent = np.where(measurements[:,self.__auxFineIndex] < self.__auxFineThreshold, auxFineCurrents, auxCoarseCurrents)
                self.__addMeasurement(channels.AuxCurrent,auxCurrent)
                #self.__auxCurrent.append(auxCurrent)
                sDebug = sDebug + " Aux Current: " + repr(round(auxCurrent[0], 2))

            #Voltages
            if(self.__channels[channels.MainVoltage]):
                mainVoltages = measurements[:,self.__mainVoltageIndex] * self.__ADCRatio * self.__mainVoltageScale
                self.__addMeasurement(channels.MainVoltage,mainVoltages)
                #self.__mainVoltage.append(mainVoltages)
                
                sDebug = sDebug + " Main Voltage: " + repr(round(mainVoltages[0],2))
                

            if(self.__channels[channels.USBVoltage]):
                usbVoltages = measurements[:,self.__usbVoltageIndex] * self.__ADCRatio * self.__usbVoltageScale
                self.__addMeasurement(channels.USBVoltage,usbVoltages)
                #self.__usbVoltage.append(usbVoltages)
                sDebug = sDebug + " USB Voltage: " + repr(round(usbVoltages[0],2))
            timeStamp = measurements[:,self.__timestampIndex]
            self.__addMeasurement(channels.timeStamp,timeStamp)
            #self.__timeStamps.append(timeStamp)
            sDebug = sDebug + " Dropped: " + repr(self.dropped)
            sDebug = sDebug + " Total Sample Count: " + repr(self.__sampleCount)
            if(self.__outputConsoleMeasurements):
                print(sDebug)
            if not self.__startTriggerSet:
                self.__ClearOutput()


    def __processPacket(self, measurements):
        """Separates received packets into ZeroCal, RefCal, and measurement samples."""
        Samples = []
        for measurement in measurements:
            self.dropped = measurement[0]
            flags = measurement[1]
            numObs = measurement[2]
            offset = 3
            for _ in range(0,numObs):
                sample = measurement[offset:offset+10]
                sample.append(measurement[len(measurement)-1])
                sampletype = sample[8] & 0x30
                if(sampletype == ops.SampleType.ZeroCal):
                    self.__processZeroCal(sample)
                elif(sampletype == ops.SampleType.refCal):
                    self.__processRefCal(sample)
                elif(sampletype == ops.SampleType.Measurement):
                    Samples.append(sample)
                    
                offset += 10
        return Samples

    def __startupCheck(self,verbose=False):
        """Verify the sample engine is setup to start."""
        if(verbose):
            print("Verifying ready to start up")
            print("Calibrating...")
        Samples = [[0 for _ in range(self.__packetSize+1)] for _ in range(self.bulkProcessRate)]
        while(not self.__isCalibrated() and self.__sampleCount < 20000):
            self.__sampleLoop(0,Samples,1)
        self.getSamples()
        if not self.__isCalibrated():
            print("Connection error, failed to calibrate after 20,000 samples")
            return False
        if not self.__channels[self.__triggerChannel]:
            print("Error:  Trigger channel not enabled.")
            return False
        return True
    def __processZeroCal(self,meas):
        """Adds raw measurement data to the zeroCal tracker"""
        self.__mainCal.addZeroCal(meas[self.__mainCoarseIndex], True)
        self.__mainCal.addZeroCal(meas[self.__mainFineIndex], False)
        self.__usbCal.addZeroCal(meas[self.__usbCoarseIndex], True)
        self.__usbCal.addZeroCal(meas[self.__usbFineIndex], False)
        self.__auxCal.addZeroCal(meas[self.__auxCoarseIndex], True)
        self.__auxCal.addZeroCal(meas[self.__auxFineIndex], False)
        return True
    def __processRefCal(self, meas):
        """Adds raw measurement data to the refcal tracker"""
        self.__mainCal.addRefCal(meas[self.__mainCoarseIndex], True)
        self.__mainCal.addRefCal(meas[self.__mainFineIndex], False)
        self.__usbCal.addRefCal(meas[self.__usbCoarseIndex], True)
        self.__usbCal.addRefCal(meas[self.__usbFineIndex], False)
        self.__auxCal.addRefCal(meas[self.__auxCoarseIndex], True)
        self.__auxCal.addRefCal(meas[self.__auxFineIndex], False)
        return True

    def getSamples(self):
        """Returns samples in a Python list.  Format is [timestamp, main, usb, aux, mainVolts,usbVolts]."""
        result = self.__arrangeSamples(True)
        return result

    def __outputToCSV(self):
        """This is intended to be called periodically during sampling.  
        The alternative is to store measurements in an array or queue, which will overflow allocated memory within a few hours depending on system settings.
        Writes measurements to a CSV file"""

        output = self.__arrangeSamples()
        for i in range(len(output[0])):
            sOut = ""
            for j in range(len(output)):
                sOut = sOut + repr(output[j][i]) + ","
            sOut = sOut + "\n"
            self.__f.write(sOut)

    def __arrangeSamples(self, exportAllIndices = False):
        """Arranges output lists so they're a bit easier to process."""
        output = []
        times = []
        for data in self.__timeStamps:
            for measurement in data:
                times.append(measurement)
        output.append(times)
        self.__timeStamps = []
        if(self.__channels[channels.MainCurrent] or exportAllIndices):
            main = []
            for data in self.__mainCurrent:
                for measurement in data:
                    main.append(measurement)
            output.append(main)
            self.__mainCurrent = []
        if(self.__channels[channels.USBCurrent]or exportAllIndices):
            usb = []
            for data in self.__usbCurrent:
                for measurement in data:
                    usb.append(measurement)
            output.append(usb)
            self.__usbCurrent = []
        if(self.__channels[channels.AuxCurrent]or exportAllIndices):
            Aux = []
            for data in self.__auxCurrent:
                for measurement in data:
                    Aux.append(measurement)
            output.append(Aux)
            self.__auxCurrent = []
        if(self.__channels[channels.MainVoltage]or exportAllIndices):
            volts = []
            for data in self.__mainVoltage:
                for measurement in data:
                    volts.append(measurement)
            output.append(volts)
            self.__mainVoltage = []
        if(self.__channels[channels.USBVoltage]or exportAllIndices):
            volts = []
            for data in self.__usbVoltage:
                for measurement in data:
                    volts.append(measurement)
            output.append(volts)
            self.__usbVoltage = []
        return output
    def outputCSVHeaders(self):
        """Creates column headers in the CSV output file for each enabled channel."""
        for i in range(len(self.__channelnames)):
            if(self.__channels[i]):
                self.__f.write((self.__channelnames[i] + ","))
        self.__f.write("\n")

    def __sampleLoop(self,S,Samples,ProcessRate):
        buffer = self.monsoon.BulkRead()
        for start in range(0,len(buffer),64):
            buf = buffer[start:start+64]
            Sample = self.monsoon.swizzlePacket(buf)
            numSamples = Sample[2]
            Sample.append(time.time() - self.__startTime)
            Samples[S] = Sample
            S += numSamples
            if(S >= ProcessRate):
                bulkPackets = self.__processPacket(Samples)
                if(len(bulkPackets) > 0):
                    self.__vectorProcess(bulkPackets)
                    self.__sampleCount += len(bulkPackets)
                S = 0
        return S

    def startSampling(self, samples=5000, granularity = 1):
        """Starts sampling."""
        """granularity: Controls the resolution at which samples are stored.  1 = all samples stored, 10 = 1 out of 10 samples stored, etc."""
        self.__Reset()
        self.__sampleLimit = samples
        self.__granularity = granularity
        Samples = [[0 for _ in range(self.__packetSize+1)] for _ in range(self.bulkProcessRate)]
        S = 0
        debugcount = 0
        minutes = 0
        granularity_index = 0
        csvOutRateLimit = True
        csvOutThreshold = self.bulkProcessRate/2
        self.__startTime = time.time()
        if(self.__CSVOutEnable):
            self.outputCSVHeaders()
        self.monsoon.StartSampling(1250,0xFFFFFFFF)
        if not self.__startupCheck():
            self.monsoon.stopSampling()
            return False
        while not self.__stopTriggerSet:
            S = self.__sampleLoop(S,Samples,self.bulkProcessRate)
            if(S == 0):
                csvOutRateLimit = True
            if(S >= csvOutThreshold and self.__CSVOutEnable and self.__startTriggerSet):
                self.__outputToCSV()
                csvOutRateLimit = False
        self.monsoon.stopSampling()
        if(self.__CSVOutEnable):
            self.__outputToCSV()
            self.disableCSVOutput()
        pass

    def periodicStartSampling(self):
        """Causes the Power Monitor to enter sample mode, but doesn't actively collect samples.
        Call periodicCollectSamples() periodically get measurements.
        """
        self.__Reset()
        self.__sampleLimit = triggers.SAMPLECOUNT_INFINITE
        self.__granularity = 1
        if(self.__CSVOutEnable):
            self.outputCSVHeaders()
        Samples = [[0 for _ in range(self.__packetSize+1)] for _ in range(self.bulkProcessRate)]
        self.__startTime = time.time()
        self.monsoon.StartSampling(1250,triggers.SAMPLECOUNT_INFINITE)
        if not self.__startupCheck():
            self.monsoon.stopSampling()
            return False
        result = self.getSamples()
        return result


    def periodicCollectSamples(self,samples=100):
        """Start sampling with periodicStartSampling(), then call this to collect samples.
        Returns the most recent measurements made by the Power Monitor."""
        #TODO:  This normally returns 3-5 samples over the requested number of samples.
        self.__sampleCount = 0
        self.__sampleLimit = samples
        self.__stopTriggerSet = False
        self.monsoon.BulkRead() #Clear out stale buffer
        Samples = [[0 for _ in range(self.__packetSize+1)] for _ in range(1)]
        while not self.__stopTriggerSet:
            S = self.__sampleLoop(0,Samples,1)
        if(self.__CSVOutEnable and self.__startTriggerSet):
            self.__outputToCSV() #Note that this will cause the script to return nothing.
        result = self.getSamples()
        return result

    def periodicStopSampling(self, closeCSV=False):
        """Performs cleanup tasks when finished sampling."""
        if(self.__CSVOutEnable and self.__startTriggerSet):
            self.__outputToCSV()
            if(closeCSV):
                self.disableCSVOutput()
        self.monsoon.stopSampling()




