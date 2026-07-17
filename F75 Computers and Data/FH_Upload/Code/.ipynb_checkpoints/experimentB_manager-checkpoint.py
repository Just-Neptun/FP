import numpy as np
from datetime import datetime
from time import sleep
from tqdm import tqdm

from Code.device_managers import Devices
from Code.data_managers import DataWriter

def calc_amplitude(x, y):
    return np.sqrt(x**2 + y**2)

def calc_phase_shift(x, y):
    return np.arctan2(y, x)

TIME_TO_WAIT_BEFORE_CHECKING_THERMALIZATION = 60 * 5    # 5 mins
INDPENDENT_TEMP_MEASUREMENT_DELAY = 1

UPDATE_TEMP_TRIALS = 100
MAX_STD_TEMP = 0.5    # maximum error in temperature that we want
MAX_GRAD_TEMP = 0.5    # maximum gradient in temperature from first to last measurement

def is_below_std_threshold(val):
    return val < MAX_STD_TEMP

def is_below_grad_threshold(val):
    return val < MAX_GRAD_TEMP

INDEPENDENT_A_PHI_MEASUREMENT_DELAY = 0.9

class ExperimentB:
    def __init__(
        self, 
        loc: str,
        freqs_series,
        target_voltage,
        trials: int = 20,
        sleeptime: float = INDEPENDENT_A_PHI_MEASUREMENT_DELAY,
        init_metadata: dict = dict()
    ):
        timestamp = datetime.now().strftime("%m%d_%H%M%S")
        self.loc = loc + "_" + timestamp + ".txt"
        self.freqs_series = freqs_series
        self.trials = trials
        self.sleeptime = sleeptime
        self.target_voltage = target_voltage

        self.devices = Devices()

        self.set_voltage(self.target_voltage)
        
        self.init_metadata = init_metadata
        self.dw = DataWriter(self.loc, ["freq", "A", "A_std", "phi", "phi_std"], str(self.create_metadata()))

    def create_metadata(self) -> dict:
        return {
            "trials": self.trials,
            "sleeptime": self.sleeptime,
            "target_voltage": self.target_voltage,
            "current_temp": self.current_temp,
            "current_temp_err": self.current_temp_err,
            "current_temp_gradient": self.current_temp_gradient,
            "loops_to_stabilize_temperature": self.loops
        } | self.init_metadata

    def set_voltage(self, target_voltage):
        self.devices.write("out", target_voltage)
        i = 0
        print(f"Setting voltage: {target_voltage} V, waiting for thermalization, loops: {i}.", end="\r")
        sleep(TIME_TO_WAIT_BEFORE_CHECKING_THERMALIZATION)
        self.update_temp()
        while not self.is_temp_stabilized():
            i += 1
            print(f"Setting voltage: {target_voltage} V, waiting for thermalization, loops: {i}.", end="\r")
            sleep(TIME_TO_WAIT_BEFORE_CHECKING_THERMALIZATION)
            self.update_temp()
        print(f"Finished setting voltage: {self.target_voltage} V. Current temp: {self.current_temp} C.                       ")
        self.loops = i

    def update_temp(self):
        temps = []
        for _ in range(UPDATE_TEMP_TRIALS):
            sleep(INDPENDENT_TEMP_MEASUREMENT_DELAY)
            temps.append(self.devices.get_temp())
        self.current_temp = np.mean(temps)
        self.current_temp_err = np.std(temps) / len(temps)
        self.current_temp_gradient = np.abs(temps[0] - temps[-1])

    def is_temp_stabilized(self):
        return is_below_std_threshold(self.current_temp_err) and is_below_grad_threshold(self.current_temp_gradient)
    
    def measure_A_phi(self):
        sleep(self.sleeptime)
        x = self.devices.query("X")
        y = self.devices.query("Y")
        return calc_amplitude(x, y), calc_phase_shift(x, y)
    
    def measure_at_freq(self, freq):
        self.devices.write("FREQ", freq)
        sleep(self.sleeptime)
        results = np.array([self.measure_A_phi() for _ in range(self.trials)])
        means = results.mean(axis=0)
        stds = results.std(axis=0) / np.sqrt(20)
        result = {"freq": freq, "A": means[0], "A_std": stds[0], "phi": means[1], "phi_std": stds[1]}
        self.dw.write(result)

    def execute(self):
        rt = self.sleeptime * len(self.freqs_series) * self.trials
        print(f"Starting Experiment with expected runtime: {rt} s.")
        for freq in tqdm(self.freqs_series):
            self.measure_at_freq(freq)

