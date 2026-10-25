# Byg din egen GIS-applikation

Material for a 20-minute Kortdage 2026 workshop where GIS professionals see an AI agent turn an idea into a live web map, and then repeat it at home.

## Language

### The workshop

**Session**:
The presenter's 20-minute part of the shared "GIS to go" slot at Kortdage 2026.
_Avoid_: Talk, workshop slot, oplæg

**Participant** (_deltager_):
A GIS professional attending the Session, with no programming experience assumed.
_Avoid_: User, attendee, learner

**Live demo**:
The part of the Session where the presenter runs the Build skill on stage with an Idea from the audience.
_Avoid_: Hands-on, exercise

**Backup app**:
An App built and Published before the Session, shown if the Live demo fails: the quietest hotels in Aalborg by road noise.
_Avoid_: Example app, reference solution

### Building an app

**Idea** (_problemstilling_):
The concrete problem a Participant wants a map to help with, e.g. environmental monitoring or urban planning.
_Avoid_: Use case, requirement, case

**Build skill** (`byg-gis-app`):
The instructions, usable in any AI chat, that interview a Participant about their Idea and build an App from the answers.
_Avoid_: Prompt, wizard, bot, "the skill" when the Publish skill could be meant

**Publish skill** (`publicer-gis-app`):
The instructions, usable in any AI chat, that guide a Participant through Publishing an existing App, run separately after the Build skill.
_Avoid_: Deploy skill, hosting skill

**First round** (_førsterunde_):
The short interview and build that turns an Idea into a first working App, using only Data sources that need no key.
_Avoid_: Quick mode, basic mode

**Extension round** (_udbygningsrunde_):
An optional further interview and build that adds to an existing App, where key-protected Data sources may also be used.
_Avoid_: Advanced mode, iteration, særlige ønsker

**App**:
The static web map a Participant ends up with, built from their Idea and one or more Data sources.
_Avoid_: GIS application (outside the title), website, solution

**Data source** (_datakilde_):
An open geodata service that an App shows or queries, either from the curated list or verified to work before use.
_Avoid_: Dataset, layer, API

**Publish**:
Putting an App online on the Participant's own GitHub Pages site.
_Avoid_: Deploy, host, go live
