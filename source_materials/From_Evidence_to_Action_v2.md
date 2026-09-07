---
title: "From Evidence to Action"
subtitle: "Version 2: Vision and Implementation Blueprint for a Human-Guided, AI-Expanded Mixed-Methods Policy Analysis Workbench"
author: "Integrated strategy paper for research, product, and engineering agents"
date: "1 August 2026"
version: "2.0"
status: "Strategic synthesis and implementation blueprint"
lang: en-US
---

# Revision note

This document is a self-contained revision of the original *From Evidence to Action* vision and implementation blueprint. It preserves the original ambition—a configurable AI workbench spanning major families of policy analysis—while sharpening the strategic center of the proposal.

Version 2 makes seven clarifications explicit:

1. The central product thesis is not that AI should replace policy analysts. It is that AI can expand the **methodological bandwidth** of domain experts: the range of research designs, theories, methods, representations, and analytical alternatives they can competently consider and apply.
2. The platform does not determine ultimate political or normative correctness. Its epistemic promise is inspectable, methodologically faithful, claim-relative, revisable, and decision-useful analysis.
3. Configuration is not administrative setup. Choosing the question, evidence boundary, population, outcome, theory posture, methodological profile, assumptions, and policy criteria is substantive analytical work conducted by the analyst, often in conversation with an AI methodological generalist.
4. The preferred terminology is **declared methodological profile**, **recognized methodological sources**, **source-grounded implementation**, and **methodological lineage**. No single source is assumed to possess universal authority.
5. The Study State remains the architectural center, but it is implemented through a **federated ontology**: a small shared coordination vocabulary connected to richer method-native schemas.
6. Provenance is not merely logging or compliance. Analytical lineage makes studies cheap to inspect, revise, compare, invalidate, rerun, and reuse. It converts a static report into an evolving computational research asset.
7. The initial strategy is capability-led. The first users are policy analysts and research teams, especially in think tanks and adjacent organizations. A detailed commercialization thesis is not a prerequisite for demonstrating the capability, although real analyst workflows should constrain product design continuously.

This paper assumes competent software implementation. It records technical invariants, failure modes, schemas, and acceptance conditions because they define the product's scientific character, but it does not treat elementary implementation correctness as the central strategic question.

# Abstract

This paper presents the product vision, epistemic posture, methodological strategy, architecture, implementation sequence, and open questions for an AI-driven mixed-methods policy analysis workbench. The long-run objective is to support a substantial portion of the work performed by policy analysts: framing policy problems, finding and synthesizing evidence, applying established theories and methodologies, developing and revising theories, integrating qualitative and quantitative results, modeling possible futures, comparing policy options, and producing findings whose evidence, assumptions, transformations, and analytical lineage remain inspectable.

The central product thesis is **human-guided, AI-expanded analysis**. Domain experts possess institutional knowledge, substantive judgment, contextual understanding, and accountability that a general-purpose model does not. Large language models possess unusually broad, though fallible, knowledge across methodological traditions and can perform semantic and integrative labor at a scale impractical for most human teams. The workbench combines these strengths. The analyst frames or approves the problem, consequential assumptions, methodological stance, interpretation, and policy judgment. The AI helps formulate alternative designs, operationalize the analyst's knowledge, connect the problem to a wider repertoire of methods, process evidence, identify tensions, and propose revisions. Deterministic software, statistical packages, graph engines, and simulation runtimes execute computation, state transitions, validation, replay, and rendering.

The proposed product is not an autonomous policy oracle, a generic research chatbot, a universal prompt, or a menu of disconnected tools. It is a configurable research environment in which declared methodological profiles are represented through versioned method packs; theories can be operationalized through Theory Forge; qualitative, relational, statistical, causal, structural-equation, simulation, foresight, and decision methods retain their own semantics; and a versioned Study State connects sources, concepts, measurements, assumptions, models, findings, uncertainties, revisions, and decisions.

The platform does not claim to determine whether a political position or policy choice is ultimately correct. Policy analysis combines empirical inquiry with contested objectives, values, legal duties, distributional judgments, institutional constraints, and risk preferences. The system instead aims to make configured analyses executable, inspectable, methodologically explicit, claim-relative, and revisable. Evaluation should therefore prioritize inspectability, methodological fidelity, claim-relative warrant, decision usefulness, revision capacity, and expansion of the analyst's methodological repertoire rather than a universal measure of policy correctness.

The central architectural decision is to maintain a versioned Study State implemented through a federated ontology. A small shared coordination layer represents projects, questions, evidence, artifacts, method runs, assumptions, findings, versions, dependencies, reviews, and uncertainty. Method-native extensions retain the specialized meanings of qualitative categories, process-tracing tests, causal estimands, graph projections, latent constructs, simulation parameters, and decision models. Text, tables, graphs, vectors, causal diagrams, covariance structures, and simulation states remain fit-for-purpose representations attached to the study rather than being forced into one universal truth store.

The immediate strategy is thin-slice composition rather than speculative breadth. The platform should establish a common study, method-run, and analytical-lineage envelope around existing systems; complete the SQA Theory Quality Audit; demonstrate Theory Forge's paper-to-reusable-instrument loop; add evidence synthesis and research-design alternatives as a front door; and then prove selected seams to process tracing, graph analysis, causal analysis, measurement and SEM, simulation, and decision analysis. A coherent hero workflow should demonstrate the integrated user experience, while a fixture portfolio tests method-specific and architectural claims independently. The defining long-term advantage is **cumulative analytical capital**: every analysis should make the next analysis easier to conduct, inspect, revise, compare, and reuse.

# Executive summary

## The product promise

**Broaden the analytical repertoire of policy experts without displacing their authority.**

A concise public description is:

> An AI workbench for rigorous policy analysis. It helps analysts frame problems, review evidence, compare research designs, apply established qualitative and quantitative methods, integrate results, and produce findings whose evidence and reasoning remain inspectable.

A capability-forward description is:

> The workbench combines domain-expert judgment with an AI methodological generalist, source-grounded analytical workflows, specialized computational backends, and a persistent study state so that complex policy analysis can be conducted, revised, and reused as one connected research process.

The internal architectural description is:

> A methodology-composition runtime that maintains an evolving, source-grounded Study State while human analysts, AI agents, and computational backends configure, execute, connect, inspect, revise, and reuse method-specific analytical objects.

The public description communicates user value. The internal definition prevents the implementation from collapsing into a chatbot, monolithic ontology, or indiscriminate tool router.

## The strategic thesis

Policy analysts are usually deep specialists in a substantive domain, institution, jurisdiction, dataset, or policy process. They are rarely equally expert in systematic review, grounded theory, process tracing, causal identification, network analysis, measurement theory, structural equation modeling, simulation, forecasting, robust decision making, and policy appraisal.

Large language models have the inverse profile. They possess broad but uneven knowledge across many methodological traditions and can rapidly compare formulations, process large text corpora, translate concepts among analytical representations, and draft structured alternatives. They lack reliable institutional judgment, accountable value preferences, and the deep contextual knowledge needed to determine whether an assumption is substantively credible in a particular case.

The product opportunity lies in this complementarity:

```text
human domain expertise and accountability
+ AI methodological breadth and semantic scale
+ deterministic and specialized computation
+ persistent analytical state and lineage
= broader, faster, more revisable policy analysis
```

The AI should not merely automate clerical labor, although it will do so. Its more important role is to help a domain expert integrate their knowledge into a broader methodological repertoire than any individual analyst normally commands.

## The epistemic contract

The workbench does not determine whether Republicans, Democrats, ministries, agencies, stakeholders, or policy advocates are ultimately "right." A policy recommendation depends not only on empirical claims but also on objectives, distributional judgments, legal obligations, institutional constraints, political feasibility, and risk tolerance. Those inputs can be made explicit, compared, and analyzed; they cannot be converted into a universal objective truth by software.

The system can nevertheless make strong, bounded claims about an analysis:

- which problem and scope were configured;
- which evidence was available and excluded;
- which methodological profile was used;
- which assumptions and value criteria were introduced;
- which operations were performed;
- which method-native diagnostics succeeded or failed;
- which findings follow under the configured analysis;
- which contrary evidence, rival explanations, and non-results remain;
- which outputs became stale after a revision;
- where empirical evidence ends and policy judgment begins.

The evaluation target is therefore not ultimate policy correctness. It is:

1. **Inspectability:** the analytical chain can be examined at an appropriate level of detail.
2. **Methodological fidelity:** the declared profile is materially reflected in execution, diagnostics, stopping conditions, and interpretation.
3. **Claim-relative warrant:** each finding shows why it is supported, qualified, contradicted, unresolved, or unavailable within a stated scope.
4. **Decision usefulness:** the analysis improves understanding, reveals trade-offs, narrows uncertainty, exposes disagreements, or guides evidence acquisition.
5. **Revision capacity:** evidence, theories, codebooks, mappings, assumptions, and models can be changed without rebuilding the study manually.
6. **Methodological expansion:** the analyst can competently consider and employ perspectives that would otherwise be inaccessible or too expensive.

## Configuration is analysis

The most consequential human–AI interaction occurs before and between method runs. Configuration includes the research question, population, units, cases, time horizon, evidence boundary, outcome definition, theoretical posture, methodological profile, causal assumptions, missing-evidence treatment, policy criteria, simulation ranges, assurance profile, and stopping rules.

These are not ordinary settings. They shape what the analysis can observe and conclude. The analyst may set them directly or develop them through conversation with a state-of-the-art policy-analysis agent. The agent should propose two to four coherent research designs rather than one supposedly correct method. Each alternative should state its rationale, source lineage, evidence requirements, assumptions, outputs, branch points, resource implications, and limitations.

The analyst retains authority to accept, modify, combine, reject, or replace those alternatives. Review may be optional at many stages, but epistemic status is not optional: automatically generated, unreviewed, reviewed, disputed, accepted, rejected, and superseded outputs must remain distinguishable.

## What is distinctive

No individual component constitutes the product. Literature review systems, qualitative coding tools, statistical packages, graph engines, causal libraries, SEM software, simulation frameworks, and report generators already exist. The distinctive bet is their integration through six capabilities:

1. **Methodological operationalization.** Recognized methodological sources are transformed into explicit, versioned profiles and method packs whose requirements materially affect execution.
2. **Persistent analytical state.** Evidence, concepts, theories, measurements, assumptions, claims, models, findings, uncertainties, and open questions persist across methods.
3. **Productive provenance.** Source bindings, transformations, versions, dependencies, and review decisions make the analysis revisable rather than merely auditable.
4. **Cross-method translation without semantic erasure.** A qualitative proposition, graph observable, causal estimand, latent construct, simulation parameter, or decision criterion can be connected while retaining its method-specific meaning and inferential limits.
5. **Cheap revision and multiverse analysis.** Alternative defensible configurations can be executed and compared; upstream revisions can invalidate and selectively rebuild downstream results.
6. **Cumulative analytical capital.** Reusable evidence maps, operationalized theories, codebooks, instruments, mappings, method configurations, models, and validated transformations reduce the cost and improve the quality of future studies.

## The central architectural decision

The universal center is a **versioned Study State**, not a graph, vector store, assertion ledger, report, or LLM conversation. The Study State is the evolving index of the investigation: its questions, design, evidence, concepts, measurements, methods, models, findings, uncertainty, revisions, and next actions.

The Study State uses a federated ontology:

- a shared coordination layer represents common lifecycle and lineage objects;
- a thin cross-method layer represents scoped questions, assumptions, findings, uncertainty, and decisions;
- method-native schemas preserve specialized scientific meanings.

The graph platform remains strategically important for relational evidence, retrieval and navigation, dependency lineage, and graph-native analysis. It is not a compulsory gateway for methods whose natural authority is source text, a table, a qualitative memo system, a process-tracing ledger, a covariance structure, or a simulation state.

## Provenance as productive infrastructure

Basic logging records what executed. The workbench requires analytical lineage: a structured account of how source material, observations, interpretations, assumptions, mappings, methods, and models produced a result.

This distinction matters when a category is split, a theory operationalization changes, new evidence appears, a graph projection is revised, a causal assumption is challenged, or a simulation parameter range changes. The system should identify which findings depend on the changed object, which outputs are stale, what must be rerun, what survives, and why the new result differs.

Provenance therefore enables:

- source-to-finding inspection;
- finding-to-source reconstruction;
- selective invalidation and rerun;
- comparison of alternative configurations;
- reuse of validated analytical assets;
- regeneration of multiple outputs from one study state.

The strategic formulation is:

> Provenance converts policy analysis from a static report into a revisable computational research asset.

## Program boundaries

Four connected responsibilities should remain distinct:

- **The policy-analysis workbench** owns the user experience, policy and research framing, design alternatives, project configuration, method composition, integration, and policy-facing synthesis.
- **The governed knowledge-analysis substrate** owns source identity, exact source windows, durable artifact versions, generic lineage, derivation, replay, and—in later secure deployments—authorization and rights propagation.
- **Method-specific systems** own scientific semantics: theory operationalization, qualitative coding, process tracing, graph construction, causal identification, measurement validity, simulation specification, diagnostics, and method-native conclusions.
- **The agentic engineering control plane** owns orchestration, budgets, retries, checkpoints, traces, model and tool invocation, and escalation. It does not decide whether a substantive conclusion or policy recommendation is warranted.

## Initial users and development posture

The initial users are policy analysts and research teams, particularly in think tanks and adjacent research organizations. The program is capability-led: it is reasonable to demonstrate the analytical capability before establishing a complete commercialization, procurement, or deployment thesis.

However, the capability should be developed against real analyst work rather than an abstract catalogue of methods. A coherent hero workflow should supply the product narrative. Small controlled fixtures should test individual methods, transformations, and failure states. Detailed enterprise security is outside the scope of a public or synthetic single-user demonstration, although stable artifact boundaries and lineage should avoid gratuitously foreclosing later secure deployment.

## Immediate implementation strategy

The recommended order remains a sequence of vertical composition seams:

1. Common `StudyState`, `MethodRun`, artifact, version, lineage, and review envelope.
2. SQA proposition-relative Theory Quality Audit.
3. Theory Forge paper-to-schema-to-rerunnable-module vertical.
4. Evidence-synthesis and research-design front door.
5. One mixed-method seam: graph plus qualitative interpretation or SQA to process tracing.
6. One causal-analysis path from DAG and estimand through identification, estimation, and refutation.
7. One construct-to-measurement-to-SEM path.
8. One theory-and-evidence-to-simulation path using an accepted model-description profile.
9. One policy-appraisal and decision path.
10. A second-project proof and, only after repeated needs appear, a method-pack authoring workflow.

One study should not be forced through every method. Integration value and method rigor require different demonstrations.

## The governing principle

> **Every analysis should make the next one easier.**

# Part I. Strategic foundation

# 1. Purpose, status, and reading instructions

## 1.1 Purpose

This paper provides a coherent basis for discussing, reviewing, designing, and implementing an AI-driven mixed-methods policy analysis workbench. It is intended to be sufficiently self-contained for:

- a fresh research or planning agent evaluating the strategic vision;
- a product or policy-analysis expert assessing the proposed human–AI workflow;
- an architect examining program boundaries, ontology, lineage, and composition;
- a coding agent planning interfaces, implementation slices, dependencies, and acceptance criteria.

It consolidates the original *Evidence to Action* vision with project directions concerning SQA, grounded theory, Theory Forge, governed knowledge analysis, graph systems, process tracing, computational social science, causal analysis, measurement, simulation, and policy decision support. Version 2 also incorporates subsequent strategic clarification concerning epistemic modesty, methodological breadth, configuration, provenance, ontology, and capability-led development.

## 1.2 Status and non-authority

This is a strategy and architecture paper. It is not:

- an executable roadmap;
- a source of current repository or implementation status;
- authorization to merge, rename, or replace any existing system;
- evidence that the complete product has been validated;
- a claim that every proposed method family belongs in the first product.

Mutable facts about what is built, merged, blocked, or planned must be checked against current repositories and approved plans.

## 1.3 Content classes

The paper distinguishes four kinds of statements:

- **Existing direction:** propositions already present in the supplied project documents or explicitly established by the project owner.
- **Strategic clarification:** later statements that sharpen the intended product thesis or reject a misleading interpretation.
- **Synthesis:** an interpretation connecting multiple project directions into a broader architecture.
- **Recommendation:** a proposed design, implementation order, contract, or evaluative criterion requiring review before adoption.

A reviewer should challenge the synthesis and recommendations rather than treating them as settled requirements.

## 1.4 Review posture

The primary review questions are strategic:

- Is the human–AI complementarity coherent and valuable?
- Is the epistemic promise appropriately bounded?
- Does configuration correctly occupy the center of the analyst interaction?
- Can a Study State and federated ontology compose heterogeneous methods without erasing their meanings?
- Does analytical lineage create durable advantage or merely infrastructure burden?
- Is the long-run scope coherent even if implementation remains thin-sliced?
- Does the proposed sequence prove the central thesis efficiently?
- Which assumptions, contradictions, or missing alternatives would materially weaken the vision?

The review should assume competent implementation of ordinary software requirements. Technical defects remain relevant where they reveal a strategic contradiction—for example, when a proposed common schema cannot preserve a method's semantics—but basic assertions such as "the system must calculate metrics correctly" are not the principal subject of the vision review.

## 1.5 Terminology posture

The paper uses the following preferred terms:

- **Declared methodological profile:** a coherent, explicit implementation of one recognized method tradition or a justified hybrid.
- **Recognized methodological source:** a respected handbook, standard, framework, textbook, protocol, or scholarly source informing the profile.
- **Source-grounded implementation:** an implementation whose steps, choices, diagnostics, outputs, and interpretation limits materially reflect identified sources.
- **Methodological lineage:** the record connecting source statements, platform interpretations, implementation choices, method-pack versions, and actual method runs.
- **Warrant:** the evidence- and method-specific basis that licenses a claim within a stated scope.
- **Federated ontology:** a small shared vocabulary connected to specialized method-native vocabularies rather than one universal semantic schema.

The term "authority" may still appear where discussing an issuing institution or authoritative source record, but the product does not assume a single final methodological authority.

# 2. Product thesis and positioning

## 2.1 Primary user-facing description

> An AI workbench for rigorous, mixed-method policy analysis.

Expanded:

> The workbench helps policy analysts frame questions, review evidence, compare research designs, apply recognized qualitative and quantitative methods, integrate results, and produce findings that remain linked to their sources, assumptions, and analytical reasoning.

Analyst-centered:

> The system gives domain experts access to a broader methodological repertoire by combining their substantive judgment with an AI methodological generalist, specialized analytical software, and a persistent, revisable study state.

## 2.2 Internal product definition

Internally, the system is a **methodology-composition runtime** (an environment that executes and connects configured research methodologies). It maintains an evolving Study State while analysts, AI agents, deterministic software, and specialized backends apply and connect method-specific procedures.

This definition is more accurate than "computational policy analysis" because major portions of policy research are interpretive, qualitative, participatory, institutional, historical, or judgment-dependent. A method run may include:

- LLM-mediated semantic work;
- deterministic transformations;
- statistical estimation;
- graph computation;
- simulation execution;
- human interpretation or review;
- new data collection;
- external fieldwork or stakeholder engagement.

The runtime coordinates these activities without treating them as semantically interchangeable.

## 2.3 Primary unit of value

The primary unit of value is not an isolated chatbot answer or generated report. It is:

> **A reusable, source-grounded analytical configuration whose evidence, methods, assumptions, findings, and revision history persist as an evolving study asset.**

A completed report is one rendering of that asset. Other renderings may include a technical appendix, evidence map, policy brief, theory schema, model card, decision matrix, or evidence-acquisition agenda.

This framing has several consequences:

- analysis should survive beyond its presentation;
- revisions should update dependent objects rather than require manual reconstruction;
- a validated theory module, codebook, construct specification, graph projection, causal design, or simulation calibration can become reusable capital;
- the system's value compounds across projects rather than ending when a report is delivered.

## 2.4 Intended long-run scope

The long-run product boundary includes major families of policy research:

- policy framing, institutional analysis, and stakeholder analysis;
- systematic, rapid, scoping, living, and other evidence syntheses;
- interviews, focus groups, ethnography, case studies, content analysis, framework analysis, grounded theory, and Delphi methods;
- sampling, survey design, questionnaire development, and measurement;
- descriptive statistics, regression, experiments, quasi-experiments, causal inference, time series, prediction, and forecasting;
- process evaluation, outcome evaluation, impact evaluation, and implementation analysis;
- process tracing and comparative case methods;
- social network, relational, spatial, and temporal analysis;
- structural equation modeling and latent-variable analysis;
- agent-based modeling, system dynamics, microsimulation, discrete-event simulation, and Monte Carlo analysis;
- scenario analysis, horizon scanning, foresight, and exploratory modeling;
- robust decision making, cost-benefit analysis, cost-effectiveness analysis, MCDA, value of information, and uncertainty analysis;
- wargaming, tabletop exercises, participatory analysis, and stakeholder engagement.

This is a strategic boundary, not an instruction to implement all families before demonstrating value. The architecture should remain open to this range while generalizing only from exercised implementations.

## 2.5 Non-goals

The platform is not intended to:

- replace policy experts or accountable decision makers;
- decide which political ideology or policy objective is ultimately correct;
- collapse contested objectives and values into a hidden optimization target;
- claim one universally correct research design for every policy problem;
- collapse all methodologies into a universal prompt, graph, ontology, or confidence score;
- force every project through qualitative coding, a graph, causal analysis, SEM, simulation, or decision analysis;
- treat execution success, schema validity, provenance completeness, or source citation as proof that a substantive conclusion is true;
- obscure the analyst's framing choices behind an apparently objective configuration;
- make all projects autonomous or require human approval for every low-risk operation;
- rebuild mature numerical estimators where inspectable software already exists;
- treat evidence used to formulate a theory as independent confirmation of that theory;
- claim logically exhaustive interpretation or perfect evidence coverage;
- require a complete enterprise deployment or commercialization thesis before demonstrating the capability.

## 2.6 Initial audience and capability-led development

The initial audience consists of policy analysts and research teams, especially in think tanks and adjacent organizations conducting source-intensive, mixed-method, or repeatedly updated work.

The development posture is capability-led. The program may reasonably build and demonstrate a valuable analytical capability before determining its final market packaging, procurement route, or institutional operating model. First-principles value exists if the system can materially expand analyst capability, reduce mechanical labor, improve revision, and preserve analytical state.

Capability-led development does not imply building in isolation from users. Real analyst projects should constrain the demonstration, expose missing assumptions, and prevent the architecture from becoming an abstract catalogue of methods. The relevant distinction is:

- **not required now:** a complete business plan, pricing model, market-size estimate, or enterprise sales process;
- **required now:** a coherent analyst workflow, a credible user interaction, and evidence that the capability performs a valuable analytical function.

# 3. The policy-analysis opportunity

## 3.1 The structure of policy-analysis labor

Policy analysis combines at least five forms of work:

1. **Semantic labor:** reading evidence, identifying concepts, classifying passages, comparing accounts, extracting assumptions, and connecting claims.
2. **Procedural labor:** following review protocols, recording screening decisions, maintaining codebooks, enforcing dependencies, and documenting exclusions.
3. **Computational labor:** estimating models, querying graphs, running simulations, calculating costs, and performing sensitivity analysis.
4. **Integrative labor:** translating among methods, reconciling units and definitions, synthesizing findings, and maintaining an overall argument.
5. **Judgment:** defining the real problem, choosing scope, assessing institutional context, selecting assumptions, interpreting ambiguity, engaging stakeholders, and advising decision makers.

Large language models are unusually useful for semantic and integrative labor. Conventional software is stronger for procedural and computational labor. Human experts remain indispensable for contextual judgment, accountable configuration, interpretation, and policy choice.

## 3.2 Why domain expertise and methodological breadth are complementary

A policy analyst may know the institutional setting, relevant actors, legal framework, political constraints, administrative data, historical sequence, and practical meaning of a result. That expertise is deep but necessarily bounded.

An LLM can draw upon a broad repertoire of methodological concepts, canonical procedures, analytical analogies, and research-design patterns. It can propose that an apparent descriptive question contains a process-tracing problem, that a qualitative category may require a measurement-development path before quantification, that a graph community needs substantive validation, or that a decision problem may require robust rather than expected-value optimization.

The LLM's breadth is useful but not self-validating. Its recommendations should be grounded in declared methodological profiles, made explicit as alternatives, and open to modification. The product claim is not that the model knows the correct method. It is that it can present a wider, more structured, and more methodologically literate choice set than most individual analysts can produce unaided.

## 3.3 Current workflow fragmentation

Policy research commonly fragments the analytical loop across:

- document repositories;
- literature-review software;
- spreadsheets;
- qualitative coding systems;
- statistical scripts;
- graph notebooks and databases;
- causal diagrams;
- simulation files;
- presentation decks;
- informal notes and email discussions.

The resulting defects include:

- evidence copied out of context;
- inconsistent identifiers across tools;
- theory definitions separated from variables or observations claimed to represent them;
- undocumented transformations from text to tables, graphs, or model parameters;
- analyses that cannot be rerun after a codebook, assumption, or evidence boundary changes;
- negative evidence and failed analyses omitted from final reports;
- repeated manual reconciliation of method outputs;
- polished conclusions whose evidentiary chain is expensive to inspect;
- projects that terminate as dead reports rather than reusable research assets.

Real analysis loops around an evolving information state. Most current tools flatten that loop into disconnected outputs.

## 3.4 Comparative advantage over ordinary human-only workflows

The objective is not perfect analysis. No human or machine system can guarantee that every relevant interpretation, mechanism, dataset, or policy consequence has been discovered. The target is **bounded optimality** (the strongest achievable analysis under real constraints of time, budget, evidence, and expertise).

An AI-assisted workflow can improve bounded analysis by enabling:

- processing of every designated source unit rather than informal sampling;
- consistent application of one approved coding or theory scheme across a large corpus;
- corpus-wide reapplication after a codebook or operationalization changes;
- systematic checking of declared rivals, exceptions, and contrary evidence;
- comparison of many defensible configurations or specifications;
- automatic retention of source passages, transformations, and intermediate objects;
- explicit display of disagreements, uncertain mappings, and missing evidence;
- regeneration of outputs for different audiences from one study state;
- reuse of approved analytical instruments and transformations.

The primary value proposition is therefore not "AI writes reports." It is:

> **AI expands the analyst's methodological reach and makes source-grounded analysis cheaper to conduct, revise, inspect, and reuse.**

## 3.5 The analyst is not a ceremonial reviewer

The human role is not merely to approve machine output after execution. The analyst contributes throughout the lifecycle:

- defining or revising the policy question;
- supplying institutional and domain context;
- selecting among research designs;
- judging whether assumptions are substantively credible;
- resolving contested interpretations;
- identifying missing stakeholders, mechanisms, and consequences;
- deciding whether a methodological profile fits the actual problem;
- determining how empirical findings relate to normative or political judgment;
- deciding whether to review, revise, reject, externally critique, or use the result.

The platform should reduce low-value administration without concealing high-value judgment.

# 4. Epistemic posture and evaluative target

## 4.1 Why ultimate policy correctness is not the target

Policy analysis frequently addresses chaotic, adaptive, institutionally mediated systems. Outcomes depend on feedback, strategic behavior, path dependence, measurement limitations, incomplete evidence, and changes induced by the policy itself. Even when empirical claims can be evaluated, policy choices also depend on contested values and objectives.

A system cannot determine one universal answer to questions such as:

- how much liberty should be traded for security;
- which distributional effects are acceptable;
- which stakeholder interests deserve priority;
- whether near-term cost is justified by long-term resilience;
- whether one political conception of fairness should prevail over another.

These are not merely unresolved calculations. They involve normative and institutional judgment.

The workbench should therefore reject the posture of an automated policy oracle. It should make empirical evidence, assumptions, alternatives, trade-offs, and value inputs explicit so that accountable humans can reason about them.

## 4.2 Bounded evaluability remains possible

Rejecting ultimate policy correctness does not imply that every analytical proposition is indeterminate. The system should preserve lower-level correctness and methodological requirements as implementation invariants:

- source claims should match the source;
- computations should execute correctly;
- evidence should address the proposition rather than merely share its topic;
- causal conclusions should not exceed identification assumptions;
- simulations should report the implemented model rather than an invented narrative;
- upstream revisions should invalidate the dependent outputs they actually affect.

These requirements matter because inspectable error is still error. They are necessary conditions for the strategic promise, but they are not its central differentiator.

## 4.3 Methodological fidelity

**Methodological fidelity** means that the analysis materially follows its declared methodological profile. A recognized source is not decorative. It should affect:

- applicability conditions;
- configuration questions;
- units and evidence requirements;
- procedure order and dependencies;
- analyst choices;
- diagnostics and negative checks;
- stopping and failure states;
- outputs and interpretation limits;
- reporting requirements;
- assurance expectations.

A generic prompt with a prestigious citation is method laundering, not methodological implementation.

## 4.4 Claim-relative warrant

A finding should expose the basis that licenses the claim within its scope. Different methods produce different warrant:

```text
Qualitative fit: broad across sampled roles; two qualifying cases
Process mechanism: two links observed; one unresolved
Causal identification: conditional on declared no-unmeasured-confounding assumptions
Measurement: metric invariance supported; scalar invariance unresolved
Simulation robustness: preferred option succeeds in 78% of tested futures
Distributional evidence: weak for rural subgroups
Policy judgment: depends on equity weight and implementation-risk tolerance
```

The platform may summarize these dimensions, but it should not collapse them into a universal scalar such as `confidence = 0.82`.

## 4.5 Inspectability as practical explanation

The system cannot provide a reliable hidden chain of thought from an LLM. It can offer a more useful form of explanation:

- what evidence was available;
- what configuration was selected;
- which methodological profile and sources were used;
- which structured observations and transformations were produced;
- which assumptions were introduced;
- which alternative interpretations or specifications were considered;
- what diagnostics, failures, and reviews occurred;
- how a finding traces to source material and method-native outputs.

This is inspectable analytical provenance rather than model introspection.

## 4.6 Discovery, revision, and evaluation evidence

Each theory, hypothesis, or model should record:

- evidence visible during initial formulation;
- evidence used during material revision;
- evidence reserved for evaluation;
- evidence introduced later;
- the declared design: exploratory full-corpus exposure, discovery/evaluation split, sequential new-data evaluation, external evaluation, or another explicit posture.

This prevents same-corpus theory generation from being presented as independent confirmation. It does not prohibit exploratory analysis; it labels the result correctly.

## 4.7 Non-results are legitimate outputs

A method run may produce:

- a supported finding;
- a narrow or qualified finding;
- an unresolved result;
- a failed measurement model;
- an unidentified causal effect;
- an unsupported semantic mapping;
- a simulation that cannot be calibrated;
- a recommendation for new evidence;
- an explicit disagreement among analysts or profiles.

The workbench should preserve these states rather than force every run into a polished conclusion.

## 4.8 Evaluation criteria

The platform should be evaluated primarily on:

- inspectability;
- methodological fidelity;
- claim-relative warrant;
- decision usefulness;
- revision and replay capacity;
- methodological expansion;
- source fidelity and consequential-omission control;
- analyst effort and correction burden;
- preservation of contrary evidence and non-results;
- reuse across projects.

The relevant question is not "Did the system discover the objectively correct policy?" It is:

> Did the workbench help an analyst conduct a broader, more explicit, better-grounded, more revisable, and more useful analysis than the analyst could reasonably have produced with ordinary tools under the same constraints?

# 5. Configuration as the central human–AI interaction

## 5.1 Configuration choices are substantive analytical decisions

Configuration includes:

- the policy or research question;
- decision context and intended user;
- population, units, cases, and time horizon;
- evidence included, excluded, or collectable;
- outcomes and target quantities;
- research stance and theory posture;
- methodological profile;
- causal, measurement, or model assumptions;
- treatment of missing and conflicting evidence;
- policy criteria, stakeholder values, and distributional concerns;
- simulation ranges and deep uncertainties;
- review, assurance, and stopping rules.

These choices determine what the analysis can observe, what it can claim, and what remains outside scope. They must not be hidden as ordinary software settings.

## 5.2 Collaborative configuration

The analyst may configure the study directly or develop the configuration in conversation with the AI. A strong interaction proceeds as follows:

```text
analyst states the policy problem and contextual knowledge
-> AI elicits missing scope, decision, evidence, and consequence information
-> AI proposes alternative problem formulations and research designs
-> analyst supplies institutional corrections and preferences
-> AI maps the selected design to declared methodological profiles
-> analyst approves, edits, combines, or rejects the configuration
-> system freezes a versioned design and begins execution
```

The AI should reduce the need for a novice to know method names. It should translate substantive aims into methodological alternatives.

Instead of asking only:

> Which estimator do you want?

it should ask:

> Are you trying to describe a pattern, explain a mechanism, estimate an intervention effect, predict an outcome, compare implementation strategies, or explore robust actions under uncertainty?

## 5.3 Design alternatives, not one recommendation

The front door should present two to four coherent research-design alternatives. Each alternative should include:

- problem formulation;
- governing question and intended claim type;
- rationale;
- declared methodological profiles and source lineage;
- methods and sequence;
- evidence requirements;
- consequential assumptions;
- expected outputs;
- branch points and stopping rules;
- resource and time implications;
- limitations and claims the design cannot support.

The analyst may accept, revise, combine, or replace them. The alternatives themselves become part of the Study State so that the selected configuration is not mistaken for the only possible framing.

## 5.4 Configuration laundering

A formal workflow can make contestable framing choices appear objective. This is **configuration laundering**: subjective or politically consequential choices acquire false neutrality because they are encoded in schemas and executed consistently.

Mitigation requires preserving:

- alternatives considered;
- reasons for selection;
- analyst edits and overrides;
- consequential inclusions and exclusions;
- assumptions introduced;
- methodological profiles considered and rejected;
- sensitivity to plausible alternative configurations.

A rigorously executed analysis can still answer the wrong question. The system should make that possibility inspectable.

## 5.5 Analyst authority and review status

The analyst retains authority over:

- problem framing;
- methodological stance;
- substantive theory;
- units, populations, cases, and outcomes;
- consequential assumptions and scope conditions;
- interpretation of anomalies and contested evidence;
- stakeholder values and institutional context;
- acceptance, revision, rejection, or external critique of outputs;
- policy judgment and communication.

Review should be configurable. The system should not require human approval for every low-risk semantic operation. Nor should it represent an automatically generated consequential finding as reviewed merely because execution completed.

Output states may include:

- generated;
- unreviewed;
- reviewed;
- accepted;
- disputed;
- revised;
- rejected;
- superseded.

## 5.6 Automation profiles

The workbench should support coherent automation profiles rather than hundreds of independent switches:

- **Autonomous within fixed boundaries:** the system executes a predefined design and escalates declared exceptions.
- **Checkpoint review:** the system pauses at consequential design, mapping, or interpretation stages.
- **Analyst in the loop:** the analyst collaborates throughout the workflow.
- **Analyst-led assistance:** the system performs bounded tasks under explicit analyst direction.

The same project may use different profiles for different method nodes.

## 5.7 Configuration multiverse

Where multiple configurations are defensible, the system should support **multiverse analysis** (systematic comparison of plausible analytical choices). Examples include:

- alternative codebooks;
- competing theory operationalizations;
- different graph projections;
- alternative causal specifications;
- multiple measurement models;
- competing simulation structures or parameter ranges;
- different policy-criterion weights.

The objective is not to overwhelm the analyst with every logically possible configuration. It is to expose consequential sensitivity and identify findings that survive across defensible alternatives.


# Part II. Methodological and analytical design

# 6. Core design principles

## 6.1 Every analysis should make the next one easier

The enduring residue of a project should include more than its final report. It should preserve:

- evidence and exact source bindings;
- structured observations and interpretations;
- theories and operationalizations;
- methodological profiles, configurations, and parameters;
- measurements and models;
- findings, limitations, and non-results;
- unresolved questions and evidence gaps;
- reusable instruments, codebooks, mappings, and validated transformations;
- revision history and review decisions.

These assets constitute **cumulative analytical capital**: reusable research objects that reduce the cost and increase the quality of later analysis.

## 6.2 Questions shape representations

The same evidence can support different analytical ambitions:

- **Describe:** What actors, events, relationships, patterns, distributions, and changes are present?
- **Explain:** What mechanisms, processes, conditions, or rival accounts might explain them?
- **Predict:** What future or unobserved states are plausible, and with what uncertainty?
- **Evaluate interventions:** What changes under a specified action or condition?
- **Decide:** Which action is preferable or robust given objectives, trade-offs, constraints, and values?

Higher ambitions generally require stronger assumptions and richer representations. Prediction requires temporal structure. Intervention analysis requires causal structure. Decision analysis requires explicit objectives and value judgments. A graph may be essential for a relational question and irrelevant for a descriptive policy-framing table.

The system should therefore select representations from the question and method rather than from available infrastructure.

## 6.3 Methods retain their own meanings

A qualitative contradiction, a process-tracing hoop test, a regression coefficient, a graph residual, a failed measurement model, a simulation vulnerability region, and an MCDA trade-off are not interchangeable forms of evidence strength.

They may appear in one joint display, but each must retain:

- its method of production;
- its unit and scope;
- its assumptions;
- its diagnostics;
- its limitations;
- the claims it can and cannot support.

## 6.4 Analytical authority is partitioned

Different artifacts answer different questions:

- source bytes and exact windows are authoritative for what a source contained;
- method-native observations are authoritative for what a declared observation procedure recorded;
- reviewed interpretations are authoritative only for their recorded review state and scope;
- projection manifests are authoritative for how a representation was produced and what it lost;
- method runs and model outputs are authoritative for what the configured computation produced;
- findings are analytical interpretations with stated method, scope, warrant, and review status;
- policy recommendations add objectives, values, institutional judgment, and decision criteria.

No layer inherits the authority of another merely because they are connected. A faithfully executed model does not prove its assumptions. A source citation does not prove the cited passage supports the final claim. A reviewed interpretation does not become raw evidence.

## 6.5 Configurability should be coherent

Configurability should operate through profiles, dependencies, and visible consequential choices rather than hundreds of unrelated switches.

The principal configuration layers are:

- project purpose and decision context;
- research stance and theory posture;
- evidence and sampling strategy;
- method-family profile;
- automation and review profile;
- assurance profile;
- reporting and audience profile.

The AI may propose defaults and explain trade-offs. The effective configuration must remain inspectable and versioned.

## 6.6 Failures and non-results are first-class

Method packs should define explicit failure and non-result states. A method is not credible if it can only return success. Unidentified effects, failed models, unresolved evidence, rejected mappings, and recommendations for new data should be preserved as useful outputs.

## 6.7 Revision should be cheap but not silent

The workbench should make it inexpensive to revise:

- a question or scope;
- a codebook or qualitative category;
- a theory schema;
- a graph construction rule;
- a causal DAG or estimand;
- a measurement model;
- a simulation parameter or mechanism;
- a decision criterion or weight.

Revisions create new versions, invalidate affected downstream objects, and produce a result diff. They do not silently overwrite the previous study.

## 6.8 Progressive disclosure

The system may maintain detailed provenance and methodological structure without forcing the analyst to administer it manually. The AI copilot and deterministic runtime should capture routine metadata automatically.

The user interface should expose:

- simple summaries by default;
- consequential assumptions and review decisions at the point of choice;
- deeper lineage, diagnostics, and source detail on demand;
- explicit warnings when an output's warrant or review state is weak.

The analyst should not have to reconcile identifiers, maintain dependency graphs, or manually propagate staleness during ordinary use.

# 7. Declared methodological profiles and source-grounded implementation

## 7.1 Why methodological profiles are necessary

There is no universal meta-methodology that selects one correct method for every policy problem. Research traditions differ in their purposes, assumptions, units, evidentiary standards, and interpretive limits.

The workbench should therefore maintain declared methodological profiles. A project should be able to answer:

- What tradition or hybrid is being used?
- Which recognized sources informed it?
- Which parts of those sources were interpreted as required, recommended, optional, or explanatory?
- How did the platform translate those statements into execution?
- Which choices were left to the analyst?
- Where do legitimate alternatives exist?

The purpose is not to invoke prestige. It is to make the platform's methodological choices explicit, contestable, and traceable.

## 7.2 A starter methodological source stack

A project may draw from several layers:

| Layer | Question governed | Illustrative sources |
|---|---|---|
| General policy analysis | How is a policy problem framed, structured, and communicated? | Bardach and Patashnik; Weimer and Vining; CDC Policy Analytical Framework |
| Policy appraisal | How are objectives, options, costs, benefits, risks, distribution, and delivery assessed? | HM Treasury Green Book; Five Case Model |
| Evaluation | How should an intervention be scoped, designed, evaluated, learned from, and communicated? | HM Treasury Magenta Book and supplementary guidance |
| Evidence synthesis | How are studies searched, screened, appraised, and synthesized? | Cochrane or Campbell methods; PRISMA for reporting |
| Mixed methods | How are qualitative and quantitative components connected? | NIH/OBSSR guidance; established mixed-methods texts |
| Analytical assurance | How much verification, validation, documentation, and independent review are proportionate? | AQuA Book and domain quality-assurance standards |
| Specific method | How should grounded theory, process tracing, causal inference, SEM, RDM, ABM, or another method be conducted? | Method-specific canonical and contemporary sources |
| Domain and jurisdiction | What substantive, legal, ethical, and reporting rules apply? | Domain standards, agency guidance, law, and client requirements |

This is a starter architecture, not a universal list. A U.S. health project, a UK infrastructure appraisal, and a defense study will use different profiles.

## 7.3 Separate source, interpretation, and implementation

Each methodological requirement should preserve three layers:

1. **Source statement:** the actual passage or bounded source location.
2. **Platform interpretation:** the meaning assigned to that statement for the profile.
3. **Implementation decision:** the schema field, procedure node, diagnostic, stopping state, or reporting rule controlled by the interpretation.

This separation prevents the platform from claiming that its implementation is directly dictated by a source when substantial interpretive choices were made.

## 7.4 Methodological source records

A Methodological Source Registry should record:

- title, authors or issuing body, edition or version, publication date, and jurisdiction;
- method family and intended scope;
- exact source locations for material statements;
- statement force: required, recommended, optional, rationale, example, or unresolved;
- the platform's interpretation;
- which profile fields and procedure nodes the interpretation controls;
- known competing interpretations;
- licensing and access conditions;
- supersession, review, and expiration dates.

The interface should support a "Why this step?" view linking a workflow action to its methodological source, interpretation, and implementation consequence.

## 7.5 Multiple traditions and justified hybrids

Recognized methods often contain legitimate variants:

- grounded theory includes classical, Straussian, constructivist, and other traditions;
- causal inference can be organized around potential outcomes, structural causal models, design-based approaches, or combinations;
- SEM includes different estimation, measurement, and score-interpretation traditions;
- evidence synthesis varies by question, evidence type, and purpose;
- policy appraisal differs across institutions and jurisdictions.

The workbench should represent these differences as explicit profiles. It may support a hybrid, but the hybrid should state:

- which traditions are combined;
- where their assumptions are compatible or in tension;
- what the combination changes;
- which parts are platform-created choices.

A configurable system should not become a methodological buffet in which convenient procedures are silently selected from incompatible traditions.

## 7.6 Sources must materially change execution

A profile is source-grounded only if its sources constrain execution. At minimum, they should affect:

- questions the method can and cannot answer;
- applicability and exclusion conditions;
- evidence, unit, population, and temporal requirements;
- required procedure order and dependencies;
- analyst decisions and defaults;
- diagnostics, adversarial checks, and robustness procedures;
- stopping, failure, and non-result conditions;
- output contracts;
- interpretation limits;
- reporting requirements;
- assurance expectations.

## 7.7 Profile maturity

Methodological profiles and method packs should progress through maturity states:

- conceptual;
- executable;
- exercised on a fixture;
- reviewed for methodological fidelity;
- integrated with another method;
- reused on a second project;
- maintained under source and backend change.

A profile should not be presented as production-ready merely because a schema compiles.

## 7.8 Profile drift

Recognized sources, software backends, and disciplinary conventions change. The platform should version:

- source records;
- profile interpretations;
- method-pack implementations;
- backend adapters;
- run configurations.

A source update should trigger review rather than silently changing existing analysis. Historical runs retain the versions under which they were produced.

# 8. Composable methodologies

## 8.1 Five distinct abstractions

The implementation should distinguish:

| Layer | Definition | Example |
|---|---|---|
| **Methodological profile** | A declared version of a recognized methodological tradition or justified hybrid | Constructivist grounded theory; design-based difference-in-differences |
| **Methodology** | The research logic and procedure | Grounded theory; process tracing; difference-in-differences |
| **Method pack** | A versioned executable specification | Inputs, decisions, task graph, diagnostics, outputs, interpretation rules |
| **Operator** | One bounded analytical action | Code a passage; estimate a regression; detect communities |
| **Backend** | Software or human capability executing an operator | SQA; an LLM; NetworkX; R/lavaan; DoWhy; Mesa; expert review |

Community detection is an operator. A credible network study requires a valid network definition, research question, structural measures, comparison logic, assumptions, and interpretation.

## 8.2 The method pack

A method pack should contain:

- identity, version, family, aliases, profile, and maturity;
- recognized methodological sources and interpretation mappings;
- questions it can and cannot answer;
- applicability and exclusion conditions;
- required and optional inputs;
- unit, population, temporal, and evidence requirements;
- configuration schema and defaults;
- substantive and methodological assumptions;
- a procedure DAG (directed acyclic graph of tasks and dependencies), with loops and branches represented explicitly where needed;
- task roles: LLM, deterministic software, specialized backend, human analyst, reviewer, data collector, or external service;
- diagnostics, robustness checks, and adversarial tests;
- stopping, failure, and non-result conditions;
- outputs and interpretation rules;
- upstream and downstream integration ports;
- reporting standards;
- fixtures, golden cases, negative cases, ambiguous cases, and corruption tests.

## 8.3 Semantic composability

The meaning of a transferred object must be explicit. A qualitative category called "trusted intermediary" cannot silently become a graph variable called `brokerage_score`.

The mapping should state:

- why brokerage is a plausible observable;
- which part of the category it captures;
- which aspects it omits;
- the unit, population, and scope;
- alternative mappings;
- the evidence required to validate the mapping.

## 8.4 Procedural composability

One method's output may satisfy another method's input contract. Examples include:

- evidence map -> candidate theory and measure inventory;
- grounded-theory proposition -> process-tracing intake;
- construct specification -> measurement-development workflow;
- causal estimate -> simulation parameter distribution;
- graph community -> case-sampling frame;
- process-tracing unresolved prediction -> evidence-acquisition task.

## 8.5 Inferential composability

The downstream method cannot claim more than the upstream output licenses:

- a qualitative mechanism may seed a causal DAG but does not identify an effect;
- a graph community may guide sampling but is not automatically a substantive group;
- a process-tracing result within one case does not establish population prevalence;
- an SEM coefficient does not prove a within-case mechanism;
- a simulation result remains conditional on its structure and parameter assumptions;
- a policy appraisal adds normative criteria rather than inheriting them from empirical findings.

## 8.6 Representational composability

A transformation among text, table, graph, vector, covariance structure, causal diagram, or simulation state should record:

- what meaning survives;
- what is compressed or lost;
- whether the transformation is reversible;
- what units and scopes align;
- which source bindings remain available;
- which new assumptions were introduced.

Target-specific conformance profiles are preferable to a universal promise of lossless conversion.

## 8.7 Provenance and temporal composability

Composition must preserve:

- source versions;
- method and profile versions;
- execution time;
- evidence freshness;
- evidence-exposure state;
- dependencies and invalidation rules;
- review status.

A downstream object becomes stale when a material upstream object changes.

## 8.8 Governance composability

In secure deployments, authorization, privacy, rights, retention, and review status must survive composition. A valid schema or model does not authorize protected content or approve a scientific conclusion.

This is not a central demonstration requirement when using public or synthetic evidence, but the shared artifact model should avoid assuming that derived outputs are always unrestricted.

## 8.9 Integration operators

Cross-method integration should be explicit through typed operations:

- **Connect:** one method determines sampling or data collection for another.
- **Build:** one method creates an instrument, construct, model, or parameter used by another.
- **Merge:** two methods address the same claim and their outputs are compared.
- **Explain:** one method interprets a result from another.
- **Triangulate:** independent methods bear on the same proposition.
- **Expand:** methods address complementary dimensions of the problem.
- **Challenge:** one method exposes a defect, omitted condition, or alternative interpretation in another.
- **Parameterize:** evidence from one method supplies values or distributions to a model.

Every integration creates a `CrossMethodLink` recording source outputs, target inputs, mapping logic, unit and scope alignment, assumptions introduced, information lost, alternative mappings, and review state.

## 8.10 Mapping validation states

Documentation alone does not validate a cross-method translation. A mapping may progress through:

- proposed;
- semantically reviewed;
- empirically examined;
- validated for a limited use;
- rejected;
- superseded.

The required validation is destination-specific. A survey construct, causal variable, graph projection, and simulation parameter require different evidence.

# 9. Policy research as an adaptive lifecycle

## 9.1 Goal, plan, operate, evaluate

Policy research is not a mandatory linear pipeline. It is an adaptive loop:

1. **Goal:** frame the policy problem, knowledge need, research question, or decision.
2. **Plan:** select evidence, theories, methodological profiles, configurations, and review points.
3. **Operate:** collect, represent, measure, analyze, model, synthesize, and document.
4. **Evaluate:** inspect results, assumptions, contradictions, anomalies, uncertainty, and remaining value of information.
5. **Revise or stop:** continue, branch, narrow, seek new evidence, change methods, revise theory, compare configurations, or conclude.

The evolving Study State sits at the center. Every operation reads from and writes to that state through typed contracts.

## 9.2 Planned and emergent trajectories

Some projects know their broad trajectory:

```text
systematic review -> interviews -> construct development -> survey -> SEM
```

Others begin with an open question:

```text
map how agencies are implementing a policy
```

Descriptive analysis may reveal jurisdictional variation, triggering a review, comparative interviews, rival explanations, process tracing, and eventually quantitative analysis. Both trajectories are legitimate.

The plan should therefore support:

- declared future stages;
- conditional branches;
- emergent next actions;
- alternative design paths;
- stopping when further analysis has low expected value.

## 9.3 Evidence synthesis is a reusable operation

Evidence synthesis can be invoked to:

- scope a problem;
- identify theories, mechanisms, measures, datasets, and effect estimates;
- discover methodological precedents;
- explain an anomaly;
- find parameter values for a model;
- compare policy options and implementation experiences;
- update a study when new evidence appears.

Its output should be a structured evidence map that downstream methods can consume, not only a narrative review.

## 9.4 Optional policy-decision stage

Not every project ends in a recommendation. A study may describe an emerging threat, develop a measure, explain an institutional process, estimate an effect, or build a reusable model.

Where a decision exists, the workbench may add:

```text
evidence and models
-> policy options
-> outcomes and trade-offs
-> uncertainty, distribution, feasibility, and values
-> recommendation, adaptive strategy, or unresolved choice
```

This stage is explicitly normative. It combines empirical findings with objectives, legal duties, distributional concerns, budgets, stakeholder preferences, political feasibility, and risk tolerance.

## 9.5 Value of information

The system should consider whether additional analysis or evidence is worth acquiring. A failed model, unresolved mechanism, weak subgroup estimate, or sensitivity to one parameter may produce an evidence-acquisition agenda.

Value-of-information logic can help choose among:

- collecting new data;
- reviewing additional literature;
- interviewing a specific case or stakeholder;
- refining a measure;
- running a different method;
- accepting residual uncertainty and deciding.

# Part III. System architecture, ontology, and lineage

# 10. High-level architecture and program boundaries

## 10.1 Policy project and research-design layer

This layer owns:

- the client or policy problem;
- research and decision questions;
- objectives, options, outcomes, stakeholders, constraints, and time horizons;
- alternative research designs;
- project and automation configuration;
- the adaptive research plan;
- mixed-method integration;
- policy-facing synthesis and outputs.

It should propose designs rather than only methods. Examples include:

- review -> administrative-data analysis -> implementation interviews;
- evidence map -> comparative case study -> process tracing;
- stakeholder analysis -> survey -> measurement model -> SEM -> MCDA;
- qualitative discovery -> measurement development -> cross-case evaluation;
- graph analysis -> targeted interviews -> diffusion simulation -> robust intervention comparison.

## 10.2 Governed knowledge-analysis substrate

This layer supplies reusable epistemic and technical infrastructure:

- captured source artifacts and exact windows;
- stable artifact and entity identities;
- method-native observation references;
- optional reviewed assertions;
- derivation executions;
- projection manifests and reverse bindings;
- versioning, staleness, invalidation, and lineage;
- generic review state;
- later authorization and scope controls where required.

It must not decide whether a construct is valid, a causal effect is identified, a grounded theory fits the evidence, or an SEM is substantively meaningful.

## 10.3 Method-specific engines

Method engines own scientific semantics. Candidate engines include:

- evidence synthesis;
- Theory Forge;
- SQA and qualitative analysis;
- process tracing;
- relational and graph analysis;
- statistical and causal analysis;
- measurement development and SEM;
- simulation and foresight;
- policy appraisal and decision analysis.

Each engine may use its own native objects. The shared kernel indexes and connects those objects without absorbing their full meaning.

## 10.4 Agentic execution control plane

This layer owns:

- task scheduling and dependencies;
- model, service, and software invocation;
- budgets, rate limits, checkpoints, retries, and fallbacks;
- safe handling of files and credentials;
- execution traces;
- escalation and human-review requests.

It must not approve a research design or substantive conclusion merely because execution completed.

## 10.5 Separation without fragmentation

These layers should remain separate in authority but connected in use. The analyst should experience one workbench rather than a collection of repositories. The architecture should prevent one layer from silently taking over another's responsibilities.

# 11. Persistent Study State and federated ontology

## 11.1 Why Study State is the center

The universal project object should describe the evolving study, not one representation.

- A graph is appropriate for relational observables.
- A table is appropriate for deterministic aggregation.
- A memo and coded corpus may be appropriate for qualitative inquiry.
- A process-tracing ledger is appropriate for within-case evidence tests.
- A covariance matrix and model syntax are appropriate for SEM.
- A model state and experiment design are appropriate for simulation.

The Study State provides a shared index and typed relationships among these artifacts without forcing them into one payload.

## 11.2 Why an ontology is necessary

Without structured analytical objects, the AI cannot reliably determine:

- what question the study addresses;
- which evidence and scope are active;
- what concepts, assumptions, and findings exist;
- what depends on what;
- what became stale after revision;
- which next actions are plausible;
- how to render different outputs from the same analysis.

A chat history is too implicit. A document repository is too weakly structured. A graph alone privileges relational representation. The system therefore needs an ontology, but not a universal theory of analytical meaning.

## 11.3 Federated ontology

A federated ontology contains three layers.

### Layer 1: shared coordination objects

These are common across methods:

- project and project design;
- question and decision context;
- source, source window, and artifact;
- methodological profile and method pack;
- method run and execution event;
- version and dependency;
- review decision;
- lineage edge;
- stale state;
- actor or responsible party.

### Layer 2: thin cross-method analytical objects

These objects can be shared at a limited level:

- assumption;
- claim or proposition;
- finding;
- uncertainty;
- scope;
- transformation;
- cross-method link;
- decision object;
- open question and next-action candidate.

The shared schema should represent identity, type, scope, status, references, and lineage. It should not attempt to encode every method-specific property.

### Layer 3: method-native objects

These remain owned by their methods:

- qualitative code, category, memo, and theoretical relationship;
- process-tracing hypothesis, prediction, test, and mechanism link;
- graph projection, node, edge, metric, null model, and community;
- causal DAG, estimand, identification result, estimator, and refutation;
- construct, item, factor, invariance test, and structural path;
- simulation agent, rule, state variable, calibration target, and experiment;
- policy option, criterion, preference structure, switching value, and adaptive pathway.

The Study State references and relates these objects without asserting that they share one scientific meaning.

## 11.4 Minimal shared kernel

The smallest plausible shared kernel contains:

### `ProjectDesign`

Policy problem, research questions, decision context, population, units, case boundaries, time horizon, constraints, methodological profiles, automation profile, assurance profile, and intended outputs.

### `EvidenceItem` and `SourceWindow`

A document, dataset, interview, observation, image, model input, or bounded exact selection, with provenance, date, jurisdiction, case or participant identity, access condition, and dependence on other sources.

### `ArtifactRef`

A stable reference to a versioned native object or file without requiring the kernel to understand its entire schema.

### `MethodPackRef` and `MethodRun`

A configured execution of a method pack, including inputs, configuration, assumptions, evidence exposure, backend versions, operations, outputs, diagnostics, failures, costs, traces, and review state.

### `Assumption`

A scoped, versioned proposition introduced by a design, method, mapping, model, or decision process, with status and dependencies.

### `FindingRef`

A reference to a method-native conclusion or non-result, together with type, scope, warrant summary, review state, and lineage.

### `Transformation` and `CrossMethodLink`

Declared mappings among analytical objects, including retained meaning, lost meaning, unit and scope alignment, assumptions introduced, alternatives, validation, and review status.

### `ReviewDecision`

A recorded assessment, acceptance, rejection, revision request, disagreement, or supersession, including reviewer role and scope.

### `LineageEdge`

A typed dependency connecting source, observation, transformation, method run, model, finding, or decision object.

The kernel should remain thin enough to wrap at least two method producers without importing their domain schemas.

## 11.5 Append-only analytical history

Analytical objects should be immutable by version. Changes create new objects and events rather than overwriting the past.

Distinguish:

1. **Source change:** evidence was added, removed, corrected, or superseded.
2. **Semantic revision:** a code, category, construct, proposition, or interpretation changed.
3. **Method revision:** the design, methodological profile, method pack, configuration, or assumption changed.
4. **Recomputation:** the same declared analysis was executed again.
5. **Review change:** an object was accepted, disputed, rejected, or superseded without changing its content.

These distinctions are necessary to explain why a finding changed.

## 11.6 Staleness and invalidation

Each material dependency should define invalidation behavior. When an upstream object changes, downstream objects may become:

- unaffected;
- stale and requiring review;
- invalid and requiring recomputation;
- superseded but historically preserved;
- comparable as an alternative branch.

Invalidation should be selective rather than triggering indiscriminate reruns.

## 11.7 The ontology is a coordination system, not a theory of truth

The common ontology should not claim that every method has the same concept of evidence, model, finding, or uncertainty. Generalize only after repeated implementations reveal genuine common structure.

A useful rule is:

> The shared kernel may coordinate a method-native object without interpreting its scientific meaning.

# 12. Evidence, provenance, and analytical lineage

## 12.1 Provenance is not merely logging

Basic logging records events such as:

```text
timestamp
model or backend
prompt or command
input references
output references
runtime and cost
```

Analytical lineage records how evidence, observations, interpretations, assumptions, transformations, methods, and models produced a finding. It answers questions such as:

- Which source windows support this claim?
- Which codebook version produced these observations?
- Which theory operationalization licensed this graph measure?
- Which causal assumption identifies this estimand?
- Which parameter came from evidence, expert judgment, calibration, or an exploratory range?
- Which findings became stale after the category or assumption changed?
- Why does version 4 differ from version 3?

## 12.2 Provenance maturity levels

The platform can implement provenance in stages.

### Level 1: execution logging

Record model, prompt, code, backend, inputs, outputs, time, and cost.

### Level 2: artifact lineage

Maintain immutable artifacts, exact source windows, stable identifiers, derivation links, and reloadable outputs.

### Level 3: analytical dependency and invalidation

Represent dependencies among semantic objects, method runs, models, and findings; propagate staleness; support selective rerun and version diff.

### Level 4: cross-method semantic lineage

Record retained meaning, lost meaning, unit and scope alignment, new assumptions, alternative mappings, and validation across method seams.

The initial demonstration requires Levels 1 through 3 for a bounded workflow. Level 4 should be implemented only for real cross-method seams.

## 12.3 Exact source grounding

The workbench should preserve:

- captured source identity and version;
- exact source windows;
- source type, date, jurisdiction, case, and participant context;
- dependence among sources;
- extraction or observation procedure;
- uncertainty and review status.

A retrieval result becomes evidence only after resolving to an authoritative source or method-native record.

## 12.4 Proposition-relative evidence

A passage is not evidence for a proposition merely because it discusses the same topic. It must bear on the proposition's specified actors, relationship, direction, conditions, process, scope, or consequences.

A general evidence-disposition record should contain:

```text
proposition_id
source_window_id
disposition: support | qualification | contradiction | non_addressing
claim_component_addressed
scope_alignment
reason
ambiguity
review_state
```

This principle is central to the SQA Theory Quality Audit and generalizes to other text-grounded analyses.

## 12.5 Analytical lineage enables revision

Suppose the category "institutional distrust" is divided into:

- distrust of government;
- distrust of professional expertise.

The system should identify:

1. observations using the original category;
2. propositions depending on it;
3. theory modules, graph mappings, survey constructs, or simulation parameters inheriting it;
4. findings now stale;
5. method runs requiring recomputation;
6. findings surviving the change;
7. the reasons new outputs differ.

This is not basic logging. It is the dependency structure required for a revisable study.

## 12.6 Provenance as product value

Provenance supports:

- recursive source-to-finding and finding-to-source inspection;
- selective invalidation and rerun;
- comparison of alternative configurations;
- reconstruction of analytical decisions;
- reuse of reviewed theories, codebooks, instruments, and mappings;
- regeneration of different outputs from one study state;
- accumulation of reusable research assets.

Provenance should be justified by inspection, revision, comparison, or reuse—not completeness for its own sake.

## 12.7 Minimum sufficient provenance

The initial workbench should automate routine capture and avoid requiring analysts to maintain metadata manually.

For the first demonstration, minimum sufficient provenance includes:

- immutable artifact and method-run identifiers;
- exact source-window references;
- input, configuration, model, prompt, code, and output versions;
- explicit dependency edges;
- stale-state propagation after upstream change;
- reloadable rendering without a new model call;
- visible diffs between analytical versions.

# 13. Human, AI, and software division of labor

## 13.1 Large language models as methodological generalists

LLMs are suited to:

- structured policy and research intake;
- alternative problem formulations;
- research-design proposals;
- methodological-profile comparison;
- semantic screening and extraction;
- qualitative coding and comparison;
- theory-schema proposals;
- category, relationship, and mechanism proposals;
- proposition-relative evidence disposition;
- memo drafting and revision proposals;
- cross-method mapping proposals;
- rival explanations and adversarial critique;
- report generation from structured analytical state.

Their outputs should be typed, source-linked, versioned, and reviewable.

## 13.2 Limits of the methodological generalist

The LLM's breadth is uneven. It may:

- recommend a familiar method when a less common one fits better;
- blend incompatible traditions;
- state assumptions too generically;
- overinterpret method labels;
- produce plausible but unsupported source mappings;
- miss institutional constraints known to domain experts.

The workbench mitigates these risks through declared profiles, source grounding, alternative designs, structured outputs, diagnostics, and analyst authority.

## 13.3 Deterministic software and specialized backends

Deterministic and specialized systems are suited to:

- exact source anchoring and hashes;
- schema validation and state transitions;
- provenance and version lineage;
- candidate-pool accounting;
- table aggregation and statistical calculation;
- graph materialization and algorithms;
- model estimation and simulation execution;
- reproducible rendering and export;
- dependency invalidation;
- corruption checks and regression tests.

The platform should reuse mature software rather than asking LLMs to simulate numerical computation in prose.

## 13.4 Researchers and policy experts

Experts retain authority over:

- the real policy or research question;
- institutional and domain context;
- methodological stance and substantive theory;
- units, populations, cases, outcomes, and time boundaries;
- consequential assumptions and scope conditions;
- interpretation of anomalies and contested evidence;
- stakeholder values, legal duties, and political context;
- acceptance, revision, rejection, or external critique of analytical objects;
- policy judgment and communication.

## 13.5 The copilot should manage administrative state

The analyst should not ordinarily need to:

- reconcile identifiers across systems;
- maintain dependency graphs;
- reattach citations after every revision;
- manually propagate stale status;
- copy outputs among method tools;
- reconstruct prior configurations;
- maintain ordinary execution metadata.

The AI copilot and runtime should manage these functions automatically while exposing consequential decisions at the appropriate time.

# 14. Runtime and plugin architecture

## 14.1 Common `MethodRun` lifecycle

A neutral runtime can support the following lifecycle without owning method semantics:

```text
resolve method pack, profile, and versions
-> validate applicability and configuration
-> resolve exact inputs and evidence scope
-> freeze evidence exposure where required
-> execute procedure nodes
-> validate method-native outputs
-> persist artifacts, diagnostics, failures, costs, and traces
-> request or record review decisions
-> update Study State
-> evaluate staleness, branch conditions, and next actions
```

## 14.2 Method plugin contract

A method plugin should expose:

- methodological profile metadata and schemas;
- applicability checker;
- configuration interface schema;
- input resolvers;
- procedure graph;
- operator adapters;
- output validators;
- diagnostic and warrant renderers;
- integration ports;
- fixture, replay, and corruption suites.

The runtime should not infer method-specific meaning from generic field names.

## 14.3 Backend abstraction

Backend choice should remain distinct from method definition. For example:

- an SEM pack may call lavaan, Mplus, OpenMx, or another backend;
- a causal pack may call DoWhy and compatible estimators;
- graph operators may call NetworkX, igraph, a graph database, or custom code;
- an ABM pack may call Mesa or another simulation runtime;
- semantic tasks may call different LLM providers.

A backend replacement should not silently change methodological meaning. Each run records both method-pack and backend versions.

## 14.4 API and user-interface parity

Every meaningful user action should have a typed API operation. The user interface is a workbench over the same contracts, not a separate source of business logic.

This supports:

- automation;
- reproducibility;
- testing;
- agent use;
- alternate interfaces;
- replay and inspection.


# Part IV. Method families and their roles

# 15. Evidence synthesis and research-design discovery

## 15.1 Role in the platform

Evidence synthesis should be a major entry point because many policy projects begin by establishing what is known, disputed, measured, and missing. It also recurs when later analysis encounters a new mechanism, construct, anomaly, parameter, intervention, jurisdiction, or implementation condition.

The evidence-synthesis engine should support multiple declared profiles, including:

- systematic review;
- rapid review;
- scoping review;
- evidence map;
- literature review with explicit search and selection protocol;
- qualitative evidence synthesis;
- review of economic, implementation, or modeling evidence;
- living or updateable review.

The system should distinguish conduct methodology from reporting standards. PRISMA can govern transparent reporting without serving as the complete conduct methodology. Different domains may use Cochrane, Campbell, JBI, GRADE, or other source profiles.

## 15.2 Method-native outputs

A useful review result is not only prose. It should include:

- review question and protocol;
- search sources, queries, dates, and coverage;
- inclusion and exclusion criteria;
- screening decisions and reasons;
- study and source inventory;
- populations, settings, interventions, outcomes, and designs;
- theories and mechanisms used in the literature;
- measures and instruments;
- datasets and code availability;
- effect estimates or qualitative findings;
- bias, quality, or certainty assessments;
- implementation conditions;
- contradictions and evidence gaps;
- candidate parameters for models;
- research-design implications.

These objects can seed Theory Forge, SQA, causal design, measurement selection, simulation parameterization, policy options, or new data collection.

## 15.3 The AI contribution

AI can accelerate:

- question decomposition;
- query development;
- deduplication support;
- title, abstract, and full-text screening;
- structured extraction;
- taxonomy construction;
- study comparison;
- contradiction and gap discovery;
- update monitoring;
- proposal of downstream research designs.

Deterministic systems should preserve search records, source identity, screening decisions, exclusion reasons, and extraction schemas. Statistical backends should perform meta-analysis and related calculations.

## 15.4 Evidence synthesis as the design front door

The evidence map should support a design studio that proposes two to four next-step alternatives. For example:

- sufficient evidence for a bounded causal reanalysis;
- major mechanism uncertainty requiring comparative interviews;
- mature construct but weak measurement requiring instrument development;
- heterogeneous implementation requiring comparative case analysis;
- sparse empirical evidence but strong structural uncertainty requiring exploratory simulation.

The analyst can inspect why each design was proposed and which evidence, methodological profile, and assumptions it requires.

## 15.5 Thin slice

The first evidence-synthesis slice should take one bounded policy question and produce:

1. a reproducible search and source set;
2. a structured evidence map;
3. a theory, mechanism, measure, dataset, and implementation inventory;
4. explicit contradictions and evidence gaps;
5. two or three research-design alternatives with methodological lineage;
6. a versioned review artifact that can be updated when evidence changes.

The output should directly seed at least one downstream method without manual reconstruction.

# 16. Theory Forge

## 16.1 Exact product role

Theory Forge makes the application of a published or reviewed theory to evidence inspectable, repeatable, and reusable. Its north-star loop is:

```text
paper or reviewed theory
-> explicit theory schema
-> compile once
-> run many
-> evidence-backed results
```

The core unit of value is a reusable, reviewable theory module rather than an isolated answer or generated script.

Theory Forge is not a universal methodology compiler. It operationalizes theory. Downstream methods add their own research designs and inferential requirements.

## 16.2 Separation of source, operationalization, and application

Theory Forge separates:

1. **Source theory:** the original paper or reviewed theory remains the intellectual source.
2. **Operationalization:** a structured schema records one explicit interpretation.
3. **Application:** a compiled pipeline applies that interpretation to evidence and records outputs, source bindings, tests, uncertainty, and failures.

This prevents interpretive choices from disappearing inside prompts or code.

## 16.3 Three schema layers

### Theory semantics

The `identity`, `goal`, `mechanisms`, `uncertainties`, and `validation` sections state what the theory claims, why it is being applied, where it came from, and what would make an application credible or questionable.

### Observational model

The `constructs`, `categories`, and `representation` sections define what should be observed in evidence, how it should be classified, and in what structure the observations should be represented.

### Execution model

The `algorithms`, `parameters`, and `operations` sections define transformations, dependencies, inputs, outputs, analyst choices, and execution modes.

The layers must remain connected. A mechanism with no observable expression cannot guide analysis. A construct unused by any operation is inert. An algorithm without theoretical or source basis is unlicensed computation.

## 16.4 Theory Forge invariants

The workbench should preserve the following invariants:

- material schema claims trace to the theory source or are labeled as operationalization choices;
- mechanisms describe what the theory says happens; operations describe what the system does;
- analytical questions resolve to required operations;
- construct and category names remain consistent across representations and operations;
- operation dependencies form a complete executable order;
- deterministic work has explicit inputs, outputs, and constraints;
- interpretive work remains labeled as LLM-mediated or qualitative;
- uncertainty and validation are executable contract elements;
- compilation cannot silently alter theoretical meaning.

## 16.5 Relationship to other methods

Theory Forge can supply:

- theory-specific coded observations for descriptive analysis;
- relational observations and theory-supported graph algorithms;
- mechanisms and observable implications for process tracing;
- constructs and hypothesized relationships for measurement development;
- candidate variables, scope conditions, and hypotheses for statistical analysis;
- actors, rules, mechanisms, and parameters for simulation.

The downstream method must add its own design. Theory Forge does not identify causal effects, validate latent constructs, select process-tracing cases, or calibrate simulations by itself.

## 16.6 Published and emergent theory

Theory Forge should accept:

- a published or otherwise recognized theory source;
- a reviewed emergent theory produced through a legitimate discovery process such as SQA grounded-theory development.

The second path enables:

```text
qualitative discovery
-> reviewed candidate theory
-> Theory Forge schema
-> repeatable application to new evidence
-> downstream testing and revision
```

## 16.7 Multi-theory analysis

A later capability should compile multiple theories independently, apply them to the same evidence, and expose:

- agreement;
- tension;
- complementarity;
- competing explanations;
- different observational implications;
- distinct failures.

The system must not flatten multiple theories into a generic codebook. Every result retains its theory source and operationalization version.

## 16.8 Thin slices

1. **Paper to module:** one theory paper, reviewed schema, compiled application, corpus result, and source-theory/evidence trace.
2. **Compile once, run many:** apply the approved module to a second corpus without reinterpreting the paper.
3. **Revise and rerun:** change one operationalization choice, version it, rerun, and display changed and surviving findings.
4. **One downstream seam:** relational output to graph analysis or mechanism output to process-tracing intake.
5. **Emergent-theory handoff:** SQA candidate theory to Theory Forge to new-corpus application.

# 17. SQA, qualitative analysis, and grounded theory

## 17.1 SQA's role

SQA is the qualitative evidence and theory-development engine. It organizes large qualitative corpora, supports multiple coding postures, preserves source context, compares cases and participant positions, and develops claims that remain connected to exact passages.

Qualitative coding is not preliminary labor that disappears once a theory is produced. It remains the evidence-organization layer through theory development, negative-case analysis, process-tracing handoff, measurement development, and revision.

## 17.2 Coding profiles

The user-facing system may offer:

- **Open:** concepts and relationships are primarily generated from the corpus.
- **Framework-guided:** a declared theory or codebook organizes the analysis.
- **Abductive:** prior concepts are used while anomalies and rival explanations actively drive revision.
- **Hybrid:** predefined and emergent codes are deliberately combined.

These are configuration profiles rather than a claim that all qualitative traditions reduce to one taxonomy. A grounded-theory profile should also declare its methodological tradition.

## 17.3 Grounded-theory output

A grounded-theory-inspired result should be a candidate explanatory theory containing:

- a core category or central process;
- theoretical categories with definitions, properties, and dimensions;
- typed relationships such as condition, enables, constrains, response, consequence, feedback, or variation;
- scoped propositions such as "X enables Y when Z";
- analytic memos;
- rival interpretations;
- unresolved gaps;
- next-data questions.

A list of themes is not sufficient.

## 17.4 Theory Quality Audit

The SQA audit should expose five separate questions.

### Fit

Does each category, relationship, and proposition match the evidence? Display direct support, qualification, contradiction, and non-addressing material, including case distribution and full-context exemplars.

### Workability

Does the theory explain a process rather than list themes? A useful grammar is:

```text
conditions -> actor response or process -> consequence
```

with scope and alternatives where applicable.

### Variation

Where does the theory hold, change, or fail? Counterexamples should appear beside the proposition they challenge. The system should compare roles, settings, stages, resources, and case profiles.

### Saturation or category adequacy

What material novelty appears as cases accumulate: new categories, properties, dimensions, conditions, relationships, consequences, or counterexamples?

For a closed corpus, the strongest defensible statement is that no further material novelty was observed in that corpus under the declared processing order. Full theoretical saturation requires genuine theoretical sampling.

### Modifiability

When contrary evidence appears, the system records an explicit outcome:

- retain because the evidence does not bear on the claim;
- narrow scope;
- split a category or relationship;
- reject or replace the claim;
- request new evidence.

A memo links the revision to evidence and creates a new theory version.

## 17.5 Full-corpus processing and candidate pools

The current approach reads the designated corpus with LLMs and produces structured observations rather than relying only on vector retrieval. This supports strong operational coverage claims:

- all designated source units were processed;
- a declared procedure produced a candidate pool;
- every candidate was classified relative to the proposition;
- omissions and ambiguities remain visible.

The target is realistic procedural coverage, not an impossible guarantee of semantic exhaustiveness.

## 17.6 Process-tracing handoff

SQA can supply broad patterns, candidate explanations, rivals, observable implications, negative cases, and evidence gaps. It cannot simply relabel each category as a competing process-tracing hypothesis.

The handoff must add:

- a bounded outcome and case;
- whole-story rival explanations at comparable grain;
- opposed predictions;
- temporal mechanism links;
- source and time boundaries;
- evidence-exposure design.

## 17.7 Measurement and Theory Forge handoffs

A mature qualitative category may become:

- a Theory Forge operationalization for repeatable text application;
- a candidate construct for measurement development;
- a contextual variable, typology, mechanism, process, or scope condition;
- no quantitative object, if quantification would distort its meaning.

The mapping must preserve definition, variation, unit, scope, and lossiness.

## 17.8 Thin slice

The priority SQA slice is the Theory Quality Audit attached to an existing candidate-theory package:

- typed audit record per proposition and relationship;
- complete declared candidate pool and evidence dispositions;
- process-completeness flags with reasons;
- variation by case or participant position;
- novelty only where a real sequence exists;
- versioned memos and theory revisions;
- reloadable rendering without a new model call;
- visible comparison of theory versions.

# 18. Process tracing

## 18.1 Role

Process tracing addresses a different question from grounded theory:

> Given a bounded case, outcome, and set of rival causal explanations, which explanation receives greater comparative support from diagnostic within-case evidence, which mechanism links are observed or unresolved, and what evidence would best discriminate the rivals next?

It is especially useful when a candidate theory contains propositions such as "X enables Y under Z" and the analyst needs to examine the temporal mechanism within a case.

## 18.2 Required design additions

A process-tracing intake requires:

- one bounded case and outcome;
- a focal whole-story explanation;
- genuine rival explanations at comparable grain;
- a residual alternative where appropriate;
- explicit predictions or observable implications;
- evidence-by-hypothesis diagnostic tests;
- source and time boundaries;
- evidence dependence controls;
- a temporal mechanism with separately inspectable stages and links;
- formulation-evidence exposure.

## 18.3 Anti-circularity

Evidence used to formulate or materially refine a hypothesis remains discovery evidence. If all interviews generated the theory, the process-tracing system may still audit mechanism coherence, identify rival predictions, classify existing evidence, and produce an evidence-acquisition agenda. It should not present the same corpus as independent causal confirmation.

## 18.4 Method-native output

The output should include:

- research question and case boundary;
- rival hypothesis set;
- evidence-test matrix;
- source quality and dependence treatment;
- temporal mechanism assessment;
- comparative support conditional on the declared design;
- unresolved predictions and links;
- next evidence that would discriminate alternatives;
- feedback to SQA or Theory Forge.

Comparative support is not a probability that the theory is true and should not become a universal theory-quality score.

## 18.5 Thin slices

1. Transform one SQA proposition into a reviewable intake with outcome, focal explanation, rival, predictions, and evidence exposure.
2. Run one bounded case using distinct rivals and a method-native evidence matrix.
3. Return the result to SQA as a theory-revision or theoretical-sampling input.

# 19. Relational and graph inquiry

## 19.1 Three roles of graph systems

### Relational evidence representation

When the question concerns actors, interactions, roles, events, claims, or networks, a typed graph can preserve relationships damaged by flattening. A permissive n-ary substrate can preserve who did what to whom, in what role, when, with what uncertainty, and from which source.

### Retrieval and navigation

Graph retrieval can help agents traverse entities, sources, claims, communities, temporal paths, dependencies, and related evidence. Retrieval becomes evidentiary only after resolving to authoritative records.

### Graph-native analysis

Graph methods can address structural questions through:

- centrality and brokerage;
- community detection;
- diffusion cascades;
- path and reachability analysis;
- motifs and subgraph patterns;
- assortativity and homophily;
- comparison over time or across cases;
- multilayer and temporal structure;
- graph-based sampling.

## 19.2 Graph construction is measurement

A network is not simply found in text. The analyst or method pack must define:

- nodes and identity rules;
- edges and event roles;
- direction, weight, multiplicity, and time;
- inclusion and exclusion rules;
- missingness and uncertainty;
- projection from n-ary facts where needed;
- source dependence and duplicate handling.

These choices are measurement decisions and must remain inspectable.

## 19.3 Do not force every method through the graph

The graph is not a universal truth store. Tabular causal analysis, qualitative memos, SEM covariance structures, process-tracing ledgers, and simulation states may have method-native authority. They may link to graph artifacts without being encoded as graph assertions.

## 19.4 Theory Forge and graph observables

Theory Forge may define relational constructs and theory-supported graph algorithms. The mapping should show why a graph observable corresponds to the theory.

For example, a theory of brokerage may license specific path or betweenness measures. A generic community score should not be imported merely because it is available.

## 19.5 Graph and qualitative integration

A strong early seam is:

```text
interaction data
-> governed relational graph
-> graph patterns
-> targeted qualitative evidence
-> interpretation or challenge of communities and pathways
-> revised graph measures or sampling
-> integrated finding
```

Qualitative analysis can test whether detected communities are socially meaningful, explain anomalous structures, or identify missing relation types. Graph results can identify representative, boundary, bridge, or negative cases for qualitative inquiry.

## 19.6 Thin slice

Use one relational fixture to demonstrate:

- explicit network construction rules;
- source-linked graph projection;
- one meaningful structural result;
- qualitative challenge or interpretation;
- revision of the graph or sampling logic;
- an integrated finding that preserves both method-native warrants.

# 20. Statistical and causal analysis

## 20.1 Statistical design before estimator selection

The platform's value is not an estimator menu. It should formalize:

- the question and target quantity;
- population, unit, exposure, outcome, and time;
- sampling and data-generating process;
- measurement definitions;
- causal or predictive assumptions;
- candidate designs and estimators;
- diagnostics, robustness checks, and interpretation.

## 20.2 Causal workflow

A coherent causal adapter should separate:

1. **Model:** declare causal structure and assumptions, often through a DAG.
2. **Define the estimand:** specify the exact causal quantity of interest.
3. **Identify:** determine whether and how the estimand can be recovered under the assumptions.
4. **Estimate:** use a compatible statistical estimator.
5. **Refute and test sensitivity:** challenge the estimate with negative controls, placebo tests, alternative specifications, and unmeasured-confounding analysis.
6. **Interpret:** state population, assumptions, uncertainty, and policy relevance.

This structure is compatible with multiple statistical backends and methodological profiles.

## 20.3 Design router

The router should distinguish among:

- randomized experiments;
- difference-in-differences;
- regression discontinuity;
- instrumental variables;
- matching and weighting;
- interrupted time series;
- panel and multilevel models;
- mediation and moderation;
- descriptive or predictive analysis where causal claims are not intended.

The AI may propose designs and explain trade-offs. Domain assumptions and identification claims require substantive judgment.

## 20.4 Inputs from other methods

- reviews supply prior evidence, plausible confounders, measures, datasets, and effect ranges;
- Theory Forge supplies constructs, mechanisms, and scope conditions;
- qualitative analysis supplies contextual variables, omitted mechanisms, and measurement warnings;
- graph analysis supplies relational exposures or sampling frames;
- process tracing supplies within-case mechanism evidence;
- causal estimates may parameterize simulations or policy appraisal.

These inputs do not automatically inherit causal status.

## 20.5 Non-result handling

The system should explicitly return:

- unidentified estimand;
- unsupported overlap or positivity;
- incompatible measurement;
- inadequate sample or variation;
- fragile result under sensitivity analysis;
- descriptive association only.

A refusal to produce a causal estimate can be a high-value analytical result.

## 20.6 Thin slice

Support one defensible observational design end to end:

```text
theory and evidence
-> DAG
-> estimand
-> identification
-> compatible estimator
-> diagnostics and refutations
-> scoped finding or non-result
```

Depth and explicit failure handling are more important than broad estimator coverage.

# 21. Measurement development and structural equation modeling

## 21.1 A qualitative category is not automatically a quantitative construct

Before quantification, classify the object:

| Qualitative object | Possible quantitative representation |
|---|---|
| Degree of trust or perceived legitimacy | Reflective latent variable |
| Capacity constituted by budget, staff, authority, and expertise | Formative composite or index |
| Distinct implementation strategies | Latent class or typology |
| Context enabling an outcome | Observed moderator or level variable |
| Sequence of implementation stages | Longitudinal or event-history representation |
| Conjunctural pathway | Configurational analysis rather than SEM |
| Causal mechanism | Process tracing; mediation only with suitable design |
| Jurisdictional variation | Multilevel model |
| Dynamic feedback | Simulation or longitudinal model |

The AI may recommend a representation, but it must explain the classification, alternatives, and semantic loss.

## 21.2 Construct operationalization pipeline

```text
qualitative category or theory construct
-> construct specification
-> existing-measure search
-> candidate indicators or items
-> content and response-process review
-> pilot data
-> measurement model
-> invariance and reliability assessment
-> structural model
-> mixed-method interpretation
```

## 21.3 Construct specification

A candidate construct should record:

- conceptual definition and exclusions;
- population, context, unit, and level;
- time frame and whether it is a trait, state, event, or process;
- properties and dimensions;
- expected relationships to other constructs;
- reflective, formative, class, composite, observed, or other representation;
- source categories, passages, theory sections, and memos;
- alternative operationalizations;
- unresolved disputes;
- a lossiness memo describing meaning compressed or omitted by quantification.

## 21.4 Measure selection and item development

Search validated measures before inventing new ones. Compare intended construct, population, context, dimensions, and score interpretation with the construct specification.

When new or adapted items are needed, each item should link to one dimension and its qualitative or theoretical basis.

Content review asks whether the item set is relevant, comprehensive, and understandable. Cognitive interviewing or another response-process method asks whether respondents interpret and answer items as intended.

## 21.5 Measurement model before structural model

The system should distinguish:

- exploratory factor analysis where structure is uncertain;
- confirmatory factor analysis where a declared structure is tested;
- item-response or Rasch models for item-level measurement;
- reliability appropriate to the model;
- differential item functioning and measurement invariance across groups, jurisdictions, languages, or time.

The structural network should not be interpreted until measurement is adequate for the intended score use.

## 21.6 SEM's role

SEM can evaluate a prespecified network among observed and latent variables, including mediation, moderation, growth, and competing structures. It does not prove a grounded theory true. Good global fit can coexist with incorrect causal interpretation, omitted variables, or alternative models.

The workbench should preserve:

```text
source passage
-> qualitative code
-> category or theory construct
-> indicator
-> factor
-> structural path
-> policy interpretation
```

and permit reverse movement when quantitative anomalies reveal construct variation.

## 21.7 Joint display

For each construct or proposition, a mixed-method joint display can show:

| Qualitative or theory result | Operationalization | Quantitative result | Integrated interpretation |
|---|---|---|---|
| Category and dimensions | Items or indicators | Factor structure and estimates | Converges, qualifies, contradicts, or remains unresolved |

## 21.8 Thin slice

Select one mature category and produce:

- construct specification;
- representation classification;
- existing-measure comparison;
- candidate indicators;
- item-to-source traceability;
- cognitive-interview protocol;
- proposed measurement model;
- explicit conditions under which SEM becomes justified.

A later slice uses a real dataset to estimate measurement and structural models.

# 22. Simulation, foresight, and dynamic modeling

## 22.1 Simulation is a method family, not one engine

The design router should distinguish:

- **Agent-based modeling:** heterogeneous agents, interaction rules, adaptation, and emergent outcomes.
- **System dynamics:** stocks, flows, feedback loops, and aggregate dynamics.
- **Discrete-event simulation:** queues, resources, events, and process performance.
- **Microsimulation:** individual-level transitions and distributional policy effects.
- **Monte Carlo and probabilistic models:** propagation of parameter uncertainty.
- **Scenario and exploratory modeling:** behavior across plausible futures rather than point prediction.

## 22.2 Inputs from the workbench

Simulation may consume:

- actors, mechanisms, and scope conditions from Theory Forge;
- behavioral patterns and heterogeneity from SQA;
- interaction structure from graph analysis;
- causal estimates and parameter distributions from quantitative analysis;
- implementation constraints from process evaluation;
- policy options and criteria from appraisal;
- uncertainty ranges and deep uncertainties from foresight.

Every parameter should record its basis:

- direct estimate;
- literature value;
- expert judgment;
- calibration target;
- exploratory range.

## 22.3 Model specification

For agent-based and related models, the ODD protocol provides a useful structure for purpose, state variables, scales, process overview and scheduling, design concepts, initialization, inputs, submodels, rationale, and evaluation.

Other model families require their own profiles. The common kernel should not force every simulation into ODD fields.

## 22.4 Verification, validation, calibration, and sensitivity

Simulation quality requires distinct checks:

- **Verification:** was the intended model implemented correctly?
- **Validation:** is the model fit for its intended use and connected sufficiently to relevant real-world patterns?
- **Calibration:** which parameter values reproduce selected observations?
- **Sensitivity:** which assumptions and parameters drive outcomes?
- **Uncertainty analysis:** how do uncertain inputs propagate?
- **Structural alternatives:** do other plausible mechanisms change conclusions?

## 22.5 Policy use

Simulation is useful when the policy question involves feedback, adaptation, capacity constraints, path dependence, nonlinear effects, or futures outside observed data.

It should present conditional scenario results, not an oracle forecast. A result should state:

- model structure;
- parameter basis;
- tested futures;
- sensitivity and vulnerability regions;
- conditions under which the result changes.

## 22.6 Thin slice

```text
Theory Forge schema + graph structure + evidence-backed parameters
-> model-family selection
-> accepted specification
-> executable model
-> verification
-> calibration or plausibility checks
-> sensitivity experiments
-> conditional scenario finding
```

The first slice should use one bounded question and a small model whose assumptions are inspectable.

# 23. Policy appraisal and decision analysis

## 23.1 Optional but essential for action-oriented projects

Empirical research asks what is happening, why, what may happen, or what changes under an intervention. Policy appraisal adds:

> Given objectives, options, evidence, uncertainty, constraints, distributional effects, and stakeholder values, what action is preferable, robust, adaptive, or explicitly unresolved?

Not all studies require this stage.

## 23.2 General policy-analysis spine

Bardach and Patashnik's Eightfold Path provides an accessible workflow: define the problem, assemble evidence, construct alternatives, select criteria, project outcomes, confront trade-offs, focus and decide, and tell the story.

Weimer and Vining provide deeper foundations in problem analysis, intervention rationales, government failure, solution design, adoption, implementation, evidence gathering, and economic analysis.

The CDC Policy Analytical Framework provides a concise applied sequence for identifying problems, describing and assessing policy options, prioritizing them, and developing an adoption strategy.

These sources may inform design profiles without becoming a rigid universal pipeline.

## 23.3 Appraisal and business cases

The Green Book can inform:

- case for change and theory of change;
- business-as-usual baseline;
- objectives and strategic fit;
- option longlisting and shortlisting;
- critical success factors;
- social cost-benefit or cost-effectiveness analysis;
- unmonetized effects, risks, uncertainty, distribution, and place;
- optimism bias, sensitivity, and switching values;
- balanced identification of a preferred option.

The Five Case Model extends appraisal into strategic, economic, commercial, financial, and management cases.

## 23.4 Decision methods

The platform may support profiles for:

- cost-benefit and cost-effectiveness analysis;
- budget impact and fiscal analysis;
- MCDA with explicit criteria and structured elicitation;
- robust decision making under deep uncertainty;
- value of information and research prioritization;
- portfolio and adaptive-policy analysis;
- distributional and equity analysis;
- implementation feasibility and stakeholder analysis.

Simple weighting and scoring should not be presented as rigorous MCDA without appropriate methodological support.

## 23.5 Empirical findings do not contain policy values automatically

The decision layer should record where normative or institutional judgment enters. A preferred policy may depend on:

- objective weights;
- equity judgments;
- risk aversion;
- legal constraints;
- political feasibility;
- institutional capacity;
- time preference;
- treatment of irreversible harms.

The platform can make these inputs explicit, compare them, and test sensitivity. It cannot infer one universally correct value structure from empirical evidence.

## 23.6 Method-native output

A decision object may include:

- option definition and implementation pathway;
- objectives and critical success factors;
- expected benefits, costs, risks, and adverse effects;
- evidence and model sources;
- distributional and place effects;
- feasibility, legal, political, commercial, and delivery constraints;
- sensitivity and vulnerability regions;
- stakeholder values and disagreements;
- preferred, robust, or adaptive option;
- monitoring, evaluation, and learning plan;
- explicit residual uncertainty.

## 23.7 Thin slice

Take findings from two or three existing method runs and compare a small option set using one declared appraisal profile.

The slice should demonstrate that policy judgment is a new, traceable analytical layer rather than a paragraph appended to a research report.


# Part V. Integration and user experience

# 24. A concrete cross-method investigation

## 24.1 Hero scenario

A useful hero scenario is the spread of a false political narrative:

> Why is the narrative spreading through particular communities, and which interventions could reduce its reach or influence under different assumptions about trust, platform structure, and institutional response?

The scenario is not intended to make the system determine which political party is correct. It demonstrates how empirical, interpretive, dynamic, and decision methods can connect while preserving their distinct warrants.

## 24.2 Illustrative workflow

| Stage | Method | Output passed forward |
|---|---|---|
| 1 | Structured or systematic review | Known diffusion mechanisms, interventions, measures, datasets, and rival theories |
| 2 | Research-design studio | Alternative explanatory, causal, and exploratory designs with assumptions and evidence requirements |
| 3 | Theory Forge | Constructs such as repeated exposure, trusted messenger, perceived legitimacy, and institutional distrust |
| 4 | Data and corpus acquisition | Posts, accounts, interactions, timestamps, documents, surveys, and source provenance |
| 5 | Graph construction | Typed accounts, messages, repost events, claims, temporal roles, and uncertainty |
| 6 | Graph analysis | Communities, diffusion cascades, bridge accounts, temporal patterns, and candidate cases |
| 7 | SQA | Community-specific interpretations, motives, trust processes, qualifications, contradictions, and negative cases |
| 8 | Grounded or abductive explanation | Candidate proposition connecting exposure, messenger trust, and acceptance under defined conditions |
| 9 | Process tracing | Rival mechanisms examined within selected cascades or communities |
| 10 | Causal design | DAG, intervention, outcome, confounders, estimand, identification strategy, or explicit non-identification |
| 11 | Quantitative estimation | Effect estimates where a defensible design and data exist |
| 12 | Measurement and SEM | Optional measurement of latent trust or legitimacy from survey data |
| 13 | Simulation | Diffusion model informed by network structure, qualitative mechanisms, and quantitative estimates |
| 14 | Decision analysis | Comparison of interventions on effectiveness, cost, equity, feasibility, and robustness |

One project need not execute every stage. The scenario illustrates possible composition.

## 24.3 Configuration alternatives

The front door might propose:

### Design A: descriptive and interpretive

```text
review -> graph mapping -> targeted qualitative analysis -> intervention hypotheses
```

Appropriate when the immediate objective is to understand patterns and meanings without estimating intervention effects.

### Design B: mechanism-centered

```text
review -> SQA -> candidate explanation -> process tracing in selected cases
```

Appropriate when the main uncertainty concerns why acceptance occurs in particular settings.

### Design C: intervention-effect design

```text
theory and qualitative context -> DAG -> experiment or quasi-experiment -> effect estimate
```

Appropriate when a feasible intervention and defensible identification strategy exist.

### Design D: exploratory policy design

```text
graph + qualitative mechanisms + uncertain parameters
-> diffusion simulation
-> robust intervention comparison
```

Appropriate when feedback, adaptation, and deep uncertainty dominate and point prediction would be misleading.

The analyst selects or combines designs based on the real decision need, available evidence, and constraints.

## 24.4 Adaptive branches

```text
IF graph communities do not correspond to meaningful social groupings:
    do not use them as substantive cases without further evidence.

IF qualitative analysis reveals an omitted mechanism:
    revise the theory schema, process-tracing rivals, and causal DAG.

IF the causal effect is not identified:
    produce a non-result and consider new data, process tracing,
    natural experiments, or simulation over plausible ranges.

IF the measurement model fails:
    return to construct definition, items, and qualitative variation.

IF simulation results depend on one weak parameter:
    prioritize evidence acquisition using value-of-information logic.

IF the preferred intervention changes under plausible value weights:
    report the trade-off rather than one supposedly objective recommendation.
```

This is the intended character of the platform: one evolving investigation rather than a fixed chain of tools.

# 25. User experience

## 25.1 Front door: policy and research framing

The user may begin with:

- a policy question;
- a client request;
- a body of evidence;
- an existing theory;
- a dataset;
- a model;
- a decision that must be supported.

The AI conducts a structured intake covering:

- what decision or knowledge need exists;
- who will use the result;
- what is currently known;
- what must be described, explained, predicted, estimated, compared, or decided;
- units, populations, cases, settings, and time;
- available and collectable evidence;
- constraints, rights, ethics, and deployment conditions where relevant;
- desired assurance and deliverables.

The user should not need to know method names. The AI translates the substantive problem into alternative research designs and explains their trade-offs.

## 25.2 Design studio

The design studio is the flagship human–AI interaction. It should show:

- alternative formulations of the question;
- alternative methodological profiles;
- evidence and data requirements;
- assumptions and potential failure states;
- expected outputs and limits;
- branch conditions;
- resource implications;
- how the designs relate to the analyst's stated context.

The analyst can edit ordinary language rather than manipulate every technical field. The effective structured configuration remains available for inspection.

## 25.3 Coordinated workbench views

The interface should expose coordinated views over the same Study State.

### Project view

Question, decision context, selected and rejected designs, methods, plan, milestones, branches, and current status.

### Evidence view

Sources, datasets, exact windows, search and screening, case and participant structure, provenance, dependence, and evidence gaps.

### Theory and concepts view

Theory Forge schemas, SQA categories, mechanisms, constructs, scope conditions, rivals, alternative operationalizations, and unresolved definitions.

### Method view

Methodological profile, method-pack configuration, procedure graph, current task, inputs, outputs, diagnostics, failures, and review state.

### Findings view

Claims, proposition-relative evidence, estimates, models, simulations, warrant profiles, limitations, disagreements, and non-results.

### Decision view

Options, criteria, objectives, outcomes, distributional effects, uncertainty, feasibility, values, and recommendations.

### Lineage view

Recursive source-to-finding and finding-to-source trace, version history, staleness, transformation loss, and rebuild paths.

## 25.4 Progressive disclosure and metadata automation

Most analysts should not spend their time maintaining the Study State. The AI and runtime should automatically:

- attach source windows;
- create stable identifiers;
- record method and backend versions;
- capture dependencies;
- update stale status;
- prepare version diffs;
- maintain ordinary review and execution metadata.

Detailed lineage should remain available when requested or when consequence requires it. The interface should foreground substantive choices and hide administrative machinery by default.

## 25.5 Explainability as inspection

The system should answer practical questions:

- Why was this design proposed?
- Why did the profile require this step?
- Which evidence supports or contradicts this proposition?
- What did this transformation preserve or lose?
- Which assumption drives this result?
- Why did the finding change after revision?
- Which policy judgment depends on value choices rather than empirical evidence?

This form of explanation is more useful than an invented narrative about an LLM's hidden internal reasoning.

## 25.6 Audience-specific outputs

The same Study State should render:

- executive brief;
- technical report;
- methodology appendix;
- literature evidence table;
- theory and measurement specification;
- graph or causal analysis appendix;
- model card or simulation description;
- policy-options matrix;
- stakeholder-facing explanation;
- interactive dashboard;
- evidence-acquisition agenda.

These are different views of one analytical asset, not independently generated stories.

# 26. Method registry and method-pack authoring

## 26.1 Historical taxonomy as candidate vocabulary

A broad policy-methods taxonomy is useful for discovery, but such taxonomies often mix:

- aliases;
- complete research designs;
- estimators;
- data-collection techniques;
- analytical purposes;
- assurance practices;
- software-enabled representations.

It should seed a faceted registry rather than become executable classes directly.

## 26.2 Method profile facets

Every normalized profile should describe:

| Facet | Examples |
|---|---|
| Analytical purpose | Describe, explain, estimate, predict, compare, decide |
| Evidence form | Text, interviews, surveys, administrative data, spatial, network, experimental |
| Inferential mode | Inductive, abductive, deductive, causal, predictive, normative |
| Unit and level | Person, event, organization, jurisdiction, dyad, network, system |
| Temporal form | Cross-sectional, longitudinal, historical, prospective, dynamic |
| Output | Theme, theory, estimate, forecast, scenario, option comparison |
| Core assumptions | Exchangeability, measurement stability, case comparability, model structure |
| Diagnostics | Fit, balance, invariance, sensitivity, saturation, convergence, validation |
| Integration ports | Inputs consumed and outputs supplied |
| Methodological sources | Handbooks, standards, protocols, textbooks, articles |
| Backends | LLM, Python/R packages, graph engines, simulation runtimes, human tasks |

## 26.3 Authoring workflow

A future Method Pack Compiler or authoring environment should follow:

1. **Acquire sources.** Select recognized sources, editions, profiles, and domain supplements.
2. **Extract methodological claims.** Identify applicability, required steps, options, diagnostics, outputs, and interpretation limits.
3. **Classify source force.** Distinguish requirement, recommendation, option, rationale, and example.
4. **Record interpretation.** State how the platform understands each material source statement.
5. **Define method-native objects.** Specify inputs, observations, decisions, models, and outputs.
6. **Construct the procedure graph.** Make dependencies, loops, branch conditions, and stopping states explicit.
7. **Assign execution roles.** Mark LLM, deterministic, backend, human, data-collection, and review tasks.
8. **Map backends.** Connect abstract operators to software or human procedures.
9. **Create fixtures.** Add golden, ambiguous, negative, unsupported, and corruption cases.
10. **Review fidelity.** A knowledgeable reviewer evaluates whether the pack materially reflects the declared profile.
11. **Compile and run.** Execute on a bounded case and preserve source, profile, implementation, and backend versions.
12. **Promote by maturity.** Move from conceptual to executable, exercised, reviewed, integrated, and reused.

## 26.4 Avoid premature universal method language

A fully general domain-specific language for every research methodology would become an open-ended ontology project.

The near-term design should use:

- a stable common envelope;
- typed extension points;
- method-family-specific schemas;
- declarative procedure graphs where useful;
- Python, R, service, or human-task adapters.

Generalize only after several real packs expose repeated structure.

# Part VI. Phased implementation and evaluation

# 27. Principles for implementation phasing

## 27.1 Thin verticals over broad frameworks

A small end-to-end slice is more valuable than an elegant architecture with no credible method-native result. Each slice should connect:

- real sources or data;
- a real methodological profile;
- a real producer;
- a real output;
- a real reviewer or analyst path;
- a visible revision or failure state.

## 27.2 Hero workflow plus fixture portfolio

Use both:

- **Hero workflow:** one compelling policy problem connecting a small number of methods in a coherent user journey.
- **Fixture portfolio:** small controlled cases proving individual method, lineage, representation, and failure claims.

The hero demonstrates integration value. Fixtures demonstrate methodological and architectural rigor.

## 27.3 Reuse mature numerical software

Do not reimplement SEM estimators, graph algorithms, optimizers, causal estimators, or simulation runtimes unless existing software cannot satisfy the contract.

The product value lies in:

- research configuration;
- semantic preparation;
- source grounding;
- analytical lineage;
- integration;
- diagnostics;
- revision;
- interpretation.

## 27.4 Build only demanded representations

A method or fixture should use the representation suited to its observable. Do not build every converter or route every analysis through graph, vector, and assertion layers.

## 27.5 Generalize after repeated demand

Shared abstractions should be extracted after at least two, preferably three, real producers require them. Repository edges should reflect exercised code rather than aspirational diagrams.

## 27.6 Capability before complete commercialization

The first objective is to demonstrate the capability to analysts. Detailed commercialization, procurement, and enterprise deployment can follow. Product learning should still occur continuously through real analyst use.

# 28. Recommended implementation slices

## Slice 0. Common Study State and analytical-lineage envelope

### Objective

Create the minimal coordination kernel needed to connect existing engines without absorbing their semantics.

### Deliverables

- `ProjectDesign` and `StudyState` objects;
- immutable artifact, source-window, profile, and method-run references;
- input, configuration, output, diagnostic, review, and lineage envelopes;
- method registry with maturity status;
- local recursive trace from finding to inputs;
- dependency and stale-state handling;
- reloadable rendering;
- API and UI parity conventions.

### Acceptance

Wrap one SQA run, one Theory Forge run, and one graph or process-tracing run without rewriting their native outputs.

### Defer

- durable multi-producer registry extraction;
- universal workflow language;
- automatic method selection;
- comprehensive cross-method semantic ontology;
- enterprise authorization infrastructure.

## Slice 1. SQA Theory Quality Audit

### Objective

Make an existing candidate grounded theory evidence-steppable and revision-visible.

### Deliverables

- proposition-relative evidence dispositions;
- fit, workability, variation, category adequacy, and modifiability views;
- process-completeness flags;
- counterexamples beside challenged claims;
- versioned memos and theory history;
- fixed-corpus saturation language;
- reloadable audit package.

### Acceptance

A reviewer can inspect why a proposition fits, where it fails, and what would change it without a new model call.

## Slice 2. Theory Forge reusable-instrument proof

### Objective

Demonstrate the paper-to-schema-to-run-many product thesis.

### Deliverables

- paper-to-schema review;
- compiled prompts, algorithms, operations, validation, and manifest;
- run on one corpus;
- rerun on a second corpus without reinterpretation;
- schema revision and result diff;
- trace to source theory and evidence.

### Acceptance

A knowledgeable reviewer can identify and contest the operationalization, and reuse materially reduces effort.

## Slice 3. Evidence-synthesis and design front door

### Objective

Turn a recognized review profile into a structured starting point for the workbench and demonstrate AI-assisted methodological expansion.

### Deliverables

- bounded protocol and search;
- screening and extraction trail;
- evidence, theory, mechanism, measure, dataset, and gap map;
- two to four research-design alternatives;
- methodological lineage for each design;
- analyst selection and revision path.

### Acceptance

The output directly seeds at least one downstream method without manual reconstruction, and the analyst can explain why one design was selected over alternatives.

## Slice 4. First mixed-method seam

Choose the seam best supported by existing artifacts.

### Option A: graph plus qualitative interpretation

Graph analysis identifies communities, bridges, or pathways. SQA interprets and challenges their meaning. The integrated finding links to both representations and sources.

### Option B: SQA to process tracing

A candidate proposition becomes a bounded process-tracing intake with whole-story rivals, predictions, evidence exposure, and an evidence-acquisition agenda.

### Acceptance

The integration is typed, source-grounded, and method-native. Neither output is flattened into a generic summary. A revision on one side produces an intelligible effect on the other.

## Slice 5. Causal-analysis adapter

### Objective

Prove one rigorous causal design rather than a broad estimator catalogue.

### Deliverables

- causal question and estimand;
- DAG and assumptions;
- identification result or explicit failure;
- compatible estimator;
- diagnostics, refutation, and sensitivity;
- finding with interpretation limits.

### Acceptance

The system can refuse an unidentified claim, and every estimate retains its design and assumptions.

## Slice 6. Construct-to-measurement-to-SEM

### Objective

Prove that qualitative or theoretical concepts can be operationalized without semantic laundering.

### Deliverables

- construct specification and lossiness memo;
- measure search and candidate item bank;
- content and response-process review protocol;
- pilot dataset;
- measurement model, invariance checks, and structural alternatives;
- joint display with qualitative evidence.

### Acceptance

The structural result cannot be produced until measurement status supports its intended use.

## Slice 7. Simulation vertical

### Objective

Translate theory and evidence into a transparent dynamic model.

### Deliverables

- model-family selection;
- accepted model-description profile;
- parameter provenance;
- executable model;
- verification, calibration, or plausibility checks;
- sensitivity and scenario runs;
- conditional policy finding.

### Acceptance

A reviewer can trace each material rule and parameter to theory, evidence, expert judgment, calibration, or an explicit exploratory assumption.

## Slice 8. Policy appraisal and decision support

### Objective

Show how method-native findings become an option comparison without being collapsed into one empirical score.

### Deliverables

- objectives, baseline, and option set;
- criteria and critical success factors;
- benefits, costs, risks, distribution, and feasibility;
- explicit value judgments and stakeholder disagreements;
- sensitivity or robust-decision analysis;
- recommendation, adaptive strategy, or unresolved trade-off;
- monitoring and evaluation plan.

### Acceptance

The recommendation links to empirical findings and shows where normative or institutional judgment enters.

## Slice 9. Method-pack authoring and second-project proof

### Objective

Demonstrate reuse and the ability to absorb a new recognized methodology.

### Deliverables

- source interpretation and method-pack authoring workflow;
- one new method pack not hard-coded into the kernel;
- clean run in a second policy domain;
- no source-specific kernel edits;
- documented generalizations and retained method-specific extensions.

### Acceptance

The system demonstrates that cumulative analytical capital and the plugin architecture extend beyond the hero project.

# 29. Parallel workstreams and dependencies

## Track A. Shared platform foundation

- Study State and artifact envelope;
- federated ontology;
- methodological-profile registry;
- lineage, versioning, staleness, and replay;
- workbench API and UI shell;
- agent orchestration and budgets.

## Track B. Method verticals

- SQA audit;
- Theory Forge reusable module;
- evidence synthesis and design studio;
- process-tracing intake;
- graph analysis integration;
- later causal, SEM, simulation, and decision packs.

## Track C. Product demonstrations

- public qualitative benchmark;
- source-to-table Theory Forge case;
- process-tracing fixture;
- relational graph fixture;
- coherent hero investigation;
- second-project reuse.

## Dependency principle

The platform foundation should grow only when method verticals demand it. Method verticals should use shared infrastructure where it already exists rather than duplicating generic identity, versioning, and lineage functions.

# 30. Demonstration and evaluation strategy

## 30.1 What the demonstration should show

The demonstration should emphasize that:

- a policy question becomes alternative research designs;
- the analyst contributes domain knowledge and selects consequential configuration;
- the AI broadens the methodological choice set;
- recognized sources materially inform method execution;
- each method uses an appropriate representation;
- intermediate and final objects remain inspectable;
- methods exchange typed outputs without semantic or inferential laundering;
- revisions trigger bounded reruns and visible diffs;
- negative evidence, disagreement, and non-results remain visible;
- one project can produce technical and policy-facing outputs from the same state;
- analytical assets can be reused in a second project.

## 30.2 Evaluation dimensions

| Dimension | Core question |
|---|---|
| Inspectability | Can an analyst reconstruct the evidence, configuration, transformations, and assumptions behind a finding? |
| Methodological fidelity | Did execution materially reflect the declared profile and its interpretation limits? |
| Claim-relative warrant | Does each claim expose support, qualification, contradiction, uncertainty, and scope? |
| Decision usefulness | Did the analysis clarify the problem, reveal trade-offs, identify robust actions, or guide evidence acquisition? |
| Revision capacity | Can a material upstream change be propagated selectively with an intelligible diff? |
| Methodological expansion | Did the AI help the analyst consider or use defensible perspectives they would otherwise have missed? |
| Analyst burden | Did the system reduce mechanical work without creating excessive administrative overhead? |
| Reuse | Did prior evidence maps, theory modules, codebooks, configurations, or mappings reduce effort on a later project? |

## 30.3 Comparative evidence

A credible prototype evaluation may use:

- real or public policy-analysis cases;
- comparison with skilled analysts using ordinary tools;
- blinded expert review of intermediate and final outputs;
- source-grounded judging rather than style-only judging;
- multiple reviewer backgrounds;
- deliberately degraded negative controls;
- deterministic lineage and corruption tests;
- revision demonstrations;
- user walkthroughs of traceability and usefulness.

The claim should remain bounded: the system expanded or improved analysis under a declared rubric and made the analytical chain inspectable. A massive validation study is not a prerequisite for a prototype.

## 30.4 Flagship metrics

Useful metrics include:

- time and cost for a recurring analytical task;
- proportion of material claims resolving to exact evidence and method lineage;
- consequential unsupported-claim or source-misrepresentation rate;
- reviewer time to inspect a finding;
- analyst correction burden;
- number and importance of negative cases or rivals surfaced;
- stability and change under reruns and alternative configurations;
- time to revise a codebook, theory, or assumption and recompute;
- defects found in construct, mapping, or methodological choices;
- number of defensible design alternatives generated and used;
- usefulness of decision support;
- reuse effort on a second project.

## 30.5 Evaluation should not become the product

The system should not be designed around one benchmark or attempt to prove universal correctness. Evaluation is evidence about whether the capability works for bounded purposes. It should remain proportional to the development stage and consequence of the use case.

# 31. Implementation assurance and testing

This section records implementation invariants rather than the strategic center of the vision.

## 31.1 Verification and validation

Distinguish:

- **Verification:** did the implementation satisfy its specification?
- **Validation:** is the method, model, mapping, or output fit for the intended analytical use?

Typed schemas and passing tests establish verification, not substantive validity.

## 31.2 Test classes

### Positive and golden cases

Known valid inputs and expected outputs.

### Negative and unsupported cases

Inputs that should fail, return unavailable, or produce a non-result.

### Corruption tests

Wrong identities, changed bytes, stale versions, unauthorized scope where applicable, missing reverse bindings, or inconsistent model inputs.

### Metamorphic tests

Expected changes under controlled perturbations such as a revised codebook, omitted edge type, alternative estimator, or changed simulation parameter.

### Adversarial semantic tests

Topically related but proposition-nonresponsive passages; plausible but false theory mappings; dependent source repetitions; misleading graph communities; label similarity without construct equivalence.

### Replay tests

Frozen outputs can be rerendered; deterministic stages reproduce; recorded model outputs can be replayed; fresh LLM reruns are treated as replications rather than exact reproduction.

## 31.3 Method-specific assurance

Each method pack defines its own diagnostics, such as:

- screening and bias checks for reviews;
- fit, variation, and modification for grounded theory;
- rival discrimination and mechanism gaps for process tracing;
- graph-construction validity and null comparisons for networks;
- balance and sensitivity for causal analysis;
- content validity, invariance, and fit for SEM;
- calibration and sensitivity for simulation;
- switching values and distributional analysis for appraisal.

# Part VII. Strategic risks, choices, and recommendations

# 32. Major risks and mitigations

## 32.1 Scope explosion

**Risk:** The full gamut of policy methods becomes an unbounded platform program.

**Mitigation:** Retain the long-run boundary but build thin, method-native seams. Require a real workflow and complete producer-to-consumer path before extracting general infrastructure.

## 32.2 Method laundering

**Risk:** Generic prompts receive respected method labels and create the appearance of rigor.

**Mitigation:** Preserve source, interpretation, and implementation lineage. Require profile-specific steps, diagnostics, outputs, failure states, and review before promotion.

## 32.3 Methodological eclecticism

**Risk:** Convenient procedures from incompatible traditions are combined without acknowledging their assumptions.

**Mitigation:** Declare profiles and hybrids explicitly. Record tensions, platform-created choices, and interpretation limits.

## 32.4 Configuration laundering

**Risk:** Contestable framing, scope, outcomes, and value choices appear objective because they are encoded formally.

**Mitigation:** Preserve alternatives considered, analyst interventions, consequential exclusions, assumptions, and sensitivity to defensible configurations.

## 32.5 Premature generalization

**Risk:** A universal ontology or method language is designed before repeated structure is known.

**Mitigation:** Use a federated ontology, thin coordination kernel, and method-specific extensions. Generalize after multiple exercised implementations.

## 32.6 Ontological overreach

**Risk:** Shared objects such as claim, finding, model, or uncertainty gradually absorb incompatible method-specific meanings.

**Mitigation:** Keep common schemas thin. Allow the kernel to reference native objects without interpreting their entire scientific content.

## 32.7 Semantic loss at seams

**Risk:** Qualitative categories, graph metrics, statistical variables, and simulation parameters are treated as equivalent because their labels resemble one another.

**Mitigation:** Require typed mappings, unit and scope alignment, lossiness records, alternative mappings, destination-specific validation, and review state.

## 32.8 Inferential laundering

**Risk:** A qualitative proposition becomes a causal claim; a graph community becomes a real group; an SEM path becomes a mechanism; a simulation becomes a forecast.

**Mitigation:** Preserve method-native warrant and downstream interpretation constraints. A transformation can transfer an object but not silently strengthen its evidentiary status.

## 32.9 Graph overreach

**Risk:** Existing graph infrastructure biases every problem toward graph representation.

**Mitigation:** Choose representation from the question and observable. Keep method-native records authoritative and use graph projections only where relational structure is material.

## 32.10 Measurement failure

**Risk:** Sophisticated quantitative models are fitted to poorly operationalized constructs.

**Mitigation:** Maintain a separate measurement-development pipeline and gate structural interpretation on measurement status.

## 32.11 Circular confirmation

**Risk:** Evidence used to generate a theory is later counted as independent confirmation.

**Mitigation:** Record evidence exposure and declare exploratory, discovery/evaluation, sequential, or external-evaluation designs.

## 32.12 Universal confidence score

**Risk:** The interface creates false comparability across methods.

**Mitigation:** Use warrant profiles and method-native diagnostics with narrative or structured synthesis rather than one scalar.

## 32.13 LLM instability and provider drift

**Risk:** Results change across providers, model versions, or reruns.

**Mitigation:** Record prompts, schemas, models, configurations, and outputs; freeze reviewed artifacts; separate replay from fresh replication; use multi-run comparison where material.

## 32.14 Methodological source drift

**Risk:** Profiles become stale as guidance and software change.

**Mitigation:** Version sources, interpretations, implementations, and backends separately. Trigger review rather than silent updates.

## 32.15 User complexity and metadata burden

**Risk:** A comprehensive workbench overwhelms analysts with settings, state, and lineage details.

**Mitigation:** Use hierarchical configuration, progressive disclosure, AI-proposed defaults, conversational editing, and automated metadata capture. Measure administrative burden directly.

## 32.16 Provenance bureaucracy

**Risk:** The platform produces elaborate lineage without making analysis materially better or easier to revise.

**Mitigation:** Justify provenance features through inspection, selective rerun, comparison, or reuse. Do not pursue completeness as an end in itself.

## 32.17 Breadth displacing depth

**Risk:** Superficial support for many methods damages trust.

**Mitigation:** Require credible method-native results and failure states before adding families. Use the fixture portfolio to demonstrate depth separately from integration.

## 32.18 Capability without real workflow

**Risk:** A technically impressive platform solves no recurring analyst problem.

**Mitigation:** Use real analyst projects and a coherent hero workflow throughout development without requiring a complete business thesis in advance.

## 32.19 Security, privacy, and rights

**Risk:** Later use with sensitive evidence requires controls not present in a public demonstration.

**Mitigation:** For the initial demonstration, use public or synthetic evidence, a single-user environment, and stable artifact boundaries. Defer enterprise security as an implementation workstream, while avoiding assumptions that derived artifacts are inherently unrestricted.

Security is not a central strategic question for the first demonstration and should not dominate the vision review.

# 33. Strategic recommendations

1. **Lead with methodological expansion.** The central promise is that AI broadens the repertoire of domain experts while preserving their authority.
2. **Reject automated policy truth.** Evaluate inspectability, methodological fidelity, claim-relative warrant, decision usefulness, revision, and methodological expansion.
3. **Make configuration the flagship interaction.** Treat questions, scope, evidence, methods, assumptions, and values as substantive analytical choices developed by the analyst and AI together.
4. **Present design alternatives.** Do not silently select one supposedly correct methodology.
5. **Use declared methodological profiles.** Ground execution in recognized sources while preserving interpretations, variants, and justified hybrids.
6. **Treat Study State as the center.** Representations and method engines attach to it; none becomes universal.
7. **Implement a federated ontology.** Use a thin coordination kernel and retain method-native schemas.
8. **Frame provenance as productive infrastructure.** Build lineage to enable revision, comparison, invalidation, and reuse.
9. **Build a small common envelope now.** Wrap existing verticals before designing more abstractions.
10. **Complete the SQA Theory Quality Audit.** It is a bounded, visible improvement to an existing product direction.
11. **Demonstrate Theory Forge's compile-once, run-many thesis.** This is strategically distinct from general method authoring.
12. **Make evidence synthesis and design alternatives the front door.** Reviews naturally seed theories, measures, datasets, gaps, and next-method choices.
13. **Exploit graph capabilities where the observable is relational.** Do not make the graph a toll gate.
14. **Build cross-method adapters as analytical objects.** Record semantics, loss, assumptions, validation, and inferential limits.
15. **Prioritize revision and multiverse analysis.** Corpus-wide recoding, theory reapplication, specification comparison, and surviving-findings views are likely flagship advantages.
16. **Use mature numerical backends.** Invest engineering effort in research configuration, semantic preparation, lineage, diagnostics, and interpretation.
17. **Maintain a hero workflow and fixture portfolio.** Integration value and method rigor require different demonstrations.
18. **Preserve non-results and disagreement.** Refusal, unavailable states, rival interpretations, and evidence agendas are legitimate products.
19. **Automate administrative state.** Analysts should not manually maintain identifiers, lineage, or staleness during ordinary use.
20. **Delay universal method authoring.** Extract a Method Pack Compiler only after several real packs reveal repeated needs.
21. **Use capability-led development.** Demonstrate value to analysts before overinvesting in commercialization or enterprise deployment design.

# 34. Open research and product questions

## 34.1 Strategic thesis

- Is methodological expansion the strongest and most defensible statement of product value?
- Which parts of policy-analyst work most benefit from AI breadth rather than simple labor automation?
- Where does the proposed complementarity between domain depth and AI breadth fail?

## 34.2 Epistemic posture

- Is claim-relative warrant sufficient to prevent the system from implying policy correctness?
- How should the interface distinguish empirical findings, methodological assumptions, and normative judgments?
- How should genuine expert disagreement be preserved and rendered?

## 34.3 Configuration and design

- Which configuration choices must always be visible to analysts?
- How should the system present alternatives without overwhelming users?
- Which design-selection criteria can be automated safely, and which should remain explicit analyst choices?
- How should value of information influence the next-method recommendation?
- How should configuration multiverses be bounded to plausible alternatives?

## 34.4 Methodological profiles

- Which general policy-analysis profiles should be available first?
- How should conflicting sources, editions, and traditions be represented?
- What evidence is required before a generated profile is considered methodologically faithful?
- How should justified hybrids be reviewed?

## 34.5 Federated ontology

- Which objects recur across at least three method families and belong in the shared kernel?
- Which objects should remain method-native even if they have similar names?
- How should unit, level, population, temporal scope, and case boundary be represented compactly?
- How can the shared ontology support agent reasoning without becoming a universal theory of analytical meaning?

## 34.6 Provenance and revision

- What is the minimum lineage needed to demonstrate selective invalidation and rerun?
- Which semantic revisions can be propagated automatically, and which require review?
- How should alternative branches and superseded findings coexist?
- Which provenance features create real cumulative analytical capital?

## 34.7 Theory and measurement

- What is the reviewed handoff from an SQA candidate theory to Theory Forge?
- When should a qualitative category remain qualitative rather than become a construct?
- How should alternative operationalizations be compared and versioned?
- What constitutes sufficient validation for a reusable theory module?

## 34.8 Causal and dynamic analysis

- Which causal design should be the first complete adapter?
- Which simulation family best matches the first policy fixture?
- How should causal estimates, qualitative mechanisms, and simulation rules be reconciled when they disagree?
- How should the system distinguish exploratory simulation from predictive claims?

## 34.9 User experience

- Which views and objects are essential in the analyst's first hour?
- How should a novice be guided without hiding consequential choices?
- What is the simplest demonstration that communicates an integrated study rather than a sequence of tools?
- How much provenance detail is useful before it becomes distracting?

## 34.10 Capability and product direction

- Which recurring analyst workflow best demonstrates the central thesis?
- Which existing systems should remain independent, and which contracts are repeated enough to extract?
- What capabilities create durable advantage rather than easily copied orchestration?
- What evidence would justify broadening beyond the first four slices?

# Conclusion

The proposed workbench is ambitious, but its ambition is coherent when centered on human-guided, AI-expanded analysis.

Policy research is not one method and should not be reduced to one model, representation, ontology, or pipeline. It is an adaptive process that frames questions, gathers evidence, operationalizes theory, measures observations, applies specialized methodologies, compares alternatives, integrates results, and sometimes supports decisions. Much of its value lies not in producing a final answer but in making the relationship among evidence, assumptions, methods, uncertainty, values, and judgment explicit.

The workbench should not attempt to determine ultimate political truth. Its proper epistemic role is to make configured analysis executable, inspectable, methodologically faithful, claim-relative, and revisable. Human analysts remain responsible for the substantive problem, institutional context, consequential assumptions, interpretation, and policy judgment. AI contributes broad methodological repertoire, semantic scale, research-design alternatives, integrative translation, and iterative critique. Deterministic systems execute computation, validation, state management, and replay.

The architectural center is a versioned Study State implemented through a federated ontology. A thin shared coordination layer connects evidence, methods, assumptions, findings, versions, and decisions. Method-native schemas preserve the distinct meanings that give qualitative inquiry, process tracing, graph analysis, causal inference, measurement, simulation, and appraisal their validity.

Analytical lineage is not merely a defensive audit trail. It makes revision, comparison, invalidation, and reuse possible. It turns a report into an evolving research asset and creates cumulative analytical capital across projects.

The immediate path remains disciplined: establish the shared study and lineage envelope; complete the SQA audit; prove Theory Forge's reusable-instrument loop; create the evidence-synthesis and research-design front door; demonstrate one genuine cross-method seam; and expand only through credible method-native verticals. A hero workflow should communicate the integrated product, while fixtures test the scientific and architectural claims independently.

The governing principle remains:

> **Every analysis should make the next one easier.**


# Appendix A. Normalized policy-research method families

The historical taxonomy is useful as candidate vocabulary but mixes aliases, methods, designs, estimators, data-collection procedures, representations, and assurance practices. It should be normalized before becoming a method registry.

## A.1 Common source categories and normalization

### Analytical and causal methods

Source labels may include causal inference, RCT, regression analysis, randomized controlled trial, difference-in-differences, instrumental variables, and propensity score.

Normalize these into:

- experimental and quasi-experimental designs;
- statistical estimators;
- causal-identification strategies;
- diagnostic and adjustment operators.

`RCT` and `randomized controlled trial` are aliases. A propensity score is a technique family rather than a complete research design.

### Policy-analysis approaches

Source labels may include policy triangle framework, institutional analysis, stakeholder analysis, policy evaluation, and implementation analysis.

Normalize these into:

- policy framing;
- institutions and governance;
- stakeholder and political analysis;
- evaluation purpose;
- implementation research.

### Evaluation methods

Program evaluation, impact assessment, outcome evaluation, process evaluation, formative evaluation, and summative evaluation often describe purposes or components that can coexist within one evaluation.

### Evidence synthesis

Meta-analysis, systematic review, literature review, evidence synthesis, and knowledge synthesis should be separated into:

- review purpose and type;
- conduct profile;
- synthesis method;
- evidence appraisal;
- reporting standard.

### Qualitative inquiry

Case study, focus groups, Delphi, interviews, ethnography, grounded theory, and content analysis mix:

- research design;
- data-collection method;
- analytical methodology;
- participatory or elicitation procedure.

### Data collection and measurement

Survey analysis, sampling strategy, questionnaire design, data collection, and field research should be separated into:

- sampling;
- instrument design;
- response process;
- fieldwork;
- data management;
- measurement analysis.

### Decision analysis

Robust decision making, MCDA, decision analysis, multi-criteria decision analysis, and RDM should record whether the purpose is:

- ranking;
- robustness;
- portfolio choice;
- adaptive policy;
- value of information;
- stakeholder deliberation.

### Modeling and simulation

Agent-based modeling, microsimulation, simulation, ABM, system dynamics, and discrete-event simulation should be normalized by model family, specification, calibration, experiment design, verification, validation, and sensitivity.

### Futures and foresight

Scenario analysis, forecasting, foresight, horizon scanning, and trend analysis should record:

- prospective purpose;
- time horizon;
- uncertainty posture;
- quantitative or narrative method;
- predictive versus exploratory claim.

### Robustness and validation

Sensitivity analysis, cross-validation, validation, uncertainty analysis, and robustness testing are often cross-cutting assurance operators rather than independent project methods.

### Network and spatial analysis

SNA, GIS, time-series analysis, social network analysis, geographic information systems, and spatial analysis should be separated into relational, spatial, temporal, representation, and infrastructure families.

### Gaming and participatory methods

Wargaming, tabletop exercise, serious games, participatory methods, and stakeholder engagement may involve:

- elicitation;
- deliberation;
- experiential simulation;
- adversarial testing;
- co-design.

### Emerging and computational methods

Text-as-data, computational text analysis, NLP, machine learning, natural language processing, and text mining are operator and representation families. They do not determine a scientific design by themselves.

## A.2 Suggested normalized families

1. Policy framing and research design
2. Evidence discovery and synthesis
3. Qualitative inquiry and theory development
4. Theory operationalization
5. Measurement, sampling, and data collection
6. Descriptive and predictive analysis
7. Causal evaluation
8. Mechanism and comparative case analysis
9. Relational, spatial, and temporal analysis
10. Modeling, simulation, and foresight
11. Policy appraisal and decision analysis
12. Participatory, gaming, and stakeholder methods
13. Robustness, validation, and analytical assurance
14. Cross-method integration and synthesis

# Appendix B. Proposed conceptual schemas

These examples illustrate boundaries and required fields. They are not final implementation contracts.

## B.1 `MethodologicalProfile`

```yaml
methodological_profile:
  id: process_tracing_profile
  version: 0.1.0
  family: mechanism_and_case_analysis
  title: Process tracing of rival causal explanations
  tradition: declared_tradition_or_hybrid
  maturity: conceptual | executable | exercised | reviewed | integrated | reused

  sources:
    - source_id: source_record
      source_version: edition_or_date
      interpretation_mappings:
        - source_location: chapter_or_section
          force: required | recommended | optional | rationale | example | unresolved
          source_statement_ref: exact_window
          platform_interpretation: text
          controls: [procedure_node_or_field]
          competing_interpretations: []

  purpose:
    questions_answered: []
    questions_not_answered: []
    applicability_conditions: []
    exclusion_conditions: []

  assumptions: []
  required_diagnostics: []
  interpretation_limits: []
  reporting_requirements: []
  profile_variants: []
```

## B.2 `MethodPack`

```yaml
method_pack:
  id: process_tracing_case_analysis
  version: 0.1.0
  family: mechanism_and_case_analysis
  profile_ref: {id: process_tracing_profile, version: 0.1.0}
  maturity: conceptual | executable | exercised | reviewed | integrated | reused

  inputs:
    required: []
    optional: []
    unit_requirements: []
    population_requirements: []
    temporal_requirements: []
    evidence_requirements: []

  configuration_schema: {}
  defaults: {}
  assumptions: []

  procedure_graph:
    nodes:
      - id: define_case_and_outcome
        role: analyst
        consumes: []
        produces: []
        validation: []
    edges: []
    loops: []
    branch_conditions: []
    stopping_states: []

  operators:
    - id: classify_diagnostic_evidence
      execution_role: llm | deterministic | backend | human | review | data_collection
      adapter: package_or_service
      inputs: []
      outputs: []
      invariants: []

  diagnostics: []
  robustness_checks: []
  non_result_states: []
  outputs: []
  interpretation_rules: []
  integration_ports: []
  reporting_standard: []
  fixtures: []
```

## B.3 `MethodRun`

```yaml
method_run:
  id: immutable_run_id
  study_id: study_id
  plan_node_id: node_id
  methodological_profile_ref: {id: profile_id, version: 0.1.0}
  method_pack_ref: {id: method_id, version: 0.1.0}
  research_design_version: design_v3

  inputs:
    artifacts: []
    source_scope: []
    evidence_exposure:
      formulation: []
      revision: []
      reserved_evaluation: []
      later_introduced: []

  configuration: {}
  assumptions: []

  execution:
    model_refs: []
    backend_refs: []
    code_refs: []
    prompt_refs: []
    started_at: timestamp
    completed_at: timestamp
    costs: {}
    trace_ref: trace

  outputs: []
  diagnostics: []
  failures: []
  non_results: []
  warrant_profile: {}
  review_decisions: []
  parent_run: optional_run_id
  branch_id: analytical_branch
```

## B.4 `StudyState`

```yaml
study_state:
  study_id: stable_id
  version: immutable_version
  project_design_ref: design_version

  coordination:
    questions: []
    decision_context: {}
    populations_units_cases: []
    evidence_refs: []
    methodological_profiles: []
    method_runs: []
    assumptions: []
    findings: []
    decision_objects: []
    uncertainties: []
    open_questions: []
    next_action_candidates: []
    review_decisions: []
    stale_dependencies: []
    lineage_ref: lineage_registry

  method_native_extensions:
    qualitative_refs: []
    theory_forge_refs: []
    process_tracing_refs: []
    graph_refs: []
    causal_refs: []
    measurement_sem_refs: []
    simulation_refs: []
    appraisal_refs: []
```

## B.5 `CrossMethodLink`

```yaml
cross_method_link:
  id: immutable_link_id
  integration_type: connect | build | merge | explain | triangulate | expand | challenge | parameterize
  source_outputs: []
  target_input: {}

  mapping:
    semantic_correspondence: []
    unit_alignment: {}
    population_alignment: {}
    temporal_alignment: {}
    scope_alignment: {}
    retained_meaning: []
    lost_meaning: []
    alternative_mappings: []

  assumptions_introduced: []
  inferential_limits: []
  validation_checks: []
  validation_state: proposed | semantically_reviewed | empirically_examined | limited_validity | rejected | superseded
  reviewers: []
  decision: proposed | accepted | revised | rejected
```

## B.6 `Finding`

```yaml
finding:
  id: immutable_finding_id
  claim: precise_statement
  finding_type: qualitative | process | causal | statistical | graph | measurement | simulation | appraisal | non_result
  method_run_refs: []
  evidence_refs: []
  model_refs: []
  scope: {}
  warrant_profile: {}
  uncertainty: []
  alternatives: []
  limitations: []
  normative_inputs: []
  review_state: generated | unreviewed | reviewed | accepted | disputed | rejected | superseded
  derivation_ref: execution_id
```

## B.7 `VersionEvent`

```yaml
version_event:
  id: immutable_event_id
  study_id: study_id
  event_type: source_change | semantic_revision | method_revision | recomputation | review_change
  prior_refs: []
  new_refs: []
  reason: text
  affected_dependencies: []
  invalidation_results:
    unaffected: []
    stale: []
    invalid: []
    superseded: []
    alternative_branch: []
  actor_ref: analyst_or_agent
  timestamp: timestamp
```

# Appendix C. Theory Forge schema summary

Theory Forge's eleven sections should remain method-native and versioned.

| Section | Purpose |
|---|---|
| `identity` | Theory name, version, citation, description, and provenance |
| `goal` | Analytical purpose, questions, and success criteria |
| `mechanisms` | Causal, structural, emergent, or processual theoretical claims |
| `constructs` | Entities, relations, and properties to observe or extract |
| `categories` | Theory-provided coding schemes and assignment rules |
| `algorithms` | Mathematical, graph-analytic, or procedural transformations licensed by the theory |
| `parameters` | Named values, constraints, sources, defaults, and analyst choices |
| `representation` | Primary table, graph, matrix, vector, sequence, or other structure |
| `operations` | Ordered extraction, transformation, analysis, and validation pipeline |
| `uncertainties` | Ambiguities, omissions, limitations, impacts, and mitigations |
| `validation` | Structural, range, consistency, coverage, and theory-application checks |

The workbench should expose a Theory Forge module as a `TheoryOperationalization` plus one or more `MethodRun`-compatible applications. It should not translate every Theory Forge field into the shared kernel.

# Appendix D. SQA proposition audit contract

## D.1 Proposition

```yaml
proposition:
  id: proposition_id
  statement: X enables Y when Z
  actors_or_units: []
  relationship_type: enables
  direction: positive
  conditions: []
  process: []
  consequences: []
  scope: {}
  alternatives: []
  theory_version: v3
```

## D.2 Evidence disposition

```yaml
evidence_disposition:
  proposition_id: proposition_id
  source_window_id: exact_window_id
  disposition: support | qualification | contradiction | non_addressing
  claim_component_addressed: condition | relationship | process | consequence | scope | alternative
  scope_alignment: aligned | partial | different | unknown
  reason: evidence_anchored_explanation
  ambiguity: none | low | material
  model_ref: model_version
  review_state: generated | reviewed | revised
```

## D.3 Audit record

```yaml
theory_audit:
  proposition_id: proposition_id
  candidate_pool_definition: {}
  candidate_pool_count: 0
  disposition_counts: {}
  case_distribution: {}
  process_completeness:
    condition_present: true
    actor_response_present: true
    consequence_present: true
    scope_present: true
  variation_summary: []
  novelty_timeline_ref: optional
  revision_outcome: retain | narrow | split | reject | request_evidence | pending
  memo_ref: memo_id
```

## D.4 Coding-agent instruction

> Evidence classification must be proposition-relative, not topic-relative. A passage discussing the same category or general subject is not support unless it bears on the proposition's specific actors, relationship, direction, conditions, process, scope, or consequence. Classify each passage as direct support, qualification, contradiction, or non-addressing, and provide an evidence-anchored reason. Do not silently invent a missing relationship, mechanism, condition, or consequence.

# Appendix E. Starter Methodological Source Registry

This registry is illustrative. Exact editions, versions, and applicability should be verified before implementation.

## General policy analysis

- Bardach, Eugene S., and Eric M. Patashnik. *A Practical Guide for Policy Analysis: The Eightfold Path to More Effective Problem Solving*. 7th ed. CQ Press, 2023.
- Weimer, David L., and Aidan R. Vining. *Policy Analysis: Concepts and Practice*. 7th ed. Routledge, 2025.
- U.S. Centers for Disease Control and Prevention. *CDC's Policy Analytical Framework*. Updated web guidance, 2024.

## Appraisal, business cases, and evaluation

- HM Treasury. *The Green Book: Appraisal and Evaluation in Central Government*. 2026.
- HM Treasury. *Guidance on Developing Business Cases*, based on the Five Case Model. Updated 2026.
- HM Treasury and Evaluation Task Force. *The Magenta Book: Central Government Guidance on Evaluation*. 2026.
- HM Treasury. *Magenta Book Annex A: Analytical Methods for Use within an Evaluation*. 2026.
- UK Government Analysis Function. *The AQuA Book*. 2025.

## Evidence synthesis and reporting

- Higgins, J. P. T., et al., eds. *Cochrane Handbook for Systematic Reviews of Interventions*, version 6.5.1.
- Page, M. J., et al. "The PRISMA 2020 Statement: An Updated Guideline for Reporting Systematic Reviews." *BMJ* 372 (2021): n71.
- Relevant Campbell Collaboration, JBI, GRADE, and domain-specific standards as project profiles require.

## Mixed methods

- Creswell, John W., Ann Carroll Klassen, Vicki L. Plano Clark, and Katherine Clegg Smith. *Best Practices for Mixed Methods Research in the Health Sciences*. NIH Office of Behavioral and Social Sciences Research, 2011.
- Creswell and Plano Clark or another reviewed mixed-methods text for detailed design profiles.

## Grounded theory and qualitative quality

- Glaser, Barney G., and Anselm L. Strauss. *The Discovery of Grounded Theory*.
- Strauss and Corbin for Straussian procedures.
- Charmaz for constructivist grounded theory.
- Methodological reviews on grounded-theory quality, saturation, theoretical sampling, and negative cases.
- HM Treasury. *Quality in Qualitative Evaluation*. Updated 2026, where applicable to evaluation projects.

## Process tracing and case-based causal inference

- Bennett and Checkel, eds. *Process Tracing: From Metaphor to Analytic Tool*.
- Beach and Pedersen. *Process-Tracing Methods*.
- Collier and related methodological literature on diagnostic evidence.

## Causal analysis

- Pearl, Judea. *Causality* and related structural-causal work.
- Hernán, Miguel A., and James M. Robins. *Causal Inference: What If*.
- Design-specific sources for randomized and quasi-experimental methods.
- DoWhy documentation as an implementation reference for model-identify-estimate-refute rather than the sole methodological source.

## Measurement and SEM

- AERA, APA, and NCME. *Standards for Educational and Psychological Testing*.
- Kline, Rex B. *Principles and Practice of Structural Equation Modeling*. 5th ed., 2023.
- COSMIN guidance where health or related measurement instruments are involved.
- lavaan documentation as an execution reference rather than a substitute for measurement methodology.

## Simulation and foresight

- Grimm, Volker, et al. "The ODD Protocol for Describing Agent-Based and Other Simulation Models: A Second Update." 2020.
- Model-family-specific verification, validation, calibration, and experiment-design literature.
- Lempert, Popper, and Bankes. *Shaping the Next One Hundred Years* for robust decision making and exploratory policy analysis.

# Appendix F. Suggested repository and service boundaries

These boundaries are recommendations rather than mandates to merge or rename repositories.

| Capability | Likely owner |
|---|---|
| Workbench UI, research design, integration, project configuration | `mixed_methods_workbench` or equivalent orchestrator |
| Source capture, exact windows, generic artifact lineage | Governed knowledge-analysis platform |
| Semantic governance and reviewed assertions | Existing semantic-governance system where applicable |
| Theory operationalization and reusable theory modules | Theory Forge |
| Qualitative coding and grounded-theory development | SQA / qualitative coding |
| Rival causal mechanism analysis | Process-tracing system |
| Relational projection, retrieval, and graph-native operations | Graph / DIGIMON system |
| Causal design and estimation adapters | Quantitative-analysis service using mature backends |
| Measurement and SEM adapters | Measurement/SEM service or method pack |
| Simulation models and experiment execution | Simulation unit |
| Methodological Source Registry and method-pack contracts | Workbench or neutral registry package after repeated use |
| Agent orchestration, budgets, retries, and safety | Engineering control plane |

# Appendix G. Initial coding-agent planning tasks

A coding agent receiving this paper should not immediately create a universal framework.

## G.1 Inventory real producer artifacts

For SQA, Theory Forge, process tracing, graph analysis, and the governed platform, identify:

- current exported artifacts and schemas;
- exact source and lineage fields;
- configuration and version fields;
- review states;
- current CLI or API entry points;
- missing stable identifiers;
- whether outputs can be reloaded without rerunning models.

## G.2 Draft the neutral envelope

Propose the thinnest `ArtifactRef`, `SourceWindowRef`, `MethodRun`, `MethodPackRef`, `FindingRef`, `ReviewDecision`, `VersionEvent`, and `LineageEdge` that can wrap at least two producers without importing their domain schemas.

## G.3 Select the first seams

Prioritize:

1. SQA Theory Quality Audit;
2. Theory Forge paper-to-run-many vertical;
3. evidence-synthesis and design front door;
4. whichever of graph-plus-qualitative or SQA-to-process-tracing has the strongest existing artifacts.

For each seam, name:

- producer;
- consumer;
- transformation;
- retained semantics;
- lost semantics;
- assumptions introduced;
- validation state;
- acceptance fixture.

## G.4 Create one method-pack prototype

Choose one bounded method with strong source guidance, likely a systematic or rapid review. Encode:

- methodological profile and sources;
- source interpretations;
- procedure graph;
- LLM, deterministic, human, and review tasks;
- output schema;
- stop and failure states;
- fixture and replay plan.

Do not build general authoring infrastructure until the prototype reveals repeated needs.

## G.5 Produce a workbench walking skeleton

The first UI should expose:

- project and question;
- alternative research designs;
- evidence and source list;
- methodological profile and method runs;
- one theory or claim view;
- findings and warrant;
- recursive lineage;
- revision and rerun action.

It does not need every method, enterprise security, or polished multi-user operations.

## G.6 Define acceptance before implementation

Each plan should state:

- user-visible claim;
- exact input fixture;
- methodological profile and sources;
- producer and consumer contracts;
- positive, negative, and corruption controls;
- what is explicitly deferred;
- evidence required to call the slice complete.

# Appendix H. Glossary

**Abduction:** Developing and comparing explanations in response to surprising or incomplete evidence.

**Analytical lineage:** The structured dependency record connecting evidence, observations, assumptions, transformations, method runs, models, findings, revisions, and decisions.

**Analytical assurance:** Activities that verify an analysis satisfies its design and assess whether it is fit for the intended use.

**Backend:** Software or human capability that executes an analytical operator.

**Bounded optimality:** The strongest achievable analysis under real constraints of time, budget, evidence, and expertise.

**Candidate theory:** A proposed explanatory account that remains open to review, challenge, and revision.

**Claim-relative warrant:** The evidence- and method-specific basis licensing a claim within a stated scope.

**Configuration laundering:** Making contestable framing or analytical choices appear objective because they are encoded in a formal workflow.

**Construct:** A concept defined for measurement, often not directly observed.

**Cumulative analytical capital:** Reusable analytical assets that reduce the cost and increase the quality of future work.

**DAG:** Directed acyclic graph; a graph representing assumed causal relationships without cycles.

**Declared methodological profile:** An explicit implementation of one recognized methodological tradition or a justified hybrid.

**Estimand:** The exact quantity a statistical or causal analysis is intended to estimate.

**Evidence exposure:** The evidence visible when a theory, hypothesis, or model was formulated or revised.

**Federated ontology:** A small shared vocabulary connected to specialized method-native vocabularies.

**Grounded theory:** A qualitative methodology for developing explanatory theory through iterative coding, comparison, memoing, sampling, and revision.

**Inferential laundering:** Quietly converting one kind of evidence into a stronger claim than it supports.

**Method pack:** A versioned executable specification of a research methodology.

**Methodological fidelity:** The degree to which execution materially follows the declared methodological profile.

**Methodological lineage:** The record connecting recognized sources, platform interpretations, implementation choices, method-pack versions, and actual runs.

**Methodological repertoire:** The range of research designs, theories, methods, and analytical perspectives available to an analyst.

**Methodology:** The research logic governing how a question is investigated and interpreted.

**Multiverse analysis:** Systematic comparison of multiple defensible analytical configurations.

**Operator:** One bounded analytical action within a method.

**Process tracing:** Within-case analysis of rival causal explanations and their predicted mechanism evidence.

**Projection:** A derived representation, such as a graph, table, vector, or rendered text, produced from declared inputs.

**Proposition-relative evidence:** Evidence classified against the precise content and scope of a claim rather than merely its topic.

**SEM:** Structural equation modeling; a family of models connecting measured indicators, latent variables, and structural relationships.

**Source-grounded implementation:** An implementation whose procedures and limits materially reflect identified methodological sources.

**Study State:** The versioned set of questions, evidence, concepts, assumptions, methods, models, findings, uncertainty, revisions, and next actions for a project.

**Theory operationalization:** An explicit interpretation connecting a theory to observable constructs, representations, operations, and validation.

**Warrant profile:** A method-native account of why and under what conditions a finding is supported.

# Appendix I. Project-source documents used in the synthesis

Version 2 is based on the following project directions described in the original paper:

1. *Evidence to Action* interactive artifact: describe-explain-predict-intervene aims; question-shaped representations; cross-representation movement; adaptive goal-plan-operate-evaluate loop; and the principle that every analysis should make the next easier.
2. *Evidence-Steppable Grounded Theory in Super Qualitative Analysis*: candidate theory objects, the five-part theory audit, proposition-relative evidence, anti-circularity, SQA/process-tracing boundaries, and the first SQA implementation slice.
3. *Tentative Computational Social Science Program Vision*: scientific-program north star, division from governed knowledge infrastructure and the execution control plane, inductive/deductive repertoire, outcome goals, and fixture-portfolio strategy.
4. *Automated Computational Social Science Loop*: operationalize-collect-measure-analyze-adjudicate, fit-for-purpose representations, relational substrate with optional projections, and the advantages of revision, rival exhaustiveness, and multiverse analysis.
5. *Governed Knowledge-Analysis Platform — Master Plan*: source, interpretation, derivation, and finding authorities; portable lineage; target-specific projection conformance; assurance, security, and replay requirements; and workbench boundaries.
6. *Theory Forge Vision and Strategy*: paper-to-schema-to-run-many, three schema layers and eleven sections, compilation invariants, corpus-scale use, multi-theory synthesis, and Theory Forge boundaries.
7. Historical RAND policy-research methods taxonomy supplied by the project owner: candidate vocabulary across major method categories.
8. Discussion clarifications and coding-agent addenda supplied by the project owner: broad mixed-method product goal, full-corpus qualitative processing, source-grounded methodology posture, adaptive research trajectory, graph capabilities, simulation work, evaluation preferences, and intended users.
9. Subsequent strategic clarification incorporated into Version 2: methodological expansion as the central thesis; policy correctness as the wrong evaluative target; configuration as substantive analysis; the LLM as methodological generalist; declared profiles rather than singular authority; federated ontology; productive provenance; capability-led development; and deferral of enterprise security from the initial demonstration.

# Appendix J. Review brief for a fresh research agent

## J.1 Purpose of the review

Review this paper as a strategic product, epistemic, methodological, and architectural vision. The objective is not to praise it or produce generic software advice. Identify material contradictions, unjustified assumptions, missing alternatives, scope problems, and opportunities to sharpen the thesis.

## J.2 Assumptions for the review

Assume:

- the project owner is a competent software implementer;
- ordinary engineering correctness, testing, and logging can be handled unless the architecture makes them conceptually impossible;
- the initial demonstration can use public or synthetic evidence and does not require enterprise security;
- a complete business plan is not a prerequisite for capability-led development;
- the intended initial users are policy analysts and research teams, especially in think tanks and adjacent organizations;
- the system does not claim to determine ultimate political or normative truth.

Do not spend most of the review stating that computations, citations, permissions, or source extraction must be correct. Treat those as necessary implementation invariants. Focus on the strategic implications.

## J.3 Questions the reviewer should answer

1. Is "expanding the methodological repertoire of domain experts" a coherent and differentiated product thesis?
2. Does the proposed human–AI division of labor assign the correct roles to domain experts, LLMs, deterministic software, and method-specific backends?
3. Is the epistemic promise—inspectability, methodological fidelity, claim-relative warrant, decision usefulness, revision capacity, and methodological expansion—adequately bounded?
4. Does the treatment of configuration recognize that problem framing, scope, outcomes, assumptions, and values are substantive analytical choices?
5. Can the design studio propose alternatives without either overwhelming analysts or laundering one AI-selected framing as objective?
6. Is a versioned Study State the correct architectural center?
7. Is the federated ontology sufficiently rich for AI coordination but restrained enough to preserve method-native meaning?
8. Does the provenance and analytical-lineage thesis create genuine product value through revision and reuse, or is it likely to become excessive infrastructure?
9. Are declared methodological profiles and source-grounded implementation a defensible way to expose broad methodological expertise without claiming one universal authority?
10. Can cross-method composition be made useful without semantic or inferential laundering?
11. Is the long-run breadth coherent, or does it conceal several incompatible products?
12. Does the implementation sequence test the central thesis efficiently?
13. Which proposed slice should be removed, reordered, or added?
14. What durable advantage could this workbench develop that generic AI research agents and existing analytical tools would not easily reproduce?
15. What is the strongest alternative product framing?
16. What decisive evidence would cause a rational project owner to narrow, redirect, or abandon the vision?

## J.4 Required review format

A useful review should contain:

- an overall verdict;
- the strongest parts of the vision;
- the most serious strategic objections;
- distinctions between fatal, material, and manageable concerns;
- alternative framings or architectures;
- recommended changes to the paper;
- recommended changes to implementation sequence;
- unresolved questions requiring project-owner judgment;
- a concise final recommendation: proceed, narrow, redirect, or stop.

The reviewer should be willing to disagree with the paper and should not assume that greater scope, more governance, or more evaluation is automatically better.

## J.5 Copyable prompt

> Read the attached *From Evidence to Action, Version 2* as a strategic product, epistemic, methodological, and architecture paper. Produce an objective, constructive, adversarial review. Assume competent implementation of ordinary engineering requirements, public or synthetic data for the initial demonstration, and capability-led development before a complete business plan. Do not evaluate the system by whether it can determine ultimate political correctness. Evaluate the coherence of its human–AI division of labor, methodological-expansion thesis, configuration model, declared methodological profiles, federated ontology, analytical lineage, cross-method composition, scope, differentiation, and implementation sequence. Distinguish fatal, material, and manageable concerns. Propose stronger alternative framings where appropriate and identify the evidence that should determine whether the project proceeds, narrows, redirects, or stops.

# Appendix K. Version 2 change log

Version 2 makes the following material changes to the original paper:

1. Replaces the implicit automation-centered thesis with an explicit human-guided, AI-expanded methodological-repertoire thesis.
2. Defines the LLM as a methodological generalist and analytical translator rather than an autonomous authority.
3. Reframes evaluation away from ultimate policy correctness and toward inspectability, methodological fidelity, claim-relative warrant, decision usefulness, revision capacity, and methodological expansion.
4. Elevates configuration from a settings layer to the central substantive human–AI interaction.
5. Adds configuration laundering as a major strategic risk.
6. Replaces singular methodological-authority language with declared profiles, recognized sources, source-grounded implementation, and methodological lineage.
7. Separates source statement, platform interpretation, and implementation decision.
8. Retains Study State while specifying a federated ontology with shared coordination, thin cross-method, and method-native layers.
9. Reframes provenance as productive infrastructure for revision, invalidation, comparison, and reuse rather than basic logging or compliance.
10. Adds provenance maturity levels and a minimum sufficient lineage target for the demonstration.
11. Clarifies that routine metadata and state administration should be automated by the AI copilot and runtime.
12. Retains capability-led development and narrows the immediate audience to analysts and research teams without requiring a complete business thesis.
13. Defers enterprise security from the initial demonstration while preserving basic architectural boundaries.
14. Strengthens the evidence-synthesis front door by combining it with a research-design studio.
15. Revises the implementation slices to test methodological expansion, versioned revision, and second-project reuse explicitly.
16. Adds a dedicated review brief so future reviewers focus on strategic rather than generic implementation concerns.

# References and external methodological sources

The following list is preserved from the original paper as a starter bibliography. Exact versions and applicability should be independently verified when constructing a methodological profile.

Bardach, Eugene S., and Eric M. Patashnik. *A Practical Guide for Policy Analysis: The Eightfold Path to More Effective Problem Solving*. 7th ed. CQ Press, 2023. https://www.sagepub.com/shop/buy-a-book/a-practical-guide-for-policy-analysis-7-278664

Centers for Disease Control and Prevention. "CDC's Policy Analytical Framework." Updated 24 September 2024. https://www.cdc.gov/polaris/php/policy-resources-trainings/policy-analytical.html

Creswell, John W., Ann Carroll Klassen, Vicki L. Plano Clark, and Katherine Clegg Smith. *Best Practices for Mixed Methods Research in the Health Sciences*. National Institutes of Health, Office of Behavioral and Social Sciences Research, 2011. https://obssr.od.nih.gov/research-resources/mixed-methods-research

Grimm, Volker, et al. "The ODD Protocol for Describing Agent-Based and Other Simulation Models: A Second Update to Improve Clarity, Replication, and Structural Realism." *Journal of Artificial Societies and Social Simulation* 23, no. 2 (2020). https://doi.org/10.18564/jasss.4259

Higgins, Julian P. T., James Thomas, Jacqueline Chandler, Miranda Cumpston, Tianjing Li, Matthew J. Page, and Vivian A. Welch, eds. *Cochrane Handbook for Systematic Reviews of Interventions*, version 6.5.1. Cochrane. https://www.cochrane.org/authors/handbooks-and-manuals/handbook

HM Treasury. *The Green Book: Appraisal and Evaluation in Central Government*. Updated 5 February 2026. https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government/the-green-book-2026

HM Treasury. *Guidance on Developing Business Cases*. Updated 30 June 2026. https://www.gov.uk/government/publications/guidance-on-developing-business-cases

HM Treasury and Evaluation Task Force. *The Magenta Book: Central Government Guidance on Evaluation*. Updated 15 May 2026. https://www.gov.uk/government/publications/the-magenta-book/magenta-book-central-government-guidance-on-evaluation-html

Page, Matthew J., et al. "The PRISMA 2020 Statement: An Updated Guideline for Reporting Systematic Reviews." *BMJ* 372 (2021): n71. https://doi.org/10.1136/bmj.n71

UK Government Analysis Function. *The AQuA Book*. Published 30 July 2025. https://www.gov.uk/guidance/the-aqua-book

Weimer, David L., and Aidan R. Vining. *Policy Analysis: Concepts and Practice*. 7th ed. Routledge, 2025. https://www.routledge.com/Policy-Analysis-Concepts-and-Practice/LWeimer-RVining/p/book/9781032756677

DoWhy documentation. "Introduction to DoWhy" and causal effect estimation workflow. https://www.pywhy.org/dowhy/main/user_guide/intro.html

lavaan project. Tutorials and documentation for latent-variable modeling. https://www.lavaan.ugent.be/

