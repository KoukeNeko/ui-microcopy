# Text a model writes into the interface

When an app asks a model for text the UI renders — a photo estimate's notes,
a sleep remark, a meeting summary — the prompt and the schema decide whether
the text is interface or conversation. Editing the sentence afterwards is the
wrong layer.

## The worked case

A nutrition app asked for `{"items":[…],"notes":[…]}` with the field
described as 「照片看不出來、但會影響數字的地方」 and the rule 「一句一件事，最多三
句；不要假裝看得到」. The screen showed:

```
切片後果肉表面略微氧化，份量以碗中約 8–10 片的視覺大小估算。
未見額外添加糖、鹽或醬料，數值以生鮮蘋果連皮計。
碗與叉子本身不計入營養。
```

Every rule was followed. The instruction named a *place* (things the photo
cannot show) and a model fills a place. It needed a *test*: does this change
how the figure is read?

## Four levers

1. **Give the field a test, not a topic.** 「只寫會改變數字怎麼讀的事；沒有就回傳
   []」. Say that empty is the usual answer.
2. **One contrastive pair, with the difference named.** 「✓ 醬汁未確認 — 使用者
   可以補上；✗ 未見額外添加醬料 — 照片看不到不等於沒有」. Not a list of bad
   sentences: a list teaches the sentences, and a list of good examples primes
   content when there is nothing to say.
3. **Budget the fields.** A free-text field with no stated reader will be
   filled. Give the note a cap of two clauses and an allowed empty value; put
   the source in a source field; put the estimate label in the schema, not in
   prose; never ask the model for a confidence or a ± range — verbalised
   confidence is badly calibrated and a made-up range is worse than none
   ([uncertainty.md](uncertainty.md)).
4. **Filter after generation, narrowly.** Drop a note that matches the
   apparatus / absence / provenance patterns the linter knows
   (`apparatus-disclaimer`, `absence-disclaimer`, `provenance-meta`). Keep it
   narrow: a filtered note is a silent loss, and the filter catches apparatus
   sentences, not coaching ones — it is a backstop, not the fix.

## What the notes field should say, by situation

| Situation | Note |
| --- | --- |
| Nothing hidden, nothing ambiguous | （empty） |
| Sauce or oil present but unquantified | 醬汁未確認 |
| Portion could not be judged from the photo | 份量依一般份量估計 |
| User's own words override the photo | （nothing — the user knows what they said） |
| Part of the input was unusable | 約 40 秒錄音聽不清楚 |

Never: what was not seen, the container, the method, a caution to check, a
defence of the number, a restatement of the figures already shown.

## The block

[../assets/runtime-prompt-block.zh-TW.md](../assets/runtime-prompt-block.zh-TW.md)
is the paste-in text. Insert it beside the output-format section so it
governs the fields rather than the task.

## Checking

Run the app's own prompt through `ui-microcopy-eval` (`v2/eval_v2.py`,
`patched` arm); the note-emptiness table tells you whether the field contract
works before you ship it.
