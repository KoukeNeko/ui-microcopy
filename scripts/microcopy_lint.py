#!/usr/bin/env python3
"""Lint user-visible UI strings for register, brevity and zh-TW usage (v2).

The linter is the mechanical half of the ui-microcopy skill: it catches the
patterns that a language model falls into when it writes interface text in the
register of a chat reply. It is deliberately rule-based so the same findings
can be reproduced by a person, by CI, and by the control-group harness in
``../evals``.

Input is a list of ``{role, text}`` items, read from one of:

  ``--format tsv``   ``role<TAB>text`` per line
  ``--format json``  ``[{"role": ..., "text": ...}, ...]``
  ``--format jsonl`` one object per line
  ``--format arb``   a Flutter ARB file (``@``-prefixed keys are metadata)
  ``--format text``  one string per line, role ``generic``

Exit status is 0 when no ``error`` was found, 1 when at least one was, so the
command can gate CI. Use ``--strict`` to fail on warnings too.

Run ``--self-test`` to check the rules against the worked examples.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROLES = (
    "button",
    "dialog-title",
    "dialog-body",
    "title",
    "label",
    "status",
    "error",
    "empty",
    "value",
    "note",
    "ai-note",
    "generic",
)

# Roles whose text is a control or a state, never a sentence addressed to
# someone: a person's name for themselves does not belong in them.
IMPERSONAL_ROLES = frozenset(
    {"button", "title", "label", "status", "error", "empty", "value", "note", "ai-note"}
)

# How much a role may say before it stops being scannable. Length is a proxy
# for "this string is doing two jobs"; the cap is generous on purpose.
LENGTH_CAP = {
    "button": 8,
    "dialog-title": 16,
    "dialog-body": 96,
    "title": 16,
    "label": 12,
    "status": 24,
    "error": 48,
    "empty": 40,
    "value": 24,
    "note": 32,
    "ai-note": 32,
}

CJK = r"㐀-鿿豈-﫿"

# Terms that are Taiwan's own although they contain a China-looking piece.
TW_WHITELIST = ("伺服器端", "使用者端", "數據機", "用戶端", "租用戶", "帳號", "註冊")

# Vocabulary that is Taiwan's, not China's. ``error`` for pairs where
# the China term is simply the wrong word in a Taiwanese interface;
# ``warn`` where the term survives in some Taiwanese writing and a person
# should decide.
CN_TERMS = (
    ("error", r"當前", "目前"),
    ("error", r"默認", "預設"),
    ("error", r"軟件", "軟體"),
    ("error", r"硬件", "硬體"),
    ("error", r"硬盤", "硬碟"),
    ("error", r"內存", "記憶體"),
    ("error", r"字節", "位元組"),
    ("error", r"服務器", "伺服器"),
    ("error", r"緩存", "快取"),
    ("error", r"文件夾", "資料夾"),
    ("error", r"鼠標", "滑鼠"),
    ("error", r"屏幕", "螢幕"),
    ("error", r"視頻", "影片"),
    ("error", r"音頻", "音訊"),
    ("error", r"網絡", "網路"),
    ("error", r"消息", "訊息"),
    ("error", r"卸載", "解除安裝"),
    ("error", r"加載", "載入"),
    ("error", r"刷新", "重新整理"),
    # A restaurant's menu is 菜單 in Taiwan; only a software menu is 選單.
    ("warn", r"菜單", "軟體的 menu 用「選單」，餐廳菜單保留「菜單」"),
    ("error", r"插件", "外掛"),
    ("error", r"優盤", "隨身碟"),
    ("error", r"移動端", "行動裝置"),
    ("error", r"賬號", "帳號"),  # 賬 is simplified-only; 帳號 is correct Taiwan form
    # 用戶端 (client) and 租用戶 (tenant) are Taiwan's own terms, so 用戶 alone
    # is what to flag.
    ("warn", r"(?<!租)用戶(?!端)", "使用者"),
    ("warn", r"註冊", "註冊／建立帳號（台灣多用「註冊」可接受）"),
    ("warn", r"信息", "訊息、資訊"),
    ("warn", r"數據", "資料"),
    ("warn", r"保存", "儲存"),
    ("warn", r"打印", "列印"),
    ("warn", r"點擊", "點選、點一下"),
    ("warn", r"設置", "設定"),
    ("warn", r"反饋", "回饋"),
    ("warn", r"在線", "線上"),
    ("warn", r"提交", "送出"),
    ("warn", r"文件", "檔案"),
    ("warn", r"重啟", "重新啟動"),
    ("warn", r"快捷鍵", "快速鍵"),
    ("warn", r"剪貼板", "剪貼簿"),
    ("warn", r"智能", "智慧"),
)


@dataclass(frozen=True)
class Rule:
    id: str
    severity: str  # error | warn
    roles: frozenset[str] | None  # None = every role
    pattern: re.Pattern[str]
    message: str
    hint: str


def _cjk_pair(mark: str) -> re.Pattern[str]:
    """A half-width mark with CJK on either side, as typed by a model that
    switched keyboards mid-sentence."""
    return re.compile(rf"[{CJK}]\s*{re.escape(mark)}|{re.escape(mark)}\s*[{CJK}]")


RULES: tuple[Rule, ...] = (
    Rule(
        "chatty-lexicon",
        "error",
        frozenset(IMPERSONAL_ROLES | {"dialog-body"}),
        re.compile(
            r"算了|不用了|不要了|好吧|好的|行吧|也好|沒關係|別擔心|不用擔心|放心|"
            r"哎呀|咦|喔|哦|囉|啦|呀|嘛|耶|嘿|唉|偷偷|順便說|偷偷說|其實|"
            r"沒問題的|可以的喔"
        ),
        "A reply between two people, not interface text.",
        "Name the state or the action: 「取消」, 「無法安裝」, 「已儲存」.",
    ),
    Rule(
        "completion-slang",
        "error",
        frozenset({"status", "button", "title", "dialog-title", "generic"}),
        re.compile(r"搞定|弄好|弄完|裝好了|存好了|設好了|做好了|可以了|OK 了|好了[。！!]?$"),
        "Completion in conversational register.",
        "Use the closed form: 「安裝完成」, 「已儲存」, 「設定完成」.",
    ),
    Rule(
        "second-person",
        "warn",
        frozenset({"status", "error", "note", "ai-note", "empty", "label", "value"}),
        re.compile(r"你的|您的|你|您"),
        "The system does not address the reader here.",
        "State the condition without a person: 「找不到紀錄」, not 「你還沒有紀錄」.",
    ),
    Rule(
        "we-voice",
        "error",
        None,
        re.compile(r"我們"),
        "The interface does not speak as 「我們」.",
        "Drop the subject: 「已同步」, not 「我們已同步」.",
    ),
    Rule(
        "question-label",
        "error",
        frozenset({"button", "title", "label", "dialog-title"}),
        re.compile(r"[?？]\s*$|嗎[?？]"),
        "A control asks a question instead of naming an action.",
        "Label it with the action: 「刪除」, not 「確定要刪除嗎？」.",
    ),
    Rule(
        "provenance-meta",
        "error",
        None,
        re.compile(
            r"不是(推測|猜的|猜測|臆測|亂猜)|並非(推測|猜測|臆測)|非臆測|無需(猜測|推測)|"
            r"不(是|靠)猜|直接來自|數字來自|並非隨機|絕對(準確|正確)|保證(準確|正確)"
        ),
        "The string defends how the value was produced instead of stating what it is.",
        "Name the source once: 「Claude 估算」; drop the negation.",
    ),
    Rule(
        "boilerplate-disclaimer",
        "error",
        frozenset({"value", "label", "note", "ai-note"}),
        re.compile(r"僅供參考|請核對|請對照[^。]{0,6}核對|請自行(判斷|確認|核對)|請放心|貼心提醒|小提醒|提醒您"),
        "A caution that every row could carry, so this row learns nothing from it.",
        "Write the estimate label and the correctable rows instead: 「估計」, 「醬料 未確認 ［補充］」. A check belongs to the confirm step as an action, not to the value.",
    ),
    Rule(
        "boilerplate-disclaimer",
        "warn",
        frozenset({"status", "error", "empty", "dialog-body"}),
        re.compile(r"僅供參考|請核對|請自行(判斷|確認|核對)|請注意|貼心提醒|小提醒|提醒您|請放心"),
        "Boilerplate caution.",
        "Keep it only if this one message can mislead; otherwise state the condition and the next step.",
    ),
    Rule(
        "self-estimated-range",
        "warn",
        frozenset({"value", "note", "ai-note"}),
        re.compile(r"[±]\s*\d|約\s*[±]|信心\s*\d+\s*%|confidence\s*\d+|\d+\s*%\s*(信心|把握|確定)"),
        "A confidence or ± the model produced itself; verbalised confidence is badly calibrated.",
        "Show a range only when it comes from measured error; otherwise the figure with an 「估計」 label.",
    ),
    Rule(
        "hedge-duplication",
        "warn",
        frozenset({"value", "label", "status", "note", "ai-note"}),
        re.compile(r"約\s*\d|大概|應該是|或許|可能會有|估計[^。，]{0,8}(非實測|不是實測|並非實測)"),
        "A number that is already an estimate is hedged again in words.",
        "The figure carries it: 「200 g（170–230 g）」, not 「約 200 g」.",
    ),
    Rule(
        "apparatus-disclaimer",
        "error",
        frozenset({"note", "ai-note", "status", "error", "value", "dialog-body"}),
        re.compile(
            r"(碗|盤子|餐盤|餐具|叉子|湯匙|筷子|容器|背景|桌面|擺盤|光線|拍照角度|畫面)"
            rf"[^。；]{{0,8}}[{CJK}]{{0,4}}(不計入|不列入|不納入|不算|不影響|不包含|不列入計算)"
        ),
        "Explains away the apparatus, which nobody asked about.",
        "Delete it. Say what is in the food, if anything is unaccounted for.",
    ),
    Rule(
        "absence-disclaimer",
        "warn",
        frozenset({"note", "ai-note", "status", "error"}),
        re.compile(
            r"未見|沒看到|看不到|未觀察到|未發現|沒有發現|並未添加|不含額外|沒有額外|"
            r"無法(判斷|確認|辨識|得知)|不確定(是否|有沒有)"
        ),
        "Reports what was not seen; a photo not showing X is not evidence of no X.",
        "Delete, or name what the reader can correct: 「醬汁未確認」 — never 「未見醬料」.",
    ),
    Rule(
        "method-filler",
        "warn",
        frozenset({"note", "ai-note"}),
        re.compile(
            r"(以|依|按照|根據)[^。；]{0,12}(估算|推算|估計|判斷|換算)"
            r"|視覺(大小)?估算|份量以[^。；]{0,10}(估|算)|看起來[^。；]{0,6}(約|大概)"
        ),
        "Describes the method inside a note that is read as a result.",
        "A method belongs in help text, once, not beside every estimate.",
    ),
    Rule(
        "vague-negation",
        "warn",
        frozenset({"status", "error", "empty"}),
        re.compile(r"不能(裝|存|用|開|連|傳|填)$|不能(裝|存|用)了|不給|沒法|沒轍"),
        "Colloquial negation where the interface states a limitation.",
        "「無法安裝」, 「此磁碟為目前的開機磁碟」.",
    ),
    Rule(
        "redundant-qualifier",
        "warn",
        frozenset({"value"}),
        re.compile(r"/\s*[\d,]+\s*(mg|g|kcal|ml)?\s*(上限|目標|配額|以下|以內)|(上限|目標)值?"),
        "Says in words what the layout already says.",
        "The second number after the slash is the target: 「128 / 2,400 mg」.",
    ),
    Rule(
        "exclamation-emoji",
        "error",
        None,
        re.compile(r"[!！]|[\U0001f300-\U0001faff☀-➿⬀-⯿]"),
        "Tone no routine, error or destructive state should carry.",
        "Delete it. State the change.",
    ),
    Rule(
        "punctuation-form",
        "warn",
        None,
        re.compile(rf"[{CJK}]\s*[,.:;]\s|[,.:;!?]\s*[{CJK}]|\.\.\.|~"),
        "Half-width or English punctuation in a Chinese sentence.",
        "Use 、，。？（） and ……, and an en dash for ranges.",
    ),
    Rule(
        "trailing-period",
        "warn",
        frozenset({"button", "label", "title", "dialog-title", "value"}),
        re.compile(r"[。.]\s*$"),
        "A label is a phrase, not a sentence.",
        "Drop the full stop: 「安裝完成」 stands as the whole string.",
    ),
)


@dataclass
class Finding:
    rule: str
    severity: str
    role: str
    text: str
    message: str
    hint: str
    match: str
    where: str = ""

    def as_dict(self) -> dict:
        return {
            "rule": self.rule,
            "severity": self.severity,
            "role": self.role,
            "text": self.text,
            "match": self.match,
            "message": self.message,
            "hint": self.hint,
            "where": self.where,
        }


def lint_text(role: str, text: str, where: str = "") -> list[Finding]:
    """Every rule that fires for one string, longest match reported first."""
    findings: list[Finding] = []
    for rule in RULES:
        if rule.roles is not None and role not in rule.roles:
            continue
        match = rule.pattern.search(text)
        if match:
            findings.append(
                Finding(
                    rule.id,
                    rule.severity,
                    role,
                    text,
                    rule.message,
                    rule.hint,
                    match.group(0),
                    where,
                )
            )
    cap = LENGTH_CAP.get(role)
    if cap is not None and len(text) > cap:
        findings.append(
            Finding(
                "role-length",
                "warn",
                role,
                text,
                f"{len(text)} characters for a {role}, which reads as two strings.",
                f"Split or delete down to about {cap}.",
                text[: cap + 1],
                where,
            )
        )
    # Taiwan's own terms that contain a China-looking substring are masked
    # before the vocabulary pass, so 伺服器端 does not trip 服務器 and 數據機
    # does not trip 數據.
    masked = text
    for term in TW_WHITELIST:
        masked = masked.replace(term, "＊" * len(term))
    for severity, pattern, suggestion in CN_TERMS:
        match = re.search(pattern, masked)
        if match:
            findings.append(
                Finding(
                    "zh-tw-vocabulary",
                    severity,
                    role,
                    text,
                    f"「{match.group(0)}」 is the term used in China.",
                    f"Taiwan writes {suggestion}.",
                    match.group(0),
                    where,
                )
            )
    return findings


def lint_items(items: list[dict]) -> list[Finding]:
    findings: list[Finding] = []
    for item in items:
        findings.extend(
            lint_text(
                item.get("role", "generic"),
                item.get("text", ""),
                item.get("where", ""),
            )
        )
    return findings


def read_items(path: Path, fmt: str) -> list[dict]:
    raw = path.read_text(encoding="utf-8")
    if fmt == "tsv":
        items = []
        for line in raw.splitlines():
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            role, _, text = line.partition("\t")
            items.append({"role": role.strip() or "generic", "text": text})
        return items
    if fmt == "json":
        data = json.loads(raw)
        if isinstance(data, dict):
            data = [{"role": role, "text": text} for role, text in data.items()]
        return [{**item, "where": str(path)} for item in data]
    if fmt == "jsonl":
        return [
            {**json.loads(line), "where": str(path)}
            for line in raw.splitlines()
            if line.strip()
        ]
    if fmt == "arb":
        data = json.loads(raw)
        return [
            {"role": "generic", "text": value, "where": f"{path}:{key}"}
            for key, value in data.items()
            if not key.startswith("@") and isinstance(value, str)
        ]
    return [
        {"role": "generic", "text": line, "where": str(path)}
        for line in raw.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


# The examples the rules were written against. Every pair is one the skill
# quotes, so a rule that stops firing here is a rule that stopped working.
SELF_TEST = (
    ("button", "算了", "chatty-lexicon"),
    ("status", "裝好了", "completion-slang"),
    ("error", "第 0 顆 83 MiB 這台機器正從它開機，不能裝", "vague-negation"),
    ("ai-note", "碗與叉子本身不計入營養", "apparatus-disclaimer"),
    ("ai-note", "未見額外添加糖、鹽或醬料", "absence-disclaimer"),
    ("label", "數字直接來自 Claude Code 與 Codex，不是推測", "provenance-meta"),
    ("value", "約 200 g（170–230 g）", "hedge-duplication"),
    ("value", "128 / 2,400 mg 上限", "redundant-qualifier"),
    ("empty", "我們還沒有紀錄", "we-voice"),
    ("button", "確定要刪除嗎？", "question-label"),
    ("status", "當前設定已保存", "zh-tw-vocabulary"),
    ("status", "安裝完成", None),
    ("button", "取消", None),
    # Taiwan's own terms must not be flagged as China usage.
    ("label", "用戶端 ID", None),
    ("label", "租用戶", None),
    ("value", "帳號", None),
    ("value", "200 g（170–230 g）", None),
    ("label", "Claude 估算", None),
    ("note", "醬料未確認", None),
    ("note", "未見額外添加醬料", "absence-disclaimer"),
    ("label", "數字來自 Claude 的判讀，請對照包裝核對。", "boilerplate-disclaimer"),
    ("value", "620 kcal（約 ±100）", "self-estimated-range"),
    ("label", "伺服器端錯誤", None),
    ("label", "數據機", None),
)


def self_test() -> int:
    """Check that each worked example still draws the finding it was written
    for, and that an accepted string draws no error."""
    error_rules = {r.id for r in RULES if r.severity == "error"} | {
        "zh-tw-vocabulary"
    }
    failed = 0
    for role, text, expected in SELF_TEST:
        fired = {f.rule for f in lint_text(role, text)}
        if expected is not None:
            ok = expected in fired
            detail = f"expected {expected}"
        else:
            # An accepted string may still draw a warning a person should
            # weigh; only an error means the rules over-fire on good text.
            ok = not (fired & error_rules)
            detail = "expected no error"
        print(f"{'ok   ' if ok else 'FAIL '} {text!r} -> {sorted(fired)} ({detail})")
        failed += 0 if ok else 1
    print(f"\n{len(SELF_TEST) - failed}/{len(SELF_TEST)} passed")
    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument(
        "--format", default="tsv", choices=("tsv", "json", "jsonl", "arb", "text")
    )
    parser.add_argument("--json", action="store_true", help="print findings as JSON")
    parser.add_argument("--strict", action="store_true", help="warnings fail too")
    parser.add_argument("--skip", action="append", default=[], help="rule id to skip")
    parser.add_argument("--list-rules", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)

    if args.list_rules:
        for rule in RULES:
            print(f"{rule.severity:5} {rule.id:24} {rule.message}")
        print(f"{'warn':5} {'role-length':24} per-role length cap")
        print(f"{'error':5} {'zh-tw-vocabulary':24} China vocabulary")
        return 0
    if args.self_test:
        return self_test()

    items: list[dict] = []
    for path in args.paths:
        items.extend(read_items(path, args.format))
    if not items:
        parser.error("no strings given; pass a file or --self-test")

    findings = [f for f in lint_items(items) if f.rule not in args.skip]
    if args.json:
        print(json.dumps([f.as_dict() for f in findings], ensure_ascii=False, indent=2))
    else:
        for f in findings:
            location = f"{f.where}: " if f.where else ""
            print(f"{location}{f.severity}: {f.text!r} [{f.rule}] {f.message}")
            print(f"    → {f.hint}")
        errors = sum(1 for f in findings if f.severity == "error")
        warnings = len(findings) - errors
        print(f"\n{len(items)} strings, {errors} errors, {warnings} warnings")

    errors = [f for f in findings if f.severity == "error"]
    return 1 if errors or (args.strict and findings) else 0


if __name__ == "__main__":
    sys.exit(main())
