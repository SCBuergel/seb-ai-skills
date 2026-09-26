---
type: llm
weight: 1
---

Judge only the updated guide. Pass only if both checks pass.

1. The introduction no longer states, without exception, that every USB device is first handled by `usb-vm`. It must be consistent with the reader never being handled by `usb-vm`.
2. The failure instructions for "card not shown" and "card removed" do not use `usb-vm` for the reader and do not send the reader to a step that does. Pointing to a step that is valid under the new requirement, or explicitly flagging that the recovery procedure needs to be defined, passes.
