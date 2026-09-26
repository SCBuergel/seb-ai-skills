---
type: llm
weight: 1
---

Judge only the updated guide, plus any list of open questions that directly follows it. Pass only if both checks pass.

1. Introduction: fail if it still says the key is created on the build host or copied to staging or the gateway. Pass if it says the key is generated in and stays inside the HSM, or makes no claim about where the key is created.

2. Failure handling in the verification step: fail if it sends the reader back to a step that needs a copy of the private key (such as the old staging test) or to any step that no longer exists. Pass if it points to a step the reader can actually repeat, says what must be redone, or explicitly states that no retry or recovery procedure is established yet (for example "stop and escalate; this guide does not yet define a recovery procedure").
