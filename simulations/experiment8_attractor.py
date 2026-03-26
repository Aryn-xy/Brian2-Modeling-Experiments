from brian2 import *
import matplotlib.pyplot as plt
import numpy as np

start_scope()

# ---- Parameters ----
N         = 100      # neurons arranged on a ring
tau       = 15*ms    # membrane time constant
tau_syn   = 5*ms     # synaptic decay time constant
v_rest    = -70*mV
v_thr     = -50*mV   # threshold (20 mV above rest)
v_reset   = -70*mV
J_exc     = 7.0      # excitatory weight scale (mV)
J_inh     = 0.2      # uniform global inhibitory offset in the Mexican-hat profile (mV)
sigma_exc = 0.05     # Gaussian half-width (fraction of ring circumference)

# ---- Neuron Model ----
eqs = '''
dv/dt     = (v_rest - v + I_bg + I_stim + g_syn) / tau : volt (unless refractory)
dg_syn/dt = -g_syn / tau_syn : volt
I_bg   : volt
I_stim : volt
'''

G = NeuronGroup(N, eqs,
                threshold='v > v_thr',
                reset='v = v_reset',
                refractory=2*ms,
                method='euler')
G.v      = v_rest
G.I_bg   = 12*mV    # background drive: 8 mV below threshold (no spontaneous firing)
G.I_stim = 0*mV

# ---- Recurrent Synapses: Mexican-Hat Connectivity ----
# Close neurons receive net excitation; distant neurons receive net inhibition.
S = Synapses(G, G, 'w : volt', on_pre='g_syn_post += w')
S.connect()  # all-to-all

i_arr  = np.array(S.i)
j_arr  = np.array(S.j)
d      = np.abs(i_arr - j_arr)
d      = np.minimum(d, N - d)          # shortest distance on the ring
d_frac = d / N                         # normalise to [0, 0.5]

# Difference-of-Gaussians (Mexican-hat) weight profile
w_vals = J_exc * np.exp(-0.5 * (d_frac / sigma_exc)**2) - J_inh
S.w    = w_vals * mV

# ---- Monitors ----
spikes = SpikeMonitor(G)
state  = StateMonitor(G, 'v', record=True)

# ---- Phase 1: Baseline — no external input (50 ms) ----
print("Phase 1: Baseline (no stimulus)...")
run(50*ms)

# ---- Phase 2: Localised stimulus centred at neuron 50 (100 ms) ----
print("Phase 2: Stimulus ON (localised at neuron 50)...")
stim_center    = 50
stim_width     = 5         # half-width in neuron indices
stim_amplitude = 12*mV    # extra drive pushes bump neurons above threshold

idx    = np.arange(N)
d_stim = np.abs(idx - stim_center)
d_stim = np.minimum(d_stim, N - d_stim)   # ring distance
G.I_stim = np.where(d_stim <= stim_width, float(stim_amplitude / mV), 0) * mV

run(100*ms)

# ---- Phase 3: Stimulus OFF — observe persistent attractor state (150 ms) ----
print("Phase 3: Stimulus OFF (working-memory persistence)...")
G.I_stim = 0*mV
run(150*ms)

# ---- Scientific Analysis ----
late_persist = [(float(t), int(i)) for t, i in zip(spikes.t/ms, spikes.i) if t > 250]
bump_neurons = sorted(set(i for _, i in late_persist))

print("\n" + "="*50)
print("          RING ATTRACTOR — RESULTS")
print("="*50)
if bump_neurons:
    print(f"Active neurons during late persistence (250-300 ms): {len(bump_neurons)}")
    center_estimate = np.mean(bump_neurons)
    print(f"Estimated bump centre: neuron {center_estimate:.1f}  (stimulus was at {stim_center})")
    bump_fwhm = max(bump_neurons) - min(bump_neurons)
    print(f"Approximate bump width (FWHM): {bump_fwhm} neurons  ({bump_fwhm / N * 100:.1f}% of ring)")
    print("\nCONCLUSION: Attractor state maintained after stimulus offset.")
    print("The network exhibits working-memory — persistent activity encodes")
    print("the remembered stimulus location without ongoing external input.")
else:
    print("Bump did not persist. Consider increasing J_exc or I_bg.")
print("="*50 + "\n")

# ---- Plotting ----
t_total_ms = 300

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Experiment 8: Ring Attractor Network — Bump Attractor Dynamics',
             fontsize=14, fontweight='bold')

# -- Panel 1: Raster plot --
ax1 = axes[0, 0]
if len(spikes.t) > 0:
    ax1.scatter(spikes.t/ms, spikes.i, s=3, c='black', alpha=0.7)
ax1.axvline(50,  color='green', lw=2, linestyle='--', label='Stimulus ON')
ax1.axvline(150, color='red',   lw=2, linestyle='--', label='Stimulus OFF')
ax1.axhspan(stim_center - stim_width, stim_center + stim_width,
            color='green', alpha=0.08, label='Stimulus region')
ax1.set_xlim(0, t_total_ms)
ax1.set_ylim(0, N)
ax1.set_xlabel('Time (ms)')
ax1.set_ylabel('Neuron Index')
ax1.set_title('Raster Plot')
ax1.legend(fontsize=9)
ax1.grid(True, alpha=0.3)

# -- Panel 2: Activity heatmap — spike density over time --
bin_ms = 5
n_bins = t_total_ms // bin_ms
rate_map = np.zeros((N, n_bins))
for t_sp, i_sp in zip(spikes.t/ms, spikes.i):
    b = int(t_sp / bin_ms)
    if 0 <= b < n_bins:
        rate_map[int(i_sp), b] += 1

ax2 = axes[0, 1]
im = ax2.imshow(rate_map, aspect='auto', origin='lower',
                extent=[0, t_total_ms, 0, N],
                cmap='hot', interpolation='nearest')
ax2.axvline(50,  color='lime', lw=1.5, linestyle='--', label='Stimulus ON')
ax2.axvline(150, color='cyan', lw=1.5, linestyle='--', label='Stimulus OFF')
ax2.legend(fontsize=9)
plt.colorbar(im, ax=ax2, label='Spike count / 5 ms bin')
ax2.set_xlabel('Time (ms)')
ax2.set_ylabel('Neuron Index')
ax2.set_title('Population Activity Heatmap')

# -- Panel 3: Mexican-hat connectivity profile --
ax3 = axes[1, 0]
center_ref  = N // 2
j_test      = np.arange(N)
d_test      = np.abs(j_test - center_ref)
d_test      = np.minimum(d_test, N - d_test)
d_frac_test = d_test / N
w_profile   = J_exc * np.exp(-0.5 * (d_frac_test / sigma_exc)**2) - J_inh

ax3.plot(j_test - center_ref, w_profile, color='purple', lw=2)
ax3.fill_between(j_test - center_ref, 0, w_profile,
                 where=(w_profile > 0), color='red',  alpha=0.3, label='Net Excitation')
ax3.fill_between(j_test - center_ref, 0, w_profile,
                 where=(w_profile < 0), color='blue', alpha=0.3, label='Net Inhibition')
ax3.axhline(0, color='k', lw=1, linestyle=':')
ax3.set_xlabel('Neuron Distance from Source')
ax3.set_ylabel('Synaptic Weight (mV)')
ax3.set_title('Mexican-Hat Connectivity Profile')
ax3.legend()
ax3.grid(True, alpha=0.5)

# -- Panel 4: Spatial bump profiles at key time windows --
ax4 = axes[1, 1]
dt_ms = float(defaultclock.dt / ms)

def mean_v_window(t_start_ms, t_end_ms):
    a = max(0, int(t_start_ms / dt_ms))
    b = min(state.v.shape[1], int(t_end_ms / dt_ms))
    return np.mean(state.v[:, a:b], axis=1)

v_baseline = mean_v_window(20,  50)
v_during   = mean_v_window(80, 150)
v_after    = mean_v_window(200, 280)

ax4.plot(range(N), v_baseline/mV, color='gray',  lw=1.5, linestyle=':',
         label='Baseline  (20–50 ms)')
ax4.plot(range(N), v_during/mV,   color='blue',  lw=2,
         label='During Stimulus  (80–150 ms)')
ax4.plot(range(N), v_after/mV,    color='red',   lw=2,   linestyle='--',
         label='After Stimulus  (200–280 ms)')
ax4.axhline(v_thr/mV, color='k', lw=1, linestyle=':', label='Threshold (−50 mV)')
ax4.axvline(stim_center, color='green', lw=1, linestyle=':', alpha=0.6,
            label=f'Stimulus centre (neuron {stim_center})')
ax4.set_xlabel('Neuron Index')
ax4.set_ylabel('Mean Membrane Potential (mV)')
ax4.set_title('Spatial Bump Profile — Working Memory')
ax4.legend(fontsize=9)
ax4.grid(True, alpha=0.5)

plt.tight_layout()
plt.savefig('../plots/experiment8_attractor.png', dpi=150)
print("Plot saved to ../plots/experiment8_attractor.png")
