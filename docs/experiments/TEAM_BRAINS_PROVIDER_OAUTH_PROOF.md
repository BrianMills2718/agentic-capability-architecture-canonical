# Tentative experiment: Team-Brains managed provider/OAuth proof

**Status:** proposed experiment; non-authoritative; no vendor adopted  
**Date:** 2026-09-12  
**Primary candidate:** Nango  
**Consumer:** `Inside-Success/Team-Brains`

## Question

Can Team-Brains preserve its current semantic tools, requester authorization, exact-action approval, and brain-owner/account-owner model while moving provider OAuth custody and token lifecycle out of custom code?

The experiment is intentionally narrower than an integration-platform migration. It tests whether a mature provider layer can replace OAuth/token plumbing for one real provider without changing the product's authorization semantics.

## Hypothesis

For one brain owner and one provider, Nango can own consent, credentials, token refresh, provider auth quirks, connection health, and authenticated provider execution while Team-Brains retains:

- brain-owner identity;
- per-message requester identity;
- owner/manager/teammate policy;
- exact-action approval and live revalidation;
- ACA semantic capability identity;
- audit/evidence at the Team-Brains boundary.

If true, the custom OAuth broker can be reduced by strangler migration rather than expanded provider by provider.

## Current implementation being tested

The current Team-Brains path owns several generic OAuth responsibilities:

- `knowledge/auth_broker/providers.py` — provider authorize URLs, token exchange, refresh, revoke and provider-specific quirks;
- `knowledge/auth_broker/store.py` — encrypted access/refresh-token storage, expiry, refresh, scope drift and disconnect semantics;
- `knowledge/auth_broker/server.py` — signed connect links, callbacks, token-serving endpoint and connection listing;
- provider callers in `knowledge/mcp_server/server.py` consume the resulting fresh credentials.

This proof does **not** target `knowledge/mcp_server/mcp_oauth.py`; remote-MCP client authentication is a separate follow-up decision.
## Mapping to Nango

| Team-Brains responsibility | Tentative Nango replacement | Team-Brains remainder |
| --- | --- | --- |
| Build provider authorize URL / callback | Nango Connect session + hosted/embedded Connect UI | generate owner-scoped connect request and record completion |
| Store access and refresh tokens | Nango connection credential store | store only stable provider/integration + connection identifier and non-secret health metadata |
| Refresh expiring/rotating tokens | Nango managed token lifecycle | handle connection-needs-reauth as a product state |
| Provider-specific exchange quirks | Nango provider integration | only capability-specific semantics that Nango cannot honestly express |
| Serve raw fresh tokens through `/token/{provider}` | Nango proxy/action/MCP execution | preferably remove raw-token delivery from Team-Brains entirely |
| Disconnect/revoke bookkeeping | Nango connection deletion/revocation behavior | owner-facing intent, audit result, and honest distinction if upstream revocation is unavailable |
| Connection-to-person binding | Nango connection ID plus `end_user_id`/tags | canonical brain owner remains Team-Brains identity |

Nango's runtime model fits the required split if the stable Nango connection belongs to the **brain owner**, not the current requester. The current requester remains an independent Team-Brains policy input.

```text
Dagim asks Brian's brain
        |
requester = Dagim --------> Team-Brains policy gate
        |                         |
        |                      allow/deny
        v                         v
Brian's brain -----------> ACA semantic action
                                  |
                           Brian-scoped Nango connection
                                  |
                          external provider account
```

The Nango secret key remains backend/service material and must not be exposed to the model. If MCP is used, the provider/config and connection headers must be fixed to the brain-owner connection or injected by a trusted adapter, never selected from conversational text.

## First provider and capability

Use **Google Calendar / `availability.query`** first.

Reasons:

- existing ACA semantic action is already verified;
- read-oriented behavior gives a low-risk auth/custody test;
- Team-Brains already has per-person Google OAuth and calendar behavior;
- success can be compared against an existing working implementation;
- it exercises owner-scoped provider identity without immediately testing outward side effects.

A second phase may test `notification.email.send` or another approved outward action only after the read path proves connection correctness.
## Proof sequence

1. Create a Nango Google integration with the minimum Calendar scopes needed by the existing read path.
2. Create one Connect session tagged/mapped to the selected brain owner; complete OAuth as that owner.
3. Record only the resulting stable connection reference in the experiment adapter; do not copy provider access or refresh tokens back into Team-Brains.
4. Implement a narrow provider adapter for the existing availability behavior using Nango authenticated execution.
5. Keep the existing direct-Google implementation intact behind an experiment switch so both paths can be exercised against the same owner/calendar.
6. Run the same semantic acceptance cases against direct Google and Nango.
7. Exercise token expiry/refresh, revoked access, narrowed/changed scopes, reconnect, and provider failure.
8. Exercise delegated access: owner request and non-owner request must produce the same authorization result as today before either provider path executes.
9. Capture latency, errors, custom LOC, operational steps, connection-selection failures, and observability from both paths.
10. Decide using ACA's net-value rule; do not migrate a second provider until this one has a clear result.

## Required acceptance cases

The Nango path passes only if all of these hold:

- the exact intended brain-owner Google account is selected deterministically;
- no Google access token or refresh token is persisted in Team-Brains for the experiment connection;
- access still works after ordinary token expiry/refresh without Team-Brains refresh code;
- revoked/invalid access produces an actionable reconnect state rather than silent fallback;
- a requester cannot select another person's connection through prompt/tool arguments;
- the current Hermes requester gate runs before any provider execution and preserves current owner/manager/teammate behavior;
- `availability.query` results are semantically equivalent enough for existing consumers, with provider-specific limitations recorded;
- provider errors are visible and attributable to the semantic action and selected provider;
- the direct implementation remains a clean rollback path during the experiment;
- replacing the broker creates concrete net value after vendor dependency, operations, cost, and adapter complexity are counted.

## Negative controls

Deliberately test the failure modes that matter most:

- use Dagim as requester against Brian's brain and verify the connection remains Brian's while policy remains Dagim's;
- attempt to pass a different connection ID from model-controlled input and verify it is ignored/rejected;
- revoke the Google grant and verify the next call cannot silently use stale local credentials;
- alter required scopes and verify the system exposes reauthorization/insufficient-scope state;
- disconnect and reconnect the same owner and verify the canonical mapping cannot drift to another person;
- remove/disable the experiment mapping and verify the path fails closed or rolls back explicitly, never by guessing a connection.

## Evidence to capture

Record at least:

- lines/files of custom OAuth code bypassed by the experiment;
- secrets removed from Team-Brains custody;
- connection setup/reconnect steps;
- provider-specific code still required;
- median and tail latency for the semantic action;
- auth/refresh/revocation failure behavior;
- logs/audit evidence available from Nango and Team-Brains;
- context/tool-schema cost if MCP is used versus a direct adapter/action call;
- vendor/runtime dependency and exit strategy;
- rejected-fit evidence if Nango is not better.
## Retirement decision after proof

A successful first proof does not authorize deleting the broker wholesale. It creates a provider-by-provider retirement path.

**First deletion candidates after equivalent behavior is proven:**

- selected-provider token rows and refresh logic in `auth_broker/store.py`;
- selected-provider exchange/refresh special cases in `auth_broker/providers.py`;
- selected-provider callback handling in `auth_broker/server.py`;
- raw `/token/{provider}` dependency for the migrated capability.

**Keep until separately replaced:**

- requester identity and pre-tool authorization;
- owner-facing connection semantics/audit;
- provider-specific capability logic that remains semantically necessary;
- non-provider internal secrets such as Team-Brains service credentials;
- remote-MCP authorization server (`mcp_oauth.py`), which solves a different trust boundary.

## Decision rule

Adopt the managed path for this capability only if it is at least as correct and secure as the direct path and materially reduces custom credential/provider plumbing after all integration cost is counted.

Reject or defer Nango if:

- owner/connection identity is difficult to bind safely;
- managed execution hides failure details needed for safe behavior;
- scope/reconnect behavior is worse than the current implementation;
- the adapter becomes a second integration framework;
- cost/operations/vendor dependency exceeds the removed burden;
- direct Google remains materially simpler for this actual capability.

## Follow-up only after a pass

If the Calendar proof passes, run a consequential-action proof using the existing immutable approval/revalidation path. Then compare whether the same provider substrate can safely support Gmail, Monday, GitHub, Notion, and Slack before deciding whether the custom broker should be retired broadly.

Do not combine this proof with remote-MCP auth replacement, authorization-engine adoption, durable-workflow migration, or telemetry migration. Those have separate falsifiable questions and should remain independently reversible.
## Implementation scaffold status — 2026-09-12

A disabled-by-default Team-Brains scaffold has now been implemented locally against current `origin/main` in branch `experiment/nango-oauth-proof-scaffold-20260912`.

- `563d409` adds the owner-bound Nango connection resolver, Connect Session client, proxy transport, and focused negative tests.
- `ce460f0` updates Connect Sessions to use Nango connection `tags` (`end_user_id`, `end_user_email`, `end_user_display_name`) rather than the deprecated `end_user` object, and adds a Google Calendar `freeBusy` proxy seam.
- the free/busy seam preserves the upstream `calendars` object including per-calendar errors; Team-Brains retains attendee resolution, unreadable-calendar policy, working-hours calculation, requester authorization, audit, and final response shaping.
- focused verification: 8 tests pass; ruff, mypy, and `git diff --check` pass.

The scaffold is not imported by the Team-Brains MCP server and changes no production routing, settings, credentials, or deployment. Publishing is currently blocked because the authenticated GitHub identity has read-only permission on `Inside-Success/Team-Brains`; the two commits and a generated patch are retained locally until an authorized write path exists.
