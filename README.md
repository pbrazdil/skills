# Petr’s skills

My collection of agent skills for shipping small, well-tested changes.
Maintained by [Petr](https://github.com/pbrazdil) for Claude Code and Codex,
with optional T3 Code integrations.

Keep it simple. Fix the actual problem. Verify the result.

## Skills

| Skill | Say | What it does |
|---|---|---|
| `full-send` | "full send" | Takes a change to a merged PR with nobody watching: proves it, reviews it, files it, babysits it, merges it. |
| `full-stop` | "full stop" | Same as `full-send`, but stops when the PR is ready for you to merge. |
| `council` | "council" | Gets review from three models from different providers, and loops until they agree. |
| `sol-loop` | "sol loop" | Reviews a change with GPT Sol in a loop until both agents agree. |
| `file-pr` | "file a PR" | Files a short PR that leads with the problem, not an inventory of changes. |
| `takeover` | "take over" | Finishes someone else's PR, branch, or agent thread, and keeps their credit. |
| `babysit-pr` | "babysit" | Watches a PR through CI and review bots, and fixes the real findings. |
| `modernize` | "modernize" | Rebases an old PR and decides if it should still exist. |
| `leaving-pr-comments` | (automatic) | Formats comments that an agent posts on your behalf. |

Some skills call others. Install the ones they need too:

- `full-send` uses `sol-loop`, `file-pr`, and `babysit-pr`.
- `full-stop` uses `full-send`.
- `takeover` uses `modernize`, `file-pr`, `babysit-pr`, and `leaving-pr-comments`.
- `file-pr`, `babysit-pr`, and `modernize` use `leaving-pr-comments`.

## Install

```bash
git clone https://github.com/pbrazdil/skills.git petr-skills

# Claude Code
mkdir -p ~/.claude/skills
cp -Rn petr-skills/skills/. ~/.claude/skills/

# Codex
mkdir -p ~/.codex/skills
cp -Rn petr-skills/skills/. ~/.codex/skills/
```

These commands keep existing skill files. To update an installed skill, review
the differences and replace that skill deliberately.

## Requirements

- An authenticated [GitHub CLI](https://cli.github.com) (`gh`).
- `python3` for `babysit-pr`'s `pr-wait` script.
- `council` and `sol-loop` need subagents on other providers' models. T3 Code
  does this with `delegate_task`. Otherwise you need a harness that can run
  those models.

## Personal defaults

Shared language and working preferences live in [AGENTS.md](AGENTS.md).
The skills themselves describe their individual workflows.

The installation commands above copy only the skills, not `AGENTS.md`. To use
these preferences in other projects, merge the relevant instructions into the
`AGENTS.md` or `CLAUDE.md` that your agent loads there. Preserve existing
project instructions rather than replacing them.

## Origin and license

Adapted from [t3dotgg/tstack](https://github.com/t3dotgg/tstack), snapshot
[`7de017b`](https://github.com/t3dotgg/tstack/tree/7de017b3fc9d50c03cf3ecb98fb71e0ca65a78bd).
Personalized and maintained independently by Petr.

[MIT](LICENSE). Original copyright notices are preserved.
