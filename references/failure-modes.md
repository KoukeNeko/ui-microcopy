# Failure modes

Every case below is real output, quoted from the two screens that prompted
this skill: an installer (ZenKern) and a nutrition app that estimates a meal
from a photo. The taxonomy is ordered by how often a model reaches for it.

## Why models do this

A model writing a UI string is asked to produce text, and its prior over text
is a conversation. Chat post-training rewards the register that makes a
conversation pleasant — casual, hedged, eager to explain — and nothing in the
task "write the label for this button" tells it that the artifact has a
different contract. Three pressures push the same way:

- **Register prior.** The most likely continuation of "the Cancel button says"
  is a spoken reply, not a control label.
- **Helpfulness pressure.** Adding information feels like helping; in chat it
  is. In an interface, unrequested information is noise competing with the
  figure beside it.
- **Uncertainty deflection.** When the model is unsure (an estimate from a
  photo), it discloses the uncertainty and its method. That is good prose in
  an answer and wrong in a value's note, where it transfers the model's doubt
  to the reader without changing what the reader does.

The fix is never "write more carefully". It is a contract per role, a
deletion pass, and a check that fails loudly.

## FM1 — Register drift

*Chat words in a control or a state.*

- Reality: the cancel button read 「算了」, the completion message 「裝好了」,
  the boot-disk row 「這台機器正從它開機，不能裝」.
- Why: FM register prior; 「好了」 is how a person reports completion in speech.
- Fix: the closed written form — 「取消」, 「安裝完成」, 「無法安裝：這是目前的
  開機磁碟」.
- Probe: `P1`, `P2`, `P7` in `../evals/fixtures.jsonl`.

## FM2 — Assistant voice in a system message

*The interface explains in the first person of a helpful assistant.*

- Reality: 「這台機器正從它開機，不能裝」 reads as a person telling you why,
  not as the interface naming the condition.
- Why: the same prior, one step further — the model narrates the reason
  instead of naming the state, because a conversation would.
- Fix: name the condition, then the recovery: 「無法安裝：這是目前的開機
  磁碟。請選擇其他磁碟。」
- Probe: `P2`.

## FM3 — Defensive disclosure

*Sentences that answer a question nobody asked, usually to cover the model's
own uncertainty.*

- Reality, from the photo estimate's notes: 「碗與叉子本身不計入營養」,
  「未見額外添加糖、鹽或醬料」, 「切片後果肉表面略微氧化，份量以碗中約 8–10
  片的視覺大小估算。」
- Why: uncertainty deflection. Each sentence is true and none of them changes
  what the reader does with 104 kcal.
- Fix: the note field's contract — one clause, one fact that changes how the
  figure is read, absent when there is none. `醬汁另計` qualifies; the bowl
  does not.
- Probe: `P3`.

## FM4 — Provenance meta-commentary

*Text about how the value was produced, including a defence of its honesty.*

- Reality: a source label reading 「數字直接來自 Claude Code 與 Codex，不是
  推測」; in the app, 「數字是 $provider（$model）從照片的估算，請核對。」
- Why: the model treats "where did this come from" as the user's question, so
  it answers it and then pre-empts the suspicion it just raised.
- Fix: a source name, once, in the place reserved for it: 「Claude 估算」.
  The negation 「不是推測」 adds nothing the source name did not.
- Probe: `P4`.

## FM5 — Duplicated hedging

*A figure that already carries its uncertainty is hedged again in words.*

- Reality: 「約 200 g（170–230 g）· 104 kcal」 — the range says it; 「約」 says
  it twice. And `128 / 2,400 mg 上限`, where the slash already makes the
  second number the target.
- Why: the model writes the sentence a person would say out loud, where the
  layout cannot carry meaning.
- Fix: the figure and the layout carry it. 「200 g（170–230 g）」,
  「128 / 2,400 mg」.
- Probe: `P5`.

## FM6 — Affect and coaching

*Cheering, apologising, reassuring, or instructing in a state that should be
neutral.*

- Reality: 「別擔心」「加油！」「太棒了」 in routine, error and destructive
  states; empty states that coach (「點右下角開始吧」).
- Why: the persona that makes a chat pleasant follows the model into the
  product, and the more routine the state, the less personality it may carry.
- Fix: state the change. If the screen needs to teach, the interface is
  unclear and wants redesigning, not a sentence.
- Probe: `P6`, `P8`.

## FM7 — Explaining the app to itself

*Copy that compensates for a weak interface instead of fixing it.*

- Reality: gesture hints, 「這裡會顯示…」 promises, footnotes under forms.
- Fix: redesign the screen; the string is the symptom.

## Using the taxonomy

When reviewing a screen, classify each bad string by its mode — the mode
predicts the fix, and the same mode recurring means the contract (a prompt, a
schema, a role's template) has to change, not the individual string.
