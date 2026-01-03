# Interaction Risk Model

A proximity-based interaction risk model for autonomous systems.

This project computes a **continuous, planner-friendly risk score** from relative
kinematics between an ego agent and surrounding actors. The risk signal is designed
to generalize across domains such as:

- autonomous driving (vehicle interactions, merges, intersections)
- unmanned systems and drones (deconfliction, intercept / avoid, formation spacing)
- other autonomous or adversarial multi-agent settings

The emphasis is on **geometry, relative motion, and time-bounded proximity**, rather
than on domain-specific maneuver labels.

---

## Motivation

In many autonomous systems, downstream planners and controllers do not need a hard
classification (e.g., “cut-in” vs. “not cut-in”). Instead, they benefit from a
**smooth, interpretable risk signal** that:

- increases as interaction likelihood grows
- can be thresholded or weighted in a cost function
- degrades gracefully under uncertainty
- does not require perfect ground-truth labels

This project focuses on producing such a signal.

---

## High-level approach

1. Build a per-timestep **interaction table** describing ego–actor relative motion  
2. Compute proximity and kinematic features (distance, closure, time-to-interaction)  
3. Combine these into a continuous **interaction risk score** in \[0, 1\]  
4. Evaluate the risk signal against simple near-miss or proximity-based event proxies  

The initial implementation uses nuScenes trajectory data, but the interaction
representation and risk formulation are designed to be dataset-agnostic.

---

## Planner interface (conceptual)

The risk score produced by this model is intended to be consumed by downstream logic,
for example:

- as an additive cost term in trajectory optimization
- as a gating signal for conservative or evasive behaviors
- to rank actors or time windows by interaction priority

This separation between **risk estimation** and **decision-making** mirrors common
architectures in both autonomous driving and unmanned systems.

---

## Repository status

This repository is under active development. Current focus:

- core interaction feature computation
- proximity-based risk formulation
- clean, reproducible pipeline structure

Raw datasets are not committed to the repository.
