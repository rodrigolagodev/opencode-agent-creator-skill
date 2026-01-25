#!/usr/bin/env python3
"""
Agent Initializer - Creates a new OpenCode agent from template

Usage:
    python3 init_agent.py <agent-name> --path <output-directory>

Examples:
    python3 init_agent.py security-auditor --path ~/.config/opencode/agent
    python3 init_agent.py doc-writer --path ~/.config/opencode/agent
"""

import sys
import os
from pathlib import Path

AGENT_TEMPLATE = '''---
description: >-
  {description_placeholder}
  
  Use when [TODO: describe trigger conditions].
  
  <example>
  User: "[TODO: example user request]"
  Assistant: "I'll use the `{agent_name}` agent to [TODO: action]."
  </example>

mode: {mode}

tools:
  read: true
  glob: true
  grep: true
  write: false   # TODO: Enable if agent creates files
  edit: false    # TODO: Enable if agent modifies files
  bash: false    # TODO: Enable if agent runs commands
  webfetch: false
  todoread: true
  todowrite: true

# permission:
#   # TODO: Configure if bash/edit/write enabled
#   bash:
#     "*": ask
#     "ls *": allow
#     "rm *": deny
#   edit: ask
---

# {agent_title}

You are a specialized {agent_role}. Your expertise is [TODO: describe domain].

## Core Responsibilities

1. [TODO: Primary responsibility]
2. [TODO: Secondary responsibility]
3. [TODO: Additional responsibility]

## Operating Principles

### Safety First
- ALWAYS [TODO: safety rule]
- NEVER [TODO: anti-pattern to avoid]
- Prefer [TODO: best practice]

### Best Practices
- [TODO: Guideline 1]
- [TODO: Guideline 2]
- [TODO: Guideline 3]

## Workflow

When handling requests:

1. **Understand** - Clarify the task and requirements
2. **Plan** - For complex tasks, create a todo list
3. **Execute** - Perform the work with clear explanations
4. **Verify** - Confirm the task completed successfully

## Common Tasks

### [TODO: Task Category 1]
```bash
# TODO: Example commands or code
example-command --option value
```

### [TODO: Task Category 2]
```bash
# TODO: More examples
another-command
```

## Tool Usage Guide

### read
Use to examine [TODO: what files].

### glob/grep
Use to find [TODO: what patterns].

### [TODO: Add guides for other enabled tools]

## Error Handling

When errors occur:
1. Read and analyze the error message
2. Check common issues: [TODO: list common issues]
3. Provide clear explanation and solutions
4. Offer alternative approaches if needed

## Limitations

This agent CANNOT:
- [TODO: Limitation 1]
- [TODO: Limitation 2]
- [TODO: Limitation 3]

For those tasks, [TODO: suggest alternatives].

## Security Considerations

- [TODO: Security guideline 1]
- [TODO: Security guideline 2]

Remember: [TODO: Core philosophy or guiding principle]
'''

def create_agent(name: str, path: str, mode: str = "all") -> bool:
    """Create a new agent file from template"""
    
    # Validate name (kebab-case)
    if not name.replace('-', '').replace('_', '').isalnum():
        print(f"❌ Error: Agent name must be alphanumeric with hyphens")
        print(f"   Got: {name}")
        return False
    
    # Convert underscores to hyphens
    name = name.replace('_', '-').lower()
    
    if name.startswith('-') or name.endswith('-') or '--' in name:
        print(f"❌ Error: Invalid name format")
        print(f"   - Cannot start/end with hyphen")
        print(f"   - Cannot have consecutive hyphens")
        return False
    
    agent_path = Path(path) / f"{name}.md"
    
    if agent_path.exists():
        print(f"❌ Error: Agent already exists at {agent_path}")
        print(f"\n   Use a different name or delete the existing agent first.")
        return False
    
    # Create parent directory if needed
    agent_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Generate readable title and role from name
    agent_title = name.replace('-', ' ').title() + " Agent"
    agent_role = name.replace('-', ' ') + " specialist"
    description_placeholder = f"[TODO: Describe what {name} agent does]"
    
    # Generate content from template
    content = AGENT_TEMPLATE.format(
        agent_name=name,
        agent_title=agent_title,
        agent_role=agent_role,
        description_placeholder=description_placeholder,
        mode=mode
    )
    
    # Write file
    agent_path.write_text(content)
    
    print(f"✅ Agent created: {agent_path}")
    print(f"\n📋 Next steps:")
    print(f"   1. Edit {agent_path}")
    print(f"   2. Replace all [TODO] placeholders")
    print(f"   3. Configure tools and permissions")
    print(f"   4. Validate: python3 validate_agent.py {agent_path}")
    print(f"   5. Audit: python3 audit_agent.py {agent_path}")
    print(f"\n💡 Tips:")
    print(f"   - Check templates/ directory for ready-to-use examples")
    print(f"   - See references/frontmatter-spec.md for all options")
    print(f"   - See references/permission-patterns.md for bash patterns")
    
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 init_agent.py <agent-name> [--path <dir>] [--mode <mode>]")
        print("\nArguments:")
        print("  agent-name    Name for the agent (kebab-case)")
        print("  --path        Output directory (default: ~/.config/opencode/agent)")
        print("  --mode        Agent mode: primary, subagent, all (default: all)")
        print("\nExamples:")
        print("  python3 init_agent.py security-auditor")
        print("  python3 init_agent.py doc-writer --path ~/.config/opencode/agent")
        print("  python3 init_agent.py code-reviewer --mode subagent")
        print("\nNaming conventions:")
        print("  ✅ Good: security-auditor, doc-writer, code-reviewer")
        print("  ❌ Bad: helper, utils, agent1, MyAgent")
        return 1
    
    name = sys.argv[1]
    
    # Parse optional arguments
    path = os.path.expanduser("~/.config/opencode/agent")
    mode = "all"
    
    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == "--path" and i + 1 < len(args):
            path = os.path.expanduser(args[i + 1])
            i += 2
        elif args[i] == "--mode" and i + 1 < len(args):
            mode = args[i + 1]
            if mode not in {'primary', 'subagent', 'all'}:
                print(f"❌ Error: Invalid mode '{mode}'. Must be: primary, subagent, all")
                return 1
            i += 2
        else:
            print(f"❌ Error: Unknown argument '{args[i]}'")
            return 1
    
    success = create_agent(name, path, mode)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
