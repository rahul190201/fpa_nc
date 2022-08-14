import nengo
import matplotlib.pyplot as plt

# Create the model object
model = nengo.Network()

with model:
    
    a0 = nengo.Node(output = 1)
    a1 = nengo.Node(output = 1)
    a2 = nengo.Node(output = 0)
    a3 = nengo.Node(output = 1)
    
    b0 = nengo.Node(output = 1)
    b1 = nengo.Node(output = 1)
    b2 = nengo.Node(output = 1)
    b3 = nengo.Node(output = 1)
    
    c0 = nengo.Node(output = 1)

    a0_plus_b0 = nengo.Ensemble(n_neurons = 100, dimensions = 1, radius = 2)
    a1_plus_b1 = nengo.Ensemble(n_neurons = 100, dimensions = 1, radius = 2)
    a2_plus_b2 = nengo.Ensemble(n_neurons = 100, dimensions = 1, radius = 2)
    a3_plus_b3 = nengo.Ensemble(n_neurons = 100, dimensions = 1, radius = 2)
    
    a0_b0_c0 = nengo.Ensemble(n_neurons = 200, dimensions = 2, radius = 2)
    a1_b1_c1 = nengo.Ensemble(n_neurons = 200, dimensions = 2, radius = 2)
    a2_b2_c2 = nengo.Ensemble(n_neurons = 200, dimensions = 2, radius = 2)
    a3_b3_c3 = nengo.Ensemble(n_neurons = 200, dimensions = 2, radius = 2)
    
    s0 = nengo.Ensemble(n_neurons = 100, dimensions = 1, radius = 2)
    s1 = nengo.Ensemble(n_neurons = 100, dimensions = 1, radius = 2)
    s2 = nengo.Ensemble(n_neurons = 100, dimensions = 1, radius = 2)
    s3 = nengo.Ensemble(n_neurons = 100, dimensions = 1, radius = 2)
    
    c1 = nengo.Ensemble(n_neurons = 100, dimensions = 1, radius = 2)
    c2 = nengo.Ensemble(n_neurons = 100, dimensions = 1, radius = 2)
    c3 = nengo.Ensemble(n_neurons = 100, dimensions = 1, radius = 2)
    c4 = nengo.Ensemble(n_neurons = 100, dimensions = 1, radius = 2)
    
    # Connect the input nodes to the appropriate ensembles
    nengo.Connection(a0, a0_plus_b0)
    nengo.Connection(b0, a0_plus_b0)
    nengo.Connection(a1, a1_plus_b1)
    nengo.Connection(b1, a1_plus_b1)
    nengo.Connection(a2, a2_plus_b2)
    nengo.Connection(b2, a2_plus_b2)
    nengo.Connection(a3, a3_plus_b3)
    nengo.Connection(b3, a3_plus_b3)
    
    nengo.Connection(a0_plus_b0, a0_b0_c0[0])
    nengo.Connection(c0, a0_b0_c0[1])
    nengo.Connection(a0_b0_c0, s0, function = sum)
    nengo.Connection(a0_b0_c0, c1, function = carry)
    
    nengo.Connection(a1_plus_b1, a1_b1_c1[0])
    nengo.Connection(c1, a1_b1_c1[1])
    nengo.Connection(a1_b1_c1, s1, function = sum)
    nengo.Connection(a1_b1_c1, c2, function = carry)
    
    nengo.Connection(a2_plus_b2, a2_b2_c2[0])
    nengo.Connection(c2, a2_b2_c2[1])
    nengo.Connection(a2_b2_c2, s2, function = sum)
    nengo.Connection(a2_b2_c2, c3, function = carry)
    
    nengo.Connection(a3_plus_b3, a3_b3_c3[0])
    nengo.Connection(c3, a3_b3_c3[1])
    nengo.Connection(a3_b3_c3, s3, function = sum)
    nengo.Connection(a3_b3_c3, c4, function = carry)
    
    # Probe output
    a0_probe = nengo.Probe(a0, synapse = 0.01)
    b0_probe = nengo.Probe(b0, synapse = 0.01)
    c0_probe = nengo.Probe(c0, synapse = 0.01)
    a0_plus_b0_probe = nengo.Probe(a0_plus_b0, synapse = 0.01)
    s0_probe = nengo.Probe(s0, synapse = 0.01)
    c1_probe = nengo.Probe(c1, synapse = 0.01)
    
with nengo.Simulator(model) as sim:
    # Run the model
    sim.run(5.0)

    # Print probe values
    print(sim.data[a0_probe][-10:])
    print(sim.data[b0_probe][-10:])
    print(sim.data[c0_probe][-10:])
    print(sim.data[a0_plus_b0_probe][-10:])
    print(sim.data[s0_probe][-10:])
    print(sim.data[c1_probe][-10:])

    # Plot the input signals and ensemble values
    fig = plt.figure()
    plt.plot(sim.trange(), sim.data[a0_probe], label = 'a0', color = "blue")
    plt.plot(sim.trange(), sim.data[b0_probe], label = 'b0', color = "orange")
    plt.plot(sim.trange(), sim.data[c0_probe], label = 'carry in', color = "green")
    plt.plot(sim.trange(), sim.data[a0_plus_b0_probe], label = 'a0 + b0', color = "yellow", linewidth = 2.0)
    plt.plot(sim.trange(), sim.data[s0_probe], label = 'sum', color = "grey", linewidth = 2.0)
    plt.plot(sim.trange(), sim.data[c1_probe], label = 'carry out', color = "purple", linewidth = 2.0)
    plt.legend()
    plt.xlabel('time [s]')
    plt.show()  
