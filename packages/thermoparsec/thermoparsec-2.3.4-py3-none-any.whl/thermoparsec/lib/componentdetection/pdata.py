class Peak:
    def __init__(self):
        self.RT = 0
        self.PeakArea = 0
        self.Trace = MassTrace()


class PScan:
    def __init__(self):
        self.FileName = ""
        self.PrecursorMass = 0
        self.BasePeakIntensity = 0
        self.BasePeakMass = 0
        self.HighMass = 0
        self.LowMass = 0
        self.PacketType = 21
        self.RetentionTime = 0
        self.ScanNumber = 0
        self.ScanType = ""
        self.TIC = 0
        self.Baselines = []
        self.Intensities = []
        self.Masses = []
        self.Noises = []
        self.Resolutions = []
        self.Charges = []

class MassTrace:
    def __init__(self):
        self.FileID = ""
        self.TraceID = ""
        self.Trace = []


class MZ:
    def __init__(self):
        self.FileID = ""
        self.Mass = 0
        self.Intensity = 0
        self.RT = 0
        self.ScanNumber = 0

class MZPlus(MZ):
    def __init__(self):
        MZ.__init__(self)
        self.Processed = 0


class Peak:
    def __init__(self):
        self.FileID = ""
        self.RT = 0
        self.Intensity = 0
        self.MZ = 0


class Feature:
    def __init__(self):
        self.FileID
        self.Key
        self.RT = 0
        self.Intensity = 0
        self.A0 = 0
        self.Peaks = []