<h1 align="center">ui-microcopy</h1>

<p align="center">
  <strong>A Claude Code skill and a linter for interface strings.</strong><br>
  Button labels, statuses, errors, empty states, value rows, notes and dialog copy, in 正體中文（台灣）, English and 日本語.
</p>

<p align="center">
  <img alt="Claude Code skill" src="https://img.shields.io/badge/CLAUDE_CODE-SKILL-2196F3?style=for-the-badge">
  <img alt="Linter: Python 3, no dependencies" src="https://img.shields.io/badge/LINTER-PYTHON_3%2C_NO_DEPS-4CAF50?style=for-the-badge&logo=python&logoColor=white">
  <img alt="Languages" src="https://img.shields.io/badge/ZH--TW_·_EN_·_JA-00A5A5?style=for-the-badge">
</p>

<p align="center">
  <a href="README.md">繁體中文</a> · <strong>English</strong>
</p>

<p align="center">
  <a href="#installation">Installation</a>
  · <a href="SKILL.md">SKILL.md</a>
  · <a href="references/roles.md">Element contracts</a>
  · <a href="references/zh-tw-lexicon.md">Taiwan lexicon</a>
  · <a href="#the-linter">Linter</a>
  · <a href="#measurement">Measurement</a>
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

## Overview

Interface strings produced by language models often carry the register of a chat reply: a button
written as an answer (「算了」), a status written as spoken report (「裝好了」), a note beside an
estimate written as an account of how the number was produced (「碗與叉子本身不計入營養」「數字不是
推測」). The strings are grammatical; the defect is register — the form of a conversational reply
entering a field that has a single function.

The repository contains two parts.

- **The skill** is the writing procedure. Ten tests run in a fixed order — language, facts,
  invention, element form, deletion — with one contrastive pair per element and the difference
  stated. The order is the design decision: a procedure that begins with deletion removes required
  facts and turns answers to English briefs into Chinese; this version was rewritten after that was
  measured.
- **The linter** is a rule-based check. It covers the patterns models produce (reply lexicon,
  colloquial completion, 「我們」, provenance remarks, apparatus and absence disclaimers, exclamation
  marks, China vocabulary), reads TSV, JSON, JSONL, Flutter ARB, plain text and Markdown, and gates
  CI with its exit code. The same drift appears in a README a model writes — headings become
  invitations, sentences address the reader — and the documentation rules exist for that. Being rule-based, it gives a reviewer, a pipeline and an evaluation harness the
  same findings.

## What it provides

### Element contracts

Each interface string has one function: to name an action, state a condition, tag a figure, or
give the fact that changes how a figure is read. [references/roles.md](references/roles.md) defines
for each element its form, its voice budget and one ✓/✗ pair.

| Element | Form | Voice |
| --- | --- | --- |
| button | the action's name: verb phrase, no person, not a question | none |
| dialog-title | the decision; a question only when the buttons answer it | none |
| dialog-body | the consequence, stated once, without repeating what is on screen | low |
| status | the closed state: 已儲存 / Export complete / 保存しました | none |
| error | what happened, the cause if known, the next step if one exists | none |
| empty | the state of having nothing; the action stays on the existing control | none |
| label | the name of the thing; for a setting, the behaviour when it is on | none |
| value | figure, unit, range, target; uncertainty carried by figure and layout | none |
| note | the facts the brief gives, one clause each; empty when it gives none | none |
| title | the name of the screen or step | onboarding may be warm |

Platform conventions (Apple HIG casing and fixed names, Material sentence case, tap versus click)
are listed at the end of the same file and affect only casing, fixed names and the gesture verb.

### Uncertainty policy

[references/uncertainty.md](references/uncertainty.md) divides what may accompany an estimate into
three tiers: the estimate's identity and the assumption a reader can correct are required; a range
is conditional on calibration; apparatus remarks, absence remarks, boilerplate cautions,
self-defence and a model's own confidence figure are excluded. The basis is the
uncertainty-communication literature.

### Taiwan lexicon

[references/zh-tw-lexicon.md](references/zh-tw-lexicon.md) holds 40 term pairs grouped by screen
domain (storage, network, devices, media, accounts, actions), each with the concept it names, and a
software-context whitelist (帳號, 用戶端, 租用戶, restaurant 菜單). The skill instructs the agent to
take the rows relevant to the current screen rather than read the table. Measured on briefs that
invite drift, the one to three relevant rows raised use of the canonical Taiwan term from 43% to
66%; the whole table reached 51%; a lone negative instruction ("do not use China usage") was the
only condition that lowered the result.

### Field contracts for an in-app model

When a string is produced by a runtime model (a photo-estimate note, an AI summary), the object of
correction is the field contract rather than the prose.
[references/runtime-llm-output.md](references/runtime-llm-output.md) defines the contract and
[assets/runtime-prompt-block.zh-TW.md](assets/runtime-prompt-block.zh-TW.md) is the prompt block:
one contrastive pair per field, an allowed empty value, the source in its own field, no request
for a confidence or a ± range.

### Comparison with other approaches

Applicability of each method, from the measurements:

|                                            | Rules file only | This skill | Linter in CI | zhtw MCP |
| ------------------------------------------ | :-------------: | :--------: | :----------: | :------: |
| Strings written by a person                |       ⚠️        |     ✅     |      ✅      |    —     |
| Strings written by an agent in a session   |       ⚠️        |     ✅     |      ✅      |    —     |
| An in-app model                            |       —         |     ✅     |      ⚠️      |    —     |
| Detecting 「當前」「保存」                    |       —         |     ⚠️     |      ✅      |    —     |
| Retaining required facts                   |       ⚠️        |     ✅     |      —       |    —     |
| Keeping the brief's language               |       ⚠️        |     ✅     |      —       |    —     |
| Long-form 翻譯腔 and punctuation            |       —         |     —      |      —       |    ✅    |

A rules file is a reduced form of the skill (the rules arm of the evaluation). The linter detects
term errors with a rate of about 2%, which neither reading nor model self-checking finds reliably.
The zhtw MCP addresses long-form prose; it reported nothing on the strings above.

## Installation

With the [Skills CLI](https://github.com/vercel-labs/skills) (Node 18 or later), at user level:

```sh
npx skills add KoukeNeko/ui-microcopy -g -a claude-code
```

Omit `-g` to install into the current project's `.claude/skills/`; omit `-a` to let the CLI list
the agents it detects (Codex, Cursor, OpenCode and others read the same `SKILL.md`). Update with
`npx skills update`.

Without Node, clone the repository:

```sh
git clone https://github.com/KoukeNeko/ui-microcopy.git ~/.claude/skills/ui-microcopy
```

## Usage

1. **Writing strings.** The skill triggers when UI text is written or reviewed, a control is named,
   an error or confirmation is worded, or a prompt is written for an in-app model. The input is a
   brief: screen, element, the facts the string must carry, language. The final check before an
   answer:

   ```text
   1. Same language as the brief
   2. Every fact the brief listed is retained
   3. Element form correct, nothing further
   4. When the strings are in a file, run the linter and correct what it reports
   ```

2. **Checking strings.** Run the linter in CI or a pre-commit hook. Exit status is 0 with no
   errors, otherwise 1; `--strict` treats warnings as failures.

   ```sh
   python3 scripts/microcopy_lint.py --format arb lib/l10n/app_zh.arb
   python3 scripts/microcopy_lint.py --format tsv strings.tsv --strict
   python3 scripts/microcopy_lint.py --format json --json strings.json
   python3 scripts/microcopy_lint.py --format md README.md docs/*.md
   ```

   Input formats: TSV as `role<TAB>text` per line; JSON and JSONL as `{"role": ..., "text": ...}`
   objects; plain text as one string per line with role `generic`; Markdown with headings as `heading` and paragraphs and list items as `prose`, skipping code, tables and ✓/✗ pairs. Roles: `button`, `dialog-title`,
   `dialog-body`, `title`, `label`, `status`, `error`, `empty`, `value`, `note`, `ai-note`,
   `generic`.

3. **Constraining an in-app model.** Place
   [assets/runtime-prompt-block.zh-TW.md](assets/runtime-prompt-block.zh-TW.md) beside the output
   format section of the app's prompt; run the app's prompt through the
   [evaluation harness](https://github.com/KoukeNeko/ui-microcopy-eval) and read the note-emptiness
   table to confirm the field contract takes effect.

## The linter

```sh
python3 scripts/microcopy_lint.py --list-rules
python3 scripts/microcopy_lint.py --self-test
```

| Rule | Level | Detects |
| --- | --- | --- |
| `chatty-lexicon` | error | a conversational reply in a control or status position (算了, 裝好了) |
| `completion-slang` | error | completion reported in colloquial form |
| `we-voice` | error | an interface speaking as 「我們」 |
| `second-person` | warn | 「你的」 where no ownership needs distinguishing |
| `question-label` | error | a control worded as a question instead of an action name |
| `provenance-meta` | error | an account of how the value was produced (「數字不是推測」) |
| `apparatus-disclaimer` | error | an apparatus remark (「碗與叉子本身不計入營養」) |
| `absence-disclaimer` | warn | a statement that treats "not seen" as evidence |
| `boilerplate-disclaimer` | error / warn | a caution applicable to any row |
| `self-estimated-range` | warn | a confidence or ± produced by the model |
| `hedge-duplication` | warn | an estimate hedged again in words |
| `method-filler` | warn | method described inside a note read as a result |
| `redundant-qualifier` | warn | 「約」 before a range, 「上限」 after a slash |
| `negated-alternative` | warn | a case stated, then the alternative it already excludes denied (「顯示「無法取得」，不以 0 站計」) |
| `exclamation-emoji` | error | tone not applicable to routine, error or destructive states |
| `punctuation-form` | warn | half-width punctuation in a Chinese sentence |
| `trailing-period` | warn | a full stop on a label |
| `role-length` | warn | a string beyond the role's length cap |
| `zh-tw-vocabulary` | error / warn | China vocabulary; the Taiwan whitelist is masked before matching |
| `heading-form` | error | a documentation heading that invites or asks (「各種做法比一比」, "Let's compare") |
| `heading-question` | warn | a heading phrased as a question or how-to (「怎麼跑」, "How to install") |
| `prose-particle` | error | a speech particle at the end of a documentation sentence (吧, 喔, 啦) |
| `reader-address` | warn | documentation that addresses the reader (「你」) |
| `rhetorical-question` | warn | a question in documentation the text answers itself |

Rules and examples are in `scripts/microcopy_lint.py`, with no dependency beyond Python 3.
`--self-test` verifies each rule against its examples.

## Measurement

The first version's grader shared text with the skill: three quarters of its forbidden strings
appeared in the skill body. This version was measured on 32 held-out briefs written by two authors
who had not seen the skill, across seven model channels, scored by two judges from other model
families on two axes (no surplus, every required fact present), with paired analysis, a
brief-clustered bootstrap and calibration against 108 blind human ratings.

| | Net pass Δ vs control | Δ required facts |
| --- | --- | --- |
| first version, Claude-written briefs | +16 pp | −0.3 pp |
| first version, GPT-written briefs | −5 pp | −15.7 pp |
| **this version, all briefs, judge A** | **+8 pp [+1, +15]** | −3.4 pp |
| **this version, all briefs, judge B** | **+8 pp [+1, +15]** | +1.1 pp |

Answers to English briefs containing Chinese: 41–82% in the first version, 0–15% in this one.
Notes whose brief listed no facts: filled 88% of the time by unaided models, 0% here. These are
development figures; the language fix followed the first draft's results, and a confirmatory run
requires a frozen skill and unused briefs. The harness, briefs, generations and verdicts are in
[ui-microcopy-eval](https://github.com/KoukeNeko/ui-microcopy-eval).

## Sources of the rules

Every source was opened and its title, authors, venue and cited claim verified. The contracts agree
with existing guidance and add what it leaves implicit: Apple's Human Interface Guidelines
(Writing, Alerts), the Material 3 UX writing guide, Microsoft's zh-TW style guide, GOV.UK content
guidance, the Ministry of Education's 兩岸常用詞語對照表, the MDN and MozTW zh-TW translation
guides, and the Ministry of Digital Affairs' 政府網站服務管理規範. The uncertainty policy rests on
the uncertainty-communication literature (numeric ranges cost little trust, verbal hedges cost
more; disclaimers habituate; verbalised confidence is poorly calibrated). The contrastive-example
form and the test order rest on the instruction-following literature and this skill's own
measurement. The full list is in [References](#references).

## Repository layout

```text
SKILL.md                              the procedure, the ten tests, the final check
references/
  roles.md                            element contracts, ✓/✗ pairs, platform conventions
  uncertainty.md                      the policy for text beside an estimate
  zh-tw-lexicon.md                    Taiwan terms by screen domain, whitelist, punctuation
  runtime-llm-output.md               field contracts for an in-app model
assets/
  runtime-prompt-block.zh-TW.md       the prompt block for that model
scripts/
  microcopy_lint.py                   the linter; --self-test, --list-rules
```

## Limits

- The measurement is 32 briefs with two samples each and detects effects of ten points or more.
  One human rater, who is the person who raised the issue.
- The lexicon holds 40 pairs, covering the terms models produce in software copy rather than every
  difference between China and Taiwan usage; the second tier (提交, 點擊, 保存, 設置) is a warning.
- The Japanese and English contracts carry examples; their held-out measurement is six briefs each.
- The skill works on text only and has no view of the screen; the visible-information test relies
  on the brief stating what is on it.

## References

128 sources, alphabetical. Vendor documentation and open-source discussions are verified to the
same standard as papers; where a figure was taken from an abstract rather than the body, the skill's
evidence file records it.

<details>
<summary>Show all 128</summary>

- 0xdorian-sm. (2026, July 28). [i18n][fr] Native review of the French catalog: AI backfill + untranslated strings. apache/superset issue #42536 https://github.com/apache/superset/issues/42536
- Amugongo, L. M., Kriebitz, A., Boch, A., & Lütge, C. (2022). Mobile computer vision-based applications for food recognition and volume and calorific estimation: A systematic review. Healthcare, 11(1), 59 https://pmc.ncbi.nlm.nih.gov/articles/PMC9818870/
- Anderson, B. B., Jenkins, J. L., Vance, A., Kirwan, C. B., & Eargle, D. (2016). Your memory is working against you: How eye tracking and memory explain habituation to security warnings. Decision Support Systems, 92, 3–13. https://doi.org/10.1016/j.dss.2016.09.010
- Anthropic. (2026). How Claude remembers your project. Claude Code docs https://code.claude.com/docs/en/memory
- Anthropic. (2026). Prompting best practices — Tell Claude what to do instead of what not to do. Claude Developer Platform docs https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Anthropic. (2026). Skill authoring best practices. Claude Developer Platform docs https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Apple. (2025, December 16). Writing. Human Interface Guidelines https://developer.apple.com/design/human-interface-guidelines/writing
- Apple. (n.d.). Alerts. Human Interface Guidelines https://developer.apple.com/design/human-interface-guidelines/alerts
- Artstein, R., & Poesio, M. (2008). Inter-coder agreement for computational linguistics. Computational Linguistics, 34(4) https://aclanthology.org/J08-4004/
- Bauer, J. (2024). Does GitHub Copilot improve code quality? Here's what the data says. The GitHub Blog https://github.blog/news-insights/research/does-github-copilot-improve-code-quality-heres-what-the-data-says/
- BetterTranslator. (2026). What it costs an agent to translate a resource file https://bettertranslator.eu/en/benchmark
- Bieberstein, A., Schnitzer, B. L., Gampe, S., & Korn, O. (2026). Do prompt-level empathy instructions influence user experience? Evidence from a controlled chatbot study. CUI '26 (8th ACM Conference on Conversational User Interfaces). https://doi.org/10.1145/3816046.3816221
- BIG-bench. (n.d.). Canary GUID and training-on-test-set task documentation [GitHub] https://github.com/google/BIG-bench/blob/main/bigbench/benchmark_tasks/training_on_test_set/README.md
- Bleakley, A. (2023). Saying what not to do [blog experiment] https://alexbleakley.com/blog/saying-what-not-to-do
- Bogoychev, N., & Chen, P. (2023). Terminology-aware translation with constrained decoding and large language model prompting. Proceedings of the Eighth Conference on Machine Translation (WMT 2023) https://aclanthology.org/2023.wmt-1.80/
- Briakou, E., Agrawal, S., Zhang, K., Tetreault, J., & Carpuat, M. (2021). A review of human evaluation for style transfer. GEM 2021 https://aclanthology.org/2021.gem-1.6/
- Briakou, E., Lu, D., Zhang, K., & Tetreault, J. (2021). Olá, bonjour, salve! XFORMAL: A benchmark for multilingual formality style transfer. NAACL 2021 https://aclanthology.org/2021.naacl-main.256/
- Buçinca, Z., Malaya, M. B., & Gajos, K. Z. (2021). To trust or to think: Cognitive forcing functions can reduce overreliance on AI in AI-assisted decision-making. PACM HCI (CSCW). arXiv:2102.09692 https://arxiv.org/abs/2102.09692
- BYVoid. (n.d.). OpenCC — Open Chinese Convert [README]. s2tw／s2twp 與 --ambiguities https://github.com/BYVoid/OpenCC/blob/master/README.md
- Calò, T., Gurita, A.-E., & De Russis, L. (2026). Measuring the semantic accessibility gap in LLM-generated web UIs. CHI EA '26 https://tommasocalo.github.io/papers/26-semacces-chiea.pdf
- Castricato, L., Lile, N., Anand, S., Schoelkopf, H., Verma, S., & Biderman, S. (2024). Suppressing pink elephants with direct principle feedback. arXiv:2402.07896 https://arxiv.org/abs/2402.07896
- Chavan, A. (2026). Constrained decoding eliminates structural failures in small LLMs but reveals a scale-dependent semantic gap. arXiv:2609.23742 https://arxiv.org/abs/2609.23742
- Chen, P.-H., et al. (2024). Measuring Taiwanese Mandarin language understanding (TMLU). arXiv:2403.20180 https://arxiv.org/abs/2403.20180
- Chiang, W.-L., Zheng, L., Sheng, Y., Angelopoulos, A. N., Li, T., Li, D., Zhu, B., Zhang, H., Jordan, M., Gonzalez, J. E., & Stoica, I. (2024). Chatbot Arena: An open platform for evaluating LLMs by human preference. ICML 2024, PMLR 235:8359–8388 https://proceedings.mlr.press/v235/chiang24b.html
- Clark, E., August, T., Serrano, S., Haduong, N., Gururangan, S., & Smith, N. A. (2021). All that's 'human' is not gold: Evaluating human evaluation of generated text. ACL 2021. arXiv:2107.00061 https://arxiv.org/abs/2107.00061
- Crowdin. (2026). Crowdin AI. Crowdin Enterprise docs https://support.crowdin.com/enterprise/crowdin-ai/
- Crowdin. (2026). QA check settings. Crowdin docs https://support.crowdin.com/project-settings/qa-checks/
- Cursor. (2025, updated May 2026). How we compare model quality in Cursor (CursorBench). Cursor blog https://cursor.com/blog/cursorbench
- Cursor. (2026). Rules. Cursor docs https://cursor.com/help/customization/rules
- Dahan, N., Peng, Z., Yvon, F., & Bawden, R. (2026). Improving term evaluation in machine translation: Variation matters. AMTA 2026 https://arxiv.org/abs/2609.08779
- Dror, R., Baumer, G., Shlomov, S., & Reichart, R. (2018). The hitchhiker's guide to testing statistical significance in natural language processing. ACL 2018 https://aclanthology.org/P18-1128/
- Dubois, Y., Galambosi, B., Liang, P., & Hashimoto, T. B. (2024). Length-controlled AlpacaEval: A simple way to debias automatic evaluators. COLM 2024. arXiv:2404.04475 https://arxiv.org/abs/2404.04475
- Dussolle, A., Cardeña Díaz, A., Sato, S., & Devine, P. (2025). M-IFEval: Multilingual instruction-following evaluation. Findings of NAACL 2025 https://aclanthology.org/2025.findings-naacl.344.pdf
- Feuer, B., Goldblum, M., Datta, T., Nambiar, S., Besaleli, R., Dooley, S., Cembalest, M., & Dickerson, J. P. (2025). Style outweighs substance: Failure modes of LLM judges in alignment benchmarking. ICLR 2025 https://proceedings.iclr.cc/paper_files/paper/2025/hash/1eb36d07ebb13be16ddbda679a95018b-Abstract-Conference.html
- Fregosi, C., Vicente, L., Campagner, A., & Cabitza, F. (2026). Too sure for our own good: A user study on AI confidence and human reliance. AAAI 2026, 40(21) https://ojs.aaai.org/index.php/AAAI/article/view/38798
- Gao, X., & Das, K. (2024). Customizing language model responses with contrastive in-context learning. AAAI 2024 https://ojs.aaai.org/index.php/AAAI/article/view/29760
- Geng, S., Cooper, H., Moskal, M., Jenkins, S., Berman, J., Ranchin, N., et al. (2025). JSONSchemaBench: A rigorous benchmark of structured outputs for language models. arXiv:2501.10868 https://arxiv.org/abs/2501.10868
- Ghazvininejad, M., Gonen, H., & Zettlemoyer, L. (2023). Dictionary-based phrase-level prompting of large language models for machine translation. arXiv:2302.07856 https://arxiv.org/abs/2302.07856
- GitHub. (2026). About customizing GitHub Copilot responses. GitHub Docs https://docs.github.com/en/copilot/concepts/prompting/response-customization
- Gloaguen, T., Mündler-Sasahara, N., Müller, M. N., Raychev, V., & Vechev, M. (2026). Evaluating AGENTS.md: Are repository-level context files helpful for coding agents? arXiv:2602.11988 https://arxiv.org/abs/2602.11988
- Google Cloud. (2026). Creating and using glossaries (Advanced). Cloud Translation docs https://docs.cloud.google.com/translate/docs/advanced/glossary
- Google Research. (2022). Wiki-Conciseness dataset (concise rewrites of 2,000 Wikipedia sentences; 2-way and 5-way annotated) [Dataset README] https://github.com/google-research-datasets/wiki-conciseness-dataset/blob/main/README.md
- Google. (n.d.). Style guide — UX writing best practices. Material Design 3 https://m3.material.io/foundations/content-design/style-guide/ux-writing-best-practices
- Google. (n.d.). UI style guide for Google Workspace add-ons https://developers.google.com/workspace/add-ons/guides/workspace-style
- GOV.UK. (n.d.). Writing for user interfaces. Service Manual https://www.gov.uk/service-manual/design/writing-for-user-interfaces
- Gu, J., et al. (2024). A survey on LLM-as-a-judge. arXiv:2411.15594 https://arxiv.org/abs/2411.15594
- Hong, K., Troynikov, A., & Huber, J. (2025, July 14). Context rot: How increasing input tokens impacts LLM performance. Chroma Research https://www.trychroma.com/research/context-rot
- Hu, Z., Song, L., Zhang, J., Xiao, Z., Wang, T., Chen, Z., Yuan, N. J., Lian, J., Ding, K., & Xiong, H. (2025). Explaining length bias in LLM-based preference evaluations. Findings of EMNLP 2025 https://aclanthology.org/2025.findings-emnlp.358/
- Huang, P., Mu, Y., Wu, Y., Li, B., Xiao, C., Xiao, T., & Zhu, J. (2024). Translate-and-revise: Boosting large language models for constrained translation. CCL 2024 https://aclanthology.org/2024.ccl-1.82/
- Hwang, K., Kim, S., Lee, J., & Kwak, N. (2024). Do not think about pink elephant! arXiv:2404.15154 https://arxiv.org/abs/2404.15154
- J0s3-H3nr1qu3. (2026, July 17). fix(i18n): review and complete Portuguese (pt_PT) translation catalog. apache/superset PR #42137 https://github.com/apache/superset/pull/42137
- Jang, J., Ye, S., & Seo, M. (2023). Can large language models truly understand prompts? A case study with negated prompts. PMLR 203 (Transfer Learning for NLP workshop). arXiv:2209.12711 https://arxiv.org/abs/2209.12711
- Jaroslawicz, D., Whiting, B., Shah, P., & Maamari, K. (2025). How many instructions can LLMs follow at once? (IFScale). arXiv:2507.11538 https://arxiv.org/abs/2507.11538
- Jiang, Y., Wang, Y., Zeng, X., Zhong, W., Li, L., Mi, F., Shang, L., Jiang, X., Liu, Q., & Wang, W. (2024). FollowBench: A multi-level fine-grained constraints following benchmark for large language models. ACL 2024 https://aclanthology.org/2024.acl-long.257/
- Jon, J., Variš, D., Novák, M., Aires, J. P., & Bojar, O. (2023). Negative lexical constraints in neural machine translation. arXiv:2308.03601 https://arxiv.org/abs/2308.03601
- Joslyn, S. L., & LeClerc, J. E. (2012). Uncertainty forecasts improve weather-related decisions and attenuate the effects of forecast error. Journal of Experimental Psychology: Applied, 18(1), 126–140. https://doi.org/10.1037/a0025185 https://pubmed.ncbi.nlm.nih.gov/21875244/
- Jung, S., Garcinuno, A., & Mateega, S. (2025). UI-Bench: A benchmark for evaluating design capabilities of AI text-to-app tools. arXiv:2508.20410 https://arxiv.org/abs/2508.20410
- Kim, J., Koo, S., & Lim, H. (2024). PANDA: Persona attributes navigation for detecting and alleviating overuse problem in large language models. EMNLP 2024 (main) https://aclanthology.org/2024.emnlp-main.670/
- Kim, S. S. Y., Liao, Q. V., Vorvoreanu, M., Ballard, S., & Vaughan, J. W. (2024). "I'm not sure, but...": Examining the impact of large language models' uncertainty expression on user reliance and trust. FAccT 2024. arXiv:2405.00623 https://arxiv.org/abs/2405.00623
- Kizilcec, R. F. (2016). How much information? Effects of transparency on trust in an algorithmic interface. CHI 2016. https://doi.org/10.1145/2858036.2858402
- Lachin, J. M. (1992). Power and sample size evaluation for the McNemar test with application to matched case-control studies. Statistics in Medicine, 11(9) https://onlinelibrary.wiley.com/doi/10.1002/sim.4780110909
- Lermann Henestrosa, A., & Kimmerle, J. (2025). "Always check important information!" — The role of disclaimers in the perception of AI-generated content. Computers in Human Behavior: Artificial Humans. https://doi.org/10.1016/j.chbah.2025.100142
- Li, D., Sun, R., Huang, Y., Zhong, M., Jiang, B., Han, J., Zhang, X., Wang, W., & Liu, H. (2026). Preference leakage: A contamination problem in LLM-as-a-judge. ICLR 2026. arXiv:2502.01534 https://arxiv.org/abs/2502.01534
- Li, Y., Zhang, G., Qu, X., Li, J., et al. (2024). CIF-Bench: A Chinese instruction-following benchmark for evaluating the generalizability of large language models. arXiv:2402.13109 https://arxiv.org/abs/2402.13109
- Liao, X., & Melero, M. (2026). SalamandraTA at WMT 2026 terminology shared task: Hard examples are better teachers. arXiv:2609.09999 https://arxiv.org/abs/2609.09999
- Lin, Y.-T., & Chen, Y.-N. (2023). Taiwan LLM: Bridging the linguistic divide with a culturally aligned language model. arXiv:2311.17487 https://arxiv.org/abs/2311.17487
- Lin, Z., Zhou, Z., Zhao, Z., Wan, T., Ma, Y., Gao, J., & Li, X. (2025). WebUIBench: A comprehensive benchmark for evaluating multimodal large language models in WebUI-to-code. Findings of ACL 2025 https://aclanthology.org/2025.findings-acl.815.pdf
- Liu, J., Qader, R., Caillaut, G., & Nakhlé, M. (2025). Lingua Custodia's participation at the WMT 2025 terminology shared task. arXiv:2510.17504 https://arxiv.org/abs/2510.17504
- Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., & Liang, P. (2024). Lost in the middle: How language models use long contexts. TACL, 12 https://aclanthology.org/2024.tacl-1.9/
- Lokalise. (2026, April 26). AI translation with glossary support: Deterministic terminology for LLMs. Lokalise blog https://lokalise.com/blog/ai-translation-glossary/
- Lou, R., Zhang, K., & Yin, W. (2024). Large language model instruction following: A survey of progresses and challenges. Computational Linguistics, 50(3) https://direct.mit.edu/coli/article/50/3/1053/121669/Large-Language-Model-Instruction-Following-A
- Lu, H., Yang, H., Huang, H., Zhang, D., Lam, W., & Wei, F. (2024). Chain-of-dictionary prompting elicits translation in large language models. EMNLP 2024 https://aclanthology.org/2024.emnlp-main.55/
- Lu, Z., Yang, Y., Ren, H., Hou, H., Xiao, H., Wang, K., Shi, W., et al. (2025). WebGen-Bench: Evaluating LLMs on generating interactive and functional websites from scratch. arXiv:2505.03733 https://arxiv.org/abs/2505.03733
- Lyu, H., Luo, J., Kang, J., & Koenecke, A. (2025). Characterizing bias: Benchmarking large language models in Simplified versus Traditional Chinese (SC-TC-Bench). FAccT 2025 https://github.com/brucelyu17/SC-TC-Bench
- Mann, L., Saxena, N., Tandon, S., Sun, C., Toteja, S., & Zhu, K. (2025). Don't think of the white bear: Ironic negation in transformer models under cognitive load. arXiv:2511.12381 https://arxiv.org/abs/2511.12381
- MDN. (n.d.). zh-TW 翻譯指南（translated-content/docs/zh-tw/translation-guide.md） https://github.com/mdn/translated-content/blob/main/docs/zh-tw/translation-guide.md
- Metzger, L., Miller, L., Baumann, M., & Kraus, J. (2024). Empowering calibrated (dis-)trust in conversational agents: A user study on the persuasive power of limitation disclaimers vs. authoritative style. CHI 2024 https://doi.org/10.1145/3613904.3642122
- Microsoft. (2024). Chinese (Traditional) localization style guide (zho-twn-StyleGuide.pdf, v10, 2024-09-18) https://www.microsoft.com/zh-tw/download/details.aspx?id=103029
- Mishra, S., Khashabi, D., Baral, C., & Hajishirzi, H. (2022). Cross-task generalization via natural language crowdsourcing instructions (Natural Instructions). ACL 2022. arXiv:2104.08773 https://arxiv.org/abs/2104.08773
- Moslem, Y., Haque, R., Kelleher, J. D., & Way, A. (2023). Adaptive machine translation with large language models. EAMT 2023 https://arxiv.org/abs/2301.13294
- Moslem, Y., Romani, G., Molaei, M., Haque, R., Kelleher, J. D., & Way, A. (2023). Domain terminology integration into machine translation: Leveraging large language models. WMT 2023 https://arxiv.org/abs/2310.14451
- Mozilla L10N. (n.d.). Mozilla 正體中文（台灣）在地化樣式與翻譯規範 https://mozilla-l10n.github.io/styleguides/zh-TW/
- Ojewale, V., Ryan, ?, Venkatasubramanian, S., Boykin, ?, et al. (2026). More is not better: Visual uncertainty cues and the fragility of trust calibration in LLM-assisted decision making. Computers in Human Behavior: Artificial Humans. https://doi.org/10.1016/j.chbah.2026.100307
- Ouyang, L., et al. (2022). Training language models to follow instructions with human feedback. arXiv:2203.02155 (NeurIPS 2022) https://arxiv.org/abs/2203.02155
- Panickssery, A., Bowman, S. R., & Feng, S. (2024). LLM evaluators recognize and favor their own generations. NeurIPS 2024. arXiv:2404.13076 https://arxiv.org/abs/2404.13076
- Phrase. (2026). AI Translation Agent. Phrase support https://support.phrase.com/hc/en-us/articles/20660272640284-AI-Translation-Agent
- PostHog. (2026). AGENTS.md — User-facing copy. PostHog/posthog repository https://github.com/PostHog/posthog/blob/master/AGENTS.md
- Rana, S. (2026). Semantic gravity wells: Why negative constraints backfire. arXiv:2601.08070 https://arxiv.org/abs/2601.08070
- Rao, S., & Tetreault, J. (2018). Dear Sir or Madam, may I introduce the GYAFC dataset: Corpus, benchmarks and metrics for formality style transfer. NAACL 2018 https://aclanthology.org/N18-1012/
- Roytburg, D., Bozoukov, M., Nguyen, M., Barzdukas, J., Puig-Hall, M., & Oozeer, N. F. (2026). Are LLM evaluators really narcissists? Sanity checking self-preference evaluations. ICML 2026, PMLR 306 https://proceedings.mlr.press/v306/roytburg26a.html
- rusackas. (2026, July 16). feat(i18n): backfill Chinese (Traditional) (zh_TW) translations (AI-generated, needs review). apache/superset PR #42102 https://github.com/apache/superset/pull/42102
- rusackas. (2026, July 16). feat(i18n): backfill missing translations across 24 catalogs (AI-generated, needs review). apache/superset PR #42099 https://github.com/apache/superset/pull/42099
- Saito, K., Wachi, A., Wataoka, K., & Akimoto, Y. (2023). Verbosity bias in preference labeling by large language models. arXiv:2310.10076 https://arxiv.org/abs/2310.10076
- Scansani, R., & Dugast, L. (2021). Glossary functionality in commercial machine translation: Does it help? A first step to identify best practices for a language service provider. MT Summit 2021 (Users and Providers Track) https://aclanthology.org/2021.mtsummit-up.8.pdf
- Seegmiller, P., & Preum, S. M. (2026). Measuring distribution shift in user prompts and its effects on LLM performance. ACL 2026 https://aclanthology.org/2026.acl-long.1508/
- Semenov, K., Zhu, D., Huang, X., Oncevay, A., Zouhar, V., Berger, N., & Chen, P. (2025). Findings of the WMT25 terminology translation task: Terminology is useful especially for good MTs. WMT 2025, 554–576 https://www2.statmt.org/wmt25/pdf/2025.wmt-1.30.pdf
- Semenov, K., Zouhar, V., Kocmi, T., Zhang, D., Zhou, W., & Jiang, Y. E. (2023). Findings of the WMT 2023 shared task on machine translation with terminologies. WMT 2023 https://aclanthology.org/2023.wmt-1.54/
- Sharma, M., Tong, M., Korbak, T., Duvenaud, D., Askell, A., Bowman, S., Durmus, E., Hatfield-Dodds, Z., Johnston, S., Kravec, S., Maxwell, T., McCandlish, S., Ndousse, K., Rausch, O., Schiefer, N., Yan, D., Zhang, M., & Perez, E. (2024). Towards understanding sycophancy in language models. ICLR 2024 https://proceedings.iclr.cc/paper_files/paper/2024/hash/0105f7972202c1d4fb817da9f21a9663-Abstract-Conference.html
- Shin, J., Lee, I., & Lim, C. (2026). Controlling and assessing appropriate persona use in LLM-based dialogue generation. arXiv:2609.04676 (accepted EMNLP 2026 main) https://arxiv.org/abs/2609.04676
- Si, C., Zhang, Y., Li, R., Yang, Z., Liu, R., & Yang, D. (2025). Design2Code: Benchmarking multimodal code generation for automated front-end engineering. NAACL 2025 https://aclanthology.org/2025.naacl-long.199.pdf
- Soumik, S. K. (2026). Judging the judges: A systematic evaluation of bias mitigation strategies in LLM-as-a-judge pipelines. arXiv:2604.23178 https://arxiv.org/abs/2604.23178
- Sun, Y., et al. (2025). Exposing the cracks: Vulnerabilities of retrieval-augmented LLM-based machine translation. arXiv:2510.00829 https://arxiv.org/abs/2510.00829
- Sun, Y., Wang, H., Li, D., Wang, G., & Zhang, H. (2025). The emperor's new clothes in benchmarking? A rigorous examination of mitigation strategies for LLM benchmark data contamination. ICML 2025 https://gangw.cs.illinois.edu/ICMLEmperor25.pdf
- Sundberg, H., & Berntsson, M. (2025). Exploration of AI-powered tools and UX writing solutions for improved content design process in a robotic software [Master's thesis, Chalmers University of Technology]. https://hdl.handle.net/20.500.12380/310878
- SuperPlane. (2026). ui-copy skill (SKILL.md), adapted from Operately. superplanehq/superplane repository https://github.com/superplanehq/superplane/blob/main/.agents/skills/ui-copy/SKILL.md
- Tam, Z.-R., Pai, Y.-T., Lee, Y.-W., Chen, J.-D., Chu, W.-M., Cheng, S., & Shuai, H.-H. (2024). An improved Traditional Chinese evaluation suite for foundation model (TMMLU+). arXiv:2403.01858 https://arxiv.org/abs/2403.01858
- ui-bench.dev. (2026). UX Judge — the frontend design benchmark for LLMs https://ui-bench.dev/ux-judge
- van der Bles, A. M., van der Linden, S., Freeman, A. L. J., & Spiegelhalter, D. J. (2020). The effects of communicating uncertainty on public trust in facts and numbers. PNAS, 117(14), 7672–7683. https://doi.org/10.1073/pnas.1913678117 https://www.pnas.org/doi/10.1073/pnas.1913678117
- van der Bles, A. M., van der Linden, S., Freeman, A. L. J., Mitchell, J., Galvao, A. B., Zaval, L., & Spiegelhalter, D. J. (2019). Communicating uncertainty about facts, numbers and science. Royal Society Open Science, 6(5), 181870. https://doi.org/10.1098/rsos.181870 https://royalsocietypublishing.org/doi/10.1098/rsos.181870
- van der Lee, C., Gatt, A., van Miltenburg, E., & Krahmer, E. (2021). Human evaluation of automatically generated text: Current trends and best practice guidelines. Computer Speech & Language, 67, 101151 https://doi.org/10.1016/j.csl.2020.101151
- Vrabcová, T., Kadlčík, M., Sojka, P., Štefánik, M., & Spiegel, M. (2025). Negation: A pink elephant in the large language models' room? arXiv:2503.22395 https://arxiv.org/abs/2503.22395
- Wang, B., Li, G., Zhou, X., Chen, Z., Grossman, T., & Li, Y. (2021). Screen2Words: Automatic mobile UI summarization with multimodal learning. UIST 2021. arXiv:2108.03353 https://arxiv.org/abs/2108.03353
- Wataoka, K., Takahashi, T., & Ri, R. (2024). Self-preference bias in LLM-as-a-judge. arXiv:2410.21819 https://arxiv.org/abs/2410.21819
- Wen, B., Ke, P., Gu, X., Wu, L., Huang, H., Zhou, J., Li, W., Hu, B., Gao, W., Xu, J., Liu, Y., Tang, J., Wang, H., & Huang, M. (2024). Benchmarking complex instruction-following with multiple constraints composition (ComplexBench). NeurIPS 2024 Datasets & Benchmarks https://proceedings.neurips.cc/paper_files/paper/2024/hash/f8c24b08b96a08ec7a7a975feea7777e-Abstract-Datasets_and_Benchmarks_Track.html
- Yang, S., Chiang, W.-L., Zheng, L., Gonzalez, J. E., & Stoica, I. (2023). Rethinking benchmark and contamination for language models with rephrased samples. arXiv:2311.04850 https://arxiv.org/abs/2311.04850
- Yang, X., Hooi, B., Deng, G., Zhang, T., & Dong, J. S. (2026). Turning bias into bugs: Bandit-guided style manipulation attacks on LLM judges (BITE). ICML 2026, PMLR 306 https://proceedings.mlr.press/v306/yang26w.html
- Yin, Z., Wang, H., Horio, K., Kawahara, D., & Sekine, S. (2024). Should we respect LLMs? A cross-lingual study on the influence of prompt politeness on LLM performance. SICon 2024 https://aclanthology.org/2024.sicon-1.2/
- Yun, S., Lin, H., Thushara, R., Bhat, M. Q., Wang, Y., Jiang, Z., Deng, M., et al. (2024). Web2Code: A large-scale webpage-to-code dataset and evaluation framework for multimodal LLMs. NeurIPS 2024 Datasets and Benchmarks https://proceedings.neurips.cc/paper_files/paper/2024/hash/cb66be286795d71f89367d596bf78ea7-Abstract-Datasets_and_Benchmarks_Track.html
- Zhang, X., Xiong, W., Chen, L., Zhou, T., Huang, H., & Zhang, T. (2025). From lists to emojis: How format bias affects model alignment. ACL 2025 (long) https://aclanthology.org/2025.acl-long.1308/
- Zhang, Y., Das, S. S. S., & Zhang, R. (2025). Demystify verbosity compensation behavior of large language models. UncertaiNLP 2025 (ACL workshop) https://aclanthology.org/2025.uncertainlp-main.14/
- Zheng, L., et al. (2023). Judging LLM-as-a-judge with MT-Bench and Chatbot Arena. NeurIPS 2023 Datasets & Benchmarks. arXiv:2306.05685 https://arxiv.org/abs/2306.05685
- Zheng, M., Pei, J., Logeswaran, L., Lee, M., & Jurgens, D. (2024). When "a helpful assistant" is not really helpful: Personas in system prompts do not improve performances of large language models. Findings of EMNLP 2024 https://aclanthology.org/2024.findings-emnlp.888/
- Zhou, J., Lu, T., Mishra, S., Brahma, S., Basu, S., Luan, Y., Zhou, D., & Hou, L. (2023). Instruction-following evaluation for large language models (IFEval). arXiv:2311.07911 https://arxiv.org/abs/2311.07911
- Zhou, K., Hwang, J. D., Ren, X., & Sap, M. (2024). Relying on the unreliable: The impact of language models' reluctance to express uncertainty. ACL 2024 https://aclanthology.org/2024.acl-long.198/
- Zuppinger, C., Taffé, P., Burger, G., Badran-Amstutz, W., Niemi, T., Cornuz, C., Belle, F. N., Chatelan, A., Paclet Lafaille, M., Bochud, M., & Gonseth Nusslé, S. (2022). Performance of the digital dietary assessment tool MyFoodRepo. Nutrients, 14(3), 635 https://pmc.ncbi.nlm.nih.gov/articles/PMC8838173/
- 教育部. (2021). 兩岸常用詞語對照表. 國語辭典簡編本附錄 https://dict.concised.moe.edu.tw/appendix.jsp?AID=92209&ID=54
- 數位發展部. (2024). 政府網站服務管理規範（113 年 3 月 15 日，數位政府字第 1134000368 號） https://www.webguide.nat.gov.tw/announcement/281/file/330/H394w7tWdOzpQfL2lo2trPUvSQDZQSGY6oAqL6Vw.pdf
- 經濟部智慧財產局. (n.d.). 使用體驗設計原則（智慧財產權 e 網通 UI/UX） https://tiponet.tipo.gov.tw/TIPO_UIUX/zeng-jia-yi-ge-ye-mian-shang-chuan.html

</details>
