from brian2 import *
import matplotlib.pyplot as plt
import numpy as np

#parameters
tau = 10*ms
w_max = 1.0
tau_c = 100*ms
learning_rate = 10*Hz

#test delays from 0ms to 700ms in steps of 50ms
delays = np.arange(0, 750, 50) * ms
final_weights = []

print("Starting Reward Delay Sweep...")
print(f"Testing {len(delays)} different delay periods...")

#sweep loop
for delay in delays:
    start_scope() #reset simulation for each trial
    
    #neurons
    source = SpikeGeneratorGroup(1, [0]*10, np.linspace(10, 100, 10)*ms)
    target = NeuronGroup(1, '''dv/dt = (v_rest - v)/tau : volt
                               v_rest : volt''',
                         threshold='v>-50*mV', reset='v=-70*mV', method='exact')
    target.v = -70*mV
    target.v_rest = -70*mV
    
    #synapse
    synapse_eqs = '''
    dc/dt = -c / tau_c : 1 (clock-driven)
    dopamine : 1 (shared)
    dw/dt = learning_rate * c * dopamine * (w_max - w) * w : 1 (clock-driven)
    '''
    on_pre_rule = '''
    v_post += w * 10*mV
    c += 1.0 
    '''
    
    S = Synapses(source, target, model=synapse_eqs, on_pre=on_pre_rule, method='euler')
    S.connect()
    S.w = 0.5
    S.dopamine = 0
    S.c = 0
    
    #phase A: stimulus (runs from 0 to 150ms)
    run(150*ms)
    
    #phase B: empty delay
    run(delay)
    
    #phase C:reward (dopamine floods in for 200ms)
    S.dopamine = 1.0
    run(200*ms)
    
    #record final weight after learning finishes
    final_weights.append(S.w[0])
    print(f"Trial with {delay} delay -> Final Weight: {S.w[0]:.3f}")


plt.figure(figsize=(9, 6))

#converting delays to ms for x-axis
x_vals = delays / ms
plt.plot(x_vals, final_weights, 'bo-', linewidth=2.5, markersize=8, label='Learned Weight')

#baseline
plt.axhline(y=0.5, color='r', linestyle='--', linewidth=2, label='Baseline (No Learning)')

plt.title('Reward Delay Sensitivity: The Credit Assignment Window', fontsize=14)
plt.xlabel('Dopamine Delay After Stimulus (ms)', fontsize=12)
plt.ylabel('Final Synaptic Weight (w)', fontsize=12)
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend(fontsize=11)
plt.fill_between(x_vals, 0.5, final_weights, where=(np.array(final_weights) > 0.505), color='blue', alpha=0.1)
plt.tight_layout()
plt.savefig('../plots/experiment7_reward_delay.png', dpi=300)
print("done.")
