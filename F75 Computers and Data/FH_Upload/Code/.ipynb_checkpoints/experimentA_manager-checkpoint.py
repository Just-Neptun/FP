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

INDEPENDENT_A_PHI_MEASUREMENT_DELAY = 0.9

class ExperimentA:
    def __init__(
        self, 
        loc: str,
        freqs_series,
        trials: int = 20,
        sleeptime: float = INDEPENDENT_A_PHI_MEASUREMENT_DELAY,
        init_metadata: dict = dict()
    ):
        timestamp = datetime.now().strftime("%m%d_%H%M%S")
        self.loc = loc + "_" + timestamp + ".txt"
        self.freqs_series = freqs_series
        self.trials = trials
        self.sleeptime = sleeptime

        self.devices = Devices()

        self.init_metadata = init_metadata
        self.dw = DataWriter(self.loc, ["freq", "A", "A_std", "phi", "phi_std"], str(self.create_metadata())) # "X", "Y", 

    def create_metadata(self) -> dict:
        return {"trials": self.trials, "sleeptime": self.sleeptime} | self.init_metadata
    
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
        print("Done!")

