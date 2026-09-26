# seb-ai-skills

Claude Code skills, packaged as one plugin and published through a
[plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces).
The repository is both the marketplace and the plugin, and both are named
`seb-ai-skills`.

## Skills

| Skill | What it does |
| --- | --- |
| `write-clear-explainers` | Writes and reviews technical explainers and mixed explanation/procedure docs for readers who are technical but new to the system. |
| `test-gnosis-vpn` | Installs, funds and tests the latest Gnosis VPN client on a remote Linux server over SSH, with guards that keep the SSH session from being cut off. |

## Install

Add the marketplace, then install the plugin. In a terminal:

```sh
claude plugin marketplace add SCBuergel/seb-ai-skills
claude plugin install seb-ai-skills@seb-ai-skills
```

Inside a Claude Code session, the same commands are
`/plugin marketplace add SCBuergel/seb-ai-skills` and
`/plugin install seb-ai-skills@seb-ai-skills`. Restart Claude Code so the
skills load.

## Use a skill

Claude uses a skill on its own when your request matches the skill's
description, for example "make this README easier to follow". To call one
directly, type the plugin name, a colon and the skill name:

```text
/seb-ai-skills:write-clear-explainers
/seb-ai-skills:test-gnosis-vpn
```

## Update

Fetch the latest marketplace listing, then update the plugin:

```sh
claude plugin marketplace update seb-ai-skills
claude plugin update seb-ai-skills@seb-ai-skills
```

Restart Claude Code afterwards. The plugin only updates when `version` in
`.claude-plugin/plugin.json` has changed.

## Remove

```sh
claude plugin uninstall seb-ai-skills@seb-ai-skills
claude plugin marketplace remove seb-ai-skills
```

## Repository layout

```text
.claude-plugin/marketplace.json    marketplace listing one plugin, source "./"
.claude-plugin/plugin.json         plugin manifest (name, version, ...)
skills/<skill-name>/SKILL.md       one folder per skill, plus any files it uses
```

## Add a skill

1. Create `skills/<skill-name>/SKILL.md`. The `name` in its front matter must
   match the folder name. No manifest changes are needed; the plugin picks up
   every folder under `skills/`.
2. Bump `version` in `.claude-plugin/plugin.json`, or installed copies will
   not update.
3. Check everything:

   ```sh
   claude plugin validate .
   claude plugin validate .claude-plugin/plugin.json
   ```

4. Test locally before pushing. If the GitHub marketplace is already added,
   remove it first with `claude plugin marketplace remove seb-ai-skills`.

   ```sh
   claude plugin marketplace add ./
   claude plugin install seb-ai-skills@seb-ai-skills
   ```

## License

[MIT](LICENSE)
