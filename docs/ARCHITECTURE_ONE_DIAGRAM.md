# Agentic Capability Architecture — One Diagram

This diagram is an explanatory view of the current charter, not an independent architecture authority.

```mermaid
flowchart TB
    R[Required application behavior]
    A[Coding agent]

    subgraph S["Capability sources"]
      N[Native runtime / platform\nFrappe · ERPNext · framework facilities]
      E[Ecosystem / external\napps · packages · OSS · SaaS]
      ST[Standards / protocols\nexisting schema · auth · messaging · agent interfaces]
      I[Internal capability knowledge\nmanifests · interfaces · evidence]
    end

    subgraph SEL["Selection and composition"]
      Q[Precise semantic requirement]
      D[Compare candidates\nselect / reject with reasons]
      B[Honest typed public boundary]
      C[Configuration / composition]
      L[Residual project-local behavior]
      Q --> D --> B --> C --> L
    end

    subgraph RT["Runtime / infrastructure"]
      X[Existing execution facilities\npersistence · auth · scheduling · retries · messaging · transactions · observability]
    end

    subgraph EV["Evidence loop"]
      T[Tests + compatibility + real use\nfailures · rejected fits · incidents · limitations]
      M[Maturity / knowledge update\nlocal → candidate → proven → core]
      T --> M
    end

    subgraph EXP["Experimental research"]
      P[Primitive vocabulary / composition model\nprobationary; not the default runtime]
    end

    R --> A --> Q
    N --> D
    E --> D
    ST --> D
    I --> D
    L --> X
    C --> X
    X --> T
    M --> I
    P -.->|may improve planning / validation if proven| SEL

    RULE["Sourcing rule:\nnative → ecosystem → external → standards → internal → local gap"]
    A -.-> RULE
    RULE -.-> D
```

## How to read it

- **Start from required behavior, not from an internal package name.**
- **Capability sources are plural.** Native framework features, established packages/services, standards, and internal capabilities are all legitimate providers.
- **Selection is the strategic layer.** The agent should choose or reject candidates based on semantic fit, interfaces, constraints, evidence, and operational considerations.
- **Typed public boundaries** should reuse existing honest APIs/functions where possible; adapters exist for real translations, not symmetry.
- **Project-local behavior** remains first-class when abstraction would erase consequential domain meaning.
- **Runtime infrastructure** should usually be off-the-shelf/platform-native rather than rebuilt inside this repository.
- **Evidence** includes successful reuse and also failed fits, rejected providers, compatibility limits, incidents, and independent-consumer results.
- **Primitive research** is intentionally shown off the critical path. A semantic primitive may become useful planning/validation vocabulary without becoming a runtime owned here.

The intended flywheel is:

```text
real requirement
→ search all credible sources
→ select the best existing fit
→ implement only the residual local gap
→ test under real pressure
→ record success, rejection, and failure evidence
→ improve the next sourcing decision
```

The architecture is successful when agent work shifts from repeated reinvention toward reliable **discovery, selection, composition, and evidence-producing local implementation**, regardless of who owns the selected implementation.
