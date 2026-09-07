# Agentic Capability Architecture — One Diagram

```mermaid
flowchart TB
    R[Real requirement]
    A[Coding agent]

    subgraph F["Federated capability commons"]
      P[Public registry]
      O[Organization registry]
      T[Team / project registry]
      P --> O --> T
    end

    subgraph K["Reusable architecture"]
      PR[Semantic primitives\nstate.transition · authorize · resolve · assign · deadline · trigger]
      C[Evidence-backed capabilities\nCore · Approvals · Notifications · Scheduling · ...]
      PR --> C
    end

    subgraph PJ["Project composition"]
      M[Typed node/port composition\n+ state/action/transition\n+ triggers/constraints]
      L[Project-local behavior\ndomain rules · schemas · fulfillment · provisioning · triage]
      M --> L
    end

    subgraph RT["Runtime"]
      AD[Implementation adapters\nFrappe · Python · APIs · databases · human/agent actions]
    end

    subgraph E["Evidence loop"]
      TEST[Tests + compatibility\nreal-runtime proofs · operations · limitations]
      PROM[Promotion review\nobserved → candidate → proven → core/canonical]
      TEST --> PROM
    end

    R --> A
    A -->|query / select / reject| T
    T --> PR
    T --> C
    A -->|compose known behavior| M
    C --> M
    PR --> M
    L --> AD
    M --> AD
    AD --> TEST
    PROM -->|strengthen metadata, interfaces, evidence| F
    PROM -->|refine reusable layer| K

    N["Decision rule:\nreuse → configure → compose → local gap"]
    A -.-> N
    N -.-> M
    N -.-> L
```

## How to read it

- **Primitives** are small semantic operations with stable execution meaning.
- **Capabilities** are evidence-backed reusable packages with interfaces, configuration, dependencies, tests, and maturity.
- **Project composition** combines reusable pieces through typed connections and explicit lifecycle/trigger semantics.
- **Project-local behavior** preserves domain meaning when generalization would erase important distinctions or increase coupling.
- **Runtime adapters** execute the plan in concrete systems; Frappe is the current substrate, not the abstract architecture.
- **Evidence** flows back from tests, real deployments, compatibility checks, failures, and independent-agent use.
- **Promotion** is evidence-based rather than automatic.
- **Federation** lets public, organizational, and project registries accumulate reusable capability without forcing one monolithic codebase.

The intended flywheel is:

```text
real project
→ discover existing capability
→ compose what fits
→ implement only local gaps
→ test under new pressure
→ contribute compatibility evidence
→ strengthen the shared commons
→ make the next project easier
```

The architecture is successful when agent work shifts from repeated reinvention toward reliable **discovery, selection, composition, and evidence-producing local implementation**.
