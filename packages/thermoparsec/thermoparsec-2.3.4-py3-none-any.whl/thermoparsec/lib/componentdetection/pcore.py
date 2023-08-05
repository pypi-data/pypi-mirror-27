from lib.componentdetection.cdl import  *

def CreateKVpair(s,o):
    """
    Tuple (file name , scan) where 0 is int for msOrder (e.g ms1 or ms2 or msN)
    """
    scan = GetPScan(s,o)
    return (s.FileName, scan)

def MapMzListForScan(scan):
    return GetMzList(scan[1])


def KeyMz(m):
    return (m.FileID,m)

def KeyTraces(t):
    """
    Input is a list of trace objects and output is a list of key values (id:trace)
    """
    l = []
    traces = GetMassTracesFromFlatList(t[1])
    for i in range(len(traces)):
        l.append((i,traces[i]))
    return l

def MapPeak(t,w):
    p = PPD(t[1],w)
    return (t,p)