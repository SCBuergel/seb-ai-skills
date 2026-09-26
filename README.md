# seb-ai-skills

Claude Code skills, published through a
[plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces).
Each skill is its own plugin, so you install only the ones you want.

## Skills

| Plugin | What it does |
| --- | --- |
| `write-clear-explainers` | Writes and reviews technical explainers and mixed explanation/procedure docs for readers who are technical but new to the system. |
| `test-gnosis-vpn` | Installs, funds and tests the latest Gnosis VPN client on a remote Linux server over SSH, with guards that keep the SSH session from being cut off. |

## Install

Add the marketplace once, then install the plugins you want. In a terminal:

```sh
claude plugin marketplace add SCBuergel/seb-ai-skills
claude plugin install write-clear-explainers@seb-ai-skills
claude plugin install test-gnosis-vpn@seb-ai-skills
```

Inside a Claude Code session, run the same commands with `/plugin` instead of
`claude plugin`, for example
`/plugin install write-clear-explainers@seb-ai-skills`. Restart Claude Code
so the skills load.

## Use a skill

Claude uses a skill on its own when your request matches the skill's
description, for example "make this README easier to follow". To call one
directly, type the plugin name, a colon and the skill name. Each plugin and
its skill share a name:

```text
/write-clear-explainers:write-clear-explainers
/test-gnosis-vpn:test-gnosis-vpn
```

## Update

Fetch the latest marketplace listing, then update a plugin:

```sh
claude plugin marketplace update seb-ai-skills
claude plugin update write-clear-explainers@seb-ai-skills
```

Restart Claude Code afterwards. A plugin only updates when its `version` in
`.claude-plugin/marketplace.json` has changed.

## Remove

```sh
claude plugin uninstall write-clear-explainers@seb-ai-skills
claude plugin marketplace remove seb-ai-skills
```

## Repository layout

```text
.claude-plugin/marketplace.json    one plugin entry per skill
skills/<skill-name>/SKILL.md       the skill, plus any files it uses
```

There is no `plugin.json`. Each entry in `marketplace.json` defines its
plugin (`"strict": false`) and points at one skill folder. Installing a
plugin downloads the whole repository, but Claude Code loads only that
plugin's skill.

## Add a skill

1. Create `skills/<skill-name>/SKILL.md`. The `name` in its front matter must
   match the folder name.
2. Add an entry to `plugins` in `.claude-plugin/marketplace.json`:

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

3. When you change an existing skill, bump its `version`, or installed copies
   will not update.
4. Check everything:

   ```sh
   claude plugin validate --strict .
   claude plugin validate --strict skills
   ```

5. Test locally before pushing. If the GitHub marketplace is already added,
   remove it first with `claude plugin marketplace remove seb-ai-skills`.

   ```sh
   claude plugin marketplace add ./
   claude plugin install <skill-name>@seb-ai-skills
   ```

## License

[MIT](LICENSE)
