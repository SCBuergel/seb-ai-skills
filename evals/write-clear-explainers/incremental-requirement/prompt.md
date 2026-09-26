---
max_turns: 6
allowed_tools: [Read, Skill]
tags: [write-clear-explainers, incremental-edit]
---

Our security review produced a new requirement. Please update the guide below so it follows the requirement, and return the complete updated guide.

New requirement from the security review:

> The gateway's TLS private key must be generated inside the gateway's hardware security module (HSM) and must never exist outside it, not even temporarily. Gateways without an HSM are no longer supported in production. The HSM can generate a key with `hsmctl genkey --label gw-tls` and create a certificate signing request with `hsmctl csr --label gw-tls --subj "/CN=pay.example.com" --out gw.csr`.

The current guide:

````markdown
# Rotate the payment gateway's TLS certificate

This guide replaces the TLS key and certificate on the production payment
gateway. The private key is created on the build host and copied only to
staging and the gateway, so it never leaves our infrastructure.

## Choose your path

If the gateway has an HSM, use Path A. Otherwise, use Path B, which stores
the key as a file.

## 1. Create the key and certificate request

On the build host:

```sh
openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-256 -out gw.key
openssl req -new -key gw.key -subj "/CN=pay.example.com" -out gw.csr
```

Send `gw.csr` to the certificate authority and save the returned
certificate as `gw.crt`.

## 2. Test on staging

Copy `gw.key` and `gw.crt` from the build host to staging, restart the
staging gateway, and check that
`curl -v https://staging.pay.example.com` shows the new certificate.

## 3A. Install with an HSM

On the gateway, import the key into the HSM:

```sh
hsmctl import --label gw-tls gw.key
```

Copy `gw.crt` to `/etc/gateway/tls.crt`, then delete `gw.key` from the
build host and staging.

## 3B. Install without an HSM

Copy `gw.key` to `/etc/gateway/tls.key` and `gw.crt` to
`/etc/gateway/tls.crt` on the gateway.

## 4. Verify

Restart the gateway and check that `curl -v https://pay.example.com`
shows the new certificate's expiry date.

If verification fails, return to step 2 and test again.
````
