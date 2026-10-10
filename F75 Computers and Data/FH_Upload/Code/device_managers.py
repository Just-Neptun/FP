import pyvisa, re
from typing import Literal

def calc_temp_for_voltage(voltage):
    return (voltage - 1.000325) * 259.2684

def illegal_calc_voltage_for_temp(temp):
    return temp / 259.2684 + 1.000325

##################################################

class Base():                                                    # Class name
    def __init__(self, name="Default", purpose="communication"): # Constructor gets called when instance of class is created
        self.name = name                                         # Attribute of instance "self" called "name" will be set to value of variable "name"
        self.purpose = purpose                                   # Attribute set
        
    def help(self):
        print(f"Class {self.name} for {self.purpose}")

##################################################

ESCAPE_CHARS = ['\x1b', '\x0d', '\x0a', '\x2b'] # ESC, CR, LF, PLUS (ESC MUST BE FIRST)

def escape(data):
    # xlat_t = { ord(c):'\x1b' + c for c in '\x1b\r\n+' }; '+A\rB\nC\x1b'.translate(xlat_t)
    #==> '\x1b+A\x1b\rB\x1b\nC\x1b\x1b'
    for b in ESCAPE_CHARS:
        data = data.replace(b, '\x1b' + b) # prepend with ESC
    return data


class GPIB(Base): # Create class GPIB that interits the methods and attributes of the Base class
    """Use GPIB devices via Prologix GPIB-USB Controller Rev 6.4.1"""
    # https://pyvisa.readthedocs.io/en/latest/
    # https://prologix.biz/downloads/PrologixGpibUsbManual-6.0.pdf

    def __init__(self, dev="ttyUSBGPIB"):   # Constructor
        self.__parent = super()                        # https://docs.python.org/3/library/functions.html#super
        self.__parent.__init__("GPIB", "hardware communication") # call constructor of parent class with arguments      
        self._rm   = pyvisa.ResourceManager("@py")               # using PyVISA-py
        self.setDev(dev)
        self._addr = None

    def setDev(self, dev):
        self._dev = str(dev)
        for res in sorted(self._rm.list_resources()):
            if self._dev in res:
                self._res = self._rm.open_resource(res)
                self.setRes(self._res)
    
    def setRes(self, res):
        self._res = res
        self._res.read_termination  = "\n"
        self._res.write_termination = "\n"
        self._res.write("++mode 1") # "++mode" is "0" (GPIB TALKER or GPIB LISTENER) or "1" (Controller-In-Charge (CIC))

    def setAddr(self, addr):
        self._addr = int(addr)
        self._res.write("++addr " + str(self._addr))
            
    def write(self, addr, data):
        self.setAddr(addr)
        self._res.write(escape(data))

    def query(self, addr, data, dtype="float"):
        self.setAddr(addr)
        if dtype != "float":
            return self._res.query(data)
        return float(
            re.sub(
                '[^0-9eE\.+-]', '',
                self._res.query(escape(data))
            )
        )

##################################################

class SynFunGen(GPIB):
    def __init__(self, addr=19):
        super().__init__()
        self.name = "SynFunGen"
        self.purpose = "controlling function generator"
        self.setAddr(addr)

    def write(self, var: Literal["FREQ", "AMPL"], val):
        super().write(self._addr, f"{var} {val:.3f}")

    def query(self, var: Literal["FREQ", "AMPL"]):
        return super().query(self._addr, f"{var}?")

    def reset_freq(self):
        self.write("FREQ", 0.0)

    def reset_ampl(self):
        self.write("AMPL", 0.0)

##################################################

class LockInAmp(GPIB):
    def __init__(self, inp_key="X2", out_key="X6", addr=7):
        super().__init__()
        self.name = "LockInAmp"
        self.purpose = "Bandpass and Amplifier"
        self.setAddr(addr)
        self.keys = {
            "in": inp_key,
            "out": out_key,
            "X": "QX",
            "Y": "QY"
        }

    def write(self, ch: Literal["out"], val):
        if ch != "out":
            raise ValueError(f"Cannot write to this!")
        super().write(self._addr, f"{self.keys[ch]},{val:.3f}")

    def query(self, ch: Literal["X", "Y", "in", "out"]):
        return super().query(self._addr, f"{self.keys[ch]}")

    def get_temp(self):
        return calc_temp_for_voltage(self.query("in"))
        
    def reset_voltage(self):
        self.write("out", 0.0)

##################################################

SFG_CH = ["FREQ", "AMPL"]
LIA_CH = ["in", "out"]
LIA_CH_QUERY_ONLY = ["X", "Y"]

class Devices:
    def __init__(self):
        self.sfg = SynFunGen()
        self.lia = LockInAmp()

    def get_temp(self):
        return self.lia.get_temp()
    
    def write(self, ch: str, val):
        if ch in SFG_CH:
            self.sfg.write(ch, val)
        elif ch in LIA_CH:
            self.lia.write(ch, val)
        else:
            raise ValueError(f"Channel not valid: {ch}")

    def query(self, ch):
        if ch in SFG_CH:
            return self.sfg.query(ch)
        if ch in LIA_CH or ch in LIA_CH_QUERY_ONLY:
            return self.lia.query(ch)
        else:
            raise ValueError(f"Channel not valid: {ch}")

    def reset(self):
        self.sfg.reset_freq()
        self.lia.reset_voltage()
        

##################################################

