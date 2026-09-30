---
name: ui-microcopy
description: Use when writing or rewriting user-visible strings — button labels, statuses, errors, empty states, value rows, notes, dialog copy — in any language, and when writing the prompt or schema that makes a model inside an app produce such strings. Triggers on writing UI text, naming a control, wording an error or confirmation, deciding what goes next to an estimated number, and on any text a model generates that an interface renders.
---

# UI microcopy

**Language first: write every string in the language of the brief.** An
English brief gets English strings, a Japanese brief Japanese, a Taiwanese
brief 正體中文. The examples in this skill are mostly Chinese; they show the
form of each element, never its language. If the brief is in English, no
Chinese character belongs in the answer.

Every interface string has one job: to name an action, state a condition, tag a
figure, or give the one fact that changes how a figure is read. Write it in the
form its element takes, carry the facts the brief requires, and add nothing
else. Natural language is fine; a simulated conversation is not.

Models drift toward the second by default: they write a reply where a label
should be, add a sentence that reassures or explains, restate what the screen
already shows, and defend how a number was produced. This skill is the
procedure, the element contracts, and the checks that hold the line.

The doctrine this skill operationalises is `~/.claude/rules/ui-microcopy.md`.
Read it first; where the two disagree, the rule file wins.

## What to produce, in one paragraph

Answer in the brief's language: an English brief gets English strings, a
Japanese brief Japanese, a Taiwanese brief 正體中文. The examples in this
skill are mostly Chinese; they show the form, not the language. Decide the
element. Write in that element's form (a verb phrase for a control, a closed
state for a status, a noun for a label, a figure with its unit for a value,
the facts the brief gives or nothing for a note). Carry every fact the brief
gives you that the reader needs — an error keeps its cause and its next step,
a confirmation keeps the amount and the consequence, a note keeps each fact
the brief lists for it. Stop there. The contracts in
[references/roles.md](references/roles.md) say what each element's form is and
show one accepted and one rejected example per element with the difference
named.

The order matters: language, facts, then form, then deletion. Deletion put
first removes required facts and pulls the answer into the language of the
examples. A shorter string that lost a fact or switched language is a
failure, not a success.

## The procedure

1. **Name the element before the words.** The element fixes the grammatical
   form; wording is not free prose.
2. **Decide whether the string exists.** A heading, a figure, a control, or
   the change itself may already say it. The right text is often none.
3. **Write in the element's form, carrying the brief's facts.** Deleting a
   required fact is as wrong as adding a sentence; the checks measure both.
4. **Delete pass.** Remove any clause that does not change what the reader
   understands about the state, the consequence, or the next action.
5. **Lint.** `python3 scripts/microcopy_lint.py --format tsv strings.tsv`.
   Every finding names the element form to rewrite toward, not just the word
   to remove. Fix the string, not the rule.

## The tests, in order

The order is the priority. The first three are what a blind human rater
actually objected to when the outputs of seven models were put in front of
one (108 strings, two batches): invented claims and lost facts, not
"successfully" or a benefit clause. The rest are the register tests; they
matter for controls, statuses and notes, and they are cheap to check by
machine, so they live in the linter as much as here.

| # | Test | Question |
| --- | --- | --- |
| 1 | Language | Is the string in the brief's language? For 正體中文（台灣）, open [references/zh-tw-lexicon.md](references/zh-tw-lexicon.md), take the rows for the things this screen names, and write with those rows in view — a model handed the two rows it needs uses the Taiwan term; a model handed the whole table half the time does not. |
| 2 | Facts | Is every fact the brief requires still recoverable from the string? |
| 3 | Invention | Does it assert anything the brief did not give — a claim ("or tracked", "will not collect"), a promise, a guarantee? |
| 4 | Control | Is this control named by something other than the action it performs? |
| 5 | Reply | Could this line be one person answering another (算了, 裝好了, an apology, a cheer)? |
| 6 | Provenance | Does it say how the value was produced, or defend it, instead of what it is? |
| 7 | Absence | Does it report what was *not* seen, or describe the container, apparatus or setting? |
| 8 | Visible | Does it restate what the screen already shows? |
| 9 | Deletion | Delete this clause — does the reader lose anything that changes what they understand or do? |
| 10 | Calibration | If the value is an estimate, does the string still say so, and does the reader know what they can correct? See [references/uncertainty.md](references/uncertainty.md). |

Test 9 is last on purpose. Applied first, it removes facts (test 2) and
teaches the model to answer in the language of the examples (test 1). Applied
to a note or a control it is
right; applied to an onboarding body it deletes copy nobody minded.

## Where the string comes from changes the fix

- **In code** (an ARB file, a component, a strings table): write with the
  procedure and lint the file. `microcopy_lint.py --format arb` reads Flutter
  ARB directly.
- **At runtime** (a model inside the app writes the text the UI renders): the
  field's contract decides the register. Give the field a *test* ("only what
  changes how the figure is read; empty otherwise"), not a *topic* ("what the
  photo cannot show"); models fill topics. See
  [references/runtime-llm-output.md](references/runtime-llm-output.md) and the
  paste-in block in
  [assets/runtime-prompt-block.zh-TW.md](assets/runtime-prompt-block.zh-TW.md).

## Reviewing a screen

Inventory every string with its element, lint the inventory, classify each
string (keep / delete / shorten / merge / rewrite / redesign the surrounding
UI), report the table, and only then change one element type at a time.
Deleting a string the layout needs is a redesign, not a copy edit; say so.

## What this skill is not

It is not a ban on tone. Onboarding and marketing surfaces may carry warmth;
errors, statuses, labels and transactional controls carry none. It is not a
ban on uncertainty: an estimate stays labelled as one, a range stays with its
figure, and the assumption a reader can correct stays visible. And it is not
a licence to shorten: deletion first costs facts and language. A benefit
clause in onboarding, an example inside an error, an exclamation mark on a
confirmation are not the problem; a claim the brief never made is. What goes is
the clause that carries no information *and* the clause that carries
information the brief did not give.

## Where the pain actually was

The strings that started this — 「算了」 for Cancel, 「裝好了」 for Install
complete, 「碗與叉子本身不計入營養」, 「數字不是推測」 — did not reproduce on
32 neutral briefs across seven models; control outputs were 97% acceptable
to the blind rater. They came from two specific places: an agent writing an
installer's strings inside a coding session, and an app's runtime field
whose instruction named a topic instead of a test. Both are contracts, not
prose problems. For the first, the linter in CI catches the register slips
(reply lexicon, exclamation marks, China vocabulary, Simplified
characters) at commit time; for the second,
[references/runtime-llm-output.md](references/runtime-llm-output.md) is the
fix. The writing procedure above is what remains for a person or an agent
writing strings by hand.

## Files

- [references/roles.md](references/roles.md) — element contracts, one ✓/✗ pair each, voice budget per surface
- [references/uncertainty.md](references/uncertainty.md) — what goes next to an estimated number: required, conditional, never
- [references/runtime-llm-output.md](references/runtime-llm-output.md) — field contracts for in-app models
- [references/zh-tw-lexicon.md](references/zh-tw-lexicon.md) — Taiwan terms by screen domain; read the group the screen belongs to, not the whole file
- [assets/runtime-prompt-block.zh-TW.md](assets/runtime-prompt-block.zh-TW.md) — paste-in block
- [scripts/microcopy_lint.py](scripts/microcopy_lint.py) — the CI check

## Last check before answering

1. Same language as the brief? (English brief → English; 日本語 → 日本語; 繁體中文 → 繁體中文, with the lexicon rows for this screen picked out)
2. Every fact the brief listed for this string still present?
3. Element form correct, and nothing else?
4. When the strings sit in a file, run `python3 scripts/microcopy_lint.py <file>` and fix what it reports; a term slip is rare enough (about one string in fifty) that reading will not catch it.
