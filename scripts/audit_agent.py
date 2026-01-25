#!/usr/bin/env python3
"""
Agent Auditor - Audits OpenCode agents for quality and best practices

Usage:
    python3 audit_agent.py /path/to/agent.md
"""

import sys
import re
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime

class AgentAuditor:
    def __init__(self, agent_path: str):
        self.agent_path = Path(agent_path)
        self.scores: Dict[str, float] = {}
        self.findings: List[str] = []
        self.recommendations: List[str] = []
        
    def audit(self) -> Dict[str, Any]:
        """Run comprehensive agent audit"""
        if not self.agent_path.exists():
            return {'error': f"File not found: {self.agent_path}"}
        
        content = self.agent_path.read_text()
        frontmatter, body = self._extract_frontmatter(content)
        
        if frontmatter is None:
            return {'error': 'No valid frontmatter found'}
        
        # Run audit checks
        self._audit_frontmatter_quality(frontmatter)
        self._audit_tool_safety(frontmatter.get('tools', {}), frontmatter.get('permission', {}))
        self._audit_instruction_quality(body)
        self._audit_security(frontmatter, body)
        self._audit_documentation(body)
        
        # Calculate overall score
        overall_score = self._calculate_overall_score()
        
        # Get agent name from filename (since 'name' field is deprecated)
        agent_name = self.agent_path.stem
        
        return {
            'agent_name': agent_name,
            'audit_date': datetime.now().isoformat(),
            'overall_score': overall_score,
            'scores': self.scores,
            'findings': self.findings,
            'recommendations': self.recommendations,
            'risk_level': self._assess_risk_level(frontmatter.get('tools', {}), frontmatter.get('permission', {}))
        }
    
    def _extract_frontmatter(self, content: str) -> Tuple[Optional[Dict], str]:
        """Extract YAML frontmatter"""
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
        if not match:
            return None, content
        
        try:
            frontmatter = yaml.safe_load(match.group(1))
            body = match.group(2)
            return frontmatter, body
        except:
            return None, content
    
    def _audit_frontmatter_quality(self, frontmatter: Dict):
        """Audit frontmatter quality"""
        score = 5.0
        
        # Check description quality
        desc = frontmatter.get('description', '')
        if not desc:
            score -= 2.0
            self.findings.append("Missing description")
            self.recommendations.append("Add a description with triggers and examples")
        else:
            if len(desc) < 50:
                score -= 0.5
                self.findings.append("Description is too short")
                self.recommendations.append("Add more detail to description including trigger conditions")
            
            # Check for examples
            if '<example>' not in desc:
                score -= 0.5
                self.findings.append("Description missing <example> blocks")
                self.recommendations.append("Add <example> blocks showing typical usage")
            
            # Check for trigger keywords
            trigger_keywords = ['use when', 'use for', 'invoke when', 'use proactively']
            if not any(kw in desc.lower() for kw in trigger_keywords):
                score -= 0.3
                self.findings.append("Description missing trigger keywords")
                self.recommendations.append("Add 'Use when...' to clarify when to invoke agent")
        
        # Check mode
        mode = frontmatter.get('mode')
        if mode and mode not in {'primary', 'subagent', 'all'}:
            score -= 0.5
            self.findings.append(f"Invalid mode: {mode}")
            self.recommendations.append("Mode must be 'primary', 'subagent', or 'all'")
        
        self.scores['frontmatter_quality'] = max(0, score)
    
    def _audit_tool_safety(self, tools: Dict, permission: Dict):
        """Audit tool and permission safety"""
        score = 5.0
        
        # Count enabled tools
        enabled = [t for t, v in tools.items() if v is True]
        enabled_count = len(enabled)
        
        # Kitchen sink anti-pattern
        if enabled_count >= 9:
            score -= 1.0
            self.findings.append(f"Many tools enabled ({enabled_count})")
            self.recommendations.append("Review if all tools are necessary - apply least privilege")
        
        # bash without permission patterns
        if tools.get('bash'):
            if not permission.get('bash'):
                score -= 1.5
                self.findings.append("bash enabled but no permission patterns defined")
                self.recommendations.append("Add permission patterns for bash commands")
            else:
                bash_perms = permission.get('bash', {})
                if isinstance(bash_perms, dict):
                    # Check for deny rules on dangerous commands
                    has_deny = any(v == 'deny' for v in bash_perms.values())
                    if not has_deny:
                        score -= 0.5
                        self.findings.append("No deny rules for dangerous bash commands")
                        self.recommendations.append("Add deny rules for rm -rf, dd, mkfs, etc.")
                    
                    # Check for default rule
                    if '*' not in bash_perms:
                        score -= 0.3
                        self.findings.append("No default (*) bash permission rule")
                        self.recommendations.append("Add '*': ask as default bash permission")
        
        # write without read
        if tools.get('write') and not tools.get('read'):
            score -= 0.5
            self.findings.append("write enabled without read")
            self.recommendations.append("Add read tool (agent should read before writing)")
        
        # edit without read
        if tools.get('edit') and not tools.get('read'):
            score -= 0.5
            self.findings.append("edit enabled without read")
            self.recommendations.append("Add read tool (agent must read before editing)")
        
        self.scores['tool_safety'] = max(0, score)
    
    def _audit_instruction_quality(self, body: str):
        """Audit instruction quality"""
        score = 5.0
        
        # Check for section organization
        section_headers = re.findall(r'^##\s+(.+)$', body, re.MULTILINE)
        if len(section_headers) < 3:
            score -= 1.0
            self.findings.append("Few sections in instructions")
            self.recommendations.append("Organize instructions with clear ## headings")
        
        # Check for code examples
        code_blocks = re.findall(r'```', body)
        if len(code_blocks) < 4:  # At least 2 complete blocks
            score -= 0.5
            self.findings.append("Few code examples")
            self.recommendations.append("Add more code/command examples")
        
        # Check for workflow section
        if 'workflow' not in body.lower():
            score -= 0.5
            self.findings.append("No workflow section found")
            self.recommendations.append("Add a Workflow section with step-by-step process")
        
        # Check for responsibilities
        if 'responsibilit' not in body.lower():
            score -= 0.3
            self.findings.append("No responsibilities section found")
            self.recommendations.append("Add Core Responsibilities section")
        
        # Check instruction length
        lines = body.split('\n')
        if len(lines) < 50:
            score -= 0.5
            self.findings.append("Instructions are quite short")
            self.recommendations.append("Add more comprehensive guidance and examples")
        
        self.scores['instruction_quality'] = max(0, score)
    
    def _audit_security(self, frontmatter: Dict, body: str):
        """Audit security aspects"""
        score = 5.0
        tools = frontmatter.get('tools', {})
        permission = frontmatter.get('permission', {})
        
        # Check for safety protocols if bash enabled
        if tools.get('bash'):
            safety_keywords = ['safety', 'confirm', 'always', 'never', 'backup', 'verify', 'check']
            body_lower = body.lower()
            safety_count = sum(1 for kw in safety_keywords if kw in body_lower)
            
            if safety_count < 3:
                score -= 1.5
                self.findings.append("bash enabled but few safety keywords in instructions")
                self.recommendations.append("Add safety protocols: confirmation prompts, backup procedures")
            
            # Check for explicit deny patterns
            bash_perms = permission.get('bash', {})
            if isinstance(bash_perms, dict):
                deny_patterns = [p for p, v in bash_perms.items() if v == 'deny']
                if len(deny_patterns) < 2:
                    score -= 0.5
                    self.findings.append("Few deny patterns for bash")
                    self.recommendations.append("Add more deny patterns for dangerous commands")
        
        # Check for write safety
        if tools.get('write'):
            if 'overwrite' not in body.lower() and 'exist' not in body.lower():
                score -= 0.5
                self.findings.append("write enabled but no overwrite safety mentioned")
                self.recommendations.append("Add guidance on checking file existence before writing")
        
        # Check for secrets handling
        if tools.get('read') or tools.get('bash'):
            if 'secret' not in body.lower() and 'password' not in body.lower() and 'credential' not in body.lower():
                score -= 0.3
                self.findings.append("No guidance on handling sensitive data")
                self.recommendations.append("Add guidelines for handling secrets and credentials")
        
        self.scores['security'] = max(0, score)
    
    def _audit_documentation(self, body: str):
        """Audit documentation completeness"""
        score = 5.0
        
        # Check for key sections
        checks = [
            ('overview', 'Overview or introduction'),
            ('responsibilit', 'Core responsibilities'),
            ('example', 'Usage examples'),
            ('error', 'Error handling'),
        ]
        
        body_lower = body.lower()
        for keyword, description in checks:
            if keyword not in body_lower:
                score -= 0.5
                self.findings.append(f"Missing {description}")
                self.recommendations.append(f"Add {description} section")
        
        # Check for limitations
        if 'limitation' not in body_lower and 'cannot' not in body_lower:
            score -= 0.3
            self.findings.append("Limitations not clearly stated")
            self.recommendations.append("Document what agent CANNOT do")
        
        self.scores['documentation'] = max(0, score)
    
    def _assess_risk_level(self, tools: Dict, permission: Dict) -> str:
        """Assess overall risk level"""
        if tools.get('bash'):
            bash_perms = permission.get('bash', {})
            if isinstance(bash_perms, dict):
                has_deny = any(v == 'deny' for v in bash_perms.values())
                has_ask_default = bash_perms.get('*') == 'ask'
                if has_deny and has_ask_default:
                    return 'MEDIUM'
                return 'HIGH'
            return 'HIGH'
        if tools.get('write') or tools.get('edit'):
            return 'MEDIUM'
        return 'LOW'
    
    def _calculate_overall_score(self) -> float:
        """Calculate overall score from individual scores"""
        if not self.scores:
            return 0.0
        return round(sum(self.scores.values()) / len(self.scores), 2)


def print_audit_report(results: Dict[str, Any]):
    """Print audit report"""
    print(f"\n{'='*70}")
    print(f"Agent Audit Report: {results.get('agent_name', 'unknown')}")
    print(f"{'='*70}")
    print(f"Audit Date: {results.get('audit_date', 'unknown')}")
    overall = results.get('overall_score', 0)
    print(f"Overall Score: {overall:.2f}/5.00 {'⭐' * round(overall)}")
    print(f"Risk Level: {results.get('risk_level', 'UNKNOWN')}")
    print(f"{'='*70}\n")
    
    # Individual scores
    print("📊 Detailed Scores:")
    scores = results.get('scores', {})
    for category, score in scores.items():
        stars = '⭐' * round(score)
        category_display = category.replace('_', ' ').title()
        print(f"  {category_display:.<50} {score:.2f}/5.00 {stars}")
    print()
    
    # Findings
    findings = results.get('findings', [])
    if findings:
        print(f"🔍 Findings ({len(findings)}):")
        for i, finding in enumerate(findings, 1):
            print(f"  {i}. {finding}")
        print()
    
    # Recommendations
    recommendations = results.get('recommendations', [])
    if recommendations:
        # Deduplicate recommendations
        unique_recs = list(dict.fromkeys(recommendations))
        print(f"💡 Recommendations ({len(unique_recs)}):")
        for i, rec in enumerate(unique_recs, 1):
            print(f"  {i}. {rec}")
        print()
    
    # Overall assessment
    print(f"{'='*70}")
    if overall >= 4.5:
        print("✅ EXCELLENT - Agent follows best practices")
    elif overall >= 3.5:
        print("✅ GOOD - Agent is solid with minor improvements needed")
    elif overall >= 2.5:
        print("⚠️  FAIR - Agent needs some improvements")
    else:
        print("❌ NEEDS WORK - Agent requires significant improvements")
    print(f"{'='*70}\n")


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 audit_agent.py /path/to/agent.md")
        return 1
    
    agent_path = sys.argv[1]
    
    auditor = AgentAuditor(agent_path)
    results = auditor.audit()
    
    if 'error' in results:
        print(f"Error: {results['error']}")
        return 1
    
    print_audit_report(results)
    return 0


if __name__ == '__main__':
    sys.exit(main())
