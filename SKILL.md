---
name: agent-creator
description: Expert guidance for creating, configuring, and refining OpenCode agents. Use when working with agent files, authoring new agents, improving existing agents, or understanding agent structure and best practices. Use PROACTIVELY when user mentions creating agents, configuring tools, setting permissions, or agent architecture.
license: MIT
compatibility: agent-skills-standard
metadata:
  category: agent-development
  version: "3.0.0"
  author: "Rodrigo Lago"
---

# Creating OpenCode Agents

Expert system for creating high-quality OpenCode agents with optimal configurations, comprehensive documentation, and skills integration.

## Core Principles

### 1. ALWAYS Write Agent Files in English

**CRITICAL:** All agent files MUST be written in English, regardless of the user's language.

- **Frontmatter**: description, examples - ALL in English
- **System prompt**: Role, responsibilities, workflows - ALL in English
- **Comments and documentation** - ALL in English

**Why?** LLMs process English more efficiently, resulting in:
- Faster response times
- Lower token usage (cost savings)
- Better model comprehension
- More consistent behavior

If the user requests an agent in another language, translate the requirements to English when writing the file. The agent can still RESPOND in the user's preferred language during conversations.

### 2. Agents Are Specialized Assistants

Only add context the agent doesn't have. Assume intelligence. Focus on configuration and behavior, not teaching basics.

### 3. Standard YAML + Markdown Format

Use YAML frontmatter + markdown body. **No XML tags** - use standard markdown headings.

```yaml
---
description: What it does + when to use + examples
mode: primary|subagent|all
tools: {read: true, write: false}
permission: {bash: ask, edit: deny}
---

You are [ROLE]. Your expertise is [DOMAIN].
```

### 4. Progressive Disclosure

- **SKILL.md** < 500 lines (entry point)
- **references/** detailed documentation (loaded when needed)
- **templates/** ready-to-use agent templates
- **workflows/** step-by-step processes

### 5. Effective Descriptions

Include **WHEN to use** (triggers) and **WHAT it does**. Write in third person. Add `<example>` blocks.

**Good:**
```yaml
description: >-
  Reviews React components for performance issues.
  Use when asked to review, optimize, or analyze React code.
  
  <example>
  User: "Review this component for performance"
  Assistant: "I'll use the `react-reviewer` agent."
  </example>
```

**Bad:**
```yaml
description: Helps with React
```

## Quick Start

**What would you like to do?**

1. **Create new agent** → Use the `Write` tool to create `~/.config/opencode/agent/<name>.md`
2. **Audit existing agent** → Use the `Read` tool to review, then apply fixes with `Edit`
3. **Upgrade prompt to agent** → Read the prompt, then create proper agent file
4. **Get guidance** → Continue reading below

> **Important:** This skill is **passive knowledge**. When creating agents, use OpenCode's 
> `Write` and `Edit` tools directly to create/modify agent files. Do NOT require users 
> to run scripts manually. The scripts in `scripts/` are optional CLI utilities for 
> validation - the primary workflow is direct file creation.

**Example Workflow:**
```
User: "Create an agent for reviewing database schemas"
    ↓
1. Agent loads this skill for guidance
2. Agent reads templates/references as needed
3. Agent uses Write tool to create ~/.config/opencode/agent/db-schema-reviewer.md
4. Done! User can now use @db-schema-reviewer
```

## Agent Structure

### Required Frontmatter

| Field | Required | Max Length | Example |
|-------|----------|------------|---------|
| `description` | Yes | 1024 chars | What + when + examples |
| `mode` | No (default: all) | - | primary, subagent, all |
| `tools` | No | - | `{read: true, write: false}` |
| `permission` | No | - | Permission overrides |
| `model` | No | - | `anthropic/claude-sonnet-4` |
| `temperature` | No | - | 0.1 - 1.0 |
| `maxSteps` | No | - | 5, 10, 250 |
| `hidden` | No | - | true (subagents only) |

See [references/frontmatter-spec.md](references/frontmatter-spec.md) for complete specification.

### Naming Conventions

Use **gerund form** (verb + -ing) or **noun-role**:

✅ **Good:**
- `analyzing-security`
- `reviewing-code`
- `security-auditor`
- `doc-writer`
- `db-admin`

❌ **Avoid:**
- `helper`, `utils`, `tool`
- `claude-*`, `opencode-*`
- Vague names like `agent1`, `my-agent`

### Body Structure

```markdown
---
[frontmatter]
---

You are [ROLE/PERSONA]. Your expertise is [DOMAIN].

## Core Responsibilities

1. [PRIMARY RESPONSIBILITY]
2. [SECONDARY RESPONSIBILITY]

## Operating Principles

### Safety First
- ALWAYS [RULE]
- NEVER [ANTI-RULE]

## Workflow

1. **Understand** - Clarify requirements
2. **Plan** - Design approach
3. **Execute** - Implement
4. **Verify** - Validate results

## Common Tasks

[Examples with commands]
```

## Agent Types

See [references/agent-types.md](references/agent-types.md) for detailed guide.

**Quick Reference:**

| Type | Mode | Tools | Permissions | Use Case |
|------|------|-------|-------------|----------|
| **Builder** | primary | all | edit=ask, bash=ask | Full development |
| **Planner** | primary | read, grep | edit=deny, bash=deny | Analysis only |
| **Reviewer** | subagent | read, grep | write=deny | Code review |
| **Executor** | subagent | bash, read | bash=patterns | System tasks |
| **Researcher** | subagent | read, webfetch | write=deny | Documentation |

## Tool Selection

See [references/tool-selection.md](references/tool-selection.md) for detailed guide.

**Quick Decision Tree:**

- Need to **read** files? → `read: true`
- Need to **search** content? → `grep: true, glob: true`
- Need to **modify** files? → `write: true, edit: true`
- Need to **execute** commands? → `bash: true`
- Need **web access**? → `webfetch: true`
- Need to **spawn subagents**? → `task: true`
- Need **task tracking**? → `todowrite: true, todoread: true`

**Rule:** Start minimal. Only enable tools needed for the agent's purpose.

## Permission Patterns

See [references/permission-patterns.md](references/permission-patterns.md) for complete library.

**Quick Examples:**

```yaml
# Safe by default
permission:
  bash:
    "*": ask                    # Ask for all
    "git status*": allow        # Allow safe commands
    "rm *": deny                # Deny dangerous

# Read-only agent
permission:
  edit: deny
  write: deny
  bash: deny

# Task-specific (database admin)
permission:
  bash:
    "*": ask
    "psql -c 'SELECT*": allow
    "psql -c 'DROP*": deny
```

## Validation Checklist

Before creating an agent, verify:

- [ ] **Written entirely in English** (frontmatter, prompt, examples)
- [ ] Valid YAML frontmatter with description and examples
- [ ] Description includes triggers + `<example>` blocks
- [ ] Tools match agent purpose
- [ ] Dangerous tools have permission controls
- [ ] System prompt defines clear responsibilities
- [ ] Workflow is documented
- [ ] Tested with real tasks

See [workflows/audit-agent.md](workflows/audit-agent.md) for complete rubric.

## Anti-Patterns

See [references/anti-patterns.md](references/anti-patterns.md) for complete list.

**Common Mistakes:**

1. ❌ **Non-English Content** - Writing agents in other languages (always use English)
2. ❌ **Tool Overload** - Enabling all tools "just in case"
3. ❌ **Permission Promiscuity** - `bash: allow` without controls
4. ❌ **Vague Description** - "Helps with coding tasks"
5. ❌ **Missing Examples** - No `<example>` blocks
6. ❌ **Wrong Mode** - Security auditor as primary instead of subagent
7. ❌ **No Workflow** - Pile of instructions without process

## Templates

Ready-to-use templates in [templates/](templates/) directory:

### Basic Templates
- **[simple-agent.md](templates/simple-agent.md)** - Basic template with TODOs (starting point)

### Specialized Templates
- **[security-auditor.md](templates/security-auditor.md)** - Security review without changes (read-only)
- **[doc-writer.md](templates/doc-writer.md)** - Documentation specialist
- **[db-admin.md](templates/db-admin.md)** - Database operations with safe permissions
- **[code-reviewer.md](templates/code-reviewer.md)** - Code quality analysis (read-only)
- **[refactoring-agent.md](templates/refactoring-agent.md)** - Code structure improvements
- **[testing-agent.md](templates/testing-agent.md)** - Automated testing specialist
- **[api-developer.md](templates/api-developer.md)** - REST/GraphQL API development
- **[devops-agent.md](templates/devops-agent.md)** - CI/CD and infrastructure automation
- **[frontend-dev.md](templates/frontend-dev.md)** - React/Next.js frontend development

## Agent Creation Process

### Primary Method: Direct File Creation

When a user asks you to create an agent, use the `Write` tool directly:

```markdown
1. Understand what the agent should do (ask clarifying questions if needed)
2. Read relevant templates from this skill: templates/*.md
3. Use the Write tool to create: ~/.config/opencode/agent/<agent-name>.md
4. Confirm creation and explain how to use (@agent-name or Tab to switch)
```

**Example:**
```
User: "Create an agent for database migrations"

Agent steps:
1. Read templates/db-admin.md for reference
2. Customize for migrations (add migration-specific commands, safety rules)
3. Write to ~/.config/opencode/agent/db-migrator.md
4. Tell user: "Created db-migrator agent. Use @db-migrator to invoke."
```

### Step 1: Understand Purpose

**Ask user:**
1. "What should this agent do? Describe its main purpose."
2. "When would you invoke this agent? What triggers its use?"
3. "Should this be primary (Tab to switch) or subagent (@mention)?"

**Internally determine:**
- Agent category (builder, reviewer, researcher, etc.)
- Required tools
- Risk level (ask vs allow vs deny)

### Step 2: Create the Agent File

**Use the Write tool directly** to create `~/.config/opencode/agent/<name>.md`

Reference templates as needed:
- `templates/simple-agent.md` - Basic structure
- `templates/security-auditor.md` - Read-only reviewer pattern
- `templates/doc-writer.md` - Documentation specialist
- `templates/db-admin.md` - Database operations with safe permissions
- `templates/code-reviewer.md` - Code quality analysis
- `templates/refactoring-agent.md` - Code refactoring
- `templates/testing-agent.md` - Testing automation
- `templates/api-developer.md` - API development
- `templates/devops-agent.md` - DevOps/CI-CD
- `templates/frontend-dev.md` - Frontend development

### Step 3: Configure Frontmatter

See [references/frontmatter-spec.md](references/frontmatter-spec.md) for all options.

**Essential fields:**
- `description` with triggers and examples
- `mode` (primary/subagent/all)
- `tools` (only what's needed)
- `permission` (for dangerous tools)

**Optional fields:**
- `model` (override global model)
- `temperature` (0.1-1.0)
- `maxSteps` (iteration limit)
- `hidden` (hide from @ menu)

### Step 4: Write System Prompt

Follow the standard structure:
1. Role definition
2. Core responsibilities
3. Operating principles
4. Workflow
5. Common tasks
6. Skills integration
7. Error handling

### Step 5: Configure Tools & Permissions

See [references/tool-selection.md](references/tool-selection.md) and [references/permission-patterns.md](references/permission-patterns.md).

**Match tools to purpose:**
- Code reviewer → read, grep (no write)
- System admin → bash (with patterns), read, write
- Doc writer → read, write, edit (no bash)

### Step 6: Validate

Verify the agent using the [validation checklist](references/validation-checklist.md):

- [ ] Valid YAML frontmatter (no syntax errors)
- [ ] Description has triggers and `<example>` blocks
- [ ] Tools match agent purpose
- [ ] Dangerous tools have permission controls
- [ ] No deprecated fields (name, skills, permissions)

### Step 7: Test with Real Tasks

1. Invoke the agent with typical requests
2. Observe behavior and effectiveness
3. Refine based on real usage

### Step 8: Audit Quality

Use the [audit rubric](references/audit-rubric.md) to score:

| Category | Target |
|----------|--------|
| Frontmatter Quality | 4.5+ / 5.0 |
| Tool Safety | 4.5+ / 5.0 |
| Instruction Quality | 4.5+ / 5.0 |
| Security | 4.5+ / 5.0 |
| Documentation | 4.5+ / 5.0 |

## Success Criteria

A well-structured agent:

- ✅ **Written entirely in English** (critical for LLM efficiency)
- ✅ Has valid YAML frontmatter with descriptive name and description
- ✅ Description includes trigger keywords and `<example>` blocks
- ✅ Uses standard markdown headings (not XML tags)
- ✅ Has appropriate tools for its purpose (not all tools)
- ✅ Has safe permission controls for dangerous tools
- ✅ Documents workflow and responsibilities clearly
- ✅ Includes usage examples
- ✅ Has been tested with real tasks

## Reference Documentation

For detailed guidance, see:

- **[frontmatter-spec.md](references/frontmatter-spec.md)** - Complete YAML specification
- **[tool-selection.md](references/tool-selection.md)** - Tool selection guide
- **[permission-patterns.md](references/permission-patterns.md)** - Permission examples library
- **[agent-types.md](references/agent-types.md)** - Agent type patterns and use cases
- **[anti-patterns.md](references/anti-patterns.md)** - What to avoid with examples
- **[skills-integration.md](references/skills-integration.md)** - How to integrate skills
- **[validation-checklist.md](references/validation-checklist.md)** - Field-by-field validation
- **[audit-rubric.md](references/audit-rubric.md)** - Quality scoring rubric

## Workflows

Step-by-step processes:

- **[create-new-agent.md](workflows/create-new-agent.md)** - Create agent from scratch
- **[audit-agent.md](workflows/audit-agent.md)** - Audit existing agent
- **[upgrade-agent.md](workflows/upgrade-agent.md)** - Migrate prompt to agent

## Philosophy

> "A great agent is like a skilled specialist:
>  - Clear about their expertise (description with triggers)
>  - Equipped with the right tools (minimal tool config)
>  - Careful with dangerous operations (permission patterns)
>  - Knows when to consult references (skills integration)
>  - Focused on doing one thing well (single responsibility)"

Create agents that are **focused**, **safe**, and **well-documented**.

## Additional Resources

- **OpenCode Docs**: https://opencode.ai/docs/agents/
- **Agent Examples**: Check ~/.config/opencode/agent/
- **Skills Library**: Check ~/.config/opencode/skills/
- **Permission Guide**: https://opencode.ai/docs/permissions/
