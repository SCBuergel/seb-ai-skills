---
max_turns: 6
allowed_tools: [Read, Skill]
tags: [write-clear-explainers, incremental-edit]
---

The security review found that `usb-vm` must never handle the smartcard reader, because `usb-vm` also parses untrusted USB sticks. Please add this requirement to step 3 of our guide and return the complete updated guide.

````markdown
# Sign release artifacts on the offline laptop

The offline laptop signs release artifacts with a key stored on a
smartcard. `usb-vm` owns the laptop's USB controllers, so every USB device
is first handled there. `sign-vm` has no network access and holds the
signing tools. Artifacts arrive on a USB stick, and the signatures leave on
the same stick.

Commands starting with `vmctl` run in the admin console. All other commands
run in the VM named in the step.

## 1. Find the reader's device ID (one time)

Plug the smartcard reader into any USB port. In `usb-vm`, run `lsusb` and
note the reader's ID, for example `076b:3031`. Step 3 uses it.

## 2. Choose your path

Your laptop qualifies for one of two paths:

- **Two-controller path:** if the laptop has two USB controllers, assign the
  second controller to `sign-vm` in the VM settings. Devices plugged into
  its ports appear directly in `sign-vm`.
- Otherwise, use the **shared path:** both the reader and the stick go
  through `usb-vm`, and you attach them to `sign-vm` one at a time.

## 3. Attach the reader

- Two-controller path: plug the reader into a port on the second
  controller.
- Shared path: plug the reader into any port, then run
  `vmctl usb attach sign-vm usb-vm:076b:3031`.

In `sign-vm`, run `gpg --card-status`. It should show the card's serial
number.

## 4. Copy the artifacts in

Plug in the USB stick and attach it with
`vmctl usb attach sign-vm usb-vm:<stick-id>`. In `sign-vm`, mount it and
copy the artifacts to `~/in`.

## 5. Sign

In `sign-vm`, run `gpg --detach-sign` on each file in `~/in`.

## 6. Copy the signatures out

Copy the `.sig` files to the stick, unmount it, and run
`vmctl usb detach sign-vm usb-vm:<stick-id>`.

## If something fails

- If `gpg --card-status` does not show the card, run
  `vmctl usb detach sign-vm usb-vm:076b:3031`, unplug and replug the
  reader, and repeat step 3.
- If signing fails with "card removed", repeat step 3.
````
