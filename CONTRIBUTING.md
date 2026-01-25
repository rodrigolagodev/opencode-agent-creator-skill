# Contributing to Agent Creator Skill

Thank you for your interest in contributing to the Agent Creator Skill! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Contribution Guidelines](#contribution-guidelines)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project follows the principles of respect, collaboration, and constructive feedback. Please be kind and professional in all interactions.

## How Can I Contribute?

### 1. Adding New Templates

We welcome new agent templates! To add a template:

1. Create a new `.md` file in `templates/`
2. Follow the structure of existing templates
3. Include comprehensive frontmatter
4. Add `skill: true` to the tools section
5. Document the agent's purpose, limitations, and examples
6. Update the templates table in `README.md`

**Template Checklist:**
- [ ] Valid YAML frontmatter
- [ ] Clear description with triggers
- [ ] At least 1 `<example>` block
- [ ] Appropriate tools for the task
- [ ] Permission controls for dangerous tools
- [ ] Well-structured markdown body
- [ ] Documentation of limitations

### 2. Improving Reference Documentation

Found something unclear or missing? You can:

1. Edit files in `references/` or `workflows/`
2. Test changes with real agents
3. Ensure accuracy with [OpenCode docs](https://opencode.ai/docs/)
4. Submit a pull request

### 3. Reporting Issues

Before creating an issue:

1. Check if the issue already exists
2. Use the issue templates (if available)
3. Provide clear reproduction steps
4. Include relevant agent configuration

**Good Issue Example:**
```
**Description**: Template X has invalid YAML syntax
**Steps to Reproduce**: 
1. Load template X
2. Try to use agent
3. See error
**Expected**: Agent should load
**Actual**: YAML parse error
**Configuration**: OpenCode v1.x, Agent mode: subagent
```

### 4. Improving Documentation

Documentation improvements are always welcome:

- Fix typos or grammatical errors
- Clarify confusing sections
- Add more examples
- Improve formatting
- Update outdated information

## Development Setup

### Prerequisites

- Git installed
- OpenCode installed and configured
- Text editor or IDE
- Basic understanding of YAML and Markdown

### Local Setup

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/opencode-agent-creator-skill.git
   cd opencode-agent-creator-skill
   ```

3. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Test your changes**
   ```bash
   # Copy to OpenCode skills directory
   cp -r . ~/.config/opencode/skills/agent-creator
   
   # Test with OpenCode
   opencode
   # Ask: "Create an agent using the new template"
   ```

## Contribution Guidelines

### File Organization

- `templates/` - Agent templates (read-only by LLM)
- `references/` - Reference documentation (specification, guides)
- `workflows/` - Step-by-step processes
- `scripts/` - Utility scripts (deprecated in v3.0)
- `SKILL.md` - Main entry point for the skill

### Writing Style

- **Language**: English (LLMs process English most efficiently)
- **Tone**: Professional, clear, concise
- **Format**: Markdown with proper headings
- **Code**: Use fenced code blocks with language tags

### YAML Frontmatter

Always validate YAML:
```yaml
---
description: >-
  Clear description.
  
  When to use triggers.
  
  <example>
  User: "request"
  Assistant: "I'll use agent-name."
  </example>

mode: subagent
tools:
  read: true
  skill: true
---
```

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add database administrator template
fix: correct YAML syntax in code-reviewer template
docs: update installation instructions in README
refactor: reorganize reference documentation structure
```

**Format:**
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `refactor:` Code restructuring
- `test:` Test updates
- `chore:` Maintenance tasks

## Pull Request Process

### Before Submitting

1. **Test your changes**
   - Load the skill in OpenCode
   - Test affected templates/workflows
   - Verify YAML syntax
   - Check markdown rendering

2. **Update documentation**
   - Update README.md if needed
   - Update CHANGELOG.md
   - Add inline comments where helpful

3. **Run quality checks**
   - Check for broken links
   - Validate YAML frontmatter
   - Review for typos
   - Ensure consistent formatting

### Submitting

1. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request**
   - Use clear, descriptive title
   - Fill out the PR template
   - Link related issues
   - Add screenshots if relevant

3. **PR Description Template**
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] New template
   - [ ] Bug fix
   - [ ] Documentation update
   - [ ] Refactoring
   
   ## Testing
   - [ ] Tested locally with OpenCode
   - [ ] Validated YAML syntax
   - [ ] Reviewed documentation
   
   ## Checklist
   - [ ] Follows project conventions
   - [ ] Updated README (if needed)
   - [ ] Updated CHANGELOG
   - [ ] No breaking changes (or documented)
   ```

### Review Process

1. Maintainer will review within 1-2 weeks
2. Address feedback in new commits
3. Once approved, PR will be merged
4. Your contribution will be credited

## Version Bumping

When your PR includes significant changes:

### Semantic Versioning

- **MAJOR** (x.0.0): Breaking changes
- **MINOR** (0.x.0): New features (backwards compatible)
- **PATCH** (0.0.x): Bug fixes

### Update Files

1. **CHANGELOG.md**: Add entry under "Unreleased"
2. **README.md**: Update version badge if applicable
3. Maintainers will handle official release

## Questions?

- **Documentation**: Check [OpenCode Docs](https://opencode.ai/docs/)
- **Issues**: Open a GitHub issue
- **Discussions**: Use GitHub Discussions
- **Contact**: Open an issue or check repository contacts

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## Author

**Rodrigo Lago** - [GitHub](https://github.com/rodrigolagodev)

---

Thank you for contributing to Agent Creator Skill! 🎉
