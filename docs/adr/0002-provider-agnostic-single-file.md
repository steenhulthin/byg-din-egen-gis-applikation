# The Build skill is provider-agnostic and the App is a single HTML file

Participants must be able to repeat the Live demo at home in whatever AI chat they already use, so the Build skill is one self-contained Danish `SKILL.md` that works when uploaded or pasted into any chat interface, and the App is one `index.html` with its CSS and JavaScript inline. This rules out Claude Code-specific features, multi-file Apps, build tools and a template repo. Publishing is not done by an agent at all: it is a fixed sequence of clicks on github.com in the browser, written out in the Participant guide and shown by hand in the Live demo.

## Considered Options

- **Claude Code-first skills with a template repo**: richer automation (local verification, `gh` publishing), but requires a paid plan, an install and a terminal, which most Participants lack.
- **A Publish skill (`publicer-gis-app`) that guides the clicks in a chat**: drafted, then dropped. Publishing is the same few clicks for every App, so an interview adds nothing, and showing the clicks by hand on stage works better live than narrating an agent's instructions.
- **A plain prompt without the `SKILL.md` format**: equally portable, but loses the option to install it as a skill in agents that support the format.

## Consequences

- The data source list lives inside the Build skill, so one upload is enough.
- Verification of Data sources and the App happens in the agent only when it can make requests; otherwise the Participant opens `index.html` locally and pastes console errors back into the chat.
