# The skills are provider-agnostic and the App is a single HTML file

Participants must be able to repeat the Live demo at home in whatever AI chat they already use, so the Build skill and the Publish skill are each one self-contained Danish `SKILL.md` that works when uploaded or pasted into any chat interface, and the App is one `index.html` with its CSS and JavaScript inline. This rules out Claude Code-specific features, multi-file Apps, build tools and a template repo. Publishing is therefore guided clicks on github.com by default, with `gh` used only when the agent happens to have a terminal.

## Considered Options

- **Claude Code-first skills with a template repo**: richer automation (local verification, `gh` publishing), but requires a paid plan, an install and a terminal, which most Participants lack.
- **A plain prompt without the `SKILL.md` format**: equally portable, but loses the option to install it as a skill in agents that support the format.

## Consequences

- The data source list lives inside the Build skill, so one upload is enough.
- Verification of Data sources and the App happens in the agent only when it can make requests; otherwise the Participant opens `index.html` locally and pastes console errors back into the chat.
