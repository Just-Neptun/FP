import numpy as np

import pynn_brainscales.brainscales2 as pynn
from pynn_brainscales.brainscales2.standardmodels.synapses import StaticSynapse


# ===== Helper Functions =====

# makes sure a Population object is passed a list as an index (and NOT a np.array())
def slice_pop(pop, indices):
    indices = list(indices)
    return pop[indices]

# returns a NEW population with an element removed by its index
def remove_item(pop, index: int):
    n_neurons = len(pop)
    if index >= n_neurons:
        raise ValueError(f'Given population {pop} (length {n_neurons}) cannot be indext up to {index}.')
    indices = [i for i in range(n_neurons) if i != index]
    return slice_pop(pop, indices)

# =========================

# link neuron with the other three neurons in a group / inhibitory
def inhibit_one_to_all(pre_syn_pop, post_syn_pop, weight):
    pynn.Projection(
        pre_syn_pop,
        post_syn_pop,
        pynn.AllToAllConnector(),
        synapse_type = StaticSynapse(weight = weight),
        receptor_type = 'inhibitory'
    )

def inhibit_each_to_all_others(neurons_pop, weight):
    for i, _ in enumerate(neurons_pop):
        other_neurons = remove_item(neurons_pop, i)
        inhibit_one_to_all(neurons_pop[[i]], other_neurons, weight)



# ===== Main Functions =====

# Constraints
# create inhibitory connections to neurons in the same field representing different numbers
def inhibitory_same_field(pop, neuron_indices, dimension, weight = -30):
    for row in range(dimension):
        for column in range(dimension):
            # make a population of all neurons in the same row and column (same field) (varying numbers)
            neurons_field = slice_pop(pop, neuron_indices[row, column, :])
            inhibit_each_to_all_others(neurons_field, weight)

# create inhibitory connections to neurons in the same row representing the same number
def inhibitory_same_row(pop, neuron_indices, dimension, weight = -30):
    for number in range(dimension):
        for row in range(dimension):
            # make a population of all neurons with the same number in the same row (varying column coords)
            neurons_num_row = slice_pop(pop, neuron_indices[row, :, number])
            inhibit_each_to_all_others(neurons_num_row, weight)

# create inhibitory connections to neurons in the same column representing the same number
def inhibitory_same_column(pop, neuron_indices, dimension, weight = -30):
    for number in range(dimension):
        for column in range(dimension):
            # make a list of all neurons with the same number in the same column (varying row coords)
            neurons_num_column = slice_pop(pop, neuron_indices[:, column, number])
            inhibit_each_to_all_others(neurons_num_column, weight)


# create list of blocks, each entry is a list of coordinates [i, j] (<- list) of all neurons in the same block
def create_list_of_blocks_indices(dimension):
    step = int(np.sqrt(dimension))
    if np.sqrt(dimension) != step:
        raise ValueError(f'given dimension = {dimension} does not support blocks!')
    blocks_indices_list = []
    for i in range(step):
        row = i * step
        for j in range(step):
            column = j * step
            blocks_indices_list += [[(y, x) for y in range(row, row+step) for x in range(column, column+step)]]
    return blocks_indices_list

# create inhibitory connections to neurons in the same block representing the same number
def inhibitory_same_block(pop, neuron_indices, dimension, weight = -30):
    blocks_indices_list = create_list_of_blocks_indices(dimension)
    for number in range(dimension):
        for block_coords in blocks_indices_list:
            # make a list of all neurons with the same number in the same block
            indices = [neuron_indices[i, j, number] for (i, j) in block_coords]
            neurons_num_block = slice_pop(pop, indices)
            inhibit_each_to_all_others(neurons_num_block, weight)



# ===== Resulting Function to Use =====

def set_constraints(pop, neuron_indices, dimension):
    inhibitory_same_field(pop, neuron_indices, dimension, weight = -30)
    inhibitory_same_row(pop, neuron_indices, dimension, weight = -30)
    inhibitory_same_column(pop, neuron_indices, dimension, weight = -30)
    if np.sqrt(dimension) == int(np.sqrt(dimension)):
        inhibitory_same_block(pop, neuron_indices, dimension, weight = -30)