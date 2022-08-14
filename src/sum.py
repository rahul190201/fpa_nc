import nengo
import matplotlib.pyplot as plt

# Create the model object
model = nengo.Network()

with model:
    # Create 3 ensembles each with 100 leaky integrate-and-fire neurons
    input_1_ensemble = nengo.Ensemble(n_neurons = 1000, dimensions = 1, radius = 10)
    input_2_ensemble = nengo.Ensemble(n_neurons = 1000, dimensions = 1, radius = 10)
    output_ensemble = nengo.Ensemble(n_neurons = 1000, dimensions = 1, radius = 10)    

    # Create input nodes representing constant values
    input_node_1 = nengo.Node(output = 2.1)
    input_node_2 = nengo.Node(output = 6.9)

    # Connect the input nodes to the appropriate ensembles
    nengo.Connection(input_node_1, input_1_ensemble)
    nengo.Connection(input_node_2, input_2_ensemble)

    # Connect the input ensembles to the output ensembles    
    nengo.Connection(input_1_ensemble, output_ensemble)
    nengo.Connection(input_2_ensemble, output_ensemble)
    
    # Probe output
    input_node_1_probe = nengo.Probe(input_node_1, synapse = 0.01)
    input_node_2_probe = nengo.Probe(input_node_2, synapse = 0.01)
    input_1_ensemble_probe = nengo.Probe(input_1_ensemble, synapse = 0.01)
    input_2_ensemble_probe = nengo.Probe(input_2_ensemble, synapse = 0.01)
    output_ensemble_probe = nengo.Probe(output_ensemble, synapse = 0.01)

with nengo.Simulator(model) as sim:
    # Run the model
    sim.run(5.0)

    # Print probe values
    print(sim.data[input_node_1_probe][-10:])
    print(sim.data[input_node_2_probe][-10:])
    print(sim.data[output_ensemble_probe][-10:])

    # Plot the input signals and ensemble values
    fig = plt.figure()
    plt.plot(sim.trange(), sim.data[input_1_ensemble_probe], label = 'Decoded Ensemble for input 1', color = "blue")
    plt.plot(sim.trange(), sim.data[input_2_ensemble_probe], label = 'Decoded Ensemble for input 2', color = "orange")
    plt.plot(sim.trange(), sim.data[output_ensemble_probe], label = 'Decoded Ensemble for output', color = "green")
    plt.plot(sim.trange(), sim.data[input_node_1_probe], label = 'Input 1', color = "yellow", linewidth = 2.0)
    plt.plot(sim.trange(), sim.data[input_node_2_probe], label = 'Input 2', color = "black", linewidth = 2.0)
    plt.legend()
    plt.xlabel('time [s]')
    plt.show()  
