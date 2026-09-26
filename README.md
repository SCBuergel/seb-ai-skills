# seb-ai-skills

Claude Code skills by Sebastian C. Bürgel. A skill is a set of instructions,
in a `SKILL.md` file, that Claude loads when a task calls for it. This
repository distributes the skills through a Claude Code
[plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces):
the marketplace, named `seb-ai-skills`, lists plugins, and each plugin here
contains exactly one skill with the same name. You install only the skills
you want.

| Skill | What it does |
| --- | --- |
| `write-clear-explainers` | Writes and reviews technical explainers and mixed explanation/procedure docs for readers who are technical but new to the system. |
| `test-gnosis-vpn` | Installs, funds and tests the latest Gnosis VPN client on a remote Linux server over SSH, with guards that keep the SSH session from being cut off. |

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

The rest of this README is for adding and changing skills in this
repository.

### How the repository is laid out

```text
.claude-plugin/marketplace.json    the marketplace: one plugin entry per skill
skills/<skill-name>/SKILL.md       the skill, plus any files it uses
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

3. Validate and test as described below, then commit and push.

### Change a skill

1. Edit the files under `skills/<skill-name>/`.
2. Bump that skill's `version` in `.claude-plugin/marketplace.json`.
3. Validate and test as described below, then commit and push.

### Validate and test before pushing

In a terminal at the repository root, check the manifest and the skills:

```sh
claude plugin validate --strict .
claude plugin validate --strict skills
```

Each command should end with `Validation passed`.

Then install from your working copy. The local marketplace has the same name
as the GitHub one, so run the test with a temporary Claude Code config
directory. That leaves your own installed skills untouched:

```sh
export CLAUDE_CONFIG_DIR=$(mktemp -d)
claude plugin marketplace add ./
claude plugin install <skill-name>@seb-ai-skills
claude plugin details <skill-name>@seb-ai-skills
unset CLAUDE_CONFIG_DIR
```

`claude plugin details` should list the new version and `Skills (1)` with
the skill's name. Run the test from a working copy that contains your
changes; it does not need to be committed.

## License

[MIT](LICENSE)
