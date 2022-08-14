import numpy as np
import nengo
import matplotlib.pyplot as plt

def calculate_output_bit(vector):
    #print(vector)
    result = vector[0] + vector[1]
    if((0.5 < result <= 1.5) or (2.5 < result <= 3.5)):
        return 1
    return 0
 
def calculate_carry_out(vector):
    result = vector[0] + vector[1]
    if((1.5 < result <= 2.5) or (2.5 < result <= 3.5)):
        return 1
    return 0

# Create the model object
model = nengo.Network()

with model:
    input1 = [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1]
    input2 = [1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0]
    
    input1.reverse()
    input2.reverse()

    input1_nodes = []
    input2_nodes = []

    c00 = 0

    for i in range(len(input1)):
        input1_nodes.append(nengo.Node(output = input1[i]))
        input2_nodes.append(nengo.Node(output = input2[i]))      
    
    c0 = nengo.Node(output = c00)

    a_plus_b_ensembles = []
    a_plus_b_plus_c_ensembles = []
    sum_ensembles = []
    carry_ensembles = []
	
    carry_ensembles.append(c0)

    for i in range(len(input1)):
        a_plus_b_ensembles.append(nengo.Ensemble(n_neurons = 200, dimensions = 1, radius = 2))
        a_plus_b_plus_c_ensembles.append(nengo.Ensemble(n_neurons = 400, dimensions = 2, radius = 2))
        sum_ensembles.append(nengo.Ensemble(n_neurons = 200, dimensions = 1, radius = 2))
        carry_ensembles.append(nengo.Ensemble(n_neurons = 200, dimensions = 1, radius = 2))

    
    # Connect the input nodes to the appropriate ensembles

    for i in range(len(input1)):
        nengo.Connection(input1_nodes[i], a_plus_b_ensembles[i])
        nengo.Connection(input2_nodes[i], a_plus_b_ensembles[i])
    
    def sum(a0_b0_c0):
        s = 0
        
        if(((a0_b0_c0[0] + a0_b0_c0[1]) % 2) == 0):
            s = 0
        else:
            s = 1
            
        return s
        
    def carry(a0_b0_c0):
        c = 0
        
        if((a0_b0_c0[0] == 2 and a0_b0_c0[1] == 0) 
            or (a0_b0_c0[0] == 2 and a0_b0_c0[1] == 1) 
            or (a0_b0_c0[0] == 1 and a0_b0_c0[1] == 1)):
            c = 1
        else:
            c = 0
            
        return c

    for i in range(len(input1)):
	    nengo.Connection(a_plus_b_ensembles[i], a_plus_b_plus_c_ensembles[i][0])
	    nengo.Connection(carry_ensembles[i], a_plus_b_plus_c_ensembles[i][1])
	    nengo.Connection(a_plus_b_plus_c_ensembles[i], sum_ensembles[i], function = calculate_output_bit)
	    nengo.Connection(a_plus_b_plus_c_ensembles[i], carry_ensembles[i + 1], function = calculate_carry_out)

    # Probe output
    #a0_probe = nengo.Probe(a0, synapse = 0.01)
    #b0_probe = nengo.Probe(b0, synapse = 0.01)
    #c0_probe = nengo.Probe(c0, synapse = 0.01)
    #a0_plus_b0_probe = nengo.Probe(a0_plus_b0, synapse = 0.01)
    #s0_probe = nengo.Probe(sum_ensembles[0], synapse = 0.01)
    #c1_probe = nengo.Probe(c1, synapse = 0.01)
    #s1_probe = nengo.Probe(s1, synapse = 0.01)
    #s2_probe = nengo.Probe(s2, synapse = 0.01)
    #s3_probe = nengo.Probe(s3, synapse = 0.01)
    #c4_probe = nengo.Probe(c4, synapse = 0.01)

    sum_probes = []

    for i in range(len(input1)):
        sum_probes.append(nengo.Probe(sum_ensembles[i], synapse = 0.01))
    carry_out_probe = nengo.Probe(carry_ensembles[len(input1)], synapse = 0.01)
    
with nengo.Simulator(model) as sim:
    # Run the model
    # Print probe values
    sim.run(5.0)
    error = 0
    for i in range(len(input1)):
        j = np.mean(sim.data[sum_probes[i]])
        print("Sum Out " + str(i) + " " + str(j) + " " + str(int(round(j))))
        if (int(round(j)) == 1):
            error += 1 - j
        else:
            error += j   
    print("Carry Out: " + str(np.mean(sim.data[carry_out_probe])))
    accuracy = 1 - (error/len(input1))
    print("Accuracy: " + str(accuracy))
    #print(sim.data[a0_probe][-10:])
    #print(sim.data[b0_probe][-10:])
    #print(sim.data[c0_probe][-10:])
    #print(sim.data[a0_plus_b0_probe][-10:])
    #print(sim.data[s0_probe][-10:])
    #print(sim.data[c1_probe][-10:])

    # Plot the input signals and ensemble values
"""
    fig = plt.figure()
	input1_title = "Input 1="
	input2_title = "Input 2="
	carry_title = "Carry = " + str(c00)
	for i in range(len(input1)):
		input1_title = input1_title + str(input1[len(input1) - i - 1])
		input2_title = input2_title + str(input2[len(input2) - i - 1])
    figtitle = input1_title + ' ' + input2_title + ' ' + carry_title
    fig.suptitle(figtitle, fontsize=16, family='sans-serif')  
    plt.plot(sim.trange(), sim.data[s0_probe], label = 's0', color = "blue")
    plt.ylim(0.0, 1.0)
    plt.legend()
    fig = plt.figure()
    fig.suptitle(figtitle, fontsize=16, family='sans-serif')  
    plt.plot(sim.trange(), sim.data[s1_probe], label = 's1', color = "orange")
    plt.ylim(0.0, 1.0)
    plt.legend()
    fig = plt.figure()
    fig.suptitle(figtitle, fontsize=16, family='sans-serif')  
    plt.plot(sim.trange(), sim.data[s2_probe], label = 's2', color = "green")
    plt.ylim(0.0, 1.0)
    plt.legend()
    fig = plt.figure()
    fig.suptitle(figtitle, fontsize=16, family='sans-serif')  
    plt.plot(sim.trange(), sim.data[s3_probe], label = 's3', color = "yellow")
    plt.ylim(0.0, 1.0)
    plt.legend()
    fig = plt.figure()
    fig.suptitle(figtitle, fontsize=16, family='sans-serif')  
    plt.plot(sim.trange(), sim.data[c4_probe], label = 'c4', color = "grey")
    plt.ylim(0.0, 1.0)
    plt.legend()
    plt.xlabel('time [s]')
    plt.show()  """
