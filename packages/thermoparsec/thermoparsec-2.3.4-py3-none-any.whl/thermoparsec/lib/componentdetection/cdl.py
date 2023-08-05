import json
from lib.componentdetection.pdata import *
import numpy as np
from scipy import signal
from numpy import sqrt, pi, exp
from lmfit import Model


def ReadFile(file):
    with open(file) as data_file:
        data = json.load(data_file)
        return (data)

def GetPScan(spectrum,msOrder):
    scan = PScan()
    scan.FileName = spectrum.FileName
    scan.BasePeakIntensity = spectrum.BasePeakIntensity
    scan.BasePeakMass = spectrum.BasePeakMass
    scan.LowMass = spectrum.LowMass
    scan.HighMass = spectrum.HighMass
    scan.Masses = spectrum.Masses
    scan.PacketType = spectrum.PacketType
    scan.RetentionTime = spectrum.RetentionTime
    scan.ScanNumber = spectrum.ScanNumber
    scan.ScanType = spectrum.ScanType
    scan.TIC = spectrum.TIC
    scan.Intensities = spectrum.Intensities
    scan.Baselines = spectrum.Baselines
    scan.Noises = spectrum.Noises
    scan.Resolutions = spectrum.Resolutions
    scan.Charges = spectrum.Charges
    if msOrder >= 2:
        scan.PrecursorMass = spectrum.PrecursorMass
    return scan

def ScanFromJson(spectrum):
    scan = PScan()
    for i in spectrum:
        if i[0] == 'FileName':
            scan.FileName = i[1]
        if i[0] == 'BasePeakIntensity':
            scan.BasePeakIntensity = i[1]
        if i[0] == 'BasePeakMass':
            scan.BasePeakMass = i[1]
        if i[0] == 'LowMass':
            scan.LowMass = i[1]
        if i[0] == 'HighMass':
            scan.HighMass = i[1]
        if i[0] == 'Masses':
            scan.Masses = i[1]
        if i[0] == 'PacketType':
            scan.PacketType = i[1]
        if i[0] == 'RetentionTime':
            scan.RetentionTime = i[1]
        if i[0] == 'ScanNumber':
            scan.ScanNumber = i[1]
        if i[0] == 'ScanType':
            scan.ScanType = i[1]
        if i[0] == 'TIC':
            scan.TIC = i[1]
        if i[0] == 'Intensities':
            scan.Intensities = i[1]
        if i[0] == 'Baselines':
            scan.Baselines = i[1]
        if i[0] == 'Noises':
            scan.Noises = i[1]
        if i[0] == 'Resolutions':
            scan.Resolutions = i[1]
        if i[0] == 'Charges':
            scan.Charges = i[1]
        if i[0] == 'PrecursorMass':
                scan.PrecursorMass = i[1]
    return scan


def GetScanList(file):
    data = ReadFile(file)
    scanList = []
    for s in data:
        spectrum = s.items()
        scan = ScanFromJson(spectrum)
        scanList.append(scan)
    return scanList

def GetPPMError(t, m):
    """
    calculate theoretical (t) and measured (m) ppm
    """
    return (((t - m) / t) * 1e6)


def GetMassGivenPPM(t, p):
    """
    calculate theoretical mass (t) given a ppm tolerance (p)
    """
    return (t - ((p * t) / 1e6))


def FindNearestMass(m, t, p):
    """
    find nearest mass in the mass list dictionary (m), target mass (t) and ppm tolerance (p)
    """
    for k, mass in m.items():
        if abs(GetPPMError(mass, t)) < p:
            return k
    return None


def DetectPeaksMF(t, w):
    """
    Detect peaks from mass trace (t) where w is the expected peak width at base (choose odd value)    """
    s = []
    rt = []
    mz = []
    for i in t.Trace:
        s.append(i.Intensity)
        rt.append(i.RT)
        mz.append(i.Mass)
    m = signal.medfilt(s, w)
    r = s - m
    p = Peak()
    p.Intensity = max(r)
    p.RT = round(rt[s.index(max(s))], 1)
    p.MZ = mz[s.index(max(s))]
    p.FileID = t.FileID
    return p


def DetectIsotopes(t):
    """
    input =  tuple (key,Peaklist) peaks are already grouped via RT (the key)
    """
    peaks = sorted(t, key=lambda p: p.MZ, reverse=False)
    return peaks


def GetMedian(a):
    return np.median(a)


def GetMax(a):
    return max(a)


def RemoveZeros(x):
    """
    remove zeros from a list
    """
    return list(filter(lambda a: a != 0, x))


def GetMzList(scan):
    """
    Create mz objects from a scan
    """
    l = []
    for i in range(len(scan.Masses)):
        m = MZ()
        m.FileID = scan.FileName
        m.ScanNumber = scan.ScanNumber
        m.RT = scan.RetentionTime
        m.Intensity = scan.Intensities[i]
        m.Mass = scan.Masses[i]
        l.append(m)
    return l

def GetMassTracesFromFlatList(m):
    """
    returns a list of Trace objects from an input list of mz objects from all scans
    """
    r =  []
    f = []
    masses = sorted(m, key=lambda p: p.Mass, reverse=False)
    testmass = masses[0].Mass
    t = MassTrace()
    t.FileID = masses[0].FileID
    for i in range(len(masses)):
        err = GetPPMError(masses[i].Mass,testmass)
        if(abs(err) < 10):
            t.Trace.append(masses[i])
            testmass = masses[i].Mass
            if(len(t.Trace) > 10):
                test = 0
        else:
            #add trace and start new one
            t.FileID = masses[i].FileID
            r.append(t)
            t = MassTrace()
            t.Trace.append(masses[i])
            testmass = masses[i].Mass

    # sort all traces by RT (5 data points minimum)
    for trace in r:
        if(len(trace.Trace) > 5):
            f.append(sorted(trace.Trace, key=lambda p: p.RT, reverse=False))
    return f

def GetMassTracesFromBins(scansPerFile):

    fileId = scansPerFile[0]
    scanList = scansPerFile[1]

    #tempBins = BinMassTraces(scanList.data[0])
    #tempTraces = BuildMassTraces(tempBins[99])

    #would be nice to do a nested map call
    #binMasses = scanList.Map(lambda scan: BinMassTraces(scan))

    binMasses = {}

    for scan in scanList:
        BinMasses(scan, binMasses)

    traceList = []

    for k,bin in binMasses.items():
        traces = BuildMassTraces(k, bin)
        #traceList.append(traces)
        for j in traces:
            traceList.append((fileId, j))

    return traceList


def BinMasses(scan, binMasses):

    for i in range(len(scan.Masses)):
        binNumber = round(scan.Masses[i])

        if(binNumber in binMasses):
            massList = binMasses[binNumber]
        else:
            massList = []
            binMasses[binNumber] = massList

        mz = MZPlus()
        mz.FileID = id
        mz.Mass = scan.Masses[i]
        mz.Intensity = scan.Intensities[i]
        mz.RetentionTime = scan.RetentionTime
        mz.RT = scan.RetentionTime
        mz.ScanNumber = scan.ScanNumber
        massList.append(mz)


def BuildMassTraces(binIndex, massBin):

    # sort by intenstity, get most intense mz and anything within 5ppm of that. Mark processed so not picked up again

    MaxPPMDiff = 10
    MinTracePoints = 3
    ScalingFactor = 0

    if (binIndex <= 500):  # scaling factor for smaller masses to increase PPM tolerance, bin = rounded mz value
        f = divmod(binIndex, 100)
        f = MaxPPMDiff - f[0]
        ScalingFactor = f

    intensitySort = sorted(massBin, key=lambda  mz: mz.Intensity, reverse=True)
    massSort = sorted(massBin, key=lambda  mz: mz.Mass)
    massSortLength = len(massSort)
    massTraceList = []

    for sortedMass in intensitySort:
        if(not sortedMass.Processed):
            startIndex = massSort.index(sortedMass)
            massTrace = MassTrace()
            massTrace.Trace = []
            massTrace.Trace.append(sortedMass)
            sortedMass.Processed = True
            ppmDiff = 0
            counter = 1;

            while((ppmDiff <= (MaxPPMDiff + ScalingFactor)) and (startIndex + counter < massSortLength)):
                nextMass = massSort[startIndex + counter]
                massDiff = GetAbsolutePPMError(sortedMass.Mass, nextMass.Mass)

                if(massDiff <= (MaxPPMDiff + ScalingFactor)):
                    massTrace.Trace.append(nextMass)
                    nextMass.Processed = True
                    counter += 1
                else:
                    break

            ppmDiff = 0
            counter = 1;
            while ((ppmDiff <= (MaxPPMDiff + ScalingFactor)) and (startIndex - counter >= 0)):
                previousMass = massSort[startIndex - counter]
                massDiff = GetAbsolutePPMError(sortedMass.Mass, previousMass.Mass)
                if (massDiff <= (MaxPPMDiff + ScalingFactor)):
                    massTrace.Trace.append(previousMass)
                    previousMass.Processed = True
                    counter += 1
                else:
                    break

            if(len(massTrace.Trace) >= MinTracePoints):
                massTrace.Trace = sorted(massTrace.Trace, key=lambda m: m.RetentionTime)
                massTraceList.append(massTrace)

    return massTraceList

def GetAbsolutePPMError(t, m):
    """
    calculate theoretical (t) and measured (m) ppm
    """
    return abs(((t - m) / t) * 1e6)

def gaussian(x, amp, cen, wid):
    "1-d gaussian: gaussian(x, amp, cen, wid)"
    return (amp/(sqrt(2*pi)*wid)) * exp(-(x-cen)**2 /(2*wid**2))

def PPD(trace,w):
    x = []
    y = []
    for i in range(len(trace)):
        x.append(trace[i].RT)
        y.append(trace[i].Intensity)
    x = np.asarray(x)
    y = np.asarray(y)
    amp = np.median(y)
    cent = np.median(x)
    gmodel = Model(gaussian)

    return gmodel.fit(y, x=x, amp=amp, cen=cent, wid=w)

def PPDt(traceTuple):
    if(len((traceTuple)[1].Trace) > 3):
        peaks = PPD((traceTuple)[1].Trace, 11)
        return peaks
    else:
        return None

