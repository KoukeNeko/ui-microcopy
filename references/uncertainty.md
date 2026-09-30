# What goes next to an estimated number

The instinct that produced 「數字僅供參考，請核對」「碗與叉子本身不計入營養」
「數字不是推測」 was a good one — the number is uncertain and the reader should
know. The sentences were the wrong form of it. This page is the policy, with
the evidence behind each line in README.md §6.

## Required

1. **The estimate is labelled as an estimate.** 「估計 620 kcal」 or an
   「估計」 tag on the row — never a bare figure that reads as a measurement.
   The label does not convey *how* uncertain; it conveys that the number is an
   inference, which is true.
2. **The assumptions the reader can correct are visible.** The things that
   actually drive the error in a photo estimate are portion, ingredients and
   hidden oil or sauce. Show them as rows the reader can change:

   ```
   白飯      180 g    調整
   雞胸肉    140 g    調整
   烹調油    未確認   補充
   ```

   This is what 「請核對」 was trying to say. It says *what* to check.

## Conditional

3. **A range, when it is calibrated.** 「620 kcal（520–730）」 is good when
   the range comes from measured error on held-out data. A range the model
   invented on the spot is worse than none: it turns false precision into
   three numbers. Do not ask a model for ±.
4. **A targeted uncertainty, when this item has one.** 「醬料未確認」 on the
   plate with sauce; nothing on the plate without. The form is *X 未確認*, not
   *未見 X*: not seeing something in a photo is not evidence it is absent, and
   the wording should not imply that it is.
5. **An expandable basis.** 辨識：白飯、雞肉、青菜 ／ 份量：180 g、140 g、90 g ／
   烹調油：未確認 — behind a disclosure control, not on the row.

## Never

| String | Why |
| --- | --- |
| 碗與叉子本身不計入營養 | Segmentation detail; no reader decision depends on it |
| 未見額外添加糖、鹽或醬料 | Reports an absence the photo cannot establish |
| 份量以碗中視覺大小估算 | Explains the method; changes nothing the reader does |
| 數字僅供參考，請核對 (on every row) | Generic disclaimers do not move trust or behaviour and are habituated within a few exposures; the correctable rows above replace it |
| 數字不是推測 ／ 數字直接來自 X | Defends the figure; false for an inference; the source name alone suffices |
| 約 ／ 大概 before a figure that has a range | Verbal hedges lower trust in the number far more than a numeric range does |
| 信心 87% ／ 約 ±100 from the model | Model-verbalised confidence is badly calibrated and increases reliance on wrong answers |

## Why the split, in three lines

Numeric uncertainty barely dents trust in a number; verbal hedging does.
Disclaimers do nothing measurable and stop being read. Calibrated confidence
helps decisions; uncalibrated confidence helps nothing and adds automation
bias. So: label the estimate, show what can be corrected, and put nothing
else there.
