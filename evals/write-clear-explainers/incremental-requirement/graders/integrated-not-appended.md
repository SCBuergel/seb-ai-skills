---
type: llm
weight: 1
---

Judge the updated guide and any notes or questions that follow it.

Pass only if all three are true:

1. The requirement is built into the steps: the key and certificate request are created with `hsmctl genkey` and `hsmctl csr` as given in the requirement. A guide that keeps the old steps and only adds a warning fails.
2. The staging test is not kept in a form that needs the production private key. Removing it, or replacing it with something clearly marked as an open question or proposal, passes.
3. It does not present invented `hsmctl` subcommands (anything other than `genkey`, `csr`, `import`) or invented flags as established instructions. Mentioning such options as open questions is fine.
