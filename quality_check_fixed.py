#!/usr/bin/env python3
"""
Code Quality Check Script for VINAYAK REXINE HOUSE Catalog System
Checks for common SonarQube violations and best practices
"""

import os
import ast
import re
import sys
from pathlib import Path

class CodeQualityChecker:
    """Code quality checker following SonarQube standards"""
    
    def __init__(self):
        """Initialize the quality checker with empty issue lists."""
        self.issues = []
        self.warnings = []
        
    def check_python_files(self):
        """Check all Python files for quality issues"""
        python_files = list(Path('.').glob('**/*.py'))
        for file_path in python_files:
            if 'venv' in str(file_path) or '__pycache__' in str(file_path):
                continue
            self.check_python_file(file_path)
    
    def check_python_file(self, filepath):
        """Check individual Python file"""
        content = self.read_file(filepath)
        if not content:
            return
            
        # Check for hardcoded secrets
        self.check_hardcoded_secrets(filepath, content)
        
        # Check for missing docstrings
        self.check_missing_docstrings(filepath, content)
        
        # Check function complexity (simplified)
        self.check_function_complexity(filepath, content)
        
        # Check for SQL injection patterns
        self.check_sql_injection(filepath, content)
    
    def read_file(self, filepath):
        """Read file with proper encoding"""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            try:
                with open(filepath, 'r', encoding='latin-1') as file:
                    return file.read()
            except Exception:
                try:
                    with open(filepath, 'r', encoding='cp1252') as file:
                        return file.read()
                except Exception as e:
                    self.issues.append(f"ERROR: Cannot parse {filepath}: {e}")
                    return ""
        except Exception as e:
            self.issues.append(f"ERROR: Cannot parse {filepath}: {e}")
            return ""
    
    def check_hardcoded_secrets(self, filepath, content):
        """Check for hardcoded secrets and keys"""
        secret_patterns = [
            r'SECRET_KEY\s*=\s*["\'][\w\d]{10,}["\']',
            r'API_KEY\s*=\s*["\'][\w\d]{10,}["\']',
            r'PASSWORD\s*=\s*["\'][\w\d]{6,}["\']',
            r'app\.secret_key\s*=\s*["\'][\w\d]{10,}["\']',
        ]
        
        for pattern in secret_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                self.issues.append(f"SECURITY: Hardcoded secret found in {filepath}:{line_num}")
    
    def check_missing_docstrings(self, filepath, content):
        """Check for missing function and class docstrings"""
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            self.issues.append(f"SYNTAX: Parse error in {filepath}: {e}")
            return
            
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                if not ast.get_docstring(node):
                    line_num = node.lineno
                    node_type = "function" if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) else "class"
                    self.warnings.append(f"DOCUMENTATION: Missing docstring for {node_type} '{node.name}' in {filepath}:{line_num}")
    
    def check_function_complexity(self, filepath, content):
        """Check for high cyclomatic complexity (simplified check)"""
        lines = content.split('\n')
        in_function = False
        function_name = ""
        complexity = 0
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            if stripped.startswith('def ') or stripped.startswith('async def '):
                if in_function and complexity > 10:
                    self.warnings.append(f"COMPLEXITY: Function '{function_name}' has high complexity ({complexity}) in {filepath}")
                
                in_function = True
                function_name = stripped.split('(')[0].replace('def ', '').replace('async def ', '').strip()
                complexity = 1
            
            elif in_function:
                if any(keyword in stripped for keyword in ['if ', 'elif ', 'for ', 'while ', 'except ', 'and ', 'or ']):
                    complexity += 1
                
                if stripped.startswith('def ') or stripped.startswith('class ') or (stripped and not stripped.startswith(' ') and not stripped.startswith('\t')):
                    if stripped.startswith('def ') or stripped.startswith('async def '):
                        continue
                    in_function = False
        
        if in_function and complexity > 10:
            self.warnings.append(f"COMPLEXITY: Function '{function_name}' has high complexity ({complexity}) in {filepath}")
    
    def check_sql_injection(self, filepath, content):
        """Check for potential SQL injection vulnerabilities"""
        sql_patterns = [
            r'execute\(["\'].*%.*["\']',
            r'execute\(["\'].*\+.*["\']',
            r'execute\(["\'].*\.format\(',
        ]
        
        for pattern in sql_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                self.issues.append(f"SECURITY: Potential SQL injection in {filepath}:{line_num}")
    
    def check_javascript_files(self):
        """Check JavaScript files for quality issues"""
        js_files = list(Path('.').glob('**/*.js'))
        for file_path in js_files:
            if 'node_modules' in str(file_path):
                continue
            self.check_javascript_file(file_path)
    
    def check_javascript_file(self, filepath):
        """Check individual JavaScript file"""
        content = self.read_file(filepath)
        if not content:
            return
        
        # Check for console.log statements
        console_pattern = r'console\.(log|debug|info)'
        matches = re.finditer(console_pattern, content)
        for match in matches:
            line_num = content[:match.start()].count('\n') + 1
            self.warnings.append(f"CODE SMELL: console.log found in {filepath}")
    
    def generate_report(self):
        """Generate quality report"""
        print("Running code quality check...")
        print("=" * 60)
        print("CODE QUALITY REPORT - VINAYAK REXINE HOUSE")
        print("=" * 60)
        
        critical_count = len(self.issues)
        warning_count = len(self.warnings)
        
        if critical_count > 0:
            print(f"\n🚨 CRITICAL ISSUES ({critical_count}):")
            print("-" * 40)
            for issue in self.issues:
                print(f"  ❌ {issue}")
        
        if warning_count > 0:
            print(f"\n⚠️  WARNINGS ({warning_count}):")
            print("-" * 40)
            for warning in self.warnings:
                print(f"  ⚠️  {warning}")
        
        print(f"\nSUMMARY:")
        print(f"  Critical Issues: {critical_count}")
        print(f"  Warnings: {warning_count}")
        print(f"  Total: {critical_count + warning_count}")
        
        if critical_count == 0 and warning_count == 0:
            print("\n✅ ALL CHECKS PASSED - Code quality is excellent!")
            return True
        elif critical_count == 0:
            print(f"\n⚠️  QUALITY CHECK PASSED - {warning_count} warnings found")
            return True
        else:
            print(f"\n❌ QUALITY CHECK FAILED - Please fix critical issues")
            return False

def main():
    """Main function to run quality checks"""
    checker = CodeQualityChecker()
    
    # Check Python files
    checker.check_python_files()
    
    # Check JavaScript files  
    checker.check_javascript_files()
    
    # Generate report
    success = checker.generate_report()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()