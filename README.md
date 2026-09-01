# DynoNetTopology — MDNTF-Quantum  

### Multiscale Dynamic Network–Topology Framework for Quantum-Sensed Complex Systems

DynoNetTopology is a computational physics framework for connecting the dynamics of complex physical and biological systems with quantum-sensing models, dynamic network analysis, and multiscale topological analysis.

## Executable Example

A concrete implementation is provided in [`examples/brain_nv_pipeline.py`](examples/brain_nv_pipeline.py).

The example demonstrates the connection between NV-center sensing, simulated
measurements, dynamic network construction, and Digital Map generation.

See [`examples/README.md`](examples/README.md) for the methodological explanation
and interpretation of the example.

## The framework is organized as a modular pipeline:

```text
Physical / Biological System
            │
            ▼
     Dynamic System State
            │
            ▼
 Time-Dependent Magnetic Field
        B(x,y,z,t)
            │
            ▼
      NV-Center Simulation
            │
            ▼
      Simulated Sensor Data
            │
            ▼
    Dynamic Interaction Network
            A(t)
            │
            ▼
            MDNTF
            │
            ▼
 Multiscale Topological Analysis
            │
            ▼
   Temporal Feature Tracking
            │
            ▼
        DIGITAL MAP
```

The **Multiscale Dynamic Network–Topology Framework (MDNTF)** forms the analytical core. The quantum-sensing layer provides a physical measurement interface, while the network and topology layers characterize how system structure evolves through time and across analysis scales.

---

## 1. Project Overview

Complex systems are dynamic: their states, interactions, and measurable signals change with time. DynoNetTopology is designed to preserve this temporal structure while connecting physical measurements to evolving networks and topological representations.

The framework combines four principal layers:

1. **Physical/system dynamics** — represents the evolving system.
2. **Quantum sensing** — models measurement through nitrogen-vacancy (NV) centers.
3. **Dynamic network analysis** — converts measurements into time-dependent interaction networks.
4. **Multiscale topology** — characterizes structural changes across time and filtration scale.

The final analytical representation is a **Digital Map** of the evolving system, combining physical, network, and topological information.

The architecture is intentionally modular so that the analytical core can be applied to different classes of complex systems without redesigning the underlying MDNTF methodology.

---

## 2. Motivation

A conventional network analysis often describes a system at an individual time point. Topological Data Analysis (TDA) can reveal structural properties such as connected components, loops, and higher-dimensional features.

For a system that evolves continuously, however, independent snapshots do not fully describe the dynamics.

A central question addressed by DynoNetTopology is:

> How can topological structures be characterized and followed as they evolve through time and across multiple scales?

For example, when a feature associated with a first Betti number, \( \beta_1 \), appears at one time and a similar feature appears later, temporal analysis can distinguish between possibilities such as:

- continuation of an evolving structure,
- deformation of an existing feature,
- disappearance and replacement,
- or a transient feature associated with noise.

DynoNetTopology therefore focuses on the **dynamic and temporal organization of network topology**, rather than treating every network state as an isolated calculation.

The framework is not intended to replace established TDA or persistent-homology libraries. Instead, those libraries can provide core computational operations while DynoNetTopology provides the surrounding framework for:

- dynamic network representation,
- multiscale filtration,
- temporal alignment,
- topological feature tracking,
- feature lifetime analysis,
- and interpretation of evolving structures.

---

## 3. Quantum Sensing with NV Centers

The NV-center component provides the quantum-sensing layer of the framework.

A physical or biological system generates a time-dependent physical field. That field can be used as the input to a simulated NV-center sensor array.

Conceptually:

```text
Physical System
      │
      ▼
Magnetic Field B(x,y,z,t)
      │
      ▼
NV-Center Sensor Array
      │
      ▼
Quantum Spin Response
      │
      ▼
Simulated Measurement
      │
      ▼
Sensor Time Series
```

The NV simulation is designed to represent the physical and measurement processes relevant to the computational experiment, including:

- NV-center spin properties,
- NV spin Hamiltonian,
- Zeeman interaction,
- sensor geometry and orientation,
- magnetic-field response,
- measurement and readout modelling,
- noise,
- and decoherence effects.

The purpose of this layer is to provide a **physical measurement interface** between the simulated system and the downstream network-analysis pipeline.

The resulting methodological chain is:

```text
Physical Dynamics
        ↓
Quantum Sensing
        ↓
Measured Signals
        ↓
Network Dynamics
        ↓
Topological Dynamics
```

---

## 4. Dynamic Network Construction

Sensor measurements are represented as a time-dependent interaction network.

The network can be expressed as

\[
A(t) = [A_{ij}(t)]
\]

where:

- nodes represent sensors, physical components, or other system elements;
- edges represent interactions between nodes;
- edge weights can vary with time.

The evolving network is represented by a sequence of states:

```text
A(t₁)
A(t₂)
A(t₃)
...
A(tₙ)
```

The interaction definition depends on the application and may be based on an appropriate correlation, coupling, similarity, or other physically motivated measure.

A key requirement is that the temporal ordering of network states is preserved so that structural changes can be analyzed dynamically.

---

## 5. The MDNTF Core

The **Multiscale Dynamic Network–Topology Framework (MDNTF)** is the central analytical component of DynoNetTopology.

MDNTF connects dynamic network states with multiscale topological analysis. The evolving network is represented through filtered structures, enabling topological features to be characterized across time and analysis scale.

The core analytical sequence is:

```text
Dynamic Network
      │
      ▼
Network Representation
      │
      ▼
Multiscale Filtration
      │
      ▼
Simplicial Complexes
      │
      ▼
Persistent Homology
      │
      ▼
Temporal Feature Alignment
      │
      ▼
Topological Feature Trajectories
```

Depending on the structure of the data and the chosen complex, the framework can analyze topological quantities such as:

\[
\beta_0(t,\mathrm{scale}), \qquad
\beta_1(t,\mathrm{scale}), \qquad
\beta_2(t,\mathrm{scale})
\]

Rather than treating each network state independently, MDNTF is designed to examine how topological structures:

- appear,
- evolve,
- persist,
- merge,
- split,
- and disappear.

This temporal perspective is a central distinction between the framework and a purely snapshot-based topological analysis.

---

## 6. Digital Map

The **Digital Map** is the final analytical representation of the evolving system.

It is more than a software data-flow diagram. It is intended to combine information from the physical, sensing, network, and topological layers into an interpretable representation.

Depending on the application, the Digital Map can incorporate:

- physical/system locations,
- sensor locations,
- dynamic network connections,
- network evolution through time,
- filtration scale,
- Betti-number profiles,
- persistent features,
- feature lifetimes,
- topological transitions,
- and relationships between physical dynamics and structural changes.

Conceptually:

```text
                 DIGITAL MAP
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
   Physical       Network       Topology
    Dynamics      Evolution     Evolution
        │             │             │
        └─────────────┼─────────────┘
                      │
                      ▼
             System Interpretation
```

The Digital Map is intended to support questions such as:

- When does the network become more integrated?
- When does fragmentation occur?
- Which structures persist over time?
- Which structures are transient?
- At what scale does a structural transition occur?
- How does topology respond to changes in the underlying physical system?

---

## 7. Example: Brain-Dynamics Application

A brain-inspired system provides an initial application context for demonstrating the MDNTF analytical workflow.

The following figure illustrates the **MDNTF analytical layer using brain-dynamics data**. It is an example application and does not restrict the framework to neuroscience.

![MDNTF example implementation](https://github.com/user-attachments/assets/d04db74c-95ba-4491-a2ae-31d447680ee2)

**Figure 1.** Example implementation of the MDNTF for brain dynamics, from EEG/fMRI input through dynamic network and topological analysis to the resulting digital map, with optional physics-informed RL integration.

The figure demonstrates the network, temporal, topological, and Digital Map components independently of the quantum-sensing layer. In the broader DynoNetTopology architecture, NV-center sensing can serve as a physical measurement/input layer feeding the same analytical core.

---

## 8. Cross-Domain Design

A central design principle is the separation between the **physical system layer** and the **analytical core**.

The physical meaning of nodes, signals, and interactions can change between applications, while the network and topological analysis components remain reusable.

Potential application domains include:

```text
Brain Dynamics
      │
      ├──→ Measurement / Sensing
      │
      └──→ MDNTF
             │
             ▼
         Digital Map
```

```text
Fluid Dynamics
      │
      └──→ Dynamic Network
             │
             ▼
           MDNTF
             │
             ▼
         Digital Map
```

```text
Power Grid Dynamics
      │
      └──→ Dynamic Network
             │
             ▼
           MDNTF
             │
             ▼
         Digital Map
```

The architecture therefore separates **domain-specific physical modelling** from the **domain-independent network and topological analysis**.

---

## 9. Development Status and Roadmap

DynoNetTopology is being developed incrementally, with individual components tested before full end-to-end integration.

The current development roadmap is:

- [ ] Physical/system dynamics model
- [ ] Magnetic-field model
- [ ] NV-center sensing simulation
- [ ] Dynamic network construction
- [ ] MDNTF topological engine
- [ ] Digital Map visualization
- [ ] End-to-end integration and validation
- [ ] Optional physics-informed reinforcement-learning extension

The roadmap describes implementation status and does not change the conceptual architecture of the framework.

---

## 10. Repository Structure

The repository is organized around the separation of physical models, sensing, dynamic networks, topology, and visualization.

The target package structure is:

```text
dynonettopology/
│
├── src/
│   └── dynonettopology/
│       │
│       ├── systems/
│       │   ├── base.py
│       │   └── brain/
│       │
│       ├── fields/
│       │   └── magnetic.py
│       │
│       ├── sensors/
│       │   └── nv/
│       │       ├── hamiltonian.py
│       │       ├── sensor.py
│       │       ├── array.py
│       │       └── noise.py
│       │
│       ├── networks/
│       │   ├── construction.py
│       │   └── dynamics.py
│       │
│       ├── mdntf/
│       │   ├── filtration.py
│       │   ├── complexes.py
│       │   ├── persistence.py
│       │   └── tracker.py
│       │
│       └── digital_map/
│           ├── map.py
│           ├── metrics.py
│           └── visualization.py
│
├── examples/
│   └── brain_nv_pipeline.py
│
├── tests/
│
├── docs/
│
├── README.md
├── pyproject.toml
├── LICENSE
└── .gitignore
```

---

## 11. Methodological Architecture

The complete conceptual architecture can be summarized as:

```text
Physical Dynamics
       ↓
Magnetic Field
       ↓
NV Quantum Sensing
       ↓
Sensor Measurements
       ↓
Dynamic Network
       ↓
Multiscale Topology
       ↓
Temporal Feature Tracking
       ↓
Digital Map
```

Each layer has a distinct role:

- **NV sensing** provides the measurement layer.
- **Dynamic networks** represent interactions between measured components.
- **MDNTF** analyzes how network topology changes through time and across scales.
- **Temporal feature tracking** follows the evolution of topological structures.
- **Digital Map** provides an interpretable representation of the resulting dynamics.

The architecture is designed so that alternative physical systems or measurement modalities can feed the analytical core without requiring a redesign of the underlying MDNTF framework.

---

## 12. Scope

DynoNetTopology is intended as a computational framework for studying the relationship between:

**physical dynamics → measurements → network dynamics → topology → system interpretation**

The initial brain-dynamics example serves as a demonstration of the analytical workflow. The broader architecture is intended to remain applicable to other complex physical and biological systems.

The quantum-sensing component and the MDNTF analytical component are therefore treated as modular layers rather than as a single domain-specific workflow.

---

## 13. License

This project is distributed under the license specified in [`LICENSE`](LICENSE).
