# Brian2-Modeling-Experiments
Simulating dynamical systems in Computational Neuroscience using Brian2. Investigating neuronal dynamics, population coding, and emergent network behavior

**Tools:** Python, Brian2, Matplotlib, Linux
---

## Experiment 1: The F-I Curve (Neural Gain)
**Objective:** Characterize how a Leaky Integrate-and-Fire (LIF) neuron translates input current (I) into firing frequency (F).

* **Method:** Vectorized simulation of 100 neurons with increasing input currents (0mV-50mV).
* **Key Result:** The neuron exhibits a clear **Rheobase (Threshold)** at 20mV. Below this input, the cell is silent. Above it, the firing rate increases logarithmically, capped by the refractory period.

**Resulting Plot:**
![F-I Curve](plots/experiment1_FI_curve.png)

---
## Experiment 2: Synaptic Transmission (The EPSP)
**Objective:** Model the transmission of chemical signals between a "Source" neuron and a "Target" neuron.

* **Mechanism:** A pre-synaptic spike triggers an instantaneous increase in post synaptic voltage (`v_post += 5*mV`).
* **Key Result:** Observe **Temporal Summation**. The Target neuron integrates incoming spikes. Since the input frequency is high, the voltage "staircases" upward because the membrane potential does not fully decay between inputs.

**Resulting Plot:**
![EPSP Synapse](plots/experiment2_synapse.png)

---
## Experiment 3: Decision Making (Winner-Take-All)
**Objective:** Model how a neural network resolves conflict between two competing inputs using **lateral inhibition**.

* **Method:** Two neurons inhibit each other via mutual inhibitory synapses (`v_post -= 30 mV`). Neuron A receives a slightly stronger constant input than Neuron B, representing asymmetric evidence.
* **Analysis:** Utilize **phase-plane analysis** (plotting $V_A$ vs $V_B$) to visualize the system’s trajectory toward a **decision attractor**.
* **Key Result:** Despite both inputs being suprathreshold, the network converges to a single winner. Neuron A fires first and completely suppresses Neuron B, demonstrating **WTA**, race-to-threshold behavior, and neural contrast enhancement.

**Resulting Plot:**
![Decision Plot](plots/experiment3_decision.png)

---
## Experiment 4: Synaptic Learning (STDP)
**Objective:** Model biological learning using **Spike-Timing Dependent Plasticity (STDP)**. The synapse self adjusts its strength based on the precise timing of spikes. We replace the static synapse with a dynamic differential equation.

* **LTP (Strengthening):** If Pre-spike $\to$ Post-spike (causal), increase weight ($w$).
* **LTD (Weakening):** If Post-spike $\to$ Pre-spike (acausal), decrease weight ($w$).

**Resulting Plot:**
![STDP Plot](plots/experiment4_stdp.png)

---
## Experiment 5: Pattern Recognition (Signal vs Noise)
**Objective:** Test whether a single spiking neuron using STDP can automatically detect temporally correlated inputs embedded within random noise.

### The Setup
* **Neuron:** 1 postsynaptic LIF neuron.
* **Inputs:** 20 presynaptic channels.
    * **Signal (0–9):** Fire synchronously every 50 ms (Correlated).
    * **Noise (10–19):** Fire randomly (Uncorrelated).

### The Logic (Hebbian Learning)
Same as experiment 4.
* **Pre $\to$ Post:** Potentiation (LTP).
* **Post $\to$ Pre:** Depression (LTD).
* **Hypothesis:** Correlated inputs should strengthen (cause spikes), while random inputs should remain weak or decay.

### The Result
* **Signal Weights (Green):** Increased from 0.5 to **~0.75** (Selective Strengthening).
* **Noise Weights (Red):** Remained near baseline **~0.50** (No significant correlation).
* **Stability:** Learning stabilized after ~2–3 seconds.

### Interpretation
The neuron selectively strengthened synapses that consistently preceded its firing. This demonstrates:
1.  **Correlation Detection:** The neuron found the hidden pattern.
2.  **Competitive Learning:** The signal inputs "won" control over the neuron's firing.
3.  **Emergent Selectivity:** STDP alone is sufficient for a neuron to ignore uninformative noise without supervision.

**Resulting Plot:**
![Pattern Plot](plots/experiment5_pattern.png)

---
