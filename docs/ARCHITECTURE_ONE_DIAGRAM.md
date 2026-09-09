# Agentic Capability Architecture — One Diagram

This diagram is an explanatory view of the current charter, not an independent architecture authority.

```mermaid
flowchart TB
    R[Required application behavior]
    A[Coding agent]

    subgraph S["Capability providers"]
      N[Native runtime / platform\nFrappe · ERPNext · framework facilities]
      E[Ecosystem / external\napps · packages · OSS · SaaS]
      ST[Standards / protocols\nexisting schema · auth · messaging · agent interfaces]
      I[Internal capability knowledge\nmanifests · interfaces · evidence]
    end

    subgraph SEL["Capability representation and composition"]
      Q[Precise semantic requirement]
      ID[Capability identity / contract]
      D[Resolve provider\nselect / reject with reasons]
      B[Honest typed public boundary]
      C[Explicit configuration / composition]
      L[Residual project-local behavior]
      Q --> ID --> D --> B --> C --> L
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
    I --> ID
    L --> X
    C --> X
    X --> T
    M --> I
    M --> ID
    P -.->|may improve planning / validation if proven| SEL

    RULE["Provider sourcing policy:\nconsider native / external / internal providers; off-the-shelf wins ties"]
    A -.-> RULE
    RULE -.-> D
```

## How to read it

- **Start from required behavior, not from an internal package name.**
- **Capability sources are plural.** Native framework features, established packages/services, standards, and internal capabilities are all legitimate providers.
- **Composition is the strategic target.** The architecture exists so agents can bind known capability identities to honest interfaces and combine them into new systems instead of regenerating whole applications.
- **Typed public boundaries** should reuse existing honest APIs/functions where possible; adapters exist for real translations, not symmetry.
- **Project-local behavior** remains first-class when abstraction would erase consequential domain meaning.
- **Runtime infrastructure** should usually be off-the-shelf/platform-native rather than rebuilt inside this repository.
- **Evidence** includes successful reuse and also failed fits, rejected providers, compatibility limits, incidents, and independent-consumer results.
- **Primitive research** is intentionally shown off the critical path. A semantic primitive may become useful planning/validation vocabulary without becoming a runtime owned here.

The intended flywheel is:

```text
real requirement
→ map behavior to capability identities
→ bind providers through typed interfaces
→ compose capabilities explicitly
→ implement only the residual local gap
→ test under real pressure
→ record composition, success, rejection, and failure evidence
→ strengthen the capability ecosystem for the next project
```

The architecture is successful when agent work shifts from repeated reinvention toward reliable **discovery, selection, composition, and evidence-producing local implementation**, regardless of who owns the selected implementation.
