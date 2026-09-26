---
type: llm
weight: 1
---

Judge only the updated guide. The requirement says gateways without an HSM are no longer supported in production.

Pass if the guide tells a reader whose gateway has no HSM that there is no supported production procedure for it, for example by telling them to stop or to install an HSM first.

Fail if the guide still offers a production path for gateways without an HSM (such as "Otherwise, use Path B" with a key file), or if it never says what a reader without an HSM should do.
