from brian2 import *
import matplotlib.pyplot as plt
start_scope()

tau = 10*ms
v_rest = -70*mV
v_thr = -50*mV
v_reset=-70*mV
inhib_weight = 30*mV
eqs ='''

dv/dt=(v_rest-v+I)/tau:volt
I:volt
'''
G = NeuronGroup(2, eqs,threshold='v > v_thr', reset='v = v_reset',method='exact')
G.v = v_rest
G.I = [25*mV, 22*mV]

# when i spikes, it slams j down by 30mV
S = Synapses(G, G, on_pre='v_post -= inhib_weight')
S.connect(condition='i != j') # connect to everyone except self

M = StateMonitor(G, 'v', record=True)
spikes = SpikeMonitor(G)

print("simulating decision process...")
run(100*ms)

fig = plt.figure(figsize=(12, 5))

# timeline plot
ax1 = fig.add_subplot(121)
ax1.plot(M.t/ms, M.v[0]/mV, 'b', lw=2, label='Neuron A (Stronger)')
ax1.plot(M.t/ms, M.v[1]/mV, 'r--', alpha=0.7, lw=2, label='Neuron B (Weaker)')
ax1.axhline(y=-50, color='k', linestyle=':', label='Threshold')
ax1.set_xlabel('Time (ms)')
ax1.set_ylabel('Voltage (mV)')
ax1.set_title('Temporal Dynamics')
ax1.legend()
ax1.grid(True)

# phase plane plot
ax2 = fig.add_subplot(122)
ax2.plot(M.v[0]/mV, M.v[1]/mV, 'purple', lw=2)
ax2.set_xlabel('Neuron A Voltage (mV)')
ax2.set_ylabel('Neuron B Voltage (mV)')
ax2.set_title('Phase Plane Trajectory')
ax2.grid(True)

# marker for start and end
ax2.plot(M.v[0][0]/mV, M.v[1][0]/mV, 'go', label='Start')
ax2.plot(M.v[0][-1]/mV, M.v[1][-1]/mV, 'ro', label='End')
ax2.legend()

plt.tight_layout()
plt.savefig('../plots/experiment3_decision.png')
print("Plot saved.")

# scientific analysis
counts = spikes.count

if len(spikes.i) > 0:
    first_spiker = spikes.i[0]
    dominant_winner = np.argmax(counts)
    
    print("\n" + "="*40)
    print("       EXPERIMENTAL RESULTS       ")
    print("="*40)
    print(f"Spike Counts: Neuron 0 = {counts[0]} | Neuron 1 = {counts[1]}")
    print(f"1. Reaction Time Leader: Neuron {first_spiker}")
    print(f"2. Dominant (Total) Winner: Neuron {dominant_winner}")
    
    if first_spiker == dominant_winner:
        print("\nCONCLUSION: Strong Winner-Take-All regime confirmed.")
        print("The neuron that fired first successfully suppressed the rival.")
    else:
        print("\nCONCLUSION: Unstable decision regime.")
    print("="*40 + "\n")
else:
    print("No spikes recorded. Increase input current.")
