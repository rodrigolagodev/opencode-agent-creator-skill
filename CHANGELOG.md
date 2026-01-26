# Changelog

All notable changes to the `agent-creator` skill are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this skill adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [3.1.0] - 2026-01-25

### Fixed

- **Corrected skill name in frontmatter** - Changed `name:` from `creating-agents` to `agent-creator` to match the folder name and follow naming conventions
- **Removed obsolete script references** - Cleaned up remaining references to Python scripts that were removed in v3.0.0
- **Updated compatibility field** - Changed `compatibility:` value to `agent-skills-standard` for cross-platform consistency

### Why These Changes?

These corrections ensure the skill follows Agent Skills standard conventions:
- Skill name in frontmatter must match folder name
- No references to non-existent files
- Compatibility field uses the universal standard identifier

---

## [3.0.0] - 2026-01-25

### Breaking Changes

**Removed Python Scripts** - The skill now follows professional best practices: pure documentation for LLM context.

- Removed `scripts/validate_agent.py`
- Removed `scripts/audit_agent.py`
- Removed `scripts/init_agent.py`
- Removed `scripts/consistency_check.py`

**Why?** Skills in professional ecosystems (Cursor, Claude, OpenCode) are **documentation, not software**. The LLM can validate and audit agents by reading markdown checklists—no external dependencies needed.

### Added

- **`references/validation-checklist.md`** - Complete field-by-field validation guide that agents can follow
- **`references/audit-rubric.md`** - Quality scoring rubric with specific criteria (replaces audit script)

### Changed

- **SKILL.md** - Removed all references to scripts, updated validation/audit sections to reference new markdown guides
- **README.md** - Completely rewritten for GitHub, emphasizes pure documentation approach
- **workflows/audit-agent.md** - Updated to reference markdown checklists instead of scripts
- **Progressive Disclosure principle** - Changed from "scripts/" to "workflows/" for better clarity

### Philosophy

Skills are **passive knowledge** that the LLM loads as context. They should be:
- Pure markdown documentation
- Self-contained (no external dependencies)
- Readable by both humans and LLMs
- Easy to maintain and contribute to

---

## [2.1.0] - 2026-01-25

### Fixed

#### Critical Issues
- **Removed deprecated `skills:` field from all examples** - Skills are now correctly shown as loaded at runtime via the `skill` tool, not declared in frontmatter
- **Removed deprecated `name:` field from all examples** - Agent name comes from filename, not a YAML field
- **Fixed self-contradictions in skills-integration.md** - Removed conflicting statements about how skills are declared vs loaded

#### High Priority Issues
- **Fixed duplicate section numbering in SKILL.md** - Sections now correctly numbered 1-5
- **Fixed incorrect path in anti-patterns.md** - Changed `~/.config/opencode/agents/` to correct `~/.config/opencode/agent/` (singular)
- **Updated validation checklist** - Removed reference to deprecated `name` field
- **Updated validation rules section** - Clarified that agent name comes from filename
- **Added `skill: true` to all templates** - Templates now consistently enable the skill tool

#### Medium Priority Issues
- **Updated upgrade-agent.md workflow** - Removed deprecated field examples, updated to current format
- **Standardized permission field naming** - Use `permission:` (singular) consistently

### Changed

#### agent-types.md
- All 10 agent pattern examples updated to current frontmatter format
- Added proper `description` with triggers and `<example>` blocks
- Added `mode:` field to all examples
- Added `permission:` patterns for agents with `bash: true`
- Added notes about loading skills at runtime

#### skills-integration.md
- Clarified that skills are loaded via `skill` tool, not frontmatter
- Updated performance tips to recommend runtime loading
- Fixed debugging section to reference `tools` not `permission`
- Updated checklist to remove deprecated field references
- Rewrote example agent to use current format

#### templates/
- `simple-agent.md` - Added `skill: true`
- `security-auditor.md` - Added `skill: true`
- `doc-writer.md` - Added `skill: true`
- `db-admin.md` - Added `skill: true`

#### workflows/upgrade-agent.md
- Updated Scenario 1 example to current format
- Updated Scenario 2 to use `tools:` instead of `permissions:`
- Rewrote Scenario 3 to explain runtime skill loading
- Updated Scenario 4 to show proper `permission:` patterns

### Added
- This CHANGELOG.md file to track version history
- Clarifying notes in agent-types.md about runtime skill loading
- Example `permission:` blocks for dangerous tool patterns
- **New `scripts/consistency_check.py`** - Script to validate internal consistency of the skill (detects deprecated fields, incorrect paths, broken references)
- **6 new agent templates:**
  - `templates/code-reviewer.md` - Code quality analysis (read-only)
  - `templates/refactoring-agent.md` - Code structure improvements with edit permissions
  - `templates/testing-agent.md` - Automated testing specialist with bash patterns
  - `templates/api-developer.md` - REST/GraphQL API development
  - `templates/devops-agent.md` - CI/CD and infrastructure automation
  - `templates/frontend-dev.md` - React/Next.js frontend development

---

## [2.0.0] - 2026-01-24

### Added
- **English-only requirement** - All agent files must be written in English for LLM efficiency
- New Core Principle #1 in SKILL.md explaining the English requirement
- Added to validation checklist, anti-patterns, and success criteria

### Changed
- Restructured Core Principles section
- Enhanced anti-patterns with "Non-English Content" as first item

---

## [1.0.0] - 2025-12-01

### Added
- Initial release of agent-creator skill
- Complete frontmatter specification (`references/frontmatter-spec.md`)
- Tool selection guide (`references/tool-selection.md`)
- Permission patterns library (`references/permission-patterns.md`)
- Agent type patterns (`references/agent-types.md`)
- Anti-patterns documentation (`references/anti-patterns.md`)
- Skills integration guide (`references/skills-integration.md`)
- Templates for common agent types
- Workflows for creating, auditing, and upgrading agents
- Python scripts for validation and automation

---

## Migration Guide

### Migrating from 1.x to 2.x

If you have agents created with version 1.x, update them as follows:

#### Remove Deprecated Fields

**Before (1.x format):**
```yaml
---
name: my-agent
description: Does something
skills:
  - security-review
  - backend-patterns
permissions:
  read: true
  write: true
---
```

**After (2.x format):**
```yaml
---
description: >-
  Does something specific.
  
  Use when [trigger conditions].
  
  <example>
  User: "Do the thing"
  Assistant: "I'll use my-agent."
  </example>

mode: all

tools:
  read: true
  write: true
  skill: true
---
```

#### Key Changes

| 1.x Field | 2.x Equivalent | Notes |
|-----------|----------------|-------|
| `name:` | (filename) | Agent name comes from the filename |
| `skills:` | (runtime) | Load skills via `skill` tool at runtime |
| `permissions:` | `tools:` | Renamed for clarity |
| (none) | `mode:` | New field: `primary`, `subagent`, or `all` |
| (none) | `permission:` | Fine-grained control for dangerous tools |

#### Add Skill Loading Instructions

Instead of declaring skills in frontmatter, add a section to your agent's instructions:

```markdown
## When to Load Skills

Load skills at runtime based on the task:
- Security reviews → Load `security-review`
- React code → Load `vercel-react-best-practices`
- API design → Load `backend-patterns`
```

---

## Roadmap

### Planned for 2.2.0
- [ ] Enhanced permission pattern library with more examples
- [ ] Agent composition patterns (multi-agent collaboration)
- [ ] Interactive template generator

### Planned for 3.0.0
- [ ] Multi-language support with translation guidelines
- [ ] Agent testing framework integration
- [ ] Performance optimization guidelines
