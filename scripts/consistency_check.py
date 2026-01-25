#!/usr/bin/env python3
"""
Skill Consistency Checker - Validates internal consistency of the agent-creator skill

This script checks that all documentation, templates, and examples within the skill
are consistent with the frontmatter specification.

Usage:
    python3 consistency_check.py [skill_path]
    
    If no path provided, defaults to the parent directory of this script.
"""

import sys
import re
import os
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class Issue:
    """Represents a consistency issue found"""
    severity: str  # 'error', 'warning', 'info'
    file: str
    line: Optional[int]
    message: str
    suggestion: Optional[str] = None


@dataclass
class ConsistencyReport:
    """Full consistency check report"""
    issues: List[Issue] = field(default_factory=list)
    files_checked: int = 0
    yaml_blocks_checked: int = 0
    
    @property
    def errors(self) -> List[Issue]:
        return [i for i in self.issues if i.severity == 'error']
    
    @property
    def warnings(self) -> List[Issue]:
        return [i for i in self.issues if i.severity == 'warning']
    
    @property
    def infos(self) -> List[Issue]:
        return [i for i in self.issues if i.severity == 'info']
    
    @property
    def is_consistent(self) -> bool:
        return len(self.errors) == 0


class SkillConsistencyChecker:
    """Checks internal consistency of the agent-creator skill"""
    
    # Deprecated fields that should NOT appear in examples
    DEPRECATED_FIELDS = {'name', 'skills', 'permissions'}
    
    # Current valid frontmatter fields
    VALID_FIELDS = {
        'description', 'mode', 'tools', 'permission', 
        'model', 'temperature', 'maxSteps', 'hidden'
    }
    
    # Valid tool names
    VALID_TOOLS = {
        'bash', 'read', 'write', 'edit', 'glob', 'grep',
        'task', 'skill', 'webfetch', 'todoread', 'todowrite'
    }
    
    # Valid modes
    VALID_MODES = {'primary', 'subagent', 'all'}
    
    # Valid permission levels
    VALID_PERMISSION_LEVELS = {'allow', 'ask', 'deny'}
    
    # Correct path pattern
    CORRECT_AGENT_PATH = '~/.config/opencode/agent/'
    INCORRECT_AGENT_PATHS = [
        '~/.config/opencode/agents/',  # plural
        '~/.config/claude/agent/',
        '~/.claude/agent/',
    ]
    
    def __init__(self, skill_path: Path):
        self.skill_path = skill_path
        self.report = ConsistencyReport()
        
    def check_all(self) -> ConsistencyReport:
        """Run all consistency checks"""
        
        # Find all markdown files
        md_files = list(self.skill_path.rglob('*.md'))
        self.report.files_checked = len(md_files)
        
        for md_file in md_files:
            self._check_file(md_file)
        
        # Check cross-references
        self._check_cross_references(md_files)
        
        # Check section numbering in SKILL.md
        skill_md = self.skill_path / 'SKILL.md'
        if skill_md.exists():
            self._check_section_numbering(skill_md)
        
        return self.report
    
    def _check_file(self, file_path: Path):
        """Check a single markdown file for consistency issues"""
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            self.report.issues.append(Issue(
                severity='error',
                file=str(file_path.relative_to(self.skill_path)),
                line=None,
                message=f"Could not read file: {e}"
            ))
            return
        
        relative_path = str(file_path.relative_to(self.skill_path))
        lines = content.split('\n')
        
        # Check for deprecated fields in YAML blocks
        self._check_yaml_blocks(content, relative_path, lines)
        
        # Check for incorrect paths
        self._check_paths(content, relative_path, lines)
        
        # Check for deprecated field references in text
        self._check_deprecated_references(content, relative_path, lines)
        
    def _check_yaml_blocks(self, content: str, file_path: str, lines: List[str]):
        """Check YAML code blocks for deprecated fields"""
        
        # Pattern to find YAML code blocks
        yaml_block_pattern = re.compile(
            r'```ya?ml\s*\n(.*?)```',
            re.DOTALL | re.IGNORECASE
        )
        
        for match in yaml_block_pattern.finditer(content):
            self.report.yaml_blocks_checked += 1
            yaml_content = match.group(1)
            block_start = content[:match.start()].count('\n') + 1
            
            # Check for deprecated fields
            for deprecated in self.DEPRECATED_FIELDS:
                # Match field at start of line or after whitespace
                pattern = re.compile(rf'^(\s*){deprecated}:', re.MULTILINE)
                for field_match in pattern.finditer(yaml_content):
                    field_line = yaml_content[:field_match.start()].count('\n')
                    actual_line = block_start + field_line + 1
                    
                    suggestion = self._get_deprecation_suggestion(deprecated)
                    
                    self.report.issues.append(Issue(
                        severity='error',
                        file=file_path,
                        line=actual_line,
                        message=f"Deprecated field '{deprecated}:' found in YAML example",
                        suggestion=suggestion
                    ))
            
            # Check for 'permissions:' (should be 'permission:')
            permissions_match = re.search(r'^\s*permissions:', yaml_content, re.MULTILINE)
            if permissions_match:
                line_num = block_start + yaml_content[:permissions_match.start()].count('\n') + 1
                self.report.issues.append(Issue(
                    severity='error',
                    file=file_path,
                    line=line_num,
                    message="Field 'permissions:' should be 'permission:' (singular)",
                    suggestion="Change 'permissions:' to 'permission:'"
                ))
    
    def _get_deprecation_suggestion(self, field: str) -> str:
        """Get suggestion for deprecated field"""
        suggestions = {
            'name': "Remove 'name:' - agent name comes from the filename",
            'skills': "Remove 'skills:' - skills are loaded at runtime via the skill tool. Document when to load skills in agent instructions instead.",
            'permissions': "Rename to 'tools:' for tool enablement, or 'permission:' for access control patterns"
        }
        return suggestions.get(field, f"Remove deprecated field '{field}'")
    
    def _check_paths(self, content: str, file_path: str, lines: List[str]):
        """Check for incorrect agent paths"""
        for incorrect_path in self.INCORRECT_AGENT_PATHS:
            for i, line in enumerate(lines, 1):
                if incorrect_path in line:
                    self.report.issues.append(Issue(
                        severity='error',
                        file=file_path,
                        line=i,
                        message=f"Incorrect path '{incorrect_path}' found",
                        suggestion=f"Change to '{self.CORRECT_AGENT_PATH}'"
                    ))
    
    def _check_deprecated_references(self, content: str, file_path: str, lines: List[str]):
        """Check for textual references to deprecated patterns"""
        
        # Check for 'skills: []' pattern mentioned in text
        for i, line in enumerate(lines, 1):
            # Skip if inside a code block (rough check)
            if line.strip().startswith('```') or line.strip().startswith('#'):
                continue
                
            # Check for mentions of skills array in frontmatter context
            if 'skills: []' in line.lower() or 'skills:' in line.lower():
                # Check if it's explaining the deprecation (OK) or suggesting use (NOT OK)
                context_start = max(0, i - 3)
                context_end = min(len(lines), i + 3)
                context = ' '.join(lines[context_start:context_end]).lower()
                
                if 'deprecated' not in context and 'runtime' not in context and 'not' not in context:
                    if 'frontmatter' in context or 'yaml' in context or 'add' in context:
                        self.report.issues.append(Issue(
                            severity='warning',
                            file=file_path,
                            line=i,
                            message="Possible reference to deprecated 'skills:' field usage",
                            suggestion="Verify this doesn't suggest using skills: in frontmatter"
                        ))
    
    def _check_cross_references(self, md_files: List[Path]):
        """Check that cross-references between files are valid"""
        
        # Collect all file paths relative to skill root
        existing_files = {
            str(f.relative_to(self.skill_path)).replace('\\', '/')
            for f in md_files
        }
        
        # Add directories
        existing_dirs = {
            str(f.parent.relative_to(self.skill_path)).replace('\\', '/') + '/'
            for f in md_files
            if f.parent != self.skill_path
        }
        
        # Check references in each file
        link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
        
        for md_file in md_files:
            content = md_file.read_text(encoding='utf-8')
            relative_path = str(md_file.relative_to(self.skill_path))
            
            for match in link_pattern.finditer(content):
                link_text = match.group(1)
                link_target = match.group(2)
                
                # Skip external links and anchors
                if link_target.startswith(('http://', 'https://', '#')):
                    continue
                
                # Resolve relative path
                if link_target.startswith('./'):
                    link_target = link_target[2:]
                
                # Check if target exists (simplified check)
                target_path = (md_file.parent / link_target).resolve()
                
                try:
                    target_relative = str(target_path.relative_to(self.skill_path))
                except ValueError:
                    # Path is outside skill directory
                    continue
                
                if not target_path.exists():
                    line_num = content[:match.start()].count('\n') + 1
                    self.report.issues.append(Issue(
                        severity='warning',
                        file=relative_path,
                        line=line_num,
                        message=f"Broken link: [{link_text}]({link_target})",
                        suggestion=f"Verify the file exists at: {target_relative}"
                    ))
    
    def _check_section_numbering(self, skill_md: Path):
        """Check for duplicate section numbers in SKILL.md"""
        content = skill_md.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        # Track heading numbers at each level
        heading_numbers: Dict[int, List[Tuple[int, str]]] = defaultdict(list)
        
        for i, line in enumerate(lines, 1):
            # Match numbered headings like "### 1." or "### 2."
            match = re.match(r'^(#{2,4})\s*(\d+)\.\s+(.+)', line)
            if match:
                level = len(match.group(1))
                number = match.group(2)
                title = match.group(3)
                heading_numbers[level].append((i, f"{number}. {title}"))
        
        # Check for duplicates at each level
        for level, headings in heading_numbers.items():
            numbers_seen: Dict[str, int] = {}
            for line_num, heading in headings:
                num = heading.split('.')[0]
                if num in numbers_seen:
                    self.report.issues.append(Issue(
                        severity='error',
                        file='SKILL.md',
                        line=line_num,
                        message=f"Duplicate section number '{num}.' (first seen at line {numbers_seen[num]})",
                        suggestion="Renumber sections sequentially"
                    ))
                else:
                    numbers_seen[num] = line_num


def print_report(report: ConsistencyReport, skill_path: Path) -> int:
    """Print the consistency report"""
    print(f"\n{'='*70}")
    print(f"Skill Consistency Report: {skill_path.name}")
    print(f"{'='*70}")
    print(f"\nFiles checked: {report.files_checked}")
    print(f"YAML blocks checked: {report.yaml_blocks_checked}")
    print()
    
    if report.errors:
        print(f"❌ ERRORS ({len(report.errors)}):")
        print("-" * 50)
        for issue in report.errors:
            loc = f"{issue.file}"
            if issue.line:
                loc += f":{issue.line}"
            print(f"\n  📍 {loc}")
            print(f"     {issue.message}")
            if issue.suggestion:
                print(f"     💡 {issue.suggestion}")
        print()
    
    if report.warnings:
        print(f"⚠️  WARNINGS ({len(report.warnings)}):")
        print("-" * 50)
        for issue in report.warnings:
            loc = f"{issue.file}"
            if issue.line:
                loc += f":{issue.line}"
            print(f"\n  📍 {loc}")
            print(f"     {issue.message}")
            if issue.suggestion:
                print(f"     💡 {issue.suggestion}")
        print()
    
    if report.infos:
        print(f"ℹ️  INFO ({len(report.infos)}):")
        print("-" * 50)
        for issue in report.infos:
            loc = f"{issue.file}"
            if issue.line:
                loc += f":{issue.line}"
            print(f"  {loc}: {issue.message}")
        print()
    
    print(f"{'='*70}")
    if report.is_consistent:
        print("✅ CONSISTENCY CHECK PASSED")
        print(f"   No critical issues found in {report.files_checked} files")
    else:
        print("❌ CONSISTENCY CHECK FAILED")
        print(f"   Found {len(report.errors)} errors that need to be fixed")
    print(f"{'='*70}\n")
    
    return 0 if report.is_consistent else 1


def main():
    # Determine skill path
    if len(sys.argv) > 1:
        skill_path = Path(sys.argv[1])
    else:
        # Default to parent directory of this script
        script_dir = Path(__file__).parent
        skill_path = script_dir.parent
    
    if not skill_path.exists():
        print(f"Error: Path does not exist: {skill_path}")
        return 1
    
    if not (skill_path / 'SKILL.md').exists():
        print(f"Error: Not a valid skill directory (no SKILL.md): {skill_path}")
        return 1
    
    print(f"Checking consistency of: {skill_path}")
    
    checker = SkillConsistencyChecker(skill_path)
    report = checker.check_all()
    
    return print_report(report, skill_path)


if __name__ == '__main__':
    sys.exit(main())
