# Roles and their forms

A role fixes the grammatical form before any wording exists. Decide the role,
write in its form, then judge the wording — not the other way round, which is
how sentences end up in buttons.

## The label names the action, and the action decides the label

「算了」 is wrong for a cancel button for two reasons at once: it weakens the
action's name (Apple: always title a cancelling button *Cancel*; Microsoft's
UI guide: do not rename Cancel while Cancel is unambiguous) and it simulates a
reply. The label follows the action, not the mood:

| What the control does | Label | Not |
| --- | --- | --- |
| cancels the action the control sits on | 取消 | 算了、不用了、我不要了 |
| declines an offer the app made | 不用了、稍後 | 取消（那會取消別的東西） |
| postpones a decision | 稍後提醒、明天再說 | 取消 |
| closes without deciding | 關閉 | 好的 |

Google's style guide separates exactly these three (Cancel / No thanks /
Not now); getting them right is a semantics question before it is a tone one.

| Role | Form | Accepted | Rejected |
| --- | --- | --- | --- |
| `button` | imperative verb phrase, no person, no question, no full stop | 取消、儲存、刪除、重新開機、稍後提醒 | 算了、好的、是的、我不要了、確定要刪除嗎？ |
| `dialog-title` | names the act, noun or verb phrase, no question mark | 刪除這筆紀錄、中斷安裝 | 您確定嗎？、真的要刪除嗎？ |
| `dialog-body` | only the consequence that is not already visible; one sentence | 這筆紀錄與它的照片會一併刪除。 | 此動作無法復原，請務必小心喔！、我們很遺憾… |
| `status` / toast | closed state: 已＋動詞、動詞＋完成、無法＋動詞、動詞＋中 | 已儲存、安裝完成、同步中、無法連線 | 裝好了、搞定、存好了、可以了 |
| `error` | state, then the cause if it is known, then the recovery step if one exists | 無法安裝：這是目前的開機磁碟。請選擇其他磁碟。 | 這台機器正從它開機，不能裝、哎呀，出錯了，請再試一次 🙂 |
| `empty` | noun or state; the action lives on the button | 沒有紀錄、尚未設定體重目標 | 這裡會顯示你的紀錄、還沒有資料嗎？點右下角開始吧 |
| `label` | noun, no padding 「的」, no trailing stop | 熱量、膳食纖維、目標體重 | 你的每日熱量、本日所攝取之熱量。 |
| `value` | figure and unit, range in parentheses, no qualifier the figure already carries | 200 g（170–230 g）、128 / 2,400 mg | 約 200 g、128 / 2,400 mg 上限 |
| `note` / `ai-note` | one clause, one fact that changes how the figure is read; absent when there is none | 醬汁另計、含糖量以店家的標準甜度計 | 碗與叉子本身不計入營養、未見額外添加糖、份量以碗中視覺大小估算 |
| `title` | screen name, noun phrase | 照片估算、今日 | 來看看今天的紀錄吧 |

## What each role never carries

- **Controls** (`button`, `dialog-title`): a person, a question, an affect, a
  full stop, a sentence.
- **States** (`status`, `error`, `empty`): an apology, a reassurance, a
  promise about a future release, a retry instruction for an action the user
  cannot take.
- **Values**: a qualifier the figure already carries (`約` before an estimate,
  `上限` after a slash that already means one), a provenance defence.
- **Notes**: a method, an absence, an apparatus, a hedge. A note earns its
  place only if deleting it changes what the reader concludes about the
  figure next to it.

## Voice

Tone is surface-dependent, not a house style applied everywhere: onboarding
and marketing surfaces may carry more of a voice, while errors, statuses,
labels and transactional controls carry the least. The interface speaks as the
system — 「請輸入…」 is the standard Taiwanese form for an instruction and is
fine. 「你的」「您」 appear only where they disambiguate whose data is meant,
and 「我們」 never.

Language follows Taiwan's usage throughout: 目前 not 當前, 元件 not 組件,
快取 not 緩存, 設定 not 設置. See
[zh-tw-lexicon.md](zh-tw-lexicon.md).
