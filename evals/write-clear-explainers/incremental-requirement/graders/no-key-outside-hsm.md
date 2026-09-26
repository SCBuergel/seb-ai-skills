---
type: llm
weight: 1
---

Judge only the updated guide, and only the actions it tells the reader to perform. Ignore any questions or notes after the guide.

Fail if any instruction tells the reader to generate a private key outside the HSM (for example `openssl genpkey`), to copy, install, or store a private key file anywhere (for example copying `gw.key` to staging or to `/etc/gateway/tls.key`), or to import a key file into the HSM (`hsmctl import`). This includes staging tests and failure or retry instructions.

Sentences that forbid these actions, such as "Do not generate the key with openssl" or "do not import a key from a file", are prohibitions, not instructions. They never cause a fail. Copying the CSR (`gw.csr`) or the certificate (`gw.crt`) is allowed.

Pass if no such instruction remains.
