# LMCognition Workspace

## Overview
This workspace anchors the local development environments for the Omi Friend wearable project. It keeps lightweight pointers to the two primary codebases (`OmiBH` for the core hardware+apps stack and `IdeasGlass` for the companion glasses experience) while letting you document higher-level workflows, planning notes, and repo-specific automation.

## Directory Layout
- `OmiBH -> ../OmiBH/`: symbolic link to the BasedHardware/Omi monorepo (Flutter app, backend, firmware, docs).
- `IdeasGlass -> ../IdeasGlass/`: symbolic link to the experimental glasses project.

Because these links point outside this repository, make sure siblings exist beside this workspace:
```bash
cd /home/lachlan/ProjectsLFS
git clone git@github.com:BasedHardware/Omi.git OmiBH
git clone git@github.com:lachlanchen/IdeasGlass.git IdeasGlass
```

## Using this Repo
1. Clone this workspace (`git clone git@github.com:lachlanchen/LMCognition.git`) into `/home/lachlan/ProjectsLFS`.
2. Ensure the two target repositories exist at the sibling paths noted above.
3. Open the workspace in your editor of choice. Use the symlinked folders to work on the actual source.
4. Track local documentation here—e.g., see `docs/doc/developer/LMCognition.mdx` inside `OmiBH` for push instructions and `AGENTS.md` for contributor expectations.

## Git Hygiene
This repository intentionally ignores the symlink names (add them to `.gitignore`) so GitHub only stores the coordination docs. When syncing changes:
```bash
git status # should only show docs/metadata
git add README.md
# add any other coordination files
```

## Support
- Core device/app docs: `OmiBH/docs/`
- Contributor guide: `OmiBH/AGENTS.md`
- Hardware identification notes: `OmiBH/docs/doc/hardware/DevKit1.mdx`

Use this workspace to capture process notes, automation scripts, or onboarding guides without polluting the upstream hardware repositories.
