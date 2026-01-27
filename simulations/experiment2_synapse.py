from brian2 import *
import matplotlib.pyplot as plt

start_scope()
tau = 10*ms
v_rest = -70*mV
v_threshold = -55*mV
v_reset = -70*mV

eqs = '''
dv/dt = (v_rest - v + I) / tau : volt
I : volt # External current (stimulus)
'''

# neuron0
Source = NeuronGroup(1, eqs, threshold='v > v_threshold', reset='v = v_reset', method='exact')
Source.I = 20*mV  # high input - it will spike repeatedly
Source.v = v_rest

# Neuron 1
Target = NeuronGroup(1, eqs, threshold='v > v_threshold', reset='v = v_reset', method='exact')
Target.I = 0*mV   # no input - it should stay silent
Target.v = v_rest

S = Synapses(Source, Target, on_pre='v_post += 5*mV')
S.connect()

M_source = StateMonitor(Source, 'v', record=0)
M_target = StateMonitor(Target, 'v', record=0)

run(100*ms)


fig, axs = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
# source plot
axs[0].plot(M_source.t/ms, M_source.v[0]/mV, 'k')
axs[0].set_ylabel('Source (mV)')
axs[0].set_title('Presynaptic Neuron (Spiking)')
axs[0].axhline(y=-55, color='r', linestyle=':', label='Threshold')
axs[0].grid(True)

#target plot
axs[1].plot(M_target.t/ms, M_target.v[0]/mV, 'b', lw=2)
axs[1].set_ylabel('Target (mV)')
axs[1].set_xlabel('Time (ms)')
axs[1].set_title('Postsynaptic Neuron (EPSPs)')
axs[1].axhline(y=-70, color='gray', linestyle='--', label='Rest')
axs[1].grid(True)

plt.tight_layout()
plt.savefig('../plots/experiment2_synapse.png')
print("Plot saved")
