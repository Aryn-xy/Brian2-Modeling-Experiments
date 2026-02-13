from brian2 import *
import matplotlib.pyplot as plt

start_scope()

tau = 10*ms
#STDP parameters
tau_pre=20*ms
tau_post=20*ms
a_pre=0.01 #amount to strengthen
a_post=-0.0105  #amount to weaken
w_max=1.0 #max synaptic weight

#Neurons
source=PoissonGroup(1,rates=20*Hz)

eqs=''' 
dv/dt = (v_rest - v + I)/tau:volt
I:volt
v_rest:volt
'''
target= NeuronGroup(1,eqs,threshold='v>-50*mV', reset='v=-70*mV',method='exact')
target.v=-70*mV
target.v_rest=-70*mV
target.I=40*mV

#learning synapse
synapse_eqs='''
w:1
dapre/dt = -apre/tau_pre: 1 (event-driven)
dapost/dt = -apost/tau_post: 1 (event-driven)
'''
on_pre_rule = '''
v_post += w * 10*mV
apre += a_pre
w = clip(w + apost, 0, w_max)
'''

on_post_rule = '''
apost += a_post
w = clip(w + apre, 0, w_max)
'''

S = Synapses(source, target, 
             model=synapse_eqs,
             on_pre=on_pre_rule,
             on_post=on_post_rule)
S.connect()
S.w = 0.5


M = StateMonitor(S, 'w', record=True)

print("Simulating learning...")
run(30*second)

plt.figure(figsize=(10, 5))
plt.plot(M.t/second, M.w[0], 'g-', linewidth=2)
plt.xlabel('Time (s)')
plt.ylabel('Synaptic Weight (w)')
plt.title('Synaptic Plasticity (STDP): Evolution of a Weight')
plt.grid(True)
plt.ylim(0, 1.1)
plt.axhline(y=0.5, color='k', linestyle='--', alpha=0.5, label='Initial Weight')
plt.legend()

plt.savefig('../plots/experiment4_stdp.png')
print("plot saved")
