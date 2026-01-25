# Brian2-Modeling-Experiments
Simulating dynamical systems in Computational Neuroscience using Brian2. Investigating neuronal dynamics, population coding, and emergent network behavior

---

## Experiment 1: The F-I Curve (Neural Gain)
**Objective:** Characterize how a Leaky Integrate-and-Fire (LIF) neuron translates input current ($I$) into firing frequency ($F$).

**Tools:** Python, Brian2, Matplotlib, Linux (WSL)
* **Method:** Vectorized simulation of 100 neurons with increasing input currents (0mV-50mV).
* **Key Result:** The neuron exhibits a clear **Rheobase (Threshold)** at 20mV. Below this input, the cell is silent. Above it, the firing rate increases logarithmically, capped by the refractory period.

**Resulting Plot:**
![F-I Curve](plots/experiment1_FI_curve.png)

---
