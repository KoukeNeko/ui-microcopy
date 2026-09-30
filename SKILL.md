---
name: ui-microcopy
description: Use when writing or rewriting user-visible strings — button labels, status and completion messages, errors, empty states, value labels, notes, dialog copy — or when writing the prompt and schema that make a model inside an app produce such strings. Triggers on writing UI text, reviewing microcopy, naming a button, wording an error or confirmation, and on AI-generated text an interface renders.
---

# UI microcopy

Write naturally, but do not simulate a conversation that does not need to
exist. Mainstream guidance (Material, Microsoft, Polaris, Salesforce) does
allow a human, even conversational tone; what every one of them forbids is
content that carries no information — the extra clause, the reassurance, the
explanation of the obvious, the defence of a number. A button is an action's
name, a status line is a state, a value label is a figure's tag, and each of
them has exactly one job.

Models drift the other way by default: trained on chat, they write UI strings
in the register of a reply ("算了" for Cancel, "裝好了" for Install complete)
and add sentences nobody asked for ("碗與叉子本身不計入營養", "數字不是推測").
This skill is the procedure and the check that stop it.

The core constraint, in the form a prompt can carry:

> Add no sentence, qualification, reassurance, explanation, provenance claim,
> or personality unless it changes the reader's understanding of the state,
> the consequence, or the next action. Keep conventional action labels. Prefer
> the shortest conventional wording that preserves meaning.

## Read the doctrine first

`~/.claude/rules/ui-microcopy.md` is the canonical voice doctrine for every
project on this machine. Read it before writing or reviewing strings. This
skill operationalises it — the workflow, the tests, the worked cases, the
lexicon, and the linter — and deliberately does not restate it. When the two
seem to disagree, the rule file wins and this skill needs fixing.

## Where these strings come from

Two different places, and the fix differs:

1. **In code** — you are writing the string into source, an ARB file, or a
   component. Write it with the procedure below and lint it.
2. **At runtime** — a model inside the app generates text that the interface
   renders (a photo estimate's notes, an AI coach line, a summary). The prompt
   and the schema decide whether that text is interface or conversation. See
   [references/runtime-llm-output.md](references/runtime-llm-output.md); the
   copy-pasteable instruction block is
   [assets/runtime-prompt-block.zh-TW.md](assets/runtime-prompt-block.zh-TW.md).

Most complaints that "the AI wrote something silly in the UI" are the second
case, and cannot be fixed by editing a string — the contract that produced it
has to change.

## Writing: the procedure

1. **Name the role before the words.** Decide which UI element the string is
   and therefore which grammatical form it takes. A role's form is fixed; the
   wording is not free prose. See [references/roles.md](references/roles.md).
2. **Decide whether the string exists.** Empty space, a heading, a figure, a
   control, or the change itself may already say it. The correct text is often
   none; a deleted string cannot be too colloquial.
3. **Write in the role's form.** Imperative verb for a control, closed state
   for a status, noun for a label, figure for a value.
4. **Delete pass.** Remove every clause that does not add a state, a
   consequence, a recovery step, or an action. Delete first, rewrite second;
   never lengthen a string without naming the information it adds.
5. **Run the six tests** (below), then
   `python3 scripts/microcopy_lint.py --format tsv strings.tsv` on everything
   you wrote. Fix the findings rather than the rule.

## The six tests

Each is falsifiable; a string either passes or it does not.

| Test | Question | Fail looks like |
| --- | --- | --- |
| Deletion | Delete the clause — does the reader lose anything that changes what they understand or do? | 「碗與叉子本身不計入營養」 |
| Counter-question | Would a user ever ask the question this sentence answers? | 「未見額外添加糖、鹽或醬料」 |
| Visible | Does the screen already show it — heading, figure, layout, control? | value repeated under its own heading; gesture hints |
| Chat | Could this line be a reply between two people? | 「算了」, 「裝好了」, 「好的」 |
| Control | Does it name the action the control performs? | 「確定要刪除嗎？」 as a button |
| Provenance | Does it explain how the value came to be, rather than what it is? | 「數字直接來自 X 與 Y，不是推測」 |

A seventh, for anything a model wrote: **affect** — does it cheer, apologise,
or reassure? Delete it.

## Reviewing existing copy

Never rewrite a screen string by string. Audit first, then change one UI role
at a time:

1. **Inventory** every user-visible string with its role (from the ARB / string
   file, or from the components).
2. **Lint** the inventory in bulk to find the mechanical failures.
3. **Classify** each string: keep / delete / shorten / merge / rewrite /
   redesign-surrounding-UI. Prefer deletion over rewriting.
4. **Report** the table with the reason for each verdict, and wait for
   approval before editing.
5. **Apply** one role at a time — all buttons, then all statuses — so the
   voice stays consistent and the diff stays reviewable.

Deleting a string that the layout needs is a redesign, not a copy change; say
so rather than writing filler to keep the space filled.

## Failure modes and worked cases

[references/failure-modes.md](references/failure-modes.md) has the taxonomy —
register drift, assistant voice in a system message, defensive disclosure,
provenance meta-commentary, duplicated hedging, affect — each with the real
string that produced it, why the model did it, and the fix.

## Verification

- `python3 scripts/microcopy_lint.py --help` — roles, formats (tsv, json,
  jsonl, arb, text), `--json` for machines, `--self-test` for the rules.
- The linter exits non-zero on an error finding, so it gates CI on a string
  file or an ARB directory.
- To show that a model or an in-app prompt is clean rather than to hope so,
  run the control-group harness in the sibling skill `ui-microcopy-eval`: the
  same probes without and with this skill, scored by this linter.
