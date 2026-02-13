from brian2 import *
import matplotlib.pyplot as plt
import numpy as np

start_scope()

N_inputs = 20
#first 10 (0-9) are Pattern (correlated)
#last 10 (10-19) are Noise (uncorrelated)

tau = 10*ms
w_max = 1.0
sim_time = 20*second

# STDP Parameters
tau_pre = 20*ms
tau_post = 20*ms
a_pre = 0.01
a_post = -0.0105


indices = []
times = []

#generate 2 seconds of data
for t_ms in range(0, 2000, 10):
    t_sec = t_ms * ms
    
    # Pattern (Signal):
    #every 50ms, inputs 0-9 fire together
    if t_ms % 50 == 0:
        jitter = np.random.randint(0, 3, 10) * ms
        indices.extend(range(10)) 
        times.extend([t_sec + j for j in jitter])
        
    # Noise:
    #inputs 10-19 fire randomly
    noise_spikes = np.random.rand(10) < 0.1
    for i in range(10):
        if noise_spikes[i]:
            indices.append(10 + i)
            times.append(t_sec + np.random.randint(0, 10)*ms)

Input_Layer = SpikeGeneratorGroup(N_inputs, indices, times)

#target neuron
eqs = '''
dv/dt = (v_rest - v) / tau : volt
v_rest : volt
'''

target = NeuronGroup(1, eqs, threshold='v > -50*mV', reset='v = -70*mV')
target.v = -70*mV
target.v_rest = -70*mV

#learning synapses
synapse_eqs = '''
w : 1
dapre/dt = -apre/tau_pre : 1 (event-driven)
dapost/dt = -apost/tau_post : 1 (event-driven)
'''

on_pre_rule = '''
v_post += w * 5*mV
apre += a_pre
w = clip(w + apost, 0, w_max)
'''

on_post_rule = '''
apost += a_post
w = clip(w + apre, 0, w_max)
'''


S = Synapses(Input_Layer, target, 
             model=synapse_eqs,
             on_pre=on_pre_rule,
             on_post=on_post_rule)

S.connect() 
S.w = 0.5   

M_weights = StateMonitor(S, 'w', record=True)
M_spikes = SpikeMonitor(target)

print("Training: Listening to the cocktail party...")
run(sim_time)


plt.figure(figsize=(12, 6))
avg_signal = np.mean(M_weights.w[0:10], axis=0)
plt.plot(M_weights.t/second, avg_signal, 'g-', linewidth=3, label='Signal (Inputs 0-9)')
avg_noise = np.mean(M_weights.w[10:20], axis=0)
plt.plot(M_weights.t/second, avg_noise, 'r--', linewidth=2, label='Noise (Inputs 10-19)')

plt.xlabel('Time (s)')
plt.ylabel('Average Synaptic Weight')
plt.title('Pattern Recognition: Signal vs Noise')
plt.legend()
plt.grid(True)
plt.ylim(0, 1.1)

plt.savefig('../plots/experiment5_pattern.png')
print("plot saved")
