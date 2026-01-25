#!/usr/bin/env python3
"""
Agent Validator - Validates OpenCode agent files for correctness

Usage:
    python3 validate_agent.py /path/to/agent.md
"""

import sys
import re
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any

class AgentValidator:
    def __init__(self, agent_path: str):
        self.agent_path = Path(agent_path)
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []
        
        # Valid tool keys (OpenCode format)
        self.valid_tools = {
            'bash', 'read', 'write', 'edit', 'glob', 'grep',
            'task', 'skill', 'webfetch', 'todoread', 'todowrite'
        }
        
        # Valid permission keys
        self.valid_permission_keys = {
            'bash', 'edit', 'write', 'webfetch', 'skill', 'task'
        }
        
        # Valid modes
        self.valid_modes = {'primary', 'subagent', 'all'}
        
    def validate(self) -> Tuple[bool, Dict[str, Any]]:
        """Run all validations and return results"""
        if not self.agent_path.exists():
            self.errors.append(f"File not found: {self.agent_path}")
            return False, self._get_results()
        
        content = self.agent_path.read_text()
        
        # Extract frontmatter
        frontmatter, body = self._extract_frontmatter(content)
        
        if frontmatter is None:
            self.errors.append("No valid frontmatter found")
            return False, self._get_results()
        
        # Run validations
        self._validate_yaml_syntax(frontmatter)
        self._validate_description(frontmatter.get('description'))
        self._validate_mode(frontmatter.get('mode'))
        self._validate_tools(frontmatter.get('tools'))
        self._validate_permission(frontmatter.get('permission'))
        self._validate_optional_fields(frontmatter)
        self._validate_body(body, frontmatter.get('tools', {}))
        
        is_valid = len(self.errors) == 0
        return is_valid, self._get_results()
    
    def _extract_frontmatter(self, content: str) -> Tuple[Optional[Dict], str]:
        """Extract YAML frontmatter from content"""
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
        
        if not match:
            return None, content
        
        yaml_str = match.group(1)
        body = match.group(2)
        
        try:
            frontmatter = yaml.safe_load(yaml_str)
            return frontmatter, body
        except yaml.YAMLError as e:
            self.errors.append(f"YAML parsing error: {e}")
            return None, content
    
    def _validate_yaml_syntax(self, frontmatter: Optional[Dict]):
        """Validate YAML syntax"""
        if frontmatter is None:
            return
        if not isinstance(frontmatter, dict):
            self.errors.append("Frontmatter must be a YAML dictionary")
    
    def _validate_description(self, description: Optional[str]):
        """Validate agent description (required field)"""
        if not description:
            self.errors.append("Missing required field: description")
            return
        
        if not isinstance(description, str):
            self.errors.append("'description' must be a string")
            return
        
        # Check length
        if len(description) > 1024:
            self.errors.append(
                f"Description exceeds 1024 chars (got {len(description)})"
            )
        
        if len(description) < 20:
            self.warnings.append(
                f"Description is very short ({len(description)} chars). Add more detail."
            )
        
        # Check for examples
        if '<example>' not in description:
            self.warnings.append(
                "Description missing <example> blocks. Consider adding usage examples."
            )
        
        # Check for trigger keywords
        trigger_keywords = ['use when', 'use for', 'invoke when', 'use proactively']
        has_trigger = any(kw in description.lower() for kw in trigger_keywords)
        if not has_trigger:
            self.info.append(
                "Consider adding trigger keywords like 'Use when...' to description"
            )
    
    def _validate_mode(self, mode: Optional[str]):
        """Validate mode field"""
        if mode is None:
            self.info.append("No 'mode' specified (defaults to 'all')")
            return
        
        if mode not in self.valid_modes:
            self.errors.append(
                f"Invalid mode '{mode}'. Must be: {', '.join(self.valid_modes)}"
            )
    
    def _validate_tools(self, tools: Optional[Dict]):
        """Validate tools configuration"""
        if tools is None:
            self.info.append("No 'tools' specified (uses global config)")
            return
        
        if not isinstance(tools, dict):
            self.errors.append("'tools' must be a dictionary/object")
            return
        
        # Check for invalid tool names
        invalid_tools = set(tools.keys()) - self.valid_tools
        if invalid_tools:
            self.errors.append(
                f"Invalid tools: {', '.join(invalid_tools)}"
            )
        
        # Check tool values are boolean
        for tool, value in tools.items():
            if not isinstance(value, bool):
                self.errors.append(
                    f"Tool '{tool}' must be true/false (boolean), not '{value}'"
                )
        
        # Check for common issues
        self._check_tool_patterns(tools)
    
    def _check_tool_patterns(self, tools: Dict):
        """Check for tool anti-patterns"""
        # Count enabled tools
        enabled_count = sum(1 for v in tools.values() if v is True)
        if enabled_count >= 9:
            self.warnings.append(
                f"Agent has {enabled_count} tools enabled. Consider if all are necessary."
            )
        
        # bash enabled info
        if tools.get('bash'):
            self.info.append(
                "Agent has 'bash' enabled - verify permission patterns are configured"
            )
        
        # write without read
        if tools.get('write') and not tools.get('read'):
            self.warnings.append(
                "Agent has 'write' but not 'read'. Consider adding read."
            )
        
        # edit without read
        if tools.get('edit') and not tools.get('read'):
            self.warnings.append(
                "Agent has 'edit' but not 'read'. Consider adding read."
            )
    
    def _validate_permission(self, permission: Optional[Dict]):
        """Validate permission configuration"""
        if permission is None:
            return
        
        if not isinstance(permission, dict):
            self.errors.append("'permission' must be a dictionary/object")
            return
        
        # Check for invalid permission keys
        invalid_keys = set(permission.keys()) - self.valid_permission_keys
        if invalid_keys:
            self.warnings.append(
                f"Unusual permission keys: {', '.join(invalid_keys)}"
            )
        
        # Validate permission values
        valid_levels = {'allow', 'ask', 'deny'}
        
        for key, value in permission.items():
            if isinstance(value, str):
                if value not in valid_levels:
                    self.errors.append(
                        f"Permission '{key}' has invalid value '{value}'. "
                        f"Must be: {', '.join(valid_levels)}"
                    )
            elif isinstance(value, dict):
                # Pattern-based permissions (like bash patterns)
                for pattern, level in value.items():
                    if level not in valid_levels:
                        self.errors.append(
                            f"Permission '{key}' pattern '{pattern}' has invalid value '{level}'"
                        )
            else:
                self.errors.append(
                    f"Permission '{key}' must be a string or dictionary"
                )
    
    def _validate_optional_fields(self, frontmatter: Dict):
        """Validate optional fields"""
        # model
        model = frontmatter.get('model')
        if model:
            if not isinstance(model, str):
                self.errors.append("'model' must be a string")
            elif '/' not in model:
                self.warnings.append(
                    f"Model '{model}' should be in format 'provider/model-id'"
                )
        
        # temperature
        temp = frontmatter.get('temperature')
        if temp is not None:
            if not isinstance(temp, (int, float)):
                self.errors.append("'temperature' must be a number")
            elif not 0.0 <= temp <= 1.0:
                self.errors.append(
                    f"'temperature' must be between 0.0 and 1.0 (got {temp})"
                )
        
        # maxSteps
        max_steps = frontmatter.get('maxSteps')
        if max_steps is not None:
            if not isinstance(max_steps, int):
                self.errors.append("'maxSteps' must be an integer")
            elif max_steps < 1:
                self.errors.append("'maxSteps' must be at least 1")
        
        # hidden
        hidden = frontmatter.get('hidden')
        if hidden is not None:
            if not isinstance(hidden, bool):
                self.errors.append("'hidden' must be true/false (boolean)")
            mode = frontmatter.get('mode')
            if hidden and mode != 'subagent':
                self.warnings.append(
                    "'hidden' is only meaningful for mode: subagent"
                )
    
    def _validate_body(self, body: str, tools: Dict):
        """Validate agent instruction body"""
        if not body or not body.strip():
            self.errors.append("Agent has no instruction content after frontmatter")
            return
        
        # Check for safety protocols if bash enabled
        if tools.get('bash'):
            if not self._has_safety_keywords(body):
                self.warnings.append(
                    "Agent has 'bash' enabled but no clear safety protocols found"
                )
        
        # Check for basic structure
        if '## ' not in body:
            self.warnings.append(
                "No sections found (no ## headers). Consider organizing with headings."
            )
        
        # Check for examples
        if '```' not in body:
            self.info.append(
                "No code blocks found. Consider adding command examples."
            )
    
    def _has_safety_keywords(self, body: str) -> bool:
        """Check if body contains safety-related keywords"""
        safety_keywords = [
            'safety', 'confirm', 'verification', 'backup',
            'ALWAYS', 'NEVER', 'before', 'check', 'verify'
        ]
        body_lower = body.lower()
        count = sum(1 for kw in safety_keywords if kw.lower() in body_lower)
        return count >= 3
    
    def _get_results(self) -> Dict[str, Any]:
        """Get validation results"""
        return {
            'errors': self.errors,
            'warnings': self.warnings,
            'info': self.info,
            'is_valid': len(self.errors) == 0
        }


def print_results(results: Dict[str, Any], agent_path: str) -> int:
    """Print validation results in a readable format"""
    print(f"\n{'='*70}")
    print(f"Agent Validation Report: {Path(agent_path).name}")
    print(f"{'='*70}\n")
    
    if results['errors']:
        print(f"❌ ERRORS ({len(results['errors'])}):")
        for i, error in enumerate(results['errors'], 1):
            print(f"  {i}. {error}")
        print()
    
    if results['warnings']:
        print(f"⚠️  WARNINGS ({len(results['warnings'])}):")
        for i, warning in enumerate(results['warnings'], 1):
            print(f"  {i}. {warning}")
        print()
    
    if results['info']:
        print(f"ℹ️  INFO ({len(results['info'])}):")
        for i, info in enumerate(results['info'], 1):
            print(f"  {i}. {info}")
        print()
    
    print(f"{'='*70}")
    if results['is_valid']:
        print("✅ VALIDATION PASSED")
    else:
        print("❌ VALIDATION FAILED")
    print(f"{'='*70}\n")
    
    return 0 if results['is_valid'] else 1


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 validate_agent.py /path/to/agent.md")
        return 1
    
    agent_path = sys.argv[1]
    
    validator = AgentValidator(agent_path)
    is_valid, results = validator.validate()
    
    return print_results(results, agent_path)


if __name__ == '__main__':
    sys.exit(main())
