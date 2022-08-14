import numpy as np
import nengo

def flip_bits(input_bit):
    if(0.5 <= input_bit < 1.5):
        return 0
    return 1

def calculate_output_bit(vector):
    print(vector)
    result = vector[0] + vector[1]
    if((0.5 < result <= 1.5) or (2.5 < result <= 3.5)):
        return 1
    return 0
 
def calculate_carry_out(vector):
    result = vector[0] + vector[1]
    if((1.5 < result <= 2.5) or (2.5 < result <= 3.5)):
        return 1
    return 0

"""def select_exponent(vector):
    carry_out_bit = vector[-1]
    exponent_len = (len(vector) - 1) / 2
    if(carry_out_bit):"""


model = nengo.Network()

with model:
    exponent1_bits = [1, 0, 1, 1, 0, 1, 0, 1]
    exponent2_bits = [1, 1, 0, 1, 1, 0, 1, 1]

    exponent1_bits.reverse()
    exponent2_bits.reverse()

    exponent1_nodes = []
    exponent2_nodes = []
    
    exponent_len = len(exponent1_bits)

    for i in range(exponent_len):
        exponent1_nodes.append(nengo.Node(output = exponent1_bits[i]))
        exponent2_nodes.append(nengo.Node(output = exponent2_bits[i]))

    flipping_ensemble = nengo.Ensemble(n_neurons = exponent_len * 100,
            dimensions = exponent_len, radius = 2)
    
    for i in range(exponent_len):
        nengo.Connection(exponent2_nodes[i], flipping_ensemble[i])

    adding_bits = []

    for i in range(exponent_len):
        adding_bits.append(0)
    adding_bits[exponent_len - 1] = 1

    #Converting LSB->MSB to MSB->LSB
    adding_bits.reverse()

    adding_nodes = []

    for i in adding_bits:
        adding_nodes.append(nengo.Node(output = i))

    #exponent_len-bit Adder Code

    twos_complement_carry_in = 0
    twos_complement_carry_in_node = nengo.Node(output = twos_complement_carry_in)

    twos_complement_a_plus_b_ensembles = []
    twos_complement_a_plus_b_plus_c_ensembles = []
    twos_complement_sum_ensembles = []
    twos_complement_carry_ensembles = []
	
    twos_complement_carry_ensembles.append(twos_complement_carry_in_node)

    for i in range(exponent_len):
        twos_complement_a_plus_b_ensembles.append(nengo.Ensemble(n_neurons = 300, dimensions = 1, radius = 2))
        twos_complement_a_plus_b_plus_c_ensembles.append(nengo.Ensemble(n_neurons = 600, dimensions = 2, radius = 2))
        twos_complement_sum_ensembles.append(nengo.Ensemble(n_neurons = 300, dimensions = 1, radius = 2))
        twos_complement_carry_ensembles.append(nengo.Ensemble(n_neurons = 300, dimensions = 1, radius = 2))

    
    # Connect the flipping ensemble outputs to the appropriate ensembles for
    # adding.

    for i in range(exponent_len):
        nengo.Connection(flipping_ensemble[i], twos_complement_a_plus_b_ensembles[i],
                function=flip_bits)
        nengo.Connection(adding_nodes[i], twos_complement_a_plus_b_ensembles[i])

    for i in range(exponent_len):
	    nengo.Connection(twos_complement_a_plus_b_ensembles[i],
                    twos_complement_a_plus_b_plus_c_ensembles[i][0])
	    nengo.Connection(twos_complement_carry_ensembles[i],
                    twos_complement_a_plus_b_plus_c_ensembles[i][1])
	    nengo.Connection(twos_complement_a_plus_b_plus_c_ensembles[i],
                    twos_complement_sum_ensembles[i], function = calculate_output_bit)
	    nengo.Connection(twos_complement_a_plus_b_plus_c_ensembles[i],
                    twos_complement_carry_ensembles[i + 1], function = calculate_carry_out)

    #Last Carry Ensemble is not needed, we can remove it if needed to reduce no
    #of neurons.
    
    #Sum Ensembles are from LSB to MSB.
    #exponent_len-bit adder for adding twos complement.

    subtraction_carry_in = 0
    subtraction_carry_in_node = nengo.Node(output = subtraction_carry_in)

    subtraction_a_plus_b_ensembles = []
    subtraction_a_plus_b_plus_c_ensembles = []
    subtraction_sum_ensembles = []
    subtraction_carry_ensembles = []
	
    subtraction_carry_ensembles.append(subtraction_carry_in_node)

    for i in range(exponent_len):
        subtraction_a_plus_b_ensembles.append(nengo.Ensemble(n_neurons = 300, dimensions = 1, radius = 2))
        subtraction_a_plus_b_plus_c_ensembles.append(nengo.Ensemble(n_neurons = 600, dimensions = 2, radius = 2))
        subtraction_sum_ensembles.append(nengo.Ensemble(n_neurons = 300, dimensions = 1, radius = 2))
        subtraction_carry_ensembles.append(nengo.Ensemble(n_neurons = 300, dimensions = 1, radius = 2))

    
    # Connect the exponent1 nodes and sum_ensembles to the appropriate ensembles

    for i in range(exponent_len):
        nengo.Connection(exponent1_nodes[i], subtraction_a_plus_b_ensembles[i])
        nengo.Connection(twos_complement_sum_ensembles[i],
                subtraction_a_plus_b_ensembles[i])


    for i in range(exponent_len):
        nengo.Connection(subtraction_a_plus_b_ensembles[i], subtraction_a_plus_b_plus_c_ensembles[i][0])
        nengo.Connection(subtraction_carry_ensembles[i], subtraction_a_plus_b_plus_c_ensembles[i][1])
        nengo.Connection(subtraction_a_plus_b_plus_c_ensembles[i], subtraction_sum_ensembles[i], function = calculate_output_bit)
        nengo.Connection(subtraction_a_plus_b_plus_c_ensembles[i], subtraction_carry_ensembles[i + 1], function = calculate_carry_out)
    
    #exponent_len-bit Exponent Multiplexer
    """selected_exponent_ensemble = nengo.Ensemble(n_neurons = 100 * exponent_len,
            dimensions = exponent_len, radius = 2)

    #selected_exponent_ensembles = []
    
    exponent_multiplexer = nengo.Ensemble(n_neurons = (200 * exponent_len +
        100), dimensions = (2 * exponent_len + 1), radius = 2)
    for i in range(exponent_len):
        nengo.Connection(exponent1_nodes[i], exponent_multiplexer[i])
        nengo.Connection(exponent2_nodes[i], exponent_multiplexer[exponent_len
            + i])
    nengo.Connection(subtraction_carry_ensembles[exponent_len],
            exponent_multiplexer[2 * exponent_len])

   # for i in range(exponent_len):
   #     selected_exponent_ensembles.append(nengo.Ensemble(n_neurons = 100,
   #         dimensions = 1, radius = 2))

    nengo.Connection(exponent_multiplexer, selected_exponent_ensemble, function = select_exponent)"""


    twos_complement_sum_probes = []
    subtraction_sum_probes = []

    for i in range(exponent_len):
        twos_complement_sum_probes.append(nengo.Probe(twos_complement_sum_ensembles[i], synapse = 0.01))
        subtraction_sum_probes.append(nengo.Probe(subtraction_sum_ensembles[i],
            synapse = 0.01))
    twos_complement_carry_out_probe = nengo.Probe(twos_complement_carry_ensembles[exponent_len], synapse = 0.01)
    subtraction_carry_out_probe = nengo.Probe(subtraction_carry_ensembles[exponent_len], synapse = 0.01)
    
with nengo.Simulator(model) as sim:
    # Run the model
    # Print probe values
    sim.run(5.0)
    exponent1_string = "Exponent 1: "
    exponent2_string = "Exponent 2: "
    for i in range(exponent_len):
        exponent1_string = exponent1_string + str(exponent1_bits[exponent_len - i - 1])
        exponent2_string = exponent2_string + str(exponent2_bits[exponent_len - i - 1])
    print(exponent1_string)
    print(exponent2_string)
    print("Twos Complement Carry Out: " + str(np.mean(sim.data[twos_complement_carry_out_probe])))
    for i in range(exponent_len):
        print("Twos Complement Output Bit  " + str(i) + ": "
                + str(np.mean(sim.data[twos_complement_sum_probes[exponent_len - i - 1]])))
    print("Subtraction Carry Out: " + str(np.mean(sim.data[subtraction_carry_out_probe])))
    for i in range(exponent_len):
        print("Subtraction Output Bit  " + str(i) + ": "
                + str(np.mean(sim.data[subtraction_sum_probes[exponent_len - i - 1]])))
