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
                
            self.check_file(file_path)
    
    def check_file(self, file_path):
        """Check individual Python file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Parse AST
            tree = ast.parse(content)
            
            # Run checks
            self.check_hardcoded_secrets(content, file_path)
            self.check_sql_injection(content, file_path)
            self.check_function_complexity(tree, file_path)
            self.check_exception_handling(tree, file_path)
            self.check_imports(tree, file_path)
            self.check_docstrings(tree, file_path)
            
        except Exception as e:
            self.issues.append(f"ERROR: Cannot parse {file_path}: {e}")
    
    def check_hardcoded_secrets(self, content, file_path):
        """Check for hardcoded secrets and passwords"""
        patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'secret_key\s*=\s*["\'][^"\']+["\']',
            r'api_key\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']'
        ]
        
        for i, line in enumerate(content.split('\n'), 1):
            for pattern in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    if 'os.environ' not in line and 'os.urandom' not in line:
                        self.issues.append(
                            f"SECURITY: Hardcoded secret found in {file_path}:{i}"
                        )
    
    def check_sql_injection(self, content, file_path):
        """Check for potential SQL injection vulnerabilities"""
        # Look for string concatenation in SQL queries
        sql_patterns = [
            r'execute\s*\(\s*["\'][^"\']*\s*\+',
            r'execute\s*\(\s*f["\']',
            r'execute\s*\(\s*.*%.*["\']'
        ]
        
        for i, line in enumerate(content.split('\n'), 1):
            for pattern in sql_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    self.issues.append(
                        f"SECURITY: Potential SQL injection in {file_path}:{i}"
                    )
    
    def check_function_complexity(self, tree, file_path):
        """Check for functions with high cyclomatic complexity"""
        class ComplexityVisitor(ast.NodeVisitor):
            """AST visitor to calculate function complexity."""
            
            def __init__(self, checker, file_path):
                """Initialize complexity visitor."""
                self.checker = checker
                self.file_path = file_path
                
            def visit_FunctionDef(self, node):
                """Visit function definitions and check complexity."""
                complexity = self.calculate_complexity(node)
                if complexity > 10:
                    self.checker.issues.append(
                        f"MAINTAINABILITY: Function '{node.name}' has high complexity ({complexity}) in {self.file_path}:{node.lineno}"
                    )
                self.generic_visit(node)
            
            def calculate_complexity(self, node):
                """Calculate cyclomatic complexity"""
                complexity = 1  # Base complexity
                
                for child in ast.walk(node):
                    if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                        complexity += 1
                    elif isinstance(child, ast.BoolOp):
                        complexity += len(child.values) - 1
                        
                return complexity
        
        visitor = ComplexityVisitor(self, file_path)
        visitor.visit(tree)
    
    def check_exception_handling(self, tree, file_path):
        """Check for proper exception handling"""
        class ExceptionVisitor(ast.NodeVisitor):
            """AST visitor to check exception handling patterns."""
            
            def __init__(self, checker, file_path):
                """Initialize exception visitor."""
                self.checker = checker
                self.file_path = file_path
                
            def visit_Try(self, node):
                """Visit try-except blocks and check for issues."""
                # Check for bare except clauses
                for handler in node.handlers:
                    if handler.type is None:
                        self.checker.warnings.append(
                            f"CODE SMELL: Bare except clause in {self.file_path}:{handler.lineno}"
                        )
                
                # Check for empty except blocks
                for handler in node.handlers:
                    if len(handler.body) == 1 and isinstance(handler.body[0], ast.Pass):
                        self.checker.warnings.append(
                            f"CODE SMELL: Empty except block in {self.file_path}:{handler.lineno}"
                        )
                
                self.generic_visit(node)
        
        visitor = ExceptionVisitor(self, file_path)
        visitor.visit(tree)
    
    def check_imports(self, tree, file_path):
        """Check for import issues"""
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    imports.append(f"{module}.{alias.name}")
        
        # Check for unused imports (simplified check)
        with open(file_path, 'r') as f:
            content = f.read()
            
        for imp in imports:
            if imp.count('.') == 0 and imp not in content.replace(f"import {imp}", ""):
                pass  # This would need more sophisticated analysis
    
    def check_docstrings(self, tree, file_path):
        """Check for missing docstrings"""
        class DocstringVisitor(ast.NodeVisitor):
            """AST visitor to check for missing docstrings."""
            
            def __init__(self, checker, file_path):
                """Initialize docstring visitor."""
                self.checker = checker
                self.file_path = file_path
                
            def visit_FunctionDef(self, node):
                """Visit function definitions and check for docstrings."""
                if not ast.get_docstring(node) and not node.name.startswith('_'):
                    self.checker.warnings.append(
                        f"DOCUMENTATION: Missing docstring for function '{node.name}' in {self.file_path}:{node.lineno}"
                    )
                self.generic_visit(node)
            
            def visit_ClassDef(self, node):
                """Visit class definitions and check for docstrings."""
                if not ast.get_docstring(node):
                    self.checker.warnings.append(
                        f"DOCUMENTATION: Missing docstring for class '{node.name}' in {self.file_path}:{node.lineno}"
                    )
                self.generic_visit(node)
        
        visitor = DocstringVisitor(self, file_path)
        visitor.visit(tree)
    
    def check_javascript_files(self):
        """Check JavaScript files for quality issues"""
        js_files = list(Path('.').glob('**/*.js'))
        
        for file_path in js_files:
            if 'node_modules' in str(file_path):
                continue
                
            self.check_js_file(file_path)
    
    def check_js_file(self, file_path):
        """Check individual JavaScript file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for console.log statements
            if 'console.log' in content:
                self.warnings.append(f"CODE SMELL: console.log found in {file_path}")
            
            # Check for eval usage
            if re.search(r'\beval\s*\(', content):
                self.issues.append(f"SECURITY: eval() usage found in {file_path}")
            
            # Check for innerHTML usage
            if 'innerHTML' in content and 'textContent' not in content:
                self.warnings.append(f"SECURITY: innerHTML usage without sanitization in {file_path}")
            
        except Exception as e:
            self.issues.append(f"ERROR: Cannot read {file_path}: {e}")
    
    def report(self):
        """Generate quality report"""
        print("=" * 60)
        print("CODE QUALITY REPORT - VINAYAK REXINE HOUSE")
        print("=" * 60)
        
        if not self.issues and not self.warnings:
            print("✅ NO ISSUES FOUND - Code quality is excellent!")
            return True
        
        if self.issues:
            print(f"\n🚨 CRITICAL ISSUES ({len(self.issues)}):")
            print("-" * 40)
            for issue in self.issues:
                print(f"  ❌ {issue}")
        
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            print("-" * 40)
            for warning in self.warnings:
                print(f"  ⚠️  {warning}")
        
        print(f"\nSUMMARY:")
        print(f"  Critical Issues: {len(self.issues)}")
        print(f"  Warnings: {len(self.warnings)}")
        print(f"  Total: {len(self.issues) + len(self.warnings)}")
        
        if self.issues:
            print("\n❌ QUALITY CHECK FAILED - Please fix critical issues")
            return False
        else:
            print("\n✅ QUALITY CHECK PASSED - Only warnings found")
            return True

def main():
    """Main function"""
    print("Running code quality check...")
    
    checker = CodeQualityChecker()
    checker.check_python_files()
    checker.check_javascript_files()
    
    success = checker.report()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()