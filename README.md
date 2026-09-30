<h1 align="center">ui-microcopy</h1>

<p align="center">
  <strong>A Claude Code skill and a linter for interface strings that read like an interface.</strong><br>
  Button labels, statuses, errors, empty states, value rows, notes, dialog copy — in 正體中文（台灣）, English and 日本語.
</p>

<p align="center">
  <img alt="Claude Code skill" src="https://img.shields.io/badge/CLAUDE_CODE-SKILL-2196F3?style=for-the-badge">
  <img alt="Linter: Python 3, no dependencies" src="https://img.shields.io/badge/LINTER-PYTHON_3%2C_NO_DEPS-4CAF50?style=for-the-badge&logo=python&logoColor=white">
  <img alt="Languages" src="https://img.shields.io/badge/ZH--TW_·_EN_·_JA-00A5A5?style=for-the-badge">
</p>

<p align="center">
  <a href="#getting-started">Getting started</a>
  · <a href="SKILL.md">The skill</a>
  · <a href="references/roles.md">Element contracts</a>
  · <a href="references/zh-tw-lexicon.md">台灣用語</a>
  · <a href="#the-linter">The linter</a>
  · <a href="#how-it-was-measured">Measurement</a>
</p>

```sh
python3 scripts/microcopy_lint.py --format arb lib/l10n/app_zh.arb
```

```text
app_zh.arb: error: '裝好了！' [completion-slang] Completion in conversational register.
    → Use the closed form: 「安裝完成」, 「已儲存」, 「設定完成」.
app_zh.arb: error: '算了' [chatty-lexicon] A reply between two people, not interface text.
    → A cancelling control is 「取消」.
app_zh.arb: error: '當前設定已保存。' [zh-tw-vocabulary] 「當前」 is the term used in China.
    → Taiwan writes 目前.
3 strings, 3 errors, 0 warnings
```

A language model asked for a button writes a reply. Asked for a status it reports the way a person
would say it out loud (「裝好了」). Asked for the note under an estimated number it defends how the
number was produced (「碗與叉子本身不計入營養」「數字不是推測」). None of that is wrong grammar; it is
the register of a chat answer leaking into a field that has one job. This repository holds the
procedure that stops it and the check that catches what the procedure misses.

**The skill is the writing procedure.** Ten tests in a fixed order — language, facts, invention,
then the form of the element, then deletion — with one contrastive pair per element and the
difference named. The order is the point: a skill that teaches deletion first deletes required
facts and answers English briefs in Chinese; this one was rebuilt after measuring exactly that.

**The linter is the guarantee.** Rules for the patterns a model falls into (reply lexicon,
completion slang, 「我們」, provenance defences, apparatus and absence disclaimers, exclamation marks,
China vocabulary) run on TSV, JSON, JSONL, Flutter ARB or plain text and gate CI with an exit code.
It is deliberately rule-based, so a person, a pipeline and an evaluation harness all see the same
findings.

## What it does

### Writes each element in its own form

Every user-visible string has one job: name an action, state a condition, tag a figure, or give the
one fact that changes how a figure is read. [references/roles.md](references/roles.md) gives each
element its form, its voice budget, and one accepted / rejected pair:

| Element | Form | Voice |
| --- | --- | --- |
| button | the action's name — verb phrase, no person, no question | none |
| dialog-title | the decision; a question only when the buttons answer it | none |
| dialog-body | the consequence, once, and nothing already on screen | low |
| status | the closed state — 已儲存 / Export complete / 保存しました | none |
| error | what happened, the cause if known, the next step if one exists | none |
| empty | the state of having nothing; the action stays on the control | none |
| label | the name of the thing; for a setting, what happens when it is on | none |
| value | number, unit, range, target — figure and layout carry the uncertainty | none |
| note | the facts the brief gives, one clause each, or nothing | none |
| title | the name of the screen or step | onboarding may be warm |

Platform conventions — Apple HIG casing and fixed names, Material sentence case, tap versus click —
sit at the end of the same file and change only casing, a few names and the gesture verb.

### Says what belongs next to an estimate

[references/uncertainty.md](references/uncertainty.md) splits the disclaimer question three ways:
the estimate's identity and the assumption a reader can correct are **required**; a range is
**conditional** on calibration; apparatus remarks, absence remarks, boilerplate cautions,
self-defence and a model's own confidence figure are **never**. The evidence is from the
uncertainty-communication literature, not taste.

### Uses Taiwan's words

[references/zh-tw-lexicon.md](references/zh-tw-lexicon.md) is 40 term pairs grouped by screen
domain — storage, network, devices, media, accounts, actions — each with the concept it names, plus
a software-context whitelist (帳號, 用戶端, 租用戶, restaurant 菜單) so Taiwan's own terms are never
"corrected". The skill tells the agent to pick the rows for the screen it is writing, not to read
the table: measured on briefs written to invite drift, the two or three relevant rows raised use of
the Taiwan term from 43% to 66%; the whole table reached 51%; a lone "do not use China usage" line
was the only condition that made things worse.

### Fixes the prompt when a model inside the app writes the string

When the string comes from a runtime model — a photo-estimate note, an AI summary — the fix is the
field contract, not the prose. [references/runtime-llm-output.md](references/runtime-llm-output.md)
gives the contract and [assets/runtime-prompt-block.zh-TW.md](assets/runtime-prompt-block.zh-TW.md)
is the paste-in block: one contrastive pair per field, an allowed empty value, the source in its own
field, no request for a confidence or a ± range.

### How it compares

Where each piece works, from what was measured:

|                                              | Rules file only | This skill | Linter in CI | zhtw MCP |
| -------------------------------------------- | :-------------: | :--------: | :----------: | :------: |
| A person writing strings by hand             |       ⚠️        |     ✅     |      ✅      |    —     |
| An agent writing strings in a coding session |       ⚠️        |     ✅     |      ✅      |    —     |
| A model inside the app                       |       —         |     ✅     |      ⚠️      |    —     |
| Catches 「當前」「保存」                        |       —         |     ⚠️     |      ✅      |    —     |
| Keeps required facts                         |       ⚠️        |     ✅     |      —       |    —     |
| Keeps the brief's language                   |       ⚠️        |     ✅     |      —       |    —     |
| Long-form 翻譯腔 and punctuation              |       —         |     —      |      —       |    ✅    |

A rules file the agent already carries is a weaker version of the skill (it is what the "rules"
arm of the evaluation was). The linter catches the one-in-fifty term slip that neither a reader nor
the model notices. The zhtw MCP is a prose tool: on the strings above it reported nothing.

## Getting started

1. **Install** into Claude Code's skill directory:

   ```sh
   git clone https://github.com/KoukeNeko/ui-microcopy.git ~/.claude/skills/ui-microcopy
   ```

   The skill triggers on its own when you write or review UI text, name a control, word an error
   or confirmation, or write the prompt for a model whose output an interface renders.

2. **Write.** Give the brief — screen, element, the facts the string must carry, the language — and
   the skill answers in the element's form. The last check it runs before answering:

   ```text
   1. Same language as the brief?
   2. Every fact the brief listed still present?
   3. Element form correct, and nothing else?
   4. Strings in a file → run the linter and fix what it reports.
   ```

3. **Lint** the strings your app ships, in CI or a pre-commit hook. Exit status is 0 with no
   errors, 1 otherwise; `--strict` fails on warnings too:

   ```sh
   python3 scripts/microcopy_lint.py --format arb lib/l10n/app_zh.arb
   python3 scripts/microcopy_lint.py --format tsv strings.tsv --strict
   python3 scripts/microcopy_lint.py --format json --json strings.json
   ```

   TSV is `role<TAB>text` per line; JSON and JSONL are `{"role": ..., "text": ...}` objects; text
   is one string per line with the role `generic`. Roles: `button`, `dialog-title`, `dialog-body`,
   `title`, `label`, `status`, `error`, `empty`, `value`, `note`, `ai-note`, `generic`.

4. **Constrain the in-app model.** Paste
   [assets/runtime-prompt-block.zh-TW.md](assets/runtime-prompt-block.zh-TW.md) beside the output
   format section of the app's prompt so it governs the fields, then run the app's own prompt
   through the [evaluation harness](https://github.com/KoukeNeko/ui-microcopy-eval) — the
   note-emptiness table tells you whether the field contract works before you ship it.

## The linter

```sh
python3 scripts/microcopy_lint.py --list-rules
python3 scripts/microcopy_lint.py --self-test
```

| Rule | Level | Catches |
| --- | --- | --- |
| `chatty-lexicon` | error | a reply between two people where a control or state should be (算了, 裝好了) |
| `completion-slang` | error | completion in conversational register instead of the closed form |
| `we-voice` | error | the interface speaking as 「我們」 |
| `second-person` | warn | 「你的」 where nothing needs disambiguating |
| `question-label` | error | a control that asks a question instead of naming an action |
| `provenance-meta` | error | a string defending how the value was produced (「數字不是推測」) |
| `apparatus-disclaimer` | error | explaining away the apparatus (「碗與叉子本身不計入營養」) |
| `absence-disclaimer` | warn | reporting what was not seen as if it were evidence |
| `boilerplate-disclaimer` | error / warn | a caution every row could carry |
| `self-estimated-range` | warn | a confidence or ± the model produced itself |
| `hedge-duplication` | warn | an estimate hedged again in words |
| `method-filler` | warn | method described inside a note read as a result |
| `redundant-qualifier` | warn | 「約」 before a range, 「上限」 after a slash |
| `exclamation-emoji` | error | tone no routine, error or destructive state should carry |
| `punctuation-form` | warn | half-width punctuation in a Chinese sentence |
| `trailing-period` | warn | a full stop on a label |
| `role-length` | warn | a string doing two jobs |
| `zh-tw-vocabulary` | error / warn | China vocabulary, with the Taiwan whitelist masked first |

The rules and the worked examples are one file, `scripts/microcopy_lint.py`, with no dependencies
beyond Python 3. `--self-test` checks every rule against its examples.

## How it was measured

The first version of this skill graded itself: three quarters of its grader's forbidden strings
were in the skill text. The current version was measured on 32 held-out briefs written by two
authors who never saw the skill, across seven model channels, scored by two judges from other
model families on two axes — no surplus, and every required fact present — with paired analysis
and a probe-clustered bootstrap, and calibrated against 108 blind human ratings.

| | Net pass Δ vs control | Δ required facts |
| --- | --- | --- |
| first version, Claude-written briefs | +16 pp | −0.3 pp |
| first version, GPT-written briefs | −5 pp | −15.7 pp |
| **this version, all briefs, judge A** | **+8 pp [+1, +15]** | −3.4 pp |
| **this version, all briefs, judge B** | **+8 pp [+1, +15]** | +1.1 pp |

The first version also pulled 41–82% of English answers into Chinese; this version 0–15%. Notes
whose brief listed no facts were filled 88% of the time by the unaided models and 0% here. These
are development numbers — the language fix was made after seeing the first draft's results — and a
confirmatory run needs a frozen skill and briefs nobody has seen. The harness, briefs, generations
and verdicts are in [ui-microcopy-eval](https://github.com/KoukeNeko/ui-microcopy-eval).

## Where the rules come from

The contracts agree with the guidance that already exists and add what it leaves implicit: Apple's
Human Interface Guidelines (Writing, Alerts), Material 3's UX writing guide, Microsoft's zh-TW
style guide, GOV.UK's content guidance, the Ministry of Education's 兩岸常用詞語對照表, MDN's and
MozTW's zh-TW translation guides, and the Ministry of Digital Affairs' 政府網站服務管理規範. The
uncertainty policy rests on the uncertainty-communication literature (numeric ranges cost little
trust, verbal hedges cost a lot; disclaimers habituate; verbalised confidence is badly calibrated).
The evidence for the negative-example and ordering decisions is the instruction-following
literature and this skill's own measurement.

## Repository layout

```text
SKILL.md                              the procedure, the ten tests, the last check
references/
  roles.md                            element contracts, one ✓/✗ pair each, platform conventions
  uncertainty.md                      what goes next to an estimated number
  zh-tw-lexicon.md                    Taiwan terms by screen domain, whitelist, punctuation
  runtime-llm-output.md               field contracts for a model inside the app
assets/
  runtime-prompt-block.zh-TW.md       paste-in block for that model's prompt
scripts/
  microcopy_lint.py                   the linter; --self-test, --list-rules
```

## Limits

- The measurement is 32 briefs, two samples each: it sees effects of ten points or more, not
  finer ones. One human rater, who is also the person who raised the complaint.
- The lexicon is 40 pairs. It catches the words models actually slip on in software copy, not
  every difference between China and Taiwan usage; the second tier (提交, 點擊, 保存, 設置) is a warning because
  context decides.
- Japanese and English contracts have examples but no held-out measurement of their own beyond
  the six briefs each in the harness.
- The skill is text. It cannot see the screen; the visible-information test relies on the brief
  saying what is already on it.
