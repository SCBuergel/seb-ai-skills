---
name: write-clear-explainers
description: Write and review technical explainers and mixed explanation/procedure documents for technically capable readers unfamiliar with the specific system. Use for requests to make documentation understandable, diagnose hard-to-follow AI writing, improve conceptual flow, or explain architecture and mechanisms. Also use when incorporating new requirements, review findings, or technical corrections into existing documentation. Preserve technical precision and safety requirements. Respect review-only requests; do not rewrite unless asked.
---

# Write Clear Explainers

Make the reader's next inference easy. Optimize for understanding and correct use, not minimum word count or a superficially conversational tone.

## Establish the reader and the task

Infer from the request and source what readers already know, what is specific to this system, and what they should understand or be able to do afterwards. Treat general technical competence and project familiarity as separate things. Ask only when missing context would materially change the result; otherwise use a reasonable explicit assumption.

Identify whether the reader primarily needs an explanation, a procedure, a reference, or a tutorial. For mixed documents, separate these purposes into clearly bounded sections or linked documents. Do not force every document into a fixed template or four-document structure.

Read the whole source before diagnosing or restructuring it. In review-only work, give representative evidence, explain the reader's difficulty, and extract transferable instructions. Do not rewrite the source. Distinguish observations about the document from guesses about how an AI produced it.

## Build understanding before adding detail

1. Start with the concrete problem, intended outcome, and central mechanism. Give readers enough of the whole process to understand why the parts exist.
2. Arrange explanations in dependency order: introduce an idea before asking readers to use it. Arrange executable instructions in actual execution order. Move prerequisite actions ahead of dependent actions; eliminate circular navigation.
3. Organize around questions the reader will naturally ask. Use headings that name a question, finding, or action. Do not follow the source code's component order unless it also serves the reader.
4. Introduce each component through its job and relationship to known components, then its exact technical name. For procedures, retain exact names in commands and connect them to stable human-readable roles.
5. Explain cause and effect explicitly: what happens, why it happens, and what consequence matters here. Definitions and inventories alone do not explain a system.
6. Introduce one unfamiliar relationship at a time. Expand dense noun phrases into actors and verbs. Keep necessary technical terms; expanding an acronym alone rarely explains its meaning. If one sentence both introduces a component and explains several unfamiliar concepts, split those jobs: state the component's role first, then explain its lifecycle, implementation, or relationship to other components in following sentences. Avoid a definition nested inside another definition; parentheses and technical vocabulary remain fine.
7. Use one consistent worked example to connect abstractions when it helps. Label example values and placeholders. Explain what an output demonstrates and what the reader must do with it.

## Control detail and branching

Separate one-time preparation from repeated operation. State what must already be true when each phase starts and what changes when it ends.

For alternatives, place the decision criteria before branch-specific instructions. Make it clear which path applies, what to skip, and where paths rejoin. Put every limitation that determines whether a path or procedure is suitable before the reader chooses or starts it: compatibility requirements, costs, downtime, irreversible changes, residual risks, and recovery limits. Place prerequisites and warnings before the first instruction that initiates the affected action, including an instruction that sends the reader to another guide, and repeat the operational part at the action itself. A caveat that appears only after the consequential action does not give the reader an informed choice. Merge a new caveat into the decision or step it governs; do not accumulate caveats in a trailing paragraph.

Do not assume the documented alternatives cover every reader or configuration. When a restriction excludes a case, update every decision point and fallback instruction, such as 'otherwise, use...'. State when no supported path applies and what must change before the reader can proceed. For alternative safeguards, state the required outcome, and present methods as interchangeable only when the available evidence shows that each meets it. In an explanation, compare the meaningful tradeoff before implementation details. Do not interleave two complete procedures and make readers mentally filter every paragraph.

Keep information in the main reading path when it changes understanding, a decision, or the next action. Move exhaustive reference material and uncommon exceptions to clearly linked sections. Do not move prerequisites, stop conditions, or safety-critical qualifications out of the place where they are needed.

Give each fact a primary home. Repeat a critical warning at the action it governs when readers could otherwise miss it. Remove repetition that re-explains a settled point.

Read each heading together with its opening sentence. If the sentence only announces or paraphrases the heading, delete it rather than rewording it. Keep an opening sentence that adds purpose, prerequisites, scope, or a reason the reader needs.

Use connected prose for causal explanation, numbered steps for sequences, tables for exact comparisons or mappings, and diagrams for relationships that are difficult to hold in prose. Do not add a visual merely to repeat a short paragraph. Avoid forcing every paragraph into bullets or every idea into a new heading.

## Make procedural context explicit

At every meaningful context change, identify the machine, environment, account, or component where the action happens. In multi-machine guides, 'in the admin terminal' may be insufficient: name the machine as well.

For each substantial step, provide the action and the information needed to perform and verify it. Where relevant, include the starting state, exact command, expected observation, success criterion, and failure response. Do not mechanically print all of these as labels for trivial steps.

Name important artifacts by role as well as filename. Keep readers oriented about where an artifact came from, where it is now, and whether it is original, transformed, temporary, verified, or untrusted when those distinctions matter.

## Preserve precision while simplifying

Preserve commands, literal identifiers, quantitative bounds, assumptions, guarantees, and required ordering unless a separately justified technical correction is requested. Do not silently make technical changes during an editorial pass.

Compare each important claim in the output with the source. Check whether an edit broadened the entities it covers, removed a condition, strengthened certainty, or changed an obligation (required to optional or the reverse). Words such as all, every, only, always, never, must, may, prevents, and guarantees deserve a second look. Apply this to introductions and summaries too: they may omit detail, but not a distinction the reader needs to understand the mechanism.

State guarantees with their conditions. Keep qualifications close enough to prevent a stronger interpretation. When the source is ambiguous or contradictory, flag the exact unresolved point instead of choosing a convenient interpretation. Distinguish editorial review from technical validation.

Replace abstract labels with the concrete action or mechanism they describe when the label adds little. Introduce a formal label after its meaning if readers need it later. Prefer literal language to decorative analogies; if an analogy is useful, explain its relevant limit.

Use direct, calm language. Avoid hype, invented jargon, ornamental transitions, rhetorical questions, and strings of defensive caveats. Use straight quotation marks and ordinary hyphens. Do not impose arbitrary sentence-length limits, ban passive voice universally, or simplify by deleting necessary content.

## Integrate changes into an existing document

Treat each new requirement, review finding, or technical correction as a change to the document's logic, not as text to append. Identify which existing assumptions, decisions, instructions, and claims it affects, and update those passages together instead of adding a warning next to the old instruction. For each material change, check its consequences for the introduction and stated guarantees; prerequisites and path eligibility; setup and execution; and verification, failure handling, retries, and cleanup. This is an editing check, not a structure to impose on the document.

The claim comparison above protects the source's meaning during copy editing. When the user deliberately changes a requirement, the correction becomes the reference instead: review the affected instructions and claims against it. Check whether any step now violates a prohibition, omits a new prerequisite, or promises an outcome the correction no longer supports. Temporal scope needs particular attention: before, after, during, ever, until, and again. A rule that something must never happen also covers setup, discovery, testing, and retries. If resolving a conflict requires a technical decision that the supplied evidence does not establish, flag it rather than weakening the requirement or inventing a procedure.

## Revise before returning

Stating these principles does not ensure the draft follows them. After drafting, make one deliberate review pass over the complete output, fix what it finds, then recheck only the passages you changed and anything that depends on them. Do not loop indefinitely, and do not present self-review as a substitute for reader testing. Inspect structure first, then paragraphs, then wording:

- Can the intended reader explain the problem, central mechanism, and reason for the major design choices without rereading the whole document?
- Does each new term or component have a purpose when introduced? Are project assumptions explicit without teaching already-known basics?
- Walk through each supported path using only information already encountered or explicitly linked as a prerequisite. At each action, check who performs it, where it happens, what must already exist or be running, and what happens next. Cover setup, branch entries and exits, failures, and retries, not only the successful main sequence. Track what earlier steps changed: relevant artifacts, running components, assignments, connections, and persistent changes. At each retry destination, check that its starting conditions still hold after the failed attempt; if they do not, send the reader back far enough to repeat the preparation that restores them. Supply missing context from the available evidence, such as source code or configuration, or flag it; never invent commands or system behavior to complete the walkthrough.
- After moving or deleting material, recheck branch entry and exit instructions, cross-references, and retry destinations; they are part of the procedure's meaning. Where a step number could refer to more than one sequence, use the destination's descriptive title and a link.
- Apply the heading test to every section opening. Does each remaining paragraph advance the explanation, support a decision, or enable an action? Delete duplicate coverage.
- Are decision-critical limitations placed before the choice they affect and before the first instruction that starts the affected action? Does every decision point say what to do when no documented path applies?
- If the edit integrates a new requirement or correction, has every passage it affects been updated, including the introduction, eligibility, setup, verification, failure handling, and retries?
- Compare claims with the source, or with the user's correction when a requirement was deliberately changed, for scope, conditions, certainty, and obligation. Are commands, limitations, and essential warnings preserved? Flag missing evidence instead of smoothing it over.

Word count and the disappearance of stock phrases are signals, not success criteria. A shorter document that loses a prerequisite or a condition fails.

For edits, return the edited document without an unsolicited explanation. Keep internal planning and checking out of the deliverable unless requested.

## Review someone else's draft or a revision

Prioritize findings that could make readers misunderstand a mechanism, choose an unsuitable path, act in the wrong context, or get stuck. Report each with the passage, the reader's difficulty, and the smallest useful correction, and connect recurring problems to a reusable instruction. List optional wording preferences separately and label them as such.

When reviewing a revision, first verify whether earlier findings were resolved, then inspect the passages those fixes affect. For substantive changes, also identify what changed beyond the previous findings and check its consequences throughout the document; previous approval does not cover newly introduced requirements. Use the diff to locate changes, but assess them in the context of the complete current document. Do not assume another rewrite is necessary. If only stylistic preferences remain, say so and recommend stopping; the next useful test is a real reader following the document.

Consult [references/principles-and-examples.md](references/principles-and-examples.md) for contrasting examples of these checks from several domains and for the basis of these rules. These are editorial heuristics, not evidence that a prompt guarantees comprehension. Real reader feedback remains the strongest check.
