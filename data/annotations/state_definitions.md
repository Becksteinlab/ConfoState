# ConfoState State Definitions (LeuT Dataset v0.1)

## Purpose

This document defines the conformational state vocabulary used in the initial ConfoState training dataset. These definitions are based on the LeuT structural literature and are intended to provide consistent labels for machine learning and interpretation.

---

# Outward Open

## Definition

The extracellular vestibule is open and accessible to substrate and ions from the extracellular environment. The intracellular vestibule remains closed.

## Structural Characteristics

* Extracellular gate open
* Intracellular gate closed
* Substrate may be absent or inhibitor-bound
* Sodium sites generally accessible

## Representative Structures

* 3TT1
* 3F3A

## Biological Interpretation

This state represents the substrate-recognition phase of the transport cycle where substrate and sodium ions can enter from the extracellular side.

---

# Occluded

## Definition

Both extracellular and intracellular pathways are closed while substrate remains trapped within the transporter.

## Structural Characteristics

* Extracellular gate closed
* Intracellular gate closed
* Substrate bound
* Sodium bound
* Central binding pocket occupied

## Representative Structures

* 3F3C
* 3F3D
* 3F3E
* 3F4I
* 3F4J

## Biological Interpretation

This state corresponds to an intermediate stage of transport where substrate has been captured but has not yet been released.

---

# Inward Open

## Definition

The intracellular vestibule is open to the cytoplasm while the extracellular vestibule is closed.

## Structural Characteristics

* Extracellular gate closed
* Intracellular gate open
* Cytoplasmic cavity accessible
* Sodium sites disrupted or partially disrupted

## Representative Structures

* 3TT3
* 3TU0

## Biological Interpretation

This state allows substrate and sodium release into the cytoplasm.

---

# Inward Occluded

## Definition

An inward-facing intermediate in which substrate remains trapped while intracellular release is beginning.

## Structural Characteristics

* Inward-facing geometry
* Partial intracellular opening
* Substrate remains bound
* TM5 rearrangement
* Na2 site exposed or destabilized

## Representative Structures

* 6XWM

## Biological Interpretation

This state represents a transitional intermediate between substrate-bound and fully released states.

---

# Outward Return

## Definition

A sodium-free and substrate-free state involved in resetting the transporter after intracellular release.

## Structural Characteristics

* Outward-oriented transporter
* Empty substrate-binding site
* Empty sodium sites
* Conserved Leu25 rotated into substrate pocket
* Return-transition conformation

## Representative Structures

* 5JAE
* 5JAF
* 5JAG

## Biological Interpretation

This state participates in the inward-to-outward return transition and prepares the transporter for another transport cycle.

---

# Notes

The current state definitions are specific to the LeuT training dataset and may be revised when additional transporter families are incorporated. Future versions of ConfoState may use a hierarchical state model to accommodate family-specific conformational vocabularies.
