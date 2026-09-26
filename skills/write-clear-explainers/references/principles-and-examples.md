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
| A first revision reworded 'This subsection...' openers to 'This step...' instead of deleting them. | The scaffolding survived under new wording. | Apply the heading test: delete an opener that only paraphrases its heading. |
| The limits of power removal were explained only after the step that scans and powers off. | The reader learns whether the path was acceptable after committing to it. | Put suitability limits before the choice; repeat only the operational warning at the action. |
| A simplification turned a list of untrusted qubes into 'every qube that handles the data', which included a trusted one. | The claim now contradicts the trust model. | Compare claim scope with the source after simplifying. |
| Setup said 'edit the configuration' without saying it must be committed; the build tool reads only committed state. Found only by reading the tool's code during a walkthrough. | A reader following the text exactly would build the old configuration without an error. | Walk through setup against the available evidence, not only the main procedure. |
| 'Repeat from step 3' inside a subsection with its own numbered list. | The reader cannot tell which step 3 is meant. | Use the destination's title and a link when numbers are ambiguous. |

## Patterns from integrating new requirements into the same guide

These appeared when later security requirements were added to the QR-transfer guide. Each new requirement was correct; the failures came from not reconciling it with the rest of the document.

| Evidence | Reader burden | General instruction |
|---|---|---|
| A new rule said `sys-usb` must never handle the webcam, but hardware discovery still told the reader to plug the webcam into `sys-usb`. | Following the guide in order violates its own rule before the rule's section is reached. | Treat a new requirement as a change to the document's logic: find every step it affects, including setup and discovery, and read 'never' as covering all of them. |
| After a failed scan, the guide said to return to 'Show the QR code', but the display disposable had already shut down and discarded its copy. | The link is valid, yet the next action is impossible. | Track state through the procedure; a retry destination must have its starting conditions restored, or the reader must be sent back further. |
| A new requirement that devices be unplugged was added, but the guide still said the setup 'qualifies for one of two paths' and 'otherwise, use the sequential path'. | A reader excluded by the new rule is still routed onto a path. | Update every decision point and fallback when a restriction excludes a case, and say when no supported path applies. |
| The requirement for an alternative keyboard appeared after the build instruction. | The reader learns about a prerequisite after the action that needed it. | Place a prerequisite before the first instruction that starts the affected action. |
| Covering, disabling, and detaching the camera were listed together without saying whether each is sufficient. | The reader cannot tell whether the cheapest option meets the requirement. | State the required outcome; present methods as interchangeable only when the evidence shows each meets it. |

The same failure outside this guide: a runbook gains the rule 'the production database must never be reachable from the public internet', but its troubleshooting section still says 'temporarily open port 5432 to test connectivity from your laptop'. The rule's 'never' covers troubleshooting too, so that step must change, or be flagged if no safe alternative is known.

## Calibration examples from other domains

Weak: 'The reconciliation subsystem provides eventual consistency.'

More useful, if supported by the source: 'The worker periodically compares the requested configuration with the running service and applies missing changes. Updates may therefore take effect after a delay. This behavior is called eventual consistency.'

The improvement comes from the actor, mechanism, and consequence, not simply from word substitution. Do not invent the mechanism to make a label easier to explain.

Weak: 'This section explains how to inspect replication status.'

More useful: 'On the replica, check how far replication is behind the primary.'

The improvement adds location and purpose. Keep a longer explanation if readers also need to know what lag means or which value is acceptable.

## Contrasting examples of the checks

These come from different domains so that the checks, not the QR guide, are what transfer.

**Heading test (database operations).**

Weak: '## Promote the replica' followed by 'This step promotes the replica to primary.'

Better: '## Promote the replica' followed by 'Stop writes on the old primary first; otherwise both servers accept writes and the data diverges.' The opening now adds a prerequisite and its reason. Deleting the opener entirely is also acceptable when the steps speak for themselves.

**Decision-time limitations (firmware update).**

Weak: step 6 of an update procedure says 'The device cannot be rolled back to the previous firmware version.'

Better: the section that asks whether to update says the update is irreversible and what that rules out, before any step. Step 6 repeats 'This write cannot be undone' at the flashing command.

The same applies to downtime in a migration guide, a cost in a cloud setup guide, or a hardware requirement in an install guide.

**Claim scope (backup policy).**

Source: 'Nightly snapshots cover the database and uploaded files. Logs are not backed up.'

Weak edit: 'Nightly snapshots back up all service data.'

The edit broadened 'database and uploaded files' to 'all', and dropped an exclusion a reader needs during recovery. Similarly, 'reduces the chance of X' must not become 'prevents X', and 'should' must not become 'must' or the reverse without evidence.

**Nested definitions (container orchestration).**

Weak: 'Deploy the sidecar (a container in the same pod, the smallest deployable unit, which shares a network namespace, an isolated view of network interfaces) with the app.'

Better: 'Deploy the log shipper as a sidecar next to the app. A sidecar is a second container in the same pod, so it sees the app's network and files. A pod is the smallest unit Kubernetes schedules.' The role comes first; each concept gets its own sentence.

**Walkthrough and navigation (CI release pipeline).**

Walking through a release guide as the reader: step 4 says 'approve the deployment', but nothing says who can approve or where the button is; the failure branch says 'fix and rerun' without saying whether rerunning repeats the already-published package upload. Supply the answer from the pipeline definition if it is available, otherwise flag it. After restructuring, check that the rollback branch still ends by pointing back to the verification step it used to precede.

## Evaluate the skill

Compare assisted and unassisted outputs on the same task and source. Use questions with concrete answers: What is the system trying to do? Why does a component exist? Which path applies? Where is the next action performed? What observation means stop?

Check both comprehension and preservation of technical requirements. Walk through each path in the output and record every missing prerequisite, location, or decision. Compare claims with the source for changed scope, conditions, certainty, or obligation. A shorter document that loses a prerequisite fails. Word count and counts of stock phrases such as 'This section' are useful signals, but neither shows that the explanation works. Include incremental-editing tests: an existing procedure plus a new constraint that invalidates earlier steps, graded on whether every affected passage changed. A test that only asks for a static draft to be improved misses the integration failures above. The repository's `evals/write-clear-explainers/` directory has two such cases. In their first runs on short guides, runs without the skill passed about as often as runs with it, so they currently work as regression checks rather than evidence that the skill helps. The failures above appeared in a long guide revised over several rounds; a discriminating test probably needs a document and change history of that size. An AI self-review or independent model review is a preliminary check, not a substitute for observing representative readers.
