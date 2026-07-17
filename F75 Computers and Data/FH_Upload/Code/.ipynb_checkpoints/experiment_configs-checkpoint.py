from dataclasses import dataclass

import Code.experimentA_manager as expA_module
import Code.experimentB_manager as expB_module

class Config:    
    def summary(self):
        A_one_spectrum_runtime = expA_module.INDEPENDENT_A_PHI_MEASUREMENT_DELAY * self.A_num_of_freqs * (self.A_trials_at_each_freq + 1)
        A_total_runtime = 3 * A_one_spectrum_runtime + self.A_temp_initializing
        B_one_spectrum_runtime = expB_module.INDEPENDENT_A_PHI_MEASUREMENT_DELAY * self.B_num_of_freqs * (self.B_trials_at_each_freq + 1)
        B_one_spectrum_runtime_with_thermalization = (
            expB_module.TIME_TO_WAIT_BEFORE_CHECKING_THERMALIZATION
            + expB_module.UPDATE_TEMP_TRIALS * expB_module.INDPENDENT_TEMP_MEASUREMENT_DELAY
            + B_one_spectrum_runtime
        )
        B_total_runtime = self.B_num_voltages * B_one_spectrum_runtime_with_thermalization + self.B_initial_heating_time
        print(f"Expected runtime of A: {A_total_runtime/60} min")
        print(f"Expected runtime of A: {A_total_runtime/3600} hr")
        print(f"Expected runtime of B: {B_total_runtime/60} min")
        print(f"Expected runtime of B: {B_total_runtime/3600} hr")
        print()
        print(f"Total runtime is at least: {(B_total_runtime + A_total_runtime) / 60} min")
        print(f"Total runtime is at least: {(B_total_runtime + A_total_runtime) / 3600} hr")
        print()
        print(f"Will save to: {self.loc_prefix}")

@dataclass
class Debug_Config(Config):
    loc_prefix = "Data/Debug"
    A_trials_at_each_freq = 2
    A_num_of_freqs = 2    # at least 100

    A_temp_initializing = 1    # 20 mins

    B_trials_at_each_freq = 2
    B_num_of_freqs = 2    # make this higher than in Exp A to compensate for larger padding

    B_max_voltage = 1
    B_num_voltages = 2

    B_initial_heating_time = 10    # 20 mins

@dataclass
class Test_Config(Config):
    loc_prefix = "Data/Debug"
    A_trials_at_each_freq = 8
    A_num_of_freqs = 40    # at least 100

    A_temp_initializing = 1    # 20 mins

    B_trials_at_each_freq = 2
    B_num_of_freqs = 2    # make this higher than in Exp A to compensate for larger padding
    
    B_max_voltage = 1
    B_num_voltages = 3

    B_initial_heating_time = 10    # 20 mins

@dataclass
class Final_Config(Config):
    loc_prefix = "Data/Final"
    A_trials_at_each_freq = 20
    A_num_of_freqs = 200    # at least 100

    A_temp_initializing = 1    # 20 mins

    B_trials_at_each_freq = 20
    B_num_of_freqs = 220    # make this higher than in Exp A to compensate for larger padding
    
    B_max_voltage = 1
    B_num_voltages = 10

    B_initial_heating_time = 60 * 20    # 20 mins

            
        