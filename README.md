# seb-ai-skills

Claude Code skills by Sebastian C. Bürgel. A skill is a set of instructions,
in a `SKILL.md` file, that Claude loads when a task calls for it.

This repository is a Claude Code
[plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces)
named `seb-ai-skills`. A marketplace lists plugins, which are what you
install. Each plugin here contains exactly one skill with the same name, so
you install only the skills you want.

| Skill | What it does |
| --- | --- |
| `write-clear-explainers` | Writes and reviews technical explainers and mixed explanation/procedure docs for readers who are technical but new to the system. |
| `test-gnosis-vpn` | Installs, funds and tests the latest Gnosis VPN client on a remote Linux server over SSH, or on a throwaway DigitalOcean VM that it destroys afterwards, after sending the funds back. It measures download speed and ping per second, or checks every exit. It runs commands as root on that server, changes its routes and firewall rules, and starts a watchdog on it: if the heartbeat you send over SSH stops for 6 minutes, the watchdog tears the VPN down, and after 12 minutes it reboots the server once. |

## Install a skill

In a terminal, add the marketplace once, then install each skill you want
as `<skill>@seb-ai-skills`:

```sh
claude plugin marketplace add SCBuergel/seb-ai-skills
claude plugin install write-clear-explainers@seb-ai-skills
claude plugin install test-gnosis-vpn@seb-ai-skills
```

Inside a running Claude Code session, use the same commands with `/plugin`
in place of `claude plugin`, for example
`/plugin install write-clear-explainers@seb-ai-skills`, then run
`/reload-plugins` to load the new skill. A session started after the install
loads it automatically.

## Use a skill

Claude uses a skill on its own when your request matches the skill's
description, for example "make this README easier to follow". To call a
skill directly, type `/<plugin>:<skill>`. Because each plugin and its skill
share a name, the name appears twice:

```text
/write-clear-explainers:write-clear-explainers
/test-gnosis-vpn:test-gnosis-vpn
```

## Update or remove a skill

To get the latest version, refresh the marketplace listing, then update the
plugin. Start a new session or run `/reload-plugins` afterwards.

```sh
claude plugin marketplace update seb-ai-skills
claude plugin update write-clear-explainers@seb-ai-skills
```

To remove a skill, uninstall its plugin. Remove the marketplace only if you
no longer want any skill from it.

```sh
claude plugin uninstall write-clear-explainers@seb-ai-skills
claude plugin marketplace remove seb-ai-skills
```

## Maintain this repository

### How the repository is laid out

```text
.claude-plugin/marketplace.json    the marketplace: one plugin entry per skill
skills/<skill-name>/SKILL.md       the skill, plus any files it uses
evals/<skill-name>/<case>/         optional test cases for a skill
evals/run.sh                       runs a skill's test cases
```

There is no `plugin.json` per plugin. Instead, each entry in
`marketplace.json` defines its plugin itself (`"strict": false`) and points
at one folder under `skills/`. Installing any plugin downloads the whole
repository, but Claude Code loads only that plugin's skill.

Installed copies update only when the plugin's `version` in
`marketplace.json` changes. Pushing new skill text without a version bump
reaches nobody who already has the skill.

### Add a skill

1. Create `skills/<skill-name>/SKILL.md`. The `name` in its front matter must
   match the folder name.
2. Add an entry to the `plugins` array in `.claude-plugin/marketplace.json`:

   ```json
   {
     "name": "<skill-name>",
     "source": "./",
     "strict": false,
     "skills": ["./skills/<skill-name>"],
     "version": "0.1.0",
     "description": "<one line on what it does>"
   }
   ```

3. Run the checks in [Validate and test before pushing](#validate-and-test-before-pushing),
   then commit and push.

### Change a skill

1. Edit the files under `skills/<skill-name>/`.
2. Bump that skill's `version` in `.claude-plugin/marketplace.json`.
3. Run the checks in [Validate and test before pushing](#validate-and-test-before-pushing),
   then commit and push.

### Validate and test before pushing

In a terminal at the repository root, check the manifest and the skills:

```sh
claude plugin validate --strict .
claude plugin validate --strict skills
```

Each command should end with `Validation passed`. If either reports errors,
fix them and run both commands again.

Then install the skill from your working copy, which includes uncommitted
changes. The local marketplace has the same name as the GitHub one, so run
the test with a temporary Claude Code config directory. That leaves your own
installed skills untouched:

```sh
export CLAUDE_CONFIG_DIR=$(mktemp -d)
claude plugin marketplace add ./
claude plugin install <skill-name>@seb-ai-skills
claude plugin details <skill-name>@seb-ai-skills
unset CLAUDE_CONFIG_DIR
```

`claude plugin details` should show the version from `marketplace.json`
and `Skills (1)` followed by the skill's name. If the skill is missing, check
that its entry in `marketplace.json` points at the right folder and that the
`name` in `SKILL.md` matches the folder name.

### Run a skill's test cases

Some skills have test cases under `evals/<skill-name>/`. Each case is a
`prompt.md` plus `graders/*.md` files that describe what a good answer must
do. `claude plugin eval` runs each prompt with and without the skill and
has a model grade the answers. The runner needs a `plugin.json`, which this
repository does not have, so `evals/run.sh` builds a temporary plugin from
your working copy and runs the cases there.

In a terminal at the repository root:

```sh
evals/run.sh write-clear-explainers
```

Extra options go to `claude plugin eval`, for example `--case 'narrow*'` to
run one case or `--runs 1` for a cheaper check. Each run uses your Claude
account; a full run of both `write-clear-explainers` cases cost about 3 US
dollars. The script grades with Sonnet, because the default Haiku grader
gave inconsistent verdicts on these cases. The summary table shows scores
with the skill, without it, and the difference.

## License

[MIT](LICENSE)
