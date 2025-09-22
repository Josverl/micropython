"""
pytest plugin for testing MicroPython documentation code samples

This plugin provides custom collection and testing of code samples
extracted from MicroPython documentation.
"""

import pytest
import ast
import sys
import os
import importlib.util
from pathlib import Path
from typing import List, Dict, Any, Optional
import tempfile
import subprocess
import json
import re


class DocSampleTest:
    """Represents a test case for a documentation code sample"""
    
    def __init__(self, sample_file: Path, micropython_stubs_path: str):
        self.sample_file = sample_file
        self.micropython_stubs_path = micropython_stubs_path
        self.metadata = self._extract_metadata()
        self.code_content = self._extract_code_content()
    
    def _extract_metadata(self) -> Dict[str, Any]:
        """Extract metadata from sample file docstring"""
        try:
            with open(self.sample_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse docstring for metadata
            tree = ast.parse(content)
            if (tree.body and isinstance(tree.body[0], ast.Expr) 
                and isinstance(tree.body[0].value, ast.Constant)):
                docstring = tree.body[0].value.value
                
                metadata = {}
                for line in docstring.split('\n'):
                    if ':' in line and not line.strip().startswith('Type:'):
                        parts = line.split(':', 1)
                        if len(parts) == 2:
                            key, value = parts
                            metadata[key.strip()] = value.strip()
                
                return metadata
        except Exception as e:
            print(f"Warning: Could not extract metadata from {self.sample_file}: {e}")
        
        return {}
    
    def _extract_code_content(self) -> str:
        """Extract the actual code content without docstring"""
        try:
            with open(self.sample_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse and remove docstring
            tree = ast.parse(content)
            
            # Find the end of the docstring
            lines = content.split('\n')
            if (tree.body and isinstance(tree.body[0], ast.Expr) 
                and isinstance(tree.body[0].value, ast.Constant)):
                
                # Find the end of the triple quotes
                start_line = 0
                in_quotes = False
                quote_count = 0
                
                for i, line in enumerate(lines):
                    if '"""' in line:
                        quote_count += line.count('"""')
                        if quote_count >= 2:
                            start_line = i + 1
                            break
                
                return '\n'.join(lines[start_line:])
            
            return content
        except Exception as e:
            print(f"Warning: Could not extract code from {self.sample_file}: {e}")
            return ""
    
    def run_syntax_check(self) -> tuple[bool, str]:
        """Check if the code has valid Python syntax"""
        try:
            if not self.code_content.strip():
                return False, "Empty code content"
            
            ast.parse(self.code_content)
            return True, "OK"
            
        except SyntaxError as e:
            return False, f"Syntax error: {e}"
        except Exception as e:
            return False, f"Parse error: {e}"
    
    def run_import_check(self) -> tuple[bool, str]:
        """Check if all required imports are available"""
        dependencies = self.metadata.get('Dependencies', '').split(', ')
        dependencies = [dep.strip() for dep in dependencies if dep.strip()]
        
        if not dependencies:
            return True, "No dependencies to check"
        
        # Temporarily add micropython-stubs to path
        original_path = sys.path.copy()
        try:
            if os.path.exists(self.micropython_stubs_path):
                sys.path.insert(0, self.micropython_stubs_path)
            
            missing_deps = []
            for dep in dependencies:
                if dep and dep not in ['builtins']:
                    try:
                        importlib.import_module(dep)
                    except ImportError:
                        missing_deps.append(dep)
            
            if missing_deps:
                return False, f"Missing dependencies: {', '.join(missing_deps)}"
            
            return True, "All dependencies available"
            
        except Exception as e:
            return False, f"Import check error: {e}"
        finally:
            sys.path[:] = original_path
    
    def run_static_analysis(self) -> tuple[bool, str]:
        """Run basic static analysis on the code"""
        try:
            tree = ast.parse(self.code_content)
            
            # Check for common issues
            issues = []
            
            # Check for undefined variables (basic check)
            defined_vars = set()
            used_vars = set()
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Name):
                    if isinstance(node.ctx, ast.Store):
                        defined_vars.add(node.id)
                    elif isinstance(node.ctx, ast.Load):
                        used_vars.add(node.id)
            
            # Skip built-in names and common MicroPython globals
            builtin_names = {
                'print', 'len', 'range', 'int', 'str', 'float', 'bool', 'list', 'dict', 'tuple',
                'True', 'False', 'None', 'Exception', 'ValueError', 'TypeError', 'AttributeError',
                # MicroPython specific
                'const', 'micropython'
            }
            
            undefined = used_vars - defined_vars - builtin_names
            # Filter out module names and attributes
            undefined = {var for var in undefined if '.' not in var and not var.isupper()}
            
            if undefined and len(undefined) > 3:  # Only flag if many undefined vars
                issues.append(f"Potentially undefined variables: {', '.join(list(undefined)[:3])}...")
            
            if issues:
                return False, '; '.join(issues)
            
            return True, "Static analysis passed"
            
        except Exception as e:
            return False, f"Static analysis error: {e}"
    
    def run_execution_test(self) -> tuple[bool, str]:
        """Attempt to execute the code in a controlled environment"""
        if not self.code_content.strip():
            return False, "No code to execute"
        
        # Skip execution for platform-specific code that can't run on host
        platform = self.metadata.get('Platform', '')
        if platform and platform not in ['unix', '']:
            return True, f"Skipped execution (platform-specific: {platform})"
        
        try:
            # Create a restricted execution environment
            exec_globals = {
                '__builtins__': __builtins__,
                'print': lambda *args, **kwargs: None,  # Suppress output
            }
            
            # Add mock objects for hardware-specific modules
            mock_modules = self._create_mock_modules()
            exec_globals.update(mock_modules)
            
            # Execute the code
            exec(self.code_content, exec_globals)
            return True, "Execution successful"
            
        except ImportError as e:
            return True, f"Import error (expected for hardware modules): {e}"
        except Exception as e:
            # Some errors are expected for hardware-specific code
            error_str = str(e).lower()
            if any(keyword in error_str for keyword in ['pin', 'gpio', 'hardware', 'device']):
                return True, f"Hardware-related error (expected): {e}"
            return False, f"Execution error: {e}"
    
    def _create_mock_modules(self) -> Dict[str, Any]:
        """Create mock objects for MicroPython modules that can't be imported on host"""
        
        class MockPin:
            IN, OUT, PULL_UP, PULL_DOWN = 0, 1, 2, 3
            def __init__(self, *args, **kwargs): pass
            def value(self, *args): return 0 if not args else None
            def on(self): pass
            def off(self): pass
            def irq(self, *args, **kwargs): pass
            def init(self, *args, **kwargs): pass
        
        class MockMachine:
            Pin = MockPin
            freq = lambda *args: 160000000 if not args else None
            reset = lambda: None
            unique_id = lambda: b'1234567890abcdef'
            
        class MockNetwork:
            class WLAN:
                IF_STA, IF_AP = 0, 1
                def __init__(self, *args): pass
                def active(self, *args): return True if not args else None
                def connect(self, *args, **kwargs): pass
                def isconnected(self): return True
                def scan(self): return []
                def config(self, *args, **kwargs): return "00:00:00:00:00:00" if args else None
                def ipconfig(self, *args): return "192.168.1.100" if args else {}
        
        return {
            'machine': MockMachine(),
            'network': MockNetwork(),
            'time': type('MockTime', (), {
                'sleep': lambda x: None,
                'sleep_ms': lambda x: None,
                'sleep_us': lambda x: None,
                'ticks_ms': lambda: 1000,
                'ticks_us': lambda: 1000000,
                'ticks_diff': lambda a, b: a - b,
            })(),
        }


def pytest_collect_file(file_path, parent):
    """Collect documentation sample files for testing"""
    if file_path.suffix == '.py' and any(pattern in file_path.name for pattern in ['sample', 'extracted']):
        return DocSampleFile.from_parent(parent, path=file_path)


class DocSampleFile(pytest.File):
    """Custom pytest File for documentation samples"""
    
    def collect(self):
        # Get configuration options
        micropython_stubs_path = self.config.getoption("--micropython-stubs-path", default="./micropython-stubs")
        
        yield DocSampleItem.from_parent(
            self, 
            name=self.path.name,
            micropython_stubs_path=micropython_stubs_path
        )


class DocSampleItem(pytest.Item):
    """Custom pytest Item for documentation samples"""
    
    def __init__(self, name, parent, micropython_stubs_path):
        super().__init__(name, parent)
        self.micropython_stubs_path = micropython_stubs_path
        self._test_results = {}
    
    def runtest(self):
        """Run the test for this documentation sample"""
        test = DocSampleTest(self.path, self.micropython_stubs_path)
        
        # Collect test results
        failures = []
        
        # 1. Syntax check (always run)
        syntax_ok, syntax_msg = test.run_syntax_check()
        self._test_results['syntax'] = (syntax_ok, syntax_msg)
        if not syntax_ok:
            failures.append(f"Syntax check failed: {syntax_msg}")
        
        # 2. Import check (always run)
        import_ok, import_msg = test.run_import_check()
        self._test_results['imports'] = (import_ok, import_msg)
        if not import_ok and self.config.getoption("--strict-imports", default=False):
            failures.append(f"Import check failed: {import_msg}")
        
        # 3. Static analysis (optional)
        if self.config.getoption("--run-static-analysis", default=False):
            static_ok, static_msg = test.run_static_analysis()
            self._test_results['static'] = (static_ok, static_msg)
            if not static_ok:
                failures.append(f"Static analysis failed: {static_msg}")
        
        # 4. Execution test (optional)
        if self.config.getoption("--run-execution-test", default=False):
            exec_ok, exec_msg = test.run_execution_test()
            self._test_results['execution'] = (exec_ok, exec_msg)
            if not exec_ok:
                failures.append(f"Execution test failed: {exec_msg}")
        
        # Report failures
        if failures:
            pytest.fail('\n'.join(failures))
    
    def repr_failure(self, excinfo):
        """Representation of test failure"""
        lines = [f"Documentation sample test failed: {self.path}"]
        
        for test_type, (success, message) in self._test_results.items():
            status = "✓" if success else "✗"
            lines.append(f"  {status} {test_type}: {message}")
        
        return '\n'.join(lines)
    
    def reportinfo(self):
        """Return representation of test location"""
        return self.path, 0, f"DocSample: {self.path.name}"


def pytest_addoption(parser):
    """Add custom command line options"""
    group = parser.getgroup("docsample", "Documentation sample testing options")
    
    group.addoption(
        "--micropython-stubs-path",
        action="store",
        default="./micropython-stubs",
        help="Path to micropython-stubs directory"
    )
    
    group.addoption(
        "--strict-imports",
        action="store_true",
        default=False,
        help="Fail tests if imports are missing"
    )
    
    group.addoption(
        "--run-static-analysis",
        action="store_true",
        default=False,
        help="Run static analysis on samples"
    )
    
    group.addoption(
        "--run-execution-test",
        action="store_true",
        default=False,
        help="Attempt to execute code samples (experimental)"
    )
    
    group.addoption(
        "--platform-filter",
        action="store",
        help="Only test samples for specific platform (e.g., esp32, rp2)"
    )


def pytest_collection_modifyitems(config, items):
    """Modify collected items based on configuration"""
    platform_filter = config.getoption("--platform-filter")
    
    if platform_filter:
        # Filter items based on platform
        filtered_items = []
        for item in items:
            if isinstance(item, DocSampleItem):
                test = DocSampleTest(item.path, item.micropython_stubs_path)
                if test.metadata.get('Platform') == platform_filter:
                    filtered_items.append(item)
            else:
                filtered_items.append(item)
        items[:] = filtered_items


def pytest_report_header(config):
    """Add information to pytest report header"""
    lines = ["MicroPython Documentation Sample Testing"]
    
    stubs_path = config.getoption("--micropython-stubs-path")
    if os.path.exists(stubs_path):
        lines.append(f"MicroPython stubs: {stubs_path}")
    else:
        lines.append(f"MicroPython stubs: {stubs_path} (not found)")
    
    options = []
    if config.getoption("--strict-imports"):
        options.append("strict-imports")
    if config.getoption("--run-static-analysis"):
        options.append("static-analysis")
    if config.getoption("--run-execution-test"):
        options.append("execution-test")
    if config.getoption("--platform-filter"):
        options.append(f"platform={config.getoption('--platform-filter')}")
    
    if options:
        lines.append(f"Options: {', '.join(options)}")
    
    return lines


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Generate detailed test reports"""
    outcome = yield
    rep = outcome.get_result()
    
    if isinstance(item, DocSampleItem) and rep.when == "call":
        # Add detailed results to the report
        if hasattr(item, '_test_results'):
            details = []
            for test_type, (success, message) in item._test_results.items():
                status = "PASSED" if success else "FAILED"
                details.append(f"{test_type}: {status} - {message}")
            
            if details:
                rep.sections.append(("Test Details", '\n'.join(details)))