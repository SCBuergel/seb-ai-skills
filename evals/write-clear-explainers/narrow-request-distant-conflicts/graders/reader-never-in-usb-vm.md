---
type: llm
weight: 1
---

Judge only the updated guide and the actions it tells the reader to perform. Ignore notes or questions after the guide. Sentences that forbid an action ("never plug the reader into...") are prohibitions, not instructions, and never cause a fail.

Fail if any instruction, anywhere in the guide, would put the smartcard reader on a USB port or controller handled by `usb-vm`, or have `usb-vm` handle it. Check all of these:

- the one-time discovery step (the original says to plug the reader into "any USB port" and run `lsusb` in `usb-vm`);
- the shared path (`vmctl usb attach sign-vm usb-vm:076b:3031`);
- the failure handling (`vmctl usb detach sign-vm usb-vm:076b:3031`, then replugging).

"Plug the reader into any USB port" fails unless the guide has made clear that the port must belong to the controller assigned to `sign-vm`.

Pass if none of these survive as instructions.
