---
name: explain-technical-docs
description: Write and review technical explainers and mixed explanation/procedure documents for technically capable readers unfamiliar with the specific system. Use for requests to make documentation understandable, diagnose hard-to-follow AI writing, improve conceptual flow, or explain architecture and mechanisms. Preserve technical precision and safety requirements. Respect review-only requests; do not rewrite unless asked.
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
6. Introduce one unfamiliar relationship at a time. Expand dense noun phrases into actors and verbs. Keep necessary technical terms; expanding an acronym alone rarely explains its meaning.
7. Use one consistent worked example to connect abstractions when it helps. Label example values and placeholders. Explain what an output demonstrates and what the reader must do with it.

## Control detail and branching

Separate one-time preparation from repeated operation. State what must already be true when each phase starts and what changes when it ends.

For alternatives, place the decision criteria before branch-specific instructions. Make it clear which path applies, what to skip, and where paths rejoin. In an explanation, compare the meaningful tradeoff before implementation details. Do not interleave two complete procedures and make readers mentally filter every paragraph.

Keep information in the main reading path when it changes understanding, a decision, or the next action. Move exhaustive reference material and uncommon exceptions to clearly linked sections. Do not move prerequisites, stop conditions, or safety-critical qualifications out of the place where they are needed.

Give each fact a primary home. Repeat a critical warning at the action it governs when readers could otherwise miss it. Remove repetition that merely restates a heading or re-explains a settled point. Do not introduce every section with 'This section explains...' unless the sentence adds useful scope or context.

Use connected prose for causal explanation, numbered steps for sequences, tables for exact comparisons or mappings, and diagrams for relationships that are difficult to hold in prose. Do not add a visual merely to repeat a short paragraph. Avoid forcing every paragraph into bullets or every idea into a new heading.

## Make procedural context explicit

At every meaningful context change, identify the machine, environment, account, or component where the action happens. In multi-machine guides, 'in the admin terminal' may be insufficient: name the machine as well.

For each substantial step, provide the action and the information needed to perform and verify it. Where relevant, include the starting state, exact command, expected observation, success criterion, and failure response. Do not mechanically print all of these as labels for trivial steps.

Name important artifacts by role as well as filename. Keep readers oriented about where an artifact came from, where it is now, and whether it is original, transformed, temporary, verified, or untrusted when those distinctions matter.

## Preserve precision while simplifying

Preserve commands, literal identifiers, quantitative bounds, assumptions, guarantees, and required ordering unless a separately justified technical correction is requested. Do not silently make technical changes during an editorial pass.

State guarantees with their conditions. Keep qualifications close enough to prevent a stronger interpretation. When the source is ambiguous or contradictory, flag the exact unresolved point instead of choosing a convenient interpretation. Distinguish editorial review from technical validation.

Replace abstract labels with the concrete action or mechanism they describe when the label adds little. Introduce a formal label after its meaning if readers need it later. Prefer literal language to decorative analogies; if an analogy is useful, explain its relevant limit.

Use direct, calm language. Avoid hype, invented jargon, ornamental transitions, rhetorical questions, and strings of defensive caveats. Use straight quotation marks and ordinary hyphens. Do not impose arbitrary sentence-length limits, ban passive voice universally, or simplify by deleting necessary content.

## Review before returning

First inspect structure, then paragraphs, then wording. Perform these checks against the actual output:

- Can the intended reader explain the problem, central mechanism, and reason for the major design choices without rereading the whole document?
- Does each new term or component have a purpose when introduced? Are project assumptions explicit without teaching already-known basics?
- Can readers follow each relevant branch from start to finish without searching for an earlier or later missing prerequisite?
- Does each paragraph advance the explanation, support a decision, or enable an action? Remove empty announcements and duplicate coverage.
- Are actors, locations, artifacts, and changes of state unambiguous at transitions?
- Are commands, conditions, limitations, and essential warnings preserved? Flag missing evidence instead of smoothing it over.

For reviews, prioritize the few patterns causing the most reader effort and connect each to a reusable instruction. For edits, return the edited document without an unsolicited explanation. Keep internal planning and checking out of the deliverable unless requested.

Consult [references/principles-and-examples.md](references/principles-and-examples.md) when concrete diagnostic examples or the basis for these rules would help. These are editorial heuristics, not evidence that a prompt guarantees comprehension. Real reader feedback remains the strongest check.
