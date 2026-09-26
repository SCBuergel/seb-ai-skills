---
type: llm
weight: 1
---

Judge only the updated guide.

Under the new requirement, the shared path can no longer be used for the reader, so a laptop with a single USB controller has no documented way to use the reader.

Pass if the guide no longer routes single-controller laptops onto a path that puts the reader through `usb-vm`, and it tells those readers that no supported path applies (or explicitly flags that one must be defined) and what would have to change, such as a second controller.

Fail if it still says "Otherwise, use the shared path" for the reader, still says the laptop "qualifies for one of two paths" without qualification, or never says what a single-controller reader should do.
