import nengo

def product(x):
    return (x[0] * x[1])

model = nengo.Network()
with model:
    input_node_1 = nengo.Node(output = 0.5)
    input_node_2 = nengo.Node(output = 0.2)
    two_dim_ensemble = nengo.Ensemble(n_neurons = 1, dimensions = 2)
    nengo.Connection(input_node_1, two_dim_ensemble[0])
    nengo.Connection(input_node_2, two_dim_ensemble[1])
    output_ensemble = nengo.Ensemble(n_neurons = 1, dimensions = 1)
    nengo.Connection(two_dim_ensemble, output_ensemble, function = product)
    input_1_probe = nengo.Probe(input_node_1, synapse= 0.01)
    input_2_probe = nengo.Probe(input_node_2, synapse= 0.01)
    output_probe = nengo.Probe(output_ensemble, synapse = 0.01)
with nengo.Simulator(model) as sim:
    sim.run(5.0)
    print(sim.data[output_probe][-10:])
