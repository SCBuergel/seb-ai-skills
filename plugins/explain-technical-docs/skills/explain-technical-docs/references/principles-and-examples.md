# Principles and diagnostic examples

## Published guidance

Reviewed 2026-09-26. The workflow in SKILL.md is a synthesis, not a validated universal prompting recipe.

- [Google: Using LLMs in technical writing](https://developers.google.com/tech-writing/two/llms). Specify audience, document type, reader goal, source context, and constraints. Use examples to communicate style, iterate, and address organization before copy editing. This directly supports giving AI a concrete writing task rather than simply asking it to sound human.
- [Google: Audience](https://developers.google.com/tech-writing/one/audience). Account for what readers already know and their familiarity with the particular subject. Technical expertise alone does not establish project knowledge.
- [Diataxis: Explanation](https://diataxis.fr/explanation/). Develop understanding through context, connections, reasons, and examples. Keep explanation bounded instead of letting it absorb procedural and reference material.
- [Google: Procedures](https://developers.google.com/style/procedures). Put actions in execution order, state where actions happen, separate alternative procedures, and avoid introductory sentences that merely repeat headings.

## Patterns observed in a QR-transfer guide

Use these as diagnostic illustrations, not mandatory structures for other domains. These observations concern readability, not verification of the security design.

| Evidence | Reader burden | General instruction |
|---|---|---|
| A guide says 'Read the guide in order', then tells readers to finish encryption 'as described later'. | The reading sequence differs from the action sequence. | Order prerequisites before dependent steps and walk through each branch end to end. |
| Separate controller-operation sections precede a transfer section that includes receiving steps. | The reader must assemble a workflow from overlapping sections. | Separate setup from operation and make branch entry and rejoin points explicit. |
| A list mixes trusted roles, templates, named disposables, and hardware backends. | Different levels of abstraction look like equivalent peers. | Explain roles and relationships before introducing an implementation inventory. |
| USB is expanded to 'Universal Serial Bus', while 'recipes' and 'commit-bound runner' rely on project knowledge. | Explanation is allocated to familiar vocabulary while unfamiliar assumptions remain implicit. | Define the reader's knowledge gap rather than expanding every acronym. |
| 'This subsection receives the ciphertext after the sequential power-off' follows a heading already identifying that task. | Signposting consumes attention without adding information. | Retain introductions only when they add purpose, conditions, or context. |
| 'Conditional 2-of-2 confidentiality property' and 'cold-power boundary' lead with compressed abstractions. | Readers must unpack a label before understanding the concrete mechanism. | Explain what is separated or what action is required, then introduce a needed formal label. |
| Commands say 'In dom0' in a guide with two computers. | A local environment label may not identify the physical machine. | State machine and environment when both matter. |
| One passage relies on complete power removal, while an operational step says remove standby power 'where practical'. | The reader cannot determine the exact requirement. | Flag inconsistent obligation or scope; do not silently resolve technical uncertainty as an editorial change. |

## Calibration examples from other domains

Weak: 'The reconciliation subsystem provides eventual consistency.'

More useful, if supported by the source: 'The worker periodically compares the requested configuration with the running service and applies missing changes. Updates may therefore take effect after a delay. This behavior is called eventual consistency.'

The improvement comes from the actor, mechanism, and consequence, not simply from word substitution. Do not invent the mechanism to make a label easier to explain.

Weak: 'This section explains how to inspect replication status.'

More useful: 'On the replica, check how far replication is behind the primary.'

The improvement adds location and purpose. Keep a longer explanation if readers also need to know what lag means or which value is acceptable.

## Evaluate the skill

Compare assisted and unassisted outputs on the same task and source. Use questions with concrete answers: What is the system trying to do? Why does a component exist? Which path applies? Where is the next action performed? What observation means stop?

Check both comprehension and preservation of technical requirements. A shorter document that loses a prerequisite fails. An AI self-review or independent model review is a preliminary check, not a substitute for observing representative readers.
