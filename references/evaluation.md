# How this skill was measured

The first version of this skill was written, probed and graded by one model
(deepseek-v4.1-flash). Its evaluation looked good — control 2–5 of 9 probes,
skill 7–9 of 9 — and was circular: 76% of the grader's forbidden strings
appeared verbatim in the skill text, two probes quoted sentences from the
skill, and the "rules" arm was a slice of the skill itself. That result is
now labelled development evidence and nothing in this page rests on it.

## Design (held-out, v2)

- **Probes.** 32 briefs shaped like real product work across ten scenarios
  (finance, e-commerce, installer, settings/privacy, notifications,
  onboarding, forms, screen-reader labels, in-app AI summary, health
  tracking), ten element types, three languages (zh-TW 20, en 6, ja 6). 16
  were written by Claude (this project's experimenter), 16 by GPT through the
  user's ChatGPT session, neither given the skill or any of its strings. Each
  string's required facts (`must_convey`) come from the brief's author. A
  two-way grep confirms no string from the skill, from the v1 fixtures, or
  from the probes appears on the other side; one four-character hit (「無法判
  斷」 in a brief's scene description) was accepted and recorded.
- **Arms.** control (brief only); rules (a negative list, each "don't" paired
  with its replacement); exemplar (an element→form→example table with no
  prohibitions); skill (v1 of this skill); schema (per-field length and
  emptiness contract only); postfilter (control output through the linter's
  apparatus/absence/provenance patterns; runtime probes only); skill2 (this
  version).
- **Subjects.** deepseek-v4.1-flash, gemma4-31b, nemotron-3-super,
  glm-5.3-flash (Ollama cloud), GPT-6 (Codex, isolated home), Claude Haiku
  4.5 and Sonnet (subagents — these carry the user's rule file in context and
  are labelled *rules-in-context*, never control). Two samples per probe ×
  arm × subject.
- **Judges.** gemma4-31b and nemotron-3-super — neither wrote the skill —
  scoring each string on two axes from a rubric that names the element and
  the required facts but never the skill: `facts_present` (every required fact
  recoverable) and `surplus` (a clause that changes nothing, a reply-register
  phrase, a provenance defence, an absence or apparatus remark, a question in
  a control, content in a note that should be empty). Records were shuffled
  across arms and judged in batches with arm labels removed. A judge never
  scores its own family's output in the headline numbers.
- **Pass** = no surplus *and* all facts present. Reported as paired
  differences against control for the same subject, probe, sample and field,
  with a probe-clustered bootstrap CI and McNemar's b/c counts.
- **Human calibration.** The user, who raised the complaint, blind-rated 64
  strings (batch 1) and a second targeted batch stratified by judge verdict.

## What the v1 skill actually did (gemma judge, 504 paired strings)

| Author of the brief | arm | net pass Δ vs control | clustered 95% CI | Δ facts present |
| --- | --- | --- | --- | --- |
| Claude-written (300 pairs) | skill v1 | +16 pp | +8 … +24 | −0.3 pp |
| Claude-written | rules | +18 pp | +6 … +30 | −4.5 pp |
| Claude-written | exemplar | +12 pp | −3 … +27 | −3.0 pp |
| Claude-written | schema | +2 pp | −7 … +13 | −7.5 pp |
| GPT-written (204 pairs) | skill v1 | **−5 pp** | −15 … +3 | **−15.7 pp** |
| GPT-written | rules | +4 pp | −7 … +16 | −9.6 pp |
| GPT-written | exemplar | −1 pp | −10 … +9 | −16.2 pp |
| GPT-written | schema | −3 pp | −11 … +5 | −17.6 pp |

Surplus fell everywhere (GPT briefs: control 83% clean → skill 94%); the loss
was on the other axis. The GPT-written briefs list more required facts per
string, and every intervention that taught deletion deleted some of them —
the cause of a delay, the second fact of a note, the instruction an empty
state was asked to carry.

Two objective measures taken straight from the generations:

- **Language switching.** On English briefs, strings containing Chinese: 0%
  in control, 41–82% under skill v1, 37–38% under rules, 31–44% under
  exemplar; on Japanese briefs 8–20% under skill v1. The skill's Chinese
  text pulled the answer's language.
- **Note emptiness.** Notes whose brief listed no facts: filled 88% of the
  time by control, 12% by skill v1, 33% by rules, 67% by exemplar. Positive
  examples prime content; the note contract now lists empty first.

Judge agreement (surplus, Cohen's κ): gemma vs nemotron 0.45 on 1,276 shared
strings — moderate, so the two judges see roughly the same thing. The human
did not. Batch 1 (66 strings, random, arm hidden): the rater marked 3% as
surplus, control 0 of 12; κ with gemma 0.19. Batch 2 (44 strings from the
note, dialog-body, error, status and value elements only, half of them
judge-flagged): the rater marked 2 of 44 as surplus and 0 as missing
information; of the 22 the judge had flagged, the rater agreed with 1 — judge
precision 5%, κ 0.00. What the rater flagged, in both batches, was an
*invented claim* (「不會儲存或追蹤」 where the brief said only "not stored";
「不會收集或儲存」 likewise) and one over-instruction. What the judge flagged
and the rater let pass: "successfully", a purpose clause ("to free up
space"), benefit clauses in onboarding copy, an example inside an error, an
exclamation mark on an order confirmation, and coaching in a sleep remark.

So the judge measures a strict reading of the doctrine, and the person who
asked for the doctrine does not apply it that strictly when rating blind. The
absolute surplus rates in the tables overstate what this user objects to; the
between-arm comparisons remain informative about compliance with the strict
reading; and the two things the rater actually objected to — invented claims
and lost facts — are now tests 2 and 3 of the skill, ahead of deletion.

## What changed in v2 because of this

1. Language first: the procedure's first line is the brief's language, and
   every contract has an English and a Japanese example.
2. Facts before deletion: the note contract is "the facts the brief gives, or
   nothing"; the Facts test is scored with, not after, the surplus tests.
3. One contrastive pair per element, difference named; no lists of bad
   strings (they get copied, and a positive example gets copied where it does
   not fit).
4. Examples in the skill are scrubbed against the probe set both ways before
   any measurement.
5. Uncertainty policy split into required / conditional / never
   ([uncertainty.md](uncertainty.md)).

## v2 results

Same harness, same 32 briefs, two samples per probe; arm `skill2b` is the
shipped text minus three example numbers that were later found to come from
the probe set (scrubbed after measurement) and minus the slot templates in
the note contract (added after measurement). Matched on the five model
channels that have both v1 and v2 (Claude Haiku and Sonnet rules-in-context,
deepseek, gemma, nemotron); GPT-6 has no v2 run — the Codex quota was
exhausted. Net pass Δ is (b − c)/n against control on the same subject,
probe, sample and field; CI is a probe-clustered bootstrap.

| judge | briefs | skill v1 | skill v2 | Δ facts v1 → v2 |
| --- | --- | --- | --- | --- |
| gemma | all (504 pairs) | +8 pp [0, +15] | **+8 pp [+1, +15]** | −6.5 → −3.4 pp |
| gemma | Claude-written | +16 [+8, +25] | +13 [+3, +23] | −0.3 → +0.3 |
| gemma | GPT-written | −5 [−16, +3] | 0 [−8, +8] | −15.7 → −8.8 |
| nemotron | all (253 / 271 pairs) | −2 [−12, +7] | **+8 pp [+1, +15]** | −7.9 → +1.1 pp |
| nemotron | Claude-written | +2 [−11, +14] | +14 [+5, +21] | −6.3 → +3.2 |
| nemotron | GPT-written | −8 [−22, +5] | +1 [−8, +9] | −9.9 → −1.7 |

v2 against v1 directly (same subject, probe, sample): gemma 0 pp [−5, +5]
with Δfacts +3.2 and Δsurplus +4.6 (v2 leaves a little more of what the
strict judge calls surplus); nemotron +6 pp [−1, +14], Δfacts +6.0. On the
GPT-written briefs v2 beats v1 by +5 [−1, +12] (gemma) and +2 (nemotron).
What v2 bought is fact retention, not more deletion.

Objective measures, straight from the generations:

- **Language switching**, strings containing CJK on English briefs: deepseek
  53% → 15%, gemma 41% → 0%, nemotron 82% → 0% (v1 → v2); on Japanese
  briefs 20% → 15%, 8% → 0%, 12% → 4%. The first v2 draft, with the language
  rule only in the procedure, got nemotron to 9% and deepseek to 41%; moving
  it to the first and last lines and adding English and Japanese examples to
  every contract did the rest.
- **Note emptiness**: notes whose brief listed no facts are filled 88% by
  control, 12% by v1, 0% by v2; notes with required facts are non-empty 100%
  / 94% / 100%.
- **Post-filtering with the linter** (control output through the v1
  apparatus/absence/provenance patterns, runtime briefs only): −1 pp [−3, 0]
  against control, Δfacts −4.0. The linter is a CI check, not a fix.

Per model, v2 against control: deepseek +10 [+1, +20] (gemma judge) / +14
[+1, +25] (nemotron); nemotron +8 [−4, +18]; gemma +1 [−11, +13]; Claude
Sonnet +8 / +12, Haiku +1 / +6 (both rules-in-context).

Judge agreement on surplus, gemma vs nemotron: κ 0.45 on 1,276 shared
strings. The two judges disagree about v1 (gemma +8, nemotron −2) and agree
about v2; only v2 has the same sign and a CI excluding zero under both.

These are development numbers: the language fix (draft 1 → draft 2) was made
after seeing draft 1's results on these briefs, and the shipped skill has two
further edits (example scrub, note slots) that were not re-measured. A
confirmatory run needs a frozen skill and a brief set nobody has seen.

## Re-running

```
cd ui-microcopy-eval
python3 eval_v2.py contamination --skill-dir <skill> ; python3 eval_v2.py contamination --skill-dir <skill> --reverse
python3 eval_v2.py generate --channel ollama:<model> --arms control,skill2 --samples 2
python3 eval_v2.py judge --judge ollama:<other-family-model>
python3 eval_v2.py sample-for-human --n 18 ; python3 eval_v2.py human --rated ... --key ...
python3 eval_v2.py report
```

Anything that changes the skill's examples should be followed by the
contamination check; anything that changes the rubric should be followed by a
new human sample.

## Limits

32 base briefs is enough to see effects of ten points or more, not
fine-grained ones. One human rater, who is also the complainant. The Claude
family has no clean control on this machine. The judges' surplus criterion is
stricter than the user's; the human batches calibrate it but do not replace
it.
