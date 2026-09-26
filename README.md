# seb-ai-skills

Claude Code skills, published as a
[plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces).
Each skill is its own plugin, so you install only the ones you want.

## Plugins

| Plugin | Skill | What it does |
| --- | --- | --- |
| `explain-technical-docs` | `explain-technical-docs` | Improves technical explainer documents so readers can follow them. The instructions are still a placeholder. |

## Install

Add the marketplace once. In a terminal:

```sh
claude plugin marketplace add SCBuergel/seb-ai-skills
```

Then install a plugin:

```sh
claude plugin install explain-technical-docs@seb-ai-skills
```

Inside a Claude Code session, the same commands are
`/plugin marketplace add SCBuergel/seb-ai-skills` and
`/plugin install explain-technical-docs@seb-ai-skills`. Restart Claude Code
so the new skill loads.

## Use a skill

Claude uses a skill on its own when your request matches the skill's
description, for example "make this README easier to follow". To call it
directly, type:

```text
/explain-technical-docs:explain-technical-docs
```

The part before the colon is the plugin name, the part after it is the skill
name.

## Update

Fetch the latest marketplace listing, then update the plugin:

```sh
claude plugin marketplace update seb-ai-skills
claude plugin update explain-technical-docs@seb-ai-skills
```

Restart Claude Code afterwards. A plugin only updates when its `version` in
`plugin.json` has changed.

## Remove

```sh
claude plugin uninstall explain-technical-docs@seb-ai-skills
claude plugin marketplace remove seb-ai-skills
```

## Repository layout

```text
.claude-plugin/marketplace.json          list of plugins in this marketplace
plugins/<plugin-name>/
  .claude-plugin/plugin.json             plugin manifest (name, version, ...)
  skills/<skill-name>/SKILL.md           the skill itself
```

## Add a new skill

1. Copy `plugins/explain-technical-docs/` to `plugins/<new-plugin>/` and
   rename the skill directory inside `skills/`.
2. Edit `plugin.json` (`name`, `description`, `version`) and the `name` and
   `description` in the front matter of `SKILL.md`.
3. Add an entry to the `plugins` array in `.claude-plugin/marketplace.json`
   with `"source": "./plugins/<new-plugin>"`.
4. Check everything:

   ```sh
   claude plugin validate .
   claude plugin validate plugins/<new-plugin>
   ```

5. Test locally before pushing:

   ```sh
   claude plugin marketplace add ./
   claude plugin install <new-plugin>@seb-ai-skills
   ```

   If the GitHub marketplace is already added under the same name, remove it
   first with `claude plugin marketplace remove seb-ai-skills`.

When you change an existing skill, bump `version` in its `plugin.json`, or
users will not receive the change.

## License

[MIT](LICENSE)
