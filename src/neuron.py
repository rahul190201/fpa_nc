import nengo
import numpy as np
from nengo.dists import Uniform
from matplotlib import pyplot as plt

model = nengo.Network(label = "A Single Neuron")
with model:
    cos_input = nengo.Node(lambda t:np.cos(8 * t))
    neuron  = nengo.Ensemble(n_neurons=1, dimensions=1, intercepts = Uniform(-.5,-.5),
        max_rates=Uniform(100, 100), encoders = [[1]])
    nengo.Connection(cos_input, neuron)
    cos_probe = nengo.Probe(cos_input)
    spikes = nengo.Probe(neuron.neurons)
    voltage = nengo.Probe(neuron.neurons, 'voltage')
    filtered = nengo.Probe(neuron, synapse = 0.1)
    with nengo.Simulator(model) as sim:
        sim.run(5)
        fig1 = plt.figure()
        plt.plot(sim.trange(), sim.data[cos_probe])
        plt.plot(sim.trange(), sim.data[filtered])
        #plt.plot(sim.trange(), sim.data[spikes])
        #plt.xlim(0, 1)
        plt.show()
