#!/usr/bin/env python
#-*- coding:utf-8 -*-
#
# This file is part of the NNGT project to generate and analyze
# neuronal networks and their activity.
# Copyright (C) 2015-2017  Tanguy Fardet
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Use NNGT to analyze NEST-simulated activity of a random balanced network.
"""

import numpy as np
from scipy.special import lambertw

import matplotlib.pyplot as plt

import nngt
import nngt.generation as ng


'''
Simulation parameters
'''

nngt.set_config("omp", 8)

dt = 0.1         # the resolution in ms
simtime = 1000.  # Simulation time in ms
delay = 1.5      # synaptic delay in ms

g = 5.0          # ratio inhibitory weight/excitatory weight
eta = 2.0        # external rate relative to threshold rate
epsilon = 0.1    # connection probability


'''
Tools
'''

def ComputePSPnorm(tauMem, CMem, tauSyn):
    a = (tauMem / tauSyn)
    b = (1.0 / tauSyn - 1.0 / tauMem)

    # time of maximum
    t_max = 1.0 / b * (-lambertw(-np.exp(-1.0 / a) / a, -1) - 1.0 / a)
    t_max = np.real(t_max)

    # maximum of PSP for current of unit amplitude
    return (np.exp(1.0) / (tauSyn * CMem * b) *
            ((np.exp(-t_max / tauMem) - np.exp(-t_max / tauSyn)) / b -
             t_max * np.exp(-t_max / tauSyn)))


'''
Network parameters
'''

order = 1000
NE = 4 * order          # number of excitatory neurons
NI = 1 * order          # number of inhibitory neurons
N_neurons = NE + NI     # number of neurons in total
N_rec = 50              # record from 50 neurons

CE = int(epsilon * NE)  # number of excitatory synapses per neuron
CI = int(epsilon * NI)  # number of inhibitory synapses per neuron
C_tot = int(CI + CE)    # total number of synapses per neuron

tauSyn = 0.5  # synaptic time constant in ms
tauMem = 20.  # time constant of membrane potential in ms
CMem = 250.   # capacitance of membrane in in pF
theta = 20.   # membrane threshold potential in mV

neuron_params = {"C_m": CMem,
                 "tau_m": tauMem,
                 "tau_syn_ex": tauSyn,
                 "tau_syn_in": tauSyn,
                 "t_ref": 2.0,
                 "E_L": 0.0,
                 "V_reset": 0.0,
                 "V_m": 0.0,
                 "V_th": theta}

J_unit = ComputePSPnorm(tauMem, CMem, tauSyn)
J = 0.1            # postsynaptic amplitude in mV
J_ex = J / J_unit  # amplitude of excitatory postsynaptic current
J_in = g * J_ex   # amplitude of inhibitory postsynaptic current

nu_th = (theta * CMem) / (J_ex * CE * np.e * tauMem * tauSyn)
nu_ex = eta * nu_th
p_rate = 1000. * nu_ex * CE


'''
Create the population and network
'''

#~ synapses = {
    #~ (1, 1): {"weight": J_ex},
    #~ (1, -1): {"weight": J_ex},
    #~ (-1, 1): {"weight": J_in},
    #~ (-1, -1): {"weight": J_in}
#~ }
synapses = None

pop = nngt.NeuralPop.exc_and_inhib(
    N_neurons, en_model="iaf_psc_alpha", en_param=neuron_params,
    in_model="iaf_psc_alpha", in_param=neuron_params, syn_spec=synapses)

net = nngt.Network(population=pop)

#~ ng.connect_neural_groups(net, "excitatory", ["excitatory", "inhibitory"],
                         #~ "fixed_degree", degree=CE, weights=J_ex,
                         #~ delays=delay)

#~ ng.connect_neural_groups(net, "inhibitory", ["excitatory", "inhibitory"],
                         #~ "fixed_degree", degree=CI, weights=J_in,
                         #~ delays=delay)

ng.connect_neural_groups(net, "excitatory", ["excitatory", "inhibitory"],
                         "gaussian_degree", avg=CE, std=0.2*CE, weights=J_ex,
                         delays=delay)

ng.connect_neural_groups(net, "inhibitory", ["excitatory", "inhibitory"],
                         "gaussian_degree", avg=CI, std=0.2*CI, weights=J_in,
                         delays=delay)

#~ ng.connect_neural_groups(net, "excitatory", ["excitatory", "inhibitory"],
                         #~ "fixed_degree", degree=CE)
#~ ng.connect_neural_groups(net, "inhibitory", ["excitatory", "inhibitory"],
                         #~ "fixed_degree", degree=CI)
#~ print(net.get_weights().min(), net.get_weights().max(), len(net.get_weights()))

#~ ng.connect_neural_groups(net, "excitatory", ["excitatory", "inhibitory"],
                         #~ "distance_rule", scale=400., edges=CE*N_neurons,
                         #~ weights=J_ex, delays=delay)

#~ ng.connect_neural_groups(net, "inhibitory", ["excitatory", "inhibitory"],
                         #~ "distance_rule", scale=400., edges=CI*N_neurons,
                         #~ weights=J_in, delays=delay)
                         #~ "fixed_degree", degree=CI)


'''
Send the network to NEST, set noise and randomize parameters
'''

if nngt.get_config('with_nest'):
    import nngt.simulation as ns
    import nest

    nest.SetKernelStatus({"resolution": dt, "print_time": True,
                          "overwrite_files": True, 'local_num_threads': 4})

    gids = net.to_nest()

    '''
    Connecting the previously defined poisson generator to the excitatory
    and inhibitory neurons using the excitatory synapse. Since the poisson
    generator is connected to all neurons in the population the default
    rule ('all_to_all') of Connect() is used. The synaptic properties are
    inserted via syn_spec which expects a dictionary when defining
    multiple variables or a string when simply using a pre-defined
    synapse.
    '''

    pg = ns.set_poisson_input(gids, rate=p_rate,
                              syn_spec={"weight": J_ex, "delay": delay})

    ns.set_minis(net, base_rate=0.1)

    recorders, records = ns.monitor_groups(["excitatory", "inhibitory"], network=net)

    nest.Simulate(simtime)

    events_ex = nest.GetStatus(recorders[0], "n_events")[0]
    events_in = nest.GetStatus(recorders[1], "n_events")[0]

    '''
    Calculation of the average firing rate of the excitatory and the
    inhibitory neurons by dividing the total number of recorded spikes by
    the number of neurons recorded from and the simulation time. The
    multiplication by 1000.0 converts the unit 1/ms to 1/s=Hz.
    '''

    rate_ex = events_ex / simtime * 1000.0 / N_neurons
    rate_in = events_in / simtime * 1000.0 / N_neurons

    '''
    Reading out the number of connections established using the excitatory
    and inhibitory synapse model. The numbers are summed up resulting in
    the total number of synapses.
    '''

    num_synapses = len(nest.GetConnections())


    '''
    Printing the network properties, firing rates and building times.
    '''

    print("Brunel network simulation (Python)")
    print("Number of neurons : {0}".format(N_neurons))
    print("Number of synapses: {0}".format(num_synapses))
    print("       Exitatory  : {0}".format(int(CE * N_neurons) + N_neurons))
    print("       Inhibitory : {0}".format(int(CI * N_neurons)))
    print("Excitatory rate   : %.2f Hz" % rate_ex)
    print("Inhibitory rate   : %.2f Hz" % rate_in)

    if nngt.get_config('with_plot'):
        ideg = net.adjacency_matrix(weights=False, types=False)[pop["inhibitory"].ids, :].sum(axis=0).A1
        edeg = net.adjacency_matrix(weights=False, types=False)[pop["excitatory"].ids, :].sum(axis=0).A1
        #~ wdeg = net.get_degrees(use_weights=True)
        #~ betw = net.get_betweenness(btype="node", use_weights=True)
        #~ wdeg = nngt.analysis.subgraph_centrality(net)
        #~ ns.plot_activity(
            #~ recorders, records, network=net, transparent=True, show=True)
        #~ ns.plot_activity(
            #~ recorders, records, network=net, sort="in-degree", show=False)
        #~ ns.plot_activity(
            #~ recorders, records, network=net, sort="closeness", show=False)
        #~ ns.plot_activity(
            #~ recorders, records, network=net, sort=fr, show=False)
        #~ ns.plot_activity(
            #~ recorders, records, network=net, sort=fr, show=True)
            #~ recorders, records, network=net, sort=edeg-ideg, show=True)
            #~ recorders, records, network=net, sort=wdeg, show=True)
            #~ recorders, records, network=net, sort="win-degree", show=False)
        #~ ns.plot_activity(
            #~ recorders, records, network=net, sort="b2", show=False)
        #~ ns.plot_activity(
            #~ recorders, records, network=net, sort="firing_rate", show=True)

        exc_nodes = pop["excitatory"].ids
        inh_nodes = pop["inhibitory"].ids
        nngt.plot.correlation_to_attribute(
            net, (edeg-ideg)[exc_nodes], "firing_rate", nodes=exc_nodes,
            show=False)
        nngt.plot.correlation_to_attribute(
            net, (edeg-ideg)[inh_nodes], "firing_rate", nodes=inh_nodes,
            show=True)
        #~ nngt.plot.correlation_to_attribute(
            #~ net, edeg-ideg, "firing_rate", show=True)
