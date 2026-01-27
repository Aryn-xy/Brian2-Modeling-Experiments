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
* **Key Result:** We observe **Temporal Summation**. The Target neuron integrates incoming spikes. Since the input frequency is high, the voltage "staircases" upward because the membrane potential does not fully decay between inputs.

**Resulting Plot:**
![EPSP Synapse](plots/experiment2_synapse.png)

---
## Experiment 3: Neural Decision Making (Winner-Take-All)
**Objective:** Model how a neural network resolves conflict between two competing inputs using **Lateral Inhibition**. This simulation uses a competitive network architecture where the winner silences the loser.

**1. The Physics (LIF Model)**
We use the Leaky Integrate-and-Fire equation:
$$\frac{dv}{dt} = \frac{(v_{rest} - v + I)}{tau}$$
* **Input Bias:** Neuron A receives slightly more current ($25mV$) than Neuron B ($22mV$). Without inhibition, both would fire.

**2. The Wiring (Lateral Inhibition)**
The crucial logic lies in the synapse definition:
```python
S = Synapses(G, G, on_pre='v_post -= 30*mV')
S.connect(condition='i != j')```

**Resulting Plot:**
![Decision Plot](plots/experiment3_decision.png)

---
