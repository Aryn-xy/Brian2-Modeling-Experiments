from brian2 import *
import matplotlib.pyplot as plt

start_scope()

#Parameters
tau = 10*ms
w_max = 1.0
sim_time = 1*second
tau_c = 100*ms
learning_rate = 10*Hz

#Neurons
source = SpikeGeneratorGroup(1, [0]*10, np.linspace(100, 200, 10)*ms)
target = NeuronGroup(1, '''dv/dt = (v_rest - v)/tau : volt
                           v_rest : volt''',
                     threshold='v>-50*mV', reset='v=-70*mV')
target.v = -70*mV
target.v_rest = -70*mV

#Synapse
#c: eligibility trace
#dopamin: reward signal
#w: weight (changed by c*dopamine)
synapse_eqs = '''
dc/dt = -c / tau_c : 1 (clock-driven)
dopamine : 1 (shared)
dw/dt = learning_rate * c * dopamine * (w_max - w) * w : 1 (clock-driven)
'''

on_pre_rule = '''
v_post += w * 10*mV
c += 1.0 
'''

S = Synapses(source, target, 
             model=synapse_eqs,
             on_pre=on_pre_rule)

S.connect()
S.w = 0.5
S.dopamine = 0
S.c = 0

M = StateMonitor(S, ['w', 'c', 'dopamine'], record=True)
run(400*ms)

print("Releasing Dopamine (Reward)...")
S.dopamine = 1.0
run(200*ms)

S.dopamine = 0
run(400*ms)

fig, axs = plt.subplots(3, 1, figsize=(8, 10), sharex=True)
#plot 1: stimulus
axs[0].plot(M.t/ms, M.c[0], 'g', label='Eligibility Trace (c)')
axs[0].set_title('1. The Memory (Trace)')
axs[0].set_ylabel('Trace Magnitude')
axs[0].legend()
axs[0].grid(True)

#plot 2: reward (dopamine)
axs[1].plot(M.t/ms, M.dopamine[0], 'orange', label='Dopamine Reward', linewidth=2)
axs[1].set_title('2. The Reward (Dopamine)')
axs[1].set_ylabel('Concentration')
axs[1].fill_between(M.t/ms, M.dopamine[0], color='orange', alpha=0.3)
axs[1].grid(True)

#plot 3: result
axs[2].plot(M.t/ms, M.w[0], 'b', linewidth=3, label='Synaptic Weight (w)')
axs[2].set_title('3. The Learning (Weight Update)')
axs[2].set_ylabel('Weight Strength')
axs[2].set_xlabel('Time (ms)')
axs[2].legend()
axs[2].grid(True)

plt.tight_layout()
plt.savefig('../plots/experiment6_eligibility.png')
print("plot saved...")
