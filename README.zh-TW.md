<h1 align="center">ui-microcopy</h1>

<p align="center">
  <strong>一份 Claude Code skill 加一支 linter，讓介面字串讀起來像介面。</strong><br>
  按鈕、狀態、錯誤、空狀態、數值列、備註、對話框文案——正體中文（台灣）、英文、日文。
</p>

<p align="center">
  <img alt="Claude Code skill" src="https://img.shields.io/badge/CLAUDE_CODE-SKILL-2196F3?style=for-the-badge">
  <img alt="Linter：Python 3，無相依套件" src="https://img.shields.io/badge/LINTER-PYTHON_3%2C_NO_DEPS-4CAF50?style=for-the-badge&logo=python&logoColor=white">
  <img alt="語言" src="https://img.shields.io/badge/ZH--TW_·_EN_·_JA-00A5A5?style=for-the-badge">
</p>

<p align="center">
  <a href="README.md">English</a> · <strong>繁體中文</strong>
</p>

<p align="center">
  <a href="#開始使用">開始使用</a>
  · <a href="SKILL.md">skill 本體</a>
  · <a href="references/roles.md">元件契約</a>
  · <a href="references/zh-tw-lexicon.md">台灣用語</a>
  · <a href="#linter">linter</a>
  · <a href="#量測方式">量測</a>
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

請語言模型寫一個按鈕，它寫的是一句回話。請它寫狀態，它用人講話的方式報告（「裝好了」）。請它寫估計數字旁的備註，它替數字的來歷辯護（「碗與叉子本身不計入營養」「數字不是推測」）。這些都不是文法錯，而是聊天回答的語域滲進了只該做一件事的欄位。這個 repo 放的是擋住它的程序，以及程序漏掉時抓得到的檢查。

**skill 是寫作程序。** 十項測試、固定順序——語言、事實、不捏造，然後才是元件的形式，最後才是刪減；每個元件一組成對範例，並寫出差異在哪。順序本身就是重點：把「刪減」放最前面的 skill 會刪掉必要事實、把英文題寫成中文；這一版正是量到這件事之後重寫的。

**linter 是保證。** 模型會犯的樣式（回話用語、口語完成式、「我們」、來源辯護、器材與缺席免責、驚嘆號、中國用語）寫成規則，吃 TSV、JSON、JSONL、Flutter ARB 或純文字，用結束碼把關 CI。它刻意做成純規則，所以人、pipeline、評測工具看到的是同一份結果。

## 它做什麼

### 每個元件用自己的形式寫

每條使用者看得到的字串只有一件工作：命名一個動作、陳述一個狀態、標記一個數字，或給出那一件會改變數字怎麼讀的事實。[references/roles.md](references/roles.md) 給每個元件它的形式、語氣額度，以及一組 ✓／✗ 範例：

| 元件 | 形式 | 語氣 |
| --- | --- | --- |
| button | 動作的名字——動詞片語，沒有人稱，不是問句 | 無 |
| dialog-title | 要做的決定；只有按鈕能回答時才用問句 | 無 |
| dialog-body | 後果，說一次，不重複畫面上已有的 | 低 |
| status | 收尾的狀態——已儲存 / Export complete / 保存しました | 無 |
| error | 發生什麼、知道的話說原因、有的話說下一步 | 無 |
| empty | 「沒有東西」這個狀態；動作留在控制項上 | 無 |
| label | 東西的名字；設定項寫的是開啟後會怎樣 | 無 |
| value | 數字、單位、範圍、目標——不確定性由數字與版面承載 | 無 |
| note | 題目給的事實，一件一句，沒有就空 | 無 |
| title | 畫面或步驟的名字 | onboarding 可以溫暖 |

平台慣例——Apple HIG 的大小寫與固定名稱、Material 的 sentence case、tap 與 click——放在同一個檔案的末尾，只改大小寫、幾個固定名稱與手勢動詞。

### 說清楚估計值旁邊該放什麼

[references/uncertainty.md](references/uncertainty.md) 把「要不要加免責」拆成三層：估計的身分與讀者可以修正的假設是**必要**；範圍要看有沒有校準，是**有條件**；器材說明、缺席說明、樣板警語、自我辯護、模型自估的信心數字，**一律不放**。依據是不確定性溝通的文獻，不是品味。

### 用台灣的詞

[references/zh-tw-lexicon.md](references/zh-tw-lexicon.md) 是 40 組詞，依畫面領域分組——儲存、網路、裝置、媒體、帳號、動作——每組附它指的概念，另有軟體語境白名單（帳號、用戶端、租用戶、餐廳的菜單），台灣自己的詞不會被「改正」。skill 要 agent 挑出這個畫面會用到的那幾列，而不是讀整張表：在刻意誘發漂移的題目上量測，只給相關的兩三列讓標準台灣詞的使用率從 43% 升到 66%；整張表只到 51%；單獨一句「不用中國用語」是唯一讓結果變差的條件。

### app 內的模型寫字串時，修的是 prompt

字串來自執行時的模型時——照片估算的備註、AI 摘要——要修的是欄位契約，不是文句。[references/runtime-llm-output.md](references/runtime-llm-output.md) 是契約，[assets/runtime-prompt-block.zh-TW.md](assets/runtime-prompt-block.zh-TW.md) 是可直接貼的區塊：每個欄位一組成對範例、允許空值、來源放自己的欄位、不要求信心或 ± 範圍。

### 各種做法比一比

依量測結果，各部分在哪裡有效：

|                              | 只有規則檔 | 這個 skill | CI 裡的 linter | zhtw MCP |
| ---------------------------- | :--------: | :--------: | :------------: | :------: |
| 人手寫字串                   |     ⚠️     |     ✅     |       ✅       |    —     |
| agent 在 coding session 寫字串 |     ⚠️     |     ✅     |       ✅       |    —     |
| app 內的模型                 |     —      |     ✅     |       ⚠️       |    —     |
| 抓到「當前」「保存」          |     —      |     ⚠️     |       ✅       |    —     |
| 保留必要事實                 |     ⚠️     |     ✅     |       —        |    —     |
| 維持題目的語言               |     ⚠️     |     ✅     |       —        |    —     |
| 長文的翻譯腔與標點           |     —      |     —      |       —        |    ✅    |

agent 本來就帶著的規則檔是這個 skill 的弱化版（評測裡的「rules」arm 就是它）。linter 抓的是五十條裡一條、讀的人和模型都不會注意到的用語失誤。zhtw MCP 是長文工具：對上面那幾條字串它什麼都沒報。

## 開始使用

1. **安裝**，用 [Skills CLI](https://github.com/vercel-labs/skills)（Node 18+），對所有專案生效：

   ```sh
   npx skills add KoukeNeko/ui-microcopy -g -a claude-code
   ```

   拿掉 `-g` 就裝進目前專案的 `.claude/skills/`；拿掉 `-a` 讓 CLI 列出它偵測到的所有 agent（Codex、Cursor、OpenCode 等讀的是同一份 `SKILL.md`）。私有 repo 用你已經設好的 git 憑證。之後用 `npx skills update` 更新。沒有 Node 就直接 clone：

   ```sh
   git clone https://github.com/KoukeNeko/ui-microcopy.git ~/.claude/skills/ui-microcopy
   ```

   寫或審 UI 文字、命名控制項、措辭錯誤或確認訊息、寫 app 內模型的 prompt 時，skill 會自己觸發。

2. **寫。** 給題目——畫面、元件、字串必須帶的事實、語言——skill 用元件的形式回答。回答前它自己跑的最後檢查：

   ```text
   1. 語言與題目相同？
   2. 題目列的每個事實都還在？
   3. 元件形式正確，而且沒有多的？
   4. 字串在檔案裡 → 跑 linter，修它報的。
   ```

3. **Lint** app 實際出貨的字串，放 CI 或 pre-commit。沒有 error 結束碼是 0，否則是 1；`--strict` 連 warning 也擋：

   ```sh
   python3 scripts/microcopy_lint.py --format arb lib/l10n/app_zh.arb
   python3 scripts/microcopy_lint.py --format tsv strings.tsv --strict
   python3 scripts/microcopy_lint.py --format json --json strings.json
   ```

   TSV 每行 `role<TAB>text`；JSON 與 JSONL 是 `{"role": ..., "text": ...}` 物件；純文字每行一條，角色為 `generic`。角色：`button`、`dialog-title`、`dialog-body`、`title`、`label`、`status`、`error`、`empty`、`value`、`note`、`ai-note`、`generic`。

4. **約束 app 內的模型。** 把 [assets/runtime-prompt-block.zh-TW.md](assets/runtime-prompt-block.zh-TW.md) 貼在 app prompt 的輸出格式段落旁，讓它管欄位；再把 app 自己的 prompt 丟進[評測工具](https://github.com/KoukeNeko/ui-microcopy-eval)——備註非空率那張表會在出貨前告訴你欄位契約有沒有用。

## linter

```sh
python3 scripts/microcopy_lint.py --list-rules
python3 scripts/microcopy_lint.py --self-test
```

| 規則 | 等級 | 抓什麼 |
| --- | --- | --- |
| `chatty-lexicon` | error | 該是控制項或狀態的地方寫成兩個人的回話（算了、裝好了） |
| `completion-slang` | error | 用口語報告完成，而不是收尾形式 |
| `we-voice` | error | 介面以「我們」發言 |
| `second-person` | warn | 不需要區分歸屬的「你的」 |
| `question-label` | error | 控制項問問題而不是命名動作 |
| `provenance-meta` | error | 字串替數值的來歷辯護（「數字不是推測」） |
| `apparatus-disclaimer` | error | 解釋器材（「碗與叉子本身不計入營養」） |
| `absence-disclaimer` | warn | 把「沒看到」當成證據來報告 |
| `boilerplate-disclaimer` | error / warn | 每一列都能掛的警語 |
| `self-estimated-range` | warn | 模型自己產生的信心或 ± |
| `hedge-duplication` | warn | 已是估計值又用文字再說一次 |
| `method-filler` | warn | 在被當成結果讀的備註裡描述方法 |
| `redundant-qualifier` | warn | 範圍前的「約」、斜線後的「上限」 |
| `exclamation-emoji` | error | 例行、錯誤、破壞性狀態不該有的語氣 |
| `punctuation-form` | warn | 中文句子裡的半形標點 |
| `trailing-period` | warn | 標籤結尾的句號 |
| `role-length` | warn | 一條字串做兩件事 |
| `zh-tw-vocabulary` | error / warn | 中國用語，先遮掉台灣白名單再比對 |

規則與範例在同一個檔案 `scripts/microcopy_lint.py`，除了 Python 3 沒有相依套件。`--self-test` 用範例逐條檢查規則。

## 量測方式

這個 skill 的第一版替自己打分：評分器四分之三的禁止字串就在 skill 內文裡。現在這一版用 32 題 held-out 題目量測——由兩位沒看過 skill 的出題者寫成，跑七條模型管道，由兩個異家族的 judge 在兩軸各評 0／1（沒有多餘、必要事實齊全），配對分析加以題為叢集的 bootstrap，並以 108 條人工盲評校準。

| | 對 control 的淨通過差 | Δ 必要事實 |
| --- | --- | --- |
| 第一版，Claude 出的題 | +16 pp | −0.3 pp |
| 第一版，GPT 出的題 | −5 pp | −15.7 pp |
| **這一版，全部題目，judge A** | **+8 pp [+1, +15]** | −3.4 pp |
| **這一版，全部題目，judge B** | **+8 pp [+1, +15]** | +1.1 pp |

第一版還把 41–82% 的英文回答拉成中文；這一版 0–15%。題目沒列任何事實的備註，未加干預的模型有 88% 會填東西，這一版 0%。這些是開發過程的數字——語言修正是看了第一稿的結果才改的——驗證性的量測需要凍結的 skill 與沒人看過的題目。評測工具、題目、生成檔與判定檔在 [ui-microcopy-eval](https://github.com/KoukeNeko/ui-microcopy-eval)。

## 規則從哪裡來

下面每一筆來源都開過原文核對——題名、作者、出處、引用的主張——才拿來用；沒有任何規則建立在找不到的文獻上。契約與既有的指引一致，並補上它們沒明說的：Apple Human Interface Guidelines（Writing、Alerts）、Material 3 的 UX writing 指南、Microsoft 的繁中風格指南、GOV.UK 的內容指引、教育部《兩岸常用詞語對照表》、MDN 與 MozTW 的 zh-TW 翻譯指南、數位發展部《政府網站服務管理規範》。不確定性政策依據不確定性溝通的文獻（數字範圍幾乎不損信任、口語式的模糊損失很大；免責會習慣化；口語化的信心校準很差）。反例與順序的決定依據指令遵循文獻與這個 skill 自己的量測。完整清單在[參考文獻](#參考文獻)。

## 檔案配置

```text
SKILL.md                              程序、十項測試、最後檢查
references/
  roles.md                            元件契約，每個一組 ✓/✗，平台慣例
  uncertainty.md                      估計值旁該放什麼
  zh-tw-lexicon.md                    依畫面領域分組的台灣用語、白名單、標點
  runtime-llm-output.md               app 內模型的欄位契約
assets/
  runtime-prompt-block.zh-TW.md       貼進那個模型 prompt 的區塊
scripts/
  microcopy_lint.py                   linter；--self-test、--list-rules
```

## 限制

- 量測是 32 題、每題 2 次抽樣：看得到十個百分點以上的效果，看不到更細的。人工評分只有一位，也是提出抱怨的人。
- 詞表 40 組。它抓的是模型在軟體文案裡真的會滑掉的詞，不是中國與台灣用語的全部差異；第二層（提交、點擊、保存、設置）只 warn，因為要看語境。
- 日文與英文的契約有範例，但除了評測裡各六題之外沒有自己的 held-out 量測。
- skill 只有文字。它看不到畫面；「畫面上已有」的測試靠題目說明畫面上有什麼。

## 參考文獻

128 筆來源，依字母排序。廠商文件與開源討論和論文一樣逐筆核對；數字取自摘要而非內文的，skill 的證據檔有註記。

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
