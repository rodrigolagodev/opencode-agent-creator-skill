# Quick Start Examples

This guide provides practical examples for getting started with the Agent Creator Skill.

## Installation

```bash
# Clone into OpenCode skills directory
git clone https://github.com/rodrigolagodev/opencode-agent-creator-skill.git ~/.config/opencode/skills/agent-creator

# Verify installation
ls ~/.config/opencode/skills/agent-creator/SKILL.md
```

## Example 1: Create a Simple Code Reviewer

### Using Natural Language

Open OpenCode and ask:

```
Create a code review agent that checks for best practices
```

The agent will:
1. Load the agent-creator skill
2. Read the code-reviewer template
3. Create `~/.config/opencode/agents/code-reviewer.md`
4. Explain how to use it

### Manual Creation

Alternatively, copy a template manually:

```bash
cp ~/.config/opencode/skills/agent-creator/templates/code-reviewer.md \
   ~/.config/opencode/agents/my-reviewer.md
```

Then customize the frontmatter and instructions.

## Example 2: Create a Custom Security Auditor

Ask your assistant:

```
Create a security auditor agent that focuses on SQL injection and XSS vulnerabilities
```

The skill will guide the creation with:
- Appropriate tool selection (read, glob, grep)
- Permission patterns (deny write/bash)
- Security-focused instructions
- Validation checklist

## Example 3: Audit an Existing Agent

If you have an agent that needs improvement:

```
Audit my testing-agent and suggest improvements
```

The assistant will:
1. Load the audit workflow
2. Read your agent configuration
3. Score it using the rubric
4. Provide specific recommendations

## Example 4: Browse Available Templates

```
Show me all available agent templates in agent-creator
```

You'll see:
- Template names and descriptions
- Risk levels
- Recommended modes
- Use cases

## Example 5: Learn About Tool Selection

```
What tools should I use for a database migration agent?
```

The assistant will:
1. Load tool-selection reference
2. Analyze the task requirements
3. Recommend appropriate tools
4. Explain security considerations

## Example 6: Check Agent Best Practices

```
What are common mistakes when creating agents?
```

The assistant will reference:
- Anti-patterns documentation
- Real examples of problems
- Solutions and best practices

## Using Templates Directly

### Quick Copy

```bash
# Copy template
cp ~/.config/opencode/skills/agent-creator/templates/simple-agent.md \
   ~/.config/opencode/agents/my-agent.md

# Edit with your preferred editor
nano ~/.config/opencode/agents/my-agent.md
```

### Replace TODOs

Templates contain `TODO:` markers:

```yaml
---
description: >-
  TODO: Describe what this agent does
  
  TODO: Add trigger phrases
  
  <example>
  User: "TODO: example request"
  Assistant: "TODO: example response"
  </example>

# TODO: Replace with appropriate tools
tools:
  read: true
  skill: true
---
```

Replace each TODO with your specific requirements.

## Agent Modes

### Primary Agent (Tab to Switch)

```yaml
mode: primary
```

For general-purpose agents that handle full workflows.

### Subagent (@mention to Invoke)

```yaml
mode: subagent
```

For specialized tasks within a conversation.

### All Modes (Default)

```yaml
mode: all
```

Can be used in either context.

## Tool Configuration

### Minimal (Safest)

```yaml
tools:
  read: true
  glob: true
  skill: true
```

Read-only operations.

### Standard

```yaml
tools:
  read: true
  glob: true
  grep: true
  edit: true
  skill: true

permission:
  bash: deny
  write:
    allow:
      - "*.test.js"
      - "test/**"
```

Editing with restrictions.

### Advanced (High Risk)

```yaml
tools:
  bash: true
  # ... other tools

permission:
  bash:
    allow:
      - "npm test"
      - "docker ps"
    deny:
      - "rm -rf"
      - "sudo *"
```

Bash access with strict controls.

## Next Steps

1. **Read the [README](README.md)** for complete documentation
2. **Browse [templates](templates/)** for examples
3. **Check [references](references/)** for detailed specs
4. **Follow [workflows](workflows/)** for step-by-step guides
5. **Read [CONTRIBUTING](CONTRIBUTING.md)** to contribute

## Common Questions

### Q: Can I modify templates?

Yes! Templates are starting points. Customize them for your needs.

### Q: How do I test my agent?

1. Restart OpenCode after creating/editing agents
2. Try invoking with @agent-name or Tab-switch
3. Test with various prompts
4. Check logs for errors

### Q: My agent isn't showing up

Check:
- File is in `~/.config/opencode/agents/`
- File has `.md` extension
- YAML frontmatter is valid
- OpenCode has been restarted

### Q: Can I use multiple skills?

Yes! Add to agent frontmatter:

```yaml
tools:
  skill: true
```

Then the agent can load any skill when needed.

## Support

- **Issues**: [GitHub Issues](https://github.com/rodrigolagodev/opencode-agent-creator-skill/issues)
- **Discussions**: [GitHub Discussions](https://github.com/rodrigolagodev/opencode-agent-creator-skill/discussions)
- **OpenCode Docs**: https://opencode.ai/docs/

---

## Author

**Rodrigo Lago** - [GitHub](https://github.com/rodrigolagodev)

---

Happy agent creating! 🚀
