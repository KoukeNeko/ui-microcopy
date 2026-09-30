# Element contracts

The contracts describe form. The language of every string is the language of
the brief — the Chinese, English and Japanese examples below are
interchangeable in form, and only the one matching the brief's language is a
model for the answer. Decide the element, write in its form, then judge the
wording. Each element
below has its form, its voice budget, and one contrastive pair with the
difference named — one pair, because a list of bad strings teaches the bad
strings.

## Contracts

### button — the action's name

Form: verb phrase, imperative, no person, no question, no full stop.
Voice: none.

- ✓ 取消 ／ 刪除 ／ 重新開機 ／ Uninstall ／ 削除
- ✗ 算了 ／ 好的，刪除 ／ Yes, uninstall it ／ 削除しますか？
- Difference: the ✓ names what the control does; the ✗ answers a question
  someone asked. A cancelling control is always 取消／Cancel／キャンセル
  (Apple HIG); a control that declines an *offer* is 不用了／No thanks; a
  control that postpones is 稍後／Not now. Pick by what the control does.

### dialog-title — the decision

Form: the act or the decision as a noun or verb phrase. A question is
acceptable when the buttons answer it (刪除這筆紀錄？ → 刪除／取消), never a
generic 確定嗎？.
Voice: none.

- ✓ 刪除這筆紀錄 ／ 轉帳確認 ／ Uninstall App
- ✗ 您確定要刪除嗎？ ／ Are you sure?
- Difference: the ✓ names the thing being decided; the ✗ asks the reader to
  reassure the system.

### dialog-body — the consequence

Form: only the facts the reader needs to decide that are not already on
screen; one or two sentences.
Voice: low; onboarding bodies may carry one benefit clause the brief supports.

- ✓ 這筆紀錄與它的照片會一併刪除。 ／ NT$3,200 將轉給陳美玲，送出後無法取消。 ／ This entry and its photo will be deleted. ／ この記録と写真は削除されます。
- ✗ 這筆紀錄與它的照片會被永久刪除，此操作無法復原，請務必謹慎確認！
- Difference: the ✓ states the consequence once; the ✗ states it twice and
  adds an instruction to be careful, which changes nothing the reader can do.

### status — the state

Form: closed state: 已＋動詞、動詞＋完成、動詞＋中; Saved / Export complete /
Removing files…; 保存しました／書き出し中 42%.
Voice: none.

- ✓ 安裝完成 ／ 已儲存 ／ 匯出中 42% ／ Backup complete: 1,048 files, 640 MB
- ✗ 裝好了 ／ 太好了，已成功儲存！ ／ Backed up successfully
- Difference: the ✓ names the state; the ✗ reports it the way a person would
  say it out loud, or adds "successfully" to a state that already means success.

### error — what happened, cause, next step

Form: the failure, then the cause if known, then the next step if one exists;
each once, in that order.
Voice: none. No apology, no reassurance, no exclamation mark.

- ✓ 無法安裝：這是目前的開機磁碟。請選擇其他磁碟。 ／ Can't save settings: no connection to the server. Try again later. ／ 設定を保存できません。サーバーに接続できません。しばらくしてからもう一度お試しください。
- ✗ 哎呀，這台機器正從它開機，所以不能裝喔，別擔心，換一顆就好！
- Difference: the ✓ separates state, cause and action; the ✗ narrates the
  cause in speech register and wraps it in comfort.
- A field error sits next to the field and says what to enter, in the
  affirmative; a format example is content, not surplus: ✓ 請輸入電子郵件地址，
  格式如 name@example.com ／ Use letters only in the name field; ✗ 不要輸入數字
  或符號 ／ Invalid name.

### empty — the state of having nothing

Form: noun or short state. The call to action lives on the control the brief
says already exists.
Voice: none.

- ✓ 沒有紀錄 ／ 購物車是空的 ／ No saved items ／ カートは空です
- ✗ 還沒有任何紀錄喔，點右下角開始記錄吧！
- Difference: the ✓ states the condition; the ✗ coaches, and repeats a control
  that is already on screen.

### label — the name of the thing

Form: noun phrase; for a screen-reader label on an icon control, what the
control does. No trailing stop.
Voice: none.

- ✓ 熱量 ／ 關閉面板 ／ 更多選項 ／ Add to favourites ／ 再生キュー
- ✗ 你的每日熱量攝取。 ／ 點這裡關閉
- Difference: the ✓ names; the ✗ addresses the reader and instructs.
- A setting's label or description states what happens when it is on; the
  off case is inferred: ✓ 洗手時自動開始計時 ／ Start a timer when you wash
  your hands; ✗ 開啟後洗手時會計時，關閉後不會.

### value — the figure

Form: number, unit, and any range the brief gives, in that order; the target
after a slash when the brief gives one.
Voice: none.

- ✓ 150 g（130–170 g） ／ 96 / 1,800 mg ／ 40 shares · $2,310.50 (+$31.20, +1.37%) ／ 15 分前
- ✗ 約 150 g ／ 96 mg（上限 1,800 mg） ／ 大概兩千三左右 ／ $2,310.50 (+1.37%)（the share count the brief gave is gone）
- Difference: the ✓ lets the figure and the layout carry the uncertainty and
  the target; the ✗ says in words what the range and the slash already say.
  See [uncertainty.md](uncertainty.md) for when a range may appear at all.

### note — the facts the brief gives, or nothing

Form: the facts the brief lists for this field, one clause each, in the
brief's language; nothing when it lists none. A note that changes how the
adjacent figure or list is read (a delay's cause, an unconfirmed ingredient,
an unusable stretch of input) is a fact; a remark about the apparatus, the
method or an absence is not.
Voice: none.

- ✓ 因〔原因〕延後，預計〔日期〕出貨 ／ 〔看得到但無法估量的東西〕未確認 ／ Held for 〔cause〕; now expected 〔date〕 ／ （empty）
- ✗ 預計〔日期〕出貨（the cause the brief gave is gone） ／ 碗與叉子本身不計入營養。 ／ 未見額外添加〔X〕。 ／ 無〔X〕。
- Difference: the ✓ keeps every fact the brief asked for and adds none; the
  ✗ either drops a required fact in the name of brevity or adds an
  observation nobody needs. The note examples are written with 〔slots〕 on
  purpose: a concrete example gets pasted verbatim into a brief about a
  different ingredient, and an example with nothing to say becomes 「無油」.
  Fill the slot from the brief; when nothing fills it, the note is empty.

### title — the name of the screen or step

Form: noun phrase.
Voice: onboarding titles may be warm; screen titles are names.

- ✓ 照片估算 ／ 新增帳戶 ／ 今日 ／ Photo estimate ／ Add an account ／ 写真から推定
- ✗ 來看看今天的紀錄吧
- Difference: the ✓ names the place; the ✗ invites.

### heading — the name of the section

Form: noun phrase; not a question, not an invitation, no how-to.
Voice: none.

- ✓ 安裝 ／ 限制 ／ 量測 ／ Installation ／ Limits
- ✗ 怎麼跑 ／ 各種做法比一比 ／ How to get started ／ Let's compare
- Difference: the ✓ names what the section holds; the ✗ talks to the reader
  about it.

### prose — the sentence in a document

Form: declarative; the subject is the thing, not the reader; a quoted bad
string sits inside 「」.
Voice: none.

- ✓ 省略 -g 則安裝至目前專案的 .claude/skills/。 ／ The linter exits 1 on an error.
- ✗ 拿掉 -g 就裝進專案吧。 ／ 你只要跑一次 linter。 ／ Just run the linter and you're done!
- Difference: the ✓ states what happens; the ✗ coaches, addresses and
  reassures.

## Two failures the contracts alone do not catch

- **Restating the input.** A note or remark that lists every figure already on
  the screen ("本月支出 42,300 元，收入 58,000 元，儲蓄 15,700 元…" under a
  chart that shows exactly that) passes every register test and still fails
  the Visible test. A note says the one thing the figures do not.
- **Over-deletion.** A writer who has learned to delete will delete the cause
  from an error or the fact from a note. The Facts test is not optional: the
  writer that deletes most loses the most required facts.

## Voice budget by surface

| Surface | Voice |
| --- | --- |
| error, status, label, value, note, transactional controls | none |
| dialog-body (destructive or financial) | none |
| empty state | none |
| onboarding title and body | one warm clause the brief supports; still no coaching about controls on screen |
| marketing, release notes | outside this skill |

## Language

The interface speaks as the system, to nobody in particular. 「請輸入…」 is
the standard Taiwanese instruction form and is fine. 「你的／您的」 only where
they disambiguate whose data is meant; 「我們」 never. Vocabulary follows
[zh-tw-lexicon.md](zh-tw-lexicon.md). Japanese UI uses the conventional
polite forms for statuses (保存しました) and plain nouns for controls (削除,
キャンセル). English uses the conventional action names (Cancel, Save, Delete,
Keep).

## Platform conventions

The contracts above do not change by platform; casing, a few fixed names
and the gesture verb do. Pick the platform's convention and hold it across
the app.

- **Apple (HIG).** Button titles and alert titles that are fragments use
  title-style capitalization with no ending punctuation; alert messages use
  sentence style. A button that cancels is always Cancel; OK only in a
  purely informational alert, never as the confirming button of an action
  (Erase, Convert, Delete instead). A multi-step flow keeps one set of step
  labels — Get Started, then Continue or Next, then Done. To send someone to
  a setting, give a link or button, never a description of where it is. Say
  tap on a touch device, click with a pointer. Do not alert for a common,
  undoable action; alert for an uncommon one that cannot be undone.
- **Material.** Sentence case for everything, buttons included. Spell words
  out — no e.g., etc., or other abbreviations where there is room. State a
  consequence in neutral, direct language and how to undo it; no warning
  that alarms, intimidates or condescends.
