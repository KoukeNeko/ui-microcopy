# Why — the evidence

Every source here was opened and verified on 2026-09-30 (title, authors,
venue, and the quoted claim), except where marked *(reported)*, which means a
number from the paper's body that was relayed by a research assistant and not
checked against the original. The full ledger with verification notes is in
the companion research folder (`sources.jsonl`).

## 1. The phenomenon has no name; its neighbours do

No established term covers "a chat model leaking assistant register into
interface strings". Four measured phenomena explain it:

- **Verbosity bias.** LLM evaluators prefer longer answers at equal quality
  (Saito et al., 2023, arXiv:2310.10076); length confounds preference
  judgments enough that length-controlled comparison is needed (Hu et al.,
  Findings of EMNLP 2025; Dubois et al., COLM 2024 — correlation with Chatbot
  Arena 0.94 → 0.98 after length control).
- **Format bias.** Humans, GPT-4 and top reward models favour lists, bold and
  emoji; under 1% of biased data shifts a reward model (Zhang et al., ACL
  2025).
- **Persona overuse.** Given persona attributes, models apply them where the
  context does not call for them (Kim et al., PANDA, EMNLP 2024; Shin et al.,
  arXiv:2609.04676, EMNLP 2026); personas in system prompts do not improve
  performance and their effect is unpredictable across 162 personas × 4
  families × 2,410 questions (Zheng et al., Findings of EMNLP 2024).
- **Sycophancy.** Five RLHF assistants consistently show it; human and
  preference-model raters sometimes prefer a convincing sycophantic answer to
  a correct one (Sharma et al., ICLR 2024).

The mechanism: alignment trains whole assistant turns against human
preference (Ouyang et al., 2022). The learned turn-level behaviours have no
reason to switch off for a string field.

## 2. Negated instructions are a weak point — but not always

- Removing negative examples from instructions *improved* GPT-3 from 24 to 44
  ROUGE-L and BART from 32 to 35; definition + positive examples (33) beat the
  full instruction with negatives (32). "Negative instructions are surprisingly
  difficult for the models to learn from." (Mishra et al., ACL 2022)
- Negated prompts show inverse scaling — larger models do worse — and neither
  few-shot nor fine-tuning rescues them (Jang et al., 2023, arXiv:2209.12711).
- Naming a forbidden word primes it: 87.5% of "do not use word X" violations
  are attributable to the instruction activating X; violation follows a
  logistic curve in X's base probability over 40,000 samples (Rana, 2026,
  arXiv:2601.08070, preprint). Ironic rebound is observed directly in
  transformers on 5,000 negation prompts (Mann et al., 2025, arXiv:2511.12381,
  preprint), and in diffusion models' negative prompts (Hwang et al., 2024).
- **But:** on matched affirmative/negated constraints, Claude 2 showed no
  difference (48.5% vs 49.4%) and GPT-4 a modest one (51.7% vs 45.4%), with
  one constraint collapsing from 36.8% to 0% (Bleakley, 2023, blog
  experiment). The effect depends on the constraint and the model.
- Anthropic's own guidance: "Tell Claude what to do instead of what not to
  do" (Claude prompting best practices).
- In a UX-writing setting, 11 AI tools given the same guideline "ignored
  instruction to avoid vague button labels such as 'OK' and 'Dismiss'", and
  "five out of eleven tools used noninclusive terms … despite being instructed
  to avoid such terminology"; "no tool achieved full compliance" (Sundberg &
  Berntsson, 2025, Chalmers master's thesis with ABB Robotics).

This is why the contracts are affirmative and the prohibitions live in the
linter. It is also why the measured result — a rules list performed about as
well as the full contract on modern instruction-tuned models — is reported
rather than hidden: the rules list in the test paired every "don't" with its
replacement, which makes it contrastive rather than purely negative.

## 3. Counter-examples work when paired and explained, not as a list

Contrastive in-context learning — a positive and a negative example with the
model asked to derive the difference — significantly beats standard few-shot
on GPT-3, ChatGPT and GPT-4 (Gao & Das, AAAI 2024). Unstructured negative
examples hurt (§2). One pair per element, difference named.

## 4. More constraints, more misses

Following degrades as constraints are added one level at a time across 13
models (FollowBench, ACL 2024) and with composed constraints (ComplexBench,
NeurIPS 2024); at 500 simultaneous keyword instructions the best frontier
model manages 68% per instruction with a bias toward earlier ones (IFScale,
2025, preprint — affirmative instructions, so this is a count effect only).
Information in the middle of a long context is used worst (Liu et al., TACL
2024 — QA and retrieval, not rule lists). Machine-checkable constraints
(forbidden words, length, format) are exactly the ones benchmarks verify by
code (IFEval, Zhou et al., 2023), so they go to the linter.

## 5. Style prompts are not a reliable lever

Personas in system prompts are unpredictable (§1). A CUI '26 controlled
between-subjects study changed only the system prompt (neutral vs
empathically framed) and asked whether prompt-level framing produces
measurable UX differences at all ("Do prompt-level empathy instructions
influence user experience?", CUI 2026; reported effect near zero,
*reported*). No study directly measures "friendly system prompt → verbose UI
strings". So the
contract overrides the element's register explicitly rather than asking for
"not too chatty".

## 6. What to put next to an estimate

- Numeric uncertainty barely dents trust in a number (d = −0.15) where verbal
  uncertainty does (d = −0.55); numeric ranges do not lower trust in the
  source (d = −0.03). Five experiments, n = 5,780 (van der Bles et al., PNAS
  2020).
- First-person uncertainty ("I'm not sure, but…") lowers confidence and
  agreement and *raises* accuracy in a pre-registered N = 404 experiment;
  the impersonal form is weaker and not significant (Kim et al., FAccT 2024).
  This is a conversational reply, not a value label; the interface's
  equivalent is the estimate label and 「未確認」.
- Models are reluctant to express uncertainty, and when forced, an average of
  47% of their "confident" answers are wrong; users rely on them with or
  without certainty markers (Zhou et al., ACL 2024). Well-calibrated
  confidence improves decisions by +20% [0.18, 0.23]; miscalibrated by +2%
  [−0.00, 0.04] and adds automation bias, N = 184 (Fregosi et al., AAAI
  2026). Stacking visual and verbal cues gave the most agreement with wrong
  answers, N = 495 (Ojewale et al., 2026, *reported*).
- Disclaimers: a limitation disclaimer had no significant effect on trust
  while authoritative style raised it, N = 594 (Metzger et al., CHI 2024,
  *reported*); disclaimer type had no stable effect on credibility (Lermann
  Henestrosa & Kimmerle, 2025, *reported*); security warnings habituate within
  a few exposures (Anderson et al., 2016, *reported*).
- Explanation: moderate transparency repairs trust, more erodes it (Kizilcec,
  CHI 2016, *reported*); explanations alone do not reduce overreliance, while
  cognitive forcing does — and gets the worst ratings, N = 199 (Buçinca et
  al., 2021).
- The real error in photo estimates: 43% of 189 records needed clarification;
  portion MAPE 32.8%, range −88.5% to +242.5%; milk and sugar in drinks often
  overlooked (Zuppinger et al., Nutrients 2022). Sauce-covered composite meals
  are the known bottleneck; 1 of 22 systems explains its predictions
  (Amugongo et al., Healthcare 2022).

Hence [uncertainty.md](uncertainty.md): label the estimate, expose the
correctable assumptions, add a range only when calibrated, and nothing else.

## 7. Why the skill's own checks are not its evidence

LLM judges favour their own generations, in proportion to their ability to
recognise them (Panickssery et al., 2024), prefer familiar low-perplexity text
(Wataoka et al., 2024), and favour related models across same-model,
inheritance and same-family relations (Li et al., ICLR 2026); their
preferences track style over substance (Feuer et al., ICLR 2025) and can be
gamed by semantics-preserving style edits with >65% success (Yang et al.,
ICML 2026). Part of measured self-preference is an evaluator-quality
confound; 51% of cases survive the control (Roytburg et al., ICML 2026).
A skill, its probes and its grader written by one model is criterion leakage:
in the first version of this skill, 76% of the grader's forbidden strings
appeared verbatim in the skill text. The measurement in
[evaluation.md](evaluation.md) therefore used probes authored by two other
model families, judges from families that did not write the skill, and a
blind human rating.

## 8. Traditional Chinese

Taiwanese-Mandarin models trail their Simplified counterparts and Traditional
Chinese is under-represented in benchmarks (Chen et al., TMLU, 2024; Tam et
al., TMMLU+, 2024). The drift itself is measured: SC-TC-Bench prompted 11
models with 110 regional term pairs, 15 times each, and every model except
Breeze chose the mainland term significantly more often under a Traditional
prompt than a Simplified one — on average 37.5 of the 110 terms misaligned at
least 3 times in 15, against 4.4 under Simplified prompts; a term
character-converted but not localised counts as misaligned (Lyu, Luo, Kang &
Koenecke, FAccT 2025; Claude and Gemini were not tested). In this project's
own runs, one subject wrote a Traditional Chinese brief's answer in
Simplified characters unprompted. Getting the script right and writing the
Taiwanese word are two different tests; models fail the second.

The lexicon's word list is drawn from the Ministry of Education's cross-strait
term table and OpenCC's Taiwan-phrase dictionary (`s2twp`, which localises
數據庫→資料庫 where `s2tw` only changes the script); both are dictionaries
with one-to-many ambiguities, so the linter keeps a software-context
whitelist and warns rather than errors on the ambiguous tier.

## 9. Guidance that already says this

Apple: "Include informative text only if it adds value"; "Always use 'Cancel'
to title a button that cancels the alert's action"; "If your alert text and
button titles are clear, you don't need to explain what the buttons do"; "be
direct, and use a neutral, approachable tone" (HIG, Alerts). GOV.UK: "start
with less"; "drop any unnecessary words"; "approachable and helpful, but not
overly familiar"; "Aim to be boring"; "If you find yourself having to explain
how the user interface works, that's a sign something has gone wrong"
(Service Manual). Google Workspace add-on UI guide: "You shouldn't need to
write much. Most actions should be made clear through iconography, layout,
and short labels"; errors "explain the problem from the user's standpoint,
and suggest how to fix it". Microsoft's Traditional Chinese localization
style guide: "The general style should be clear, friendly and concise";
"Microsoft voice avoids an unnecessarily formal tone"; 「請」 before an
imperative makes it polite; buttons are ［取消］. Taiwan's own: the Ministry
of Digital Affairs' 政府網站服務管理規範 (2024) — 「內容用詞應使用一致的詞語來撰
寫」「功能按鈕應明顯易按、簡單清楚」; TIPO's UX principles — 清楚／簡要／有用，
「冗贅敘述…應…被優先改善」, form errors 「標示出問題點並提供範例或建議填寫方
式」; MozTW's l10n guide — 「需符合台灣人常用的語法（o網路 x互聯網）」; MDN's
zh-TW guide — 「台灣譯者容易受到中國慣用語的影響而不自知」 and 「毋須刻意展現謙卑
的態度」. None of them bans natural language; all of them ban the clause that
carries nothing and the word that is not Taiwan's.

## 10. What the field shows

Apache Superset backfilled 24 locale catalogues with Claude in July 2026 and
marked every string fuzzy, "flagged for human review", while still shipping
it (apache/superset PR #42099). A native French speaker then reviewed the 219
AI strings in the French catalogue and corrected 38 — for the project's own
terminology (`dataset` had been given the minority translation), and for the
non-breaking space French puts before a colon — while every placeholder check
had passed (issue #42536). The Portuguese catalogue was re-read entry by
entry against the live app for pt-PT versus pt-BR wording (PR #42137). The
mechanical checks catch what they can; what was wrong was vocabulary, locale
convention and register, which is what this skill's contracts and lexicon
are for.

Projects that constrain their agents do it the same way: PostHog's AGENTS.md
sends every user-visible string through a copy skill, names "the tells of
AI-generated text" (em dashes, "not just X, but Y", rule-of-three padding,
hedging preambles) and orders its automation lint → lint-staged → skill →
instructions; SuperPlane's ui-copy skill starts from the nearest existing
copy and asks that "every word has a job". A controlled study of
repository-level context files found they do not generally raise task
success and cost over 20% more inference — agents read and obey them, so the
burden is the surplus requirements (Gloaguen et al., 2026). That is why
SKILL.md is short and the contracts, lexicon and evidence are separate files
loaded when needed. Constrained decoding drives schema validity to 100% and
leaves semantic errors where they were (Chavan, 2026), which matches the
schema arm's near-zero effect in the measurement: a schema fixes the shape
of a string, not its wording.

## Gaps this skill's own measurement addresses

No peer-reviewed benchmark evaluates UI microcopy register in any language
(the closest, Screen2Words, summarises whole screens; the UI-generation
benchmarks score text by character overlap with a reference, and the nearest
semantic study, Calò et al. 2026, scores accessibility meaning — generic
"Submit" buttons were 27% of its 541 faults — not register). No study compares
rules-only, positive-only and contrastive contracts on interface strings. The
evaluation in the companion repository is a first, small answer.
