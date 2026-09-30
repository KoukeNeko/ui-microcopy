# Text a model writes into the interface

When an app asks a model for text that the UI renders — a photo estimate's
notes, a coach line, a summary — the prompt and the schema decide whether that
text is interface or conversation. Editing the sentence afterwards is the wrong
layer; the contract produced it.

## The worked case

MISHIRUBE estimates a meal from a photo. `lib/backend/ai/meal_draft_json.dart`
asks for `{"items":[…],"notes":[…]}` with the field described as
`"照片看不出來、但會影響數字的地方"` and the rule 「看不見的油、醬汁、滷汁、糖寫在
notes，一句一件事，最多三句；不要假裝看得到。」 The screen came back with:

```
切片後果肉表面略微氧化，份量以碗中約 8–10 片的視覺大小估算。
未見額外添加糖、鹽或醬料，數值以生鮮蘋果連皮計。
碗與叉子本身不計入營養。
```

Every rule was followed as written — three notes, one thing each, nothing
claimed that the photo does not show — and the result is still wrong. Nothing
here changes what the reader does with 104 kcal. The instruction named a
*place* (things the photo cannot show) rather than a *test* (does this change
how the figure is read), and a model fills a place.

## Four levers, in order of effect

1. **Give the field a test, not a topic.** "Write what the photo cannot show"
   invites an observation log. "Write only what changes the number next to
   it; if nothing does, return an empty list" invites a decision.
2. **Show what not to write.** Models follow counter-examples far more
   reliably than prohibitions. Two or three sentences of the kind above,
   labelled as wrong and why, do more than another adjective in the rule.
3. **Budget the fields.** A free-text field with no stated reader will be
   filled. Prefer: a source field that holds a name, a note field capped at
   two clauses and allowed to be empty, and no field whose only purpose is
   commentary. `請核對` belongs to a confirm step, not to a label.
4. **Filter after generation.** The app already trusts the model's JSON; the
   same place can drop a note that matches the apparatus/absence patterns the
   linter knows (`scripts/microcopy_lint.py`, rules `apparatus-disclaimer`
   and `absence-disclaimer`). Keep the filter narrow — a legitimately deleted
   note is a silent loss, so only patterns that cannot carry information
   qualify.

## The instruction block

[../assets/runtime-prompt-block.zh-TW.md](../assets/runtime-prompt-block.zh-TW.md)
holds the block to paste into an app's system prompt, written in the same
register as the app's own prompt. Insert it next to the output-format section
so it governs the fields rather than the task.

## Checking the result

Run the harness in `ui-microcopy-eval`: it sends the same app-shaped prompt
without and with this contract, across several models, and scores the fields
with the linter. That is the difference between "the prompt looks better" and
"the notes field is empty when it should be".
