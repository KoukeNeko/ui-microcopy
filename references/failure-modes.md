# Failure modes

Each mode has the real string that named it, why a model reaches for it, and
the fix. Rates come from the held-out evaluation in
[evaluation.md](evaluation.md); the strings that named the modes came from two
apps the author uses (an installer and a nutrition tracker) and were not used
as test items.

## Why models do this

Post-training rewards whole assistant turns judged by people: turns that
carry the reader, explain, pre-empt confusion, show care and sound sure. In a
reply these are virtues. A control label is not a turn. Nothing in "write the
label for this button" tells the model the contract changed, so it writes the
reply it was trained to write. Three measured pressures point the same way:
evaluators prefer longer answers at equal quality, preference models reward
list-and-bold formatting, and a persona given in a system prompt gets applied
where the context does not call for it ([why.md](why.md) §1). Telling the
model what *not* to write helps less than one would hope — negated
instructions are a known weak point, and naming a forbidden word primes it
([why.md](why.md) §2). Hence the contracts here are written as forms to
produce, with one contrastive pair each.

## FM1 — Register drift

Speech register where an element belongs. 「算了」 for Cancel; 「裝好了」 for
Install complete; 「Backed up successfully」.

Fix: the element's closed form — 取消, 安裝完成, Backup complete. On the
held-out set this was the commonest failure in control arms and the one every
intervention removed almost entirely.

## FM2 — Assistant voice in a system message

The interface narrates instead of naming. 「這台機器正從它開機，不能裝」.

Fix: state, cause, next step, in that order: 「無法安裝：這是目前的開機磁碟。
請選擇其他磁碟。」

## FM3 — Defensive disclosure

Sentences that answer a question nobody asked, to cover the writer's own
uncertainty. 「碗與叉子本身不計入營養」「未見額外添加糖、鹽或醬料」
「份量以碗中約 8–10 片的視覺大小估算」.

Fix: the note contract — one fact that changes the reading, or nothing; an
absence becomes 「X 未確認」 or disappears. In measurement, notes that should
have been empty were filled 88% of the time by control arms, 12% by the full
skill, 33% by a rules list, and 67% by a table of positive examples — showing
that positive examples prime content too (a writer shown 「醬汁另計」 wrote
「無醬汁。」 for a plate with no sauce). The contract therefore lists *empty*
as the first correct answer.

## FM4 — Provenance meta-commentary

Defending the figure. 「數字直接來自 Claude Code 與 Codex，不是推測」
「數字是 X 從照片的估算，請核對」.

Fix: the source name once, in the place reserved for it, and the correctable
assumptions where 「請核對」 stood. See [uncertainty.md](uncertainty.md).

## FM5 — Duplicated hedging

A figure that already carries its uncertainty is hedged again in words.
「約 200 g（170–230 g）」「128 / 2,400 mg 上限」.

Fix: the figure and the layout carry it. Verbal hedges are also the form of
uncertainty that measurably lowers trust in a number; a numeric range barely
does ([why.md](why.md) §6).

## FM6 — Affect and coaching

Cheering, apologising, reassuring, instructing. 「加油！」「別擔心」「明天早點上
床補回來」「點右下角開始吧」.

Fix: state the change. A screen that needs teaching wants redesign, not a
sentence. In measurement the coaching clause was the commonest surplus in
remark fields (health and summary probes).

## FM7 — Restating the input

New in measurement: a remark that re-lists every figure already on the
screen — a sleep summary that repeats time in bed, time asleep, minutes to
fall asleep and number of wakings under the chart that shows exactly those.
Every register test passes; the Visible test fails. The full skill produced
this more than the rules list did — a model that has been told "carry the
facts" can over-carry.

Fix: a note says the one thing the figures do not, such as how tonight's
sleep onset compares with the week's average.

## FM8 — Over-deletion

The mirror of FM3–FM7. A writer trained to delete removes the cause from an
error, the next step from a failure, the required fact from a note. This is
the failure that decided the shape of this version. On briefs written by the
skill's author, the first version of the skill raised the pass rate by 16
points; on briefs written independently by another model family, it *lowered*
it by 5 points, because it dropped required facts from 16% of strings: the
typhoon that caused a delay (「新預計送達日：10 月 5 日」 — cause gone), the
way to save an item in an empty state the brief asked to mention, the second
of two facts a note was to carry. The lists of positive examples and the
rules list did the same (−16 and −10 points of facts).

Fix: the Facts test is scored alongside the surplus tests, never after them;
the procedure now reads language → facts → form → deletion. A string that
carries every required fact with nothing else is the target; a shorter string
that drops a fact is a failure.

## FM10 — Language switching

New in measurement, and the largest single defect of the first version. The
skill's text and examples were mostly Chinese, and models followed the
skill's language instead of the brief's: on English briefs, 41–82% of strings
from the skill arm contained Chinese (0% in control); on Japanese briefs
8–20%. A rules list and an example table did it too (31–44%). An English
brief answered 「尚未儲存任何商品」 is a failure whatever its register.

Fix: the first line of the procedure is the brief's language; every element
contract carries an English and a Japanese example beside the Chinese one;
the harness measures script leakage directly from the generations.

## FM9 — Invented claims

The failure the human rater flagged that the models' judges missed: a clause
that asserts something the brief never gave. 「位置僅用於搜尋附近停車場，不會儲
存或追蹤」 — the brief said not stored; *or tracked* was invented. Onboarding
benefit clauses (「省去手動記錄的時間」) are the mild form.

Fix: every claim maps to a fact in the brief. This is the Invention test.

## Using the taxonomy

Classify each bad string by mode; the mode predicts the fix. The same mode
recurring across a screen means the contract that produced the strings (a
prompt field, a template) has to change, not the strings.
