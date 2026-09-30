# Why models write interface text like a chat reply

Research notes behind the rules, gathered 2026-09-30, with sources. Read this
when a decision needs the reason rather than the rule, or when someone asks
whether the problem is real.

## The phenomenon has no single name

No established term covers "a chat model leaking assistant register into
microcopy". The usable description is **assistant-register leakage**, and it
should be anchored to four concepts that *are* established:

| Established concept | What it contributes | Source |
| --- | --- | --- |
| Verbosity / length bias | Longer answers score higher in preference data even at equal quality | [Saito et al.](https://arxiv.org/abs/2310.10076), [Hu et al., EMNLP 2025](https://aclanthology.org/2025.findings-emnlp.358/) |
| Format bias | Preference models reward lists, bold, emoji — under 1% biased data moves a reward model | [Zhang et al., ACL 2025](https://aclanthology.org/2025.acl-long.1308/) |
| Persona overuse | Given persona traits, a model applies them even where the context does not call for them | [PANDA, EMNLP 2024](https://aclanthology.org/2024.emnlp-main.670/) |
| Sycophancy | Preference optimization can buy agreeableness with truthfulness | [Sharma et al., ICLR 2024](https://proceedings.iclr.cc/paper_files/paper/2024/hash/0105f7972202c1d4fb817da9f21a9663-Abstract-Conference.html) |

## The mechanism

Alignment trains *whole assistant turns* against human preference
([InstructGPT](https://arxiv.org/abs/2203.02155)), not single string fields. The
learned behaviour set — carry the user, explain what happened, pre-empt
confusion, state where data came from, show care, offer a next step, sound
friendly — is a virtue in conversation and noise in a control label. A
`CancelButton.label` is not a turn.

Two forces compose: training-time preference bias, plus a system prompt that
asks for a friendly, conversational, transparent assistant. There is no
component constraint to say that this string has one job, so the model
"proves" the persona in every string. Hence 「算了」 for Cancel and
「碗與叉子本身不計入營養」 in a value's note.

## Guideline adherence is genuinely unreliable

A 2025 Chalmers case study with ABB Robotics gave AI tools the UX-writing
guidelines for a product and measured the output: the tools could *state* the
rules and still violate them (banned vague labels like OK, inconsistent
terminology, missing recovery steps). Its conclusion — AI is a drafting aid,
not an autonomously reliable UX-writing source
([thesis](https://odr.chalmers.se/server/api/core/bitstreams/b1c80b27-8bd8-4dba-8c53-7b2148937a9b/content)).
This is why the skill ships a linter and a control-group harness instead of
prose encouragement.

## What the published guidance already says

Check this before repeating the folklore that "UI copy bans conversation".
It does not. Material, Microsoft, Polaris and Salesforce all *encourage* a
natural, conversational voice; what all of them forbid is content that carries
no information. The consensus is the sentence this skill opens with: write
naturally, do not simulate a conversation that need not exist.

| System | On conversational tone | On content that adds nothing |
| --- | --- | --- |
| Apple | Match tone to context; avoid cute/clever; error interjections like *oops* read as insincere | Include informative text **only if it adds value**; avoid explaining alert buttons; **always title a cancelling button *Cancel*** ([HIG — Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts), [Writing](https://developer.apple.com/design/human-interface-guidelines/writing)) |
| Material | Conversational style is the default for most situations | Simple, concise, direct; omit introductory phrasing; reveal detail as needed ([Writing](https://m1.material.io/style/writing.html)) |
| Microsoft | Error text may be conversational; warm and crisp | Eliminate extraneous information; **don't state anything the user does not need to know**; buttons at most a couple of short words ([Writing style](https://learn.microsoft.com/en-us/windows/apps/design/style/writing-style), [UI text](https://learn.microsoft.com/en-us/windows/win32/uxguide/text-ui)) |
| GOV.UK | Approachable and helpful, **not overly familiar**; friendliness can cost precision | Start with less; drop unnecessary words; if users never notice the copy, it is working — aim to be *boring* ([Writing for user interfaces](https://www.gov.uk/service-manual/design/writing-for-user-interfaces)) |
| NN/g | Character ranks third | Clarity → concision → character; do not ask a generic *Are you sure?*; buttons should state what happens, not Yes/No ([3 Cs](https://www.nngroup.com/articles/3-cs-microcopy/), [Confirmation dialogs](https://www.nngroup.com/articles/confirmation-dialog/)) |
| Polaris | Write like merchants talk | Only what clarity needs; get rid of repetition; strong actionable verbs ([Fundamentals](https://polaris-react.shopify.com/content/fundamentals)) |
| Carbon | Conversational level depends on the surface; errors are the least conversational | Economical and direct; do not repeat or paraphrase the title; action labels one or two words ([Content](https://carbondesignsystem.com/guidelines/content/overview/)) |
| Salesforce | Natural, conversational language | *Informative, not verbose — only what is necessary*; not every interaction needs a response ([SLDS feedback](https://www.lightningdesignsystem.com/2e1ef8501/p/1b1d6b-ui-feedback)) |

Two corrections to the common retellings, worth keeping straight:

- GOV.UK does **not** ban *Are you sure?* — its interruption-page pattern
  allows it for actions that cannot be undone. It is NN/g that advises against
  the generic form.
- Microsoft does **not** forbid a question in a dialog; it asks the title and
  the buttons to form a call and response (*Delete X?* → *Delete / Cancel*),
  and only warns that the bare *Are you sure…? Yes/No* pair is ineffective.

The quotable rules that hit this skill's failure modes hardest:

1. Include informative text only if it adds value. (Apple)
2. Don't state anything the user does not need to know. (Microsoft)
3. Friendliness can lead to a lack of precision and unnecessary words. (GOV.UK)
4. The tone of error messages is economical and direct. (Carbon)
5. A button names the action; do not rename a conventional action label. (Apple, Microsoft, Shopify)
6. Describe the consequence instead of asking a generic *Are you sure?* (NN/g)

## Tooling that already exists

- [Vale](https://docs.vale.sh/) — prose linting with custom rules, runs in
  editor, CLI and CI.
- [textlint](https://textlint.org/) — pluggable natural-language linter for
  JSON/ARB-extracted strings.
- GitHub's own content linter treats style errors as commit blockers
  ([docs](https://docs.github.com/en/contributing/collaborating-on-github-docs/using-the-content-linter)).

`scripts/microcopy_lint.py` is the same idea specialised to UI roles and zh-TW
usage; wiring it into CI is the part that keeps the behaviour from drifting
back.

## Two traps

1. **LLM judges share the bias.** Asked to compare 「安裝完成」 with
   「安裝已順利完成，可以開始使用了！」, a judge without component context
   tends to prefer the second — friendly, informative, complete. That is how
   an AI reviewer proves AI filler is better. Any judging here must know the
   role, must penalise unsupported propositions, and must not treat more
   information as better. This is why the harness scores mechanically.
2. **Public UX-writing prompts often say "conversational"**, and without
   per-component constraints that reintroduces the failure at the prompt
   layer. Treat 「conversational」 as a banned instruction in an interface-copy
   prompt unless it is bound to a specific element.

## The metric worth optimizing

Not length. **Semantic surplus**: does the string carry a proposition nobody
asked the interface to carry (utensils ∉ nutrition, "not a guess", "we have
noticed")? A string that stays within its one communication job passes;
anything else is surplus no matter how short.
