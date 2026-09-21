# A1 Brownfield Portability Audit — Product N TwitterAPI.io Boundary

Plan: ACA-PLAN-002, stage A1.
Recorded: 2026-09-21.
Status: technical portability audit complete; retained publication artifact and publication/source-change authorization unresolved.
ACA baseline: canonical main after PR #63 (bb7c767).
Product N repository: private GitHub repository Inside-Success/twitter-prospecting.
Inspected Product N revision: ab2cfba0e8c43f0198716dee4414dedf2212d478.

This audit does not copy Product N source into ACA, modify Product N, publish an artifact, or authorize scored A2/A3 runs. It tests whether the pre-existing implementation is portable as-is and whether a bounded consumer-blind publication-only normalization appears technically sufficient.

## 1. Boundary under test

The pre-existing Product N implementation is apps/twitter_prospecting/twitter_client.py::TwitterApiIoClient plus SearchCollection and its typed model contracts from apps/twitter_prospecting/models.py.

The meaningful behavior for ACA-PLAN-002 T1 is TwitterApiIoClient.collect(...), not only its one-request search(...) helper.

At the inspected revision, collect(...):
- executes multiple search queries independently;
- retains a QueryExecution disposition for every requested query;
- allows one query to fail while successful queries survive;
- records failed-query errors as warnings;
- isolates malformed post/author data as warnings;
- aggregates posts by normalized author identity and post ID;
- records matched query labels;
- deterministically ranks then truncates to candidate_limit;
- returns SearchCollection(candidates, executions, warnings).

The Product N focused test tests/twitter_prospecting/test_twitter_client.py::test_collect_isolates_failed_query_and_malformed_post directly exercises the partial-failure and malformed-post behavior.

## 2. Provenance and repository state

Observed through the authorized GitHub/local checkout:
- remote: https://github.com/Inside-Success/twitter-prospecting.git
- visibility: PRIVATE;
- default branch: main;
- local revision: ab2cfba0e8c43f0198716dee4414dedf2212d478;
- local checkout was clean and matched origin/main when inspected;
- GitHub reports licenseInfo: null;
- no tracked LICENSE, COPYING, or NOTICE file was found.

Therefore technical access is verified; redistribution/publication rights are not inferred from repository access. Before committing Product N code to another repository, publishing a wheel, or changing Product N packaging, the source owner/authorized user must confirm the intended reuse scope.

twitter_client.py was introduced in commit 78cefdf on 2026-07-24 ("Initial standalone Inside Success prospecting app"). Its follow-history showed no later file-specific commit at the inspected checkout. Related model contracts evolved in later commits.

The Product N evidence directory records shared llm_client revision 5d8632fb30ee241d98de527c5308ba9c265751b3, and that commit exists in the local llm_client repository.

Content hashes at the inspected Product N revision:
- twitter_client.py: a9be9aabcd5dd8be0a688c07313e0ef71d4b446e12f20d1cdd435ec907df468e
- models.py: aef6fa1dd7263fbb04a4ec246e472b8260c45cf54673f319762fbd4b62ff0149

## 3. As-is brownfield portability result

### 3.1 No installable package boundary

The repository has requirements.txt but no root pyproject.toml, setup.py, or setup.cfg.

A clean temporary virtual environment attempted pip install --no-deps against the Product N repository.

Result:
ERROR: Directory .../twitter-prospecting is not installable. Neither setup.py nor pyproject.toml found.

Classification: publication/package-shape debt, not provider behavior failure.

### 3.2 Clean external import fails

From /tmp, outside Product N and without a sibling-path injection, importing apps.twitter_prospecting.twitter_client failed with ModuleNotFoundError: No module named 'apps'.

Classification: no distributed/importable artifact exists.

### 3.3 Narrow provider import is coupled through package initialization

Product N apps/twitter_prospecting/__init__.py eagerly imports ProspectingAgent. Importing the twitter client submodule therefore executes the package initializer and imports agent.py, which imports shared llm_client.

Running the focused Twitter-client test in the ordinary user environment failed before collection code executed because the available llm_client import surface did not expose the `call_llm_structured`, `get_model`, and `render_prompt` symbols that Product N's `agent.py` imports.

This is package initialization/dependency coupling. It is not evidence that TwitterApiIoClient itself needs the LLM client.

Product N already documents the full application test dependency through PYTHONPATH plus LLM_CLIENT_PATH rather than requirements.txt.

## 4. Original-consumer regression under its documented shared dependency

A detached local llm_client worktree was created at Product N's recorded revision:
5d8632fb30ee241d98de527c5308ba9c265751b3

Product N's focused test was then run with the Product N checkout plus that pinned llm_client checkout on PYTHONPATH.

Result:
1 passed in 0.01s

This establishes that the inspected Product N client behavior remains green under the shared dependency revision Product N itself recorded. It does not make the provider boundary independently distributable.

## 5. Local publication-only feasibility test

To distinguish substantive coupling from publication debt, A1 created a temporary local artifact under /tmp only. No Product N or ACA source was changed.

The temporary artifact contained:
- the exact Product N twitter_client.py;
- the exact Product N models.py;
- a minimal package initializer exporting SearchQuery, SearchCollection, TwitterApiError, and TwitterApiIoClient;
- ordinary package metadata declaring requests and pydantic.

No provider behavior, collection behavior, error policy, model implementation, consumer-specific fields, or hidden evaluator logic was changed.

The copied source files were byte-identical to Product N:
- twitter_client.py source and bundle sha256: a9be9aabcd5dd8be0a688c07313e0ef71d4b446e12f20d1cdd435ec907df468e
- models.py source and bundle sha256: aef6fa1dd7263fbb04a4ec246e472b8260c45cf54673f319762fbd4b62ff0149

The temporary package built a wheel and installed it into a clean virtual environment. Execution occurred from /tmp, not from Product N and with no Product N PYTHONPATH.

The synthetic-provider test exercised:
- two queries;
- one successful query;
- one HTTP 503;
- one malformed post missing its author;
- surviving successful candidate output;
- two retained query dispositions;
- warnings for malformed data and the failed provider call.

Observed:
A1_TEMP_BUNDLE_PASS
1 candidate, 2 query executions, 2 warnings.

The installed module path was under the temporary environment's site-packages. The retained verification recipe is `docs/experiments/cross-repo-reuse/a1_temp_publication_check.sh`; it reads the two source files directly from the pinned Product N Git revision, verifies their expected hashes, creates only an ephemeral `/tmp` package, runs the synthetic-provider check, prints the artifact/environment evidence, and deletes the temporary private source on exit.

Reproduced runs used Python 3.12.3, requests 2.34.2, pydantic 2.13.4, setuptools 68.1.2, and wheel 0.48.0. The recipe produced `inside_success_twitter_provider_a1-0.0.0+a1.ab2cfba-py3-none-any.whl`, 9,442 bytes. Per-build wheel hashes differed across repeated ephemeral builds (`a9b64616...` then `dfc290ac...`) despite identical pinned source hashes, so the temporary build is **not** claimed reproducible at the artifact-byte level. A retained publication artifact would need its exact build hash frozen after authorization. The wheels and temporary private source were not retained, committed, uploaded, or distributed.

## 6. Interpretation

Verified:
1. As-is Product N is not publication-ready: no installable package, clean import fails, and the package initializer drags the provider client through the full agent/llm_client dependency.
2. The byte-identical `twitter_client.py` and `models.py` execute successfully from a separately installed temporary package that does not import `ProspectingAgent` or `llm_client`; this is the evidence that the retained provider logic is not intrinsically coupled to the LLM/agent runtime. The focused original Product N test passing at the recorded shared `llm_client` revision separately confirms the source product remains green at the inspected dependency snapshot.
3. A bounded publication-only normalization appears technically feasible: ordinary package metadata plus a lightweight import surface were enough for the local proof, with no substantive provider/client code change. Active publication engineering time was not instrumented precisely in A1, so this audit does not claim the normalization is economically "small"; ACA-PLAN-002 requires that cost to be measured before any economics conclusion.
4. This is evidence of publication debt, not evidence that ACA needs a runtime, schema language, or registry service.
5. The models boundary is broader than the collection capability needs. The temporary proof copied the whole `models.py`, which contains unrelated prospecting/application contracts. Any retained redistribution would therefore need authorization covering both `twitter_client.py` and the copied model definitions; narrowing that surface would be a source-owner design change and is not necessary to demonstrate technical feasibility.

Not established:
- authorization to redistribute Product N source or publish an artifact outside the private repository;
- a durable/versioned production package;
- compatibility across a future Product N change;
- Product N+1 delivery economics;
- fresh-agent discovery/selection;
- any live provider call in A1;
- any effectful behavior.

## 7. A1 gate status

| Gate | Status |
| --- | --- |
| Exact source revision and hashes recorded | PASS |
| As-is external install attempted | PASS — correctly failed; packaging absent |
| As-is clean import attempted | PASS — correctly failed; no distributed package |
| Brownfield coupling classified | PASS — packaging + eager package-init/shared-dependency coupling |
| Original-consumer focused regression at recorded shared dependency | PASS — 1 test |
| Consumer-blind publication-only feasibility demonstrated locally | PASS |
| Source-free verification recipe retained in ACA | PASS — recipe reads pinned private source at run time and cleans `/tmp`; wheel bytes are not yet deterministic |
| Provider/client source unchanged in feasibility proof | PASS — hashes identical |
| Product N source modified | NO |
| Product N code copied into ACA | NO |
| Retained/versioned artifact available to A2 consumer | NOT MET — feasibility wheel was ephemeral and deleted |
| Artifact published/distributed | NO |
| Rights/authorization for cross-repo publication | OPEN |

A1 technical conclusion: the pre-existing capability appears independently installable after conventional publication/export normalization. The current Product N architecture imposes measurable publication debt (no package boundary plus eager package-init coupling), but the audit has not found substantive provider-logic coupling that would justify new ACA infrastructure. A1's retained-artifact exit gate remains open until publication rights are confirmed and an authorized pinned artifact or source-owner package is produced.

A1 authorization gate: before a Product N source PR or any retained/distributed artifact is created, confirm that the user is authorized to modify/repackage/reuse code from the private Inside-Success/twitter-prospecting repository for this ACA experiment.

## 8. Next action after authorization

If authorization is confirmed:
1. make the smallest publication-only source-owner PR, or use an already-approved private artifact mechanism;
2. preserve twitter_client.py provider semantics and keep consumer-specific behavior out;
3. add package/install metadata and a lightweight import surface without pulling in ProspectingAgent;
4. run Product N regression tests against its documented llm_client revision;
5. build a hashed private artifact;
6. install/invoke it from a clean repository;
7. freeze that artifact before A2 scored workers see it.

If authorization is not confirmed, stop this candidate and retain A1 as a valid publication-rights failure. Do not package the P3 wrapper and call that Product N reuse.
