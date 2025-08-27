"""
Go parsing strategy using regex patterns.
"""

import re
from typing import Dict, List, Tuple, Optional
from .base_strategy import ParsingStrategy
from ..models import SymbolInfo, FileInfo


class GoParsingStrategy(ParsingStrategy):
    """Go-specific parsing strategy using regex patterns."""

    def get_language_name(self) -> str:
        return "go"

    def get_supported_extensions(self) -> List[str]:
        return ['.go']

    def parse_file(self, file_path: str, content: str) -> Tuple[Dict[str, SymbolInfo], FileInfo]:
        """Parse Go file using regex patterns."""
        symbols = {}
        functions = []
        classes = []  # Go doesn't have classes, but we'll track structs/interfaces
        imports = []
        package = None

        lines = content.splitlines()

        for i, line in enumerate(lines):
            line = line.strip()

            # Package declaration
            if line.startswith('package '):
                package = line.split('package ')[1].strip()

            # Import statements
            elif line.startswith('import '):
                import_match = re.search(r'import\s+"([^"]+)"', line)
                if import_match:
                    imports.append(import_match.group(1))

            # Function declarations
            elif line.startswith('func '):
                func_match = re.match(r'func\s+(\w+)\s*\(', line)
                if func_match:
                    func_name = func_match.group(1)
                    symbol_id = self._create_symbol_id(file_path, func_name)
                    symbols[symbol_id] = SymbolInfo(
                        type="function",
                        file=file_path,
                        line=i + 1,
                        signature=line
                    )
                    functions.append(func_name)

                # Method declarations (func (receiver) methodName)
                method_match = re.match(r'func\s+\([^)]+\)\s+(\w+)\s*\(', line)
                if method_match:
                    method_name = method_match.group(1)
                    symbol_id = self._create_symbol_id(file_path, method_name)
                    symbols[symbol_id] = SymbolInfo(
                        type="method",
                        file=file_path,
                        line=i + 1,
                        signature=line
                    )
                    functions.append(method_name)

            # Struct declarations
            elif re.match(r'type\s+\w+\s+struct\s*\{', line):
                struct_match = re.match(r'type\s+(\w+)\s+struct', line)
                if struct_match:
                    struct_name = struct_match.group(1)
                    symbol_id = self._create_symbol_id(file_path, struct_name)
                    symbols[symbol_id] = SymbolInfo(
                        type="struct",
                        file=file_path,
                        line=i + 1
                    )
                    classes.append(struct_name)

            # Interface declarations
            elif re.match(r'type\s+\w+\s+interface\s*\{', line):
                interface_match = re.match(r'type\s+(\w+)\s+interface', line)
                if interface_match:
                    interface_name = interface_match.group(1)
                    symbol_id = self._create_symbol_id(file_path, interface_name)
                    symbols[symbol_id] = SymbolInfo(
                        type="interface",
                        file=file_path,
                        line=i + 1
                    )
                    classes.append(interface_name)

        # Phase 2: Add call relationship analysis
        self._analyze_go_calls(content, symbols, file_path)

        file_info = FileInfo(
            language=self.get_language_name(),
            line_count=len(lines),
            symbols={"functions": functions, "classes": classes},
            imports=imports,
            package=package
        )

        return symbols, file_info

    def _analyze_go_calls(self, content: str, symbols: Dict[str, SymbolInfo], file_path: str):
        """Analyze Go function calls for relationships."""
        lines = content.splitlines()
        current_function = None
        is_function_declaration_line = False

        for i, line in enumerate(lines):
            original_line = line
            line = line.strip()

            # Track current function context
            if line.startswith('func '):
                func_name = self._extract_go_function_name(line)
                if func_name:
                    current_function = self._create_symbol_id(file_path, func_name)
                    is_function_declaration_line = True
            else:
                is_function_declaration_line = False

            # Find function calls: functionName() or obj.methodName()
            # Skip the function declaration line itself to avoid false self-calls
            if current_function and not is_function_declaration_line and ('(' in line and ')' in line):
                called_functions = self._extract_go_called_functions(line)
                for called_func in called_functions:
                    # Find the called function in symbols and add relationship
                    for symbol_id, symbol_info in symbols.items():
                        if called_func in symbol_id.split("::")[-1]:
                            if current_function not in symbol_info.called_by:
                                symbol_info.called_by.append(current_function)

    def _extract_go_function_name(self, line: str) -> Optional[str]:
        """Extract function name from Go function declaration."""
        try:
            # func functionName(...) or func (receiver) methodName(...)
            match = re.match(r'func\s+(?:\([^)]*\)\s+)?(\w+)\s*\(', line)
            if match:
                return match.group(1)
        except:
            pass
        return None

    def _extract_go_called_functions(self, line: str) -> List[str]:
        """Extract function names that are being called in this line."""
        called_functions = []

        # Find patterns like: functionName( or obj.methodName(
        patterns = [
            r'(\w+)\s*\(',  # functionName(
            r'\.(\w+)\s*\(',  # .methodName(
        ]

        for pattern in patterns:
            matches = re.findall(pattern, line)
            called_functions.extend(matches)

        return called_functions
