from brian2 import *
import matplotlib.pyplot as plt

start_scope()

# Parameters
N = 100
tau = 10*ms
v_rest = -70*mV
v_threshold = -50*mV
v_reset = -70*mV

# equation
eqs = '''
dv/dt = (v_rest - v + I) / tau : volt (unless refractory)
I : volt
'''

# population
G = NeuronGroup(N, eqs, 
                threshold='v > v_threshold', 
                reset='v = v_reset', 
                refractory=5*ms,
                method='exact')

G.v = v_rest
G.I = '50*mV * i / (N-1)' 

# 5. Monitor
M = SpikeMonitor(G)

print("Simulating 100 neurons simultaneously...")
run(1000*ms)


plt.figure(figsize=(8,5))

firing_rates = M.count / (1000*ms) # Convert to Hz

plt.plot(G.I/mV, firing_rates, 'k.-', lw=2)

plt.xlabel('Input Current (mV)')
plt.ylabel('Firing Rate (Hz)')
plt.title('The F-I Curve: Neural Gain')
plt.grid(True)
plt.axvline(x=20, color='r', linestyle='--', label='Theoretical Threshold')
plt.legend()

plt.savefig('../plots/experiment1_FI_curve.png')
print("Plot saved to ../plots/experiment1_FI_curve.png")
