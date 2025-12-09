#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kbconfig_validate.py - 验证 knowledge-sources.json 配置文件

验证逻辑 (per FR-016, T054a):
1. JSON 格式验证：可解析的合法 JSON
2. 四大类别完整性：standards, company_kb, reference_designs, web 全部存在
3. 字段完整性 (per FR-014)：验证每个类别的 sources[] 中条目的必需字段
4. 占位符一致性：enabled=true 的条目不得包含 {{PLACEHOLDER: 字符串
5. ENV 引用验证：ENV:变量名 格式检查
6. response_parser 安全性：禁止危险字符 (eval, exec, __import__ 等)

Usage:
    python kbconfig_validate.py <config_file>
    python kbconfig_validate.py .elecspecify/memory/knowledge-sources.json

Exit codes:
    0: 验证通过
    1: 验证失败（有错误）
"""

import io
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

# Windows 控制台 UTF-8 支持
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")


# 危险字符模式 (per FR-015 L923, L938)
DANGEROUS_PATTERNS = [
    r"eval\s*\(",
    r"exec\s*\(",
    r"__import__\s*\(",
    r"compile\s*\(",
    r"open\s*\(",
    r"execfile\s*\(",
    r"__builtins__",
]

# 必需类别
REQUIRED_CATEGORIES = ["standards", "company_kb", "reference_designs", "web"]

# 每个类别的必需字段 (per FR-014)
REQUIRED_FIELDS = {
    "standards": [
        "id",
        "standard_number",
        "year",
        "deprecated",
        "title",
        "abstract",
        "location",
        "enabled",
    ],
    "company_kb": ["id", "type", "title", "authors", "year", "abstract", "location", "enabled"],
    "reference_designs": ["id", "name", "vendor", "url", "key_parameters", "location", "enabled"],
    "web": [
        "id",
        "name",
        "url",
        "api_key",
        "method",
        "headers",
        "body_template",
        "response_parser",
        "enabled",
    ],
}


class ValidationError:
    """验证错误记录"""

    def __init__(self, category: str, field: str, message: str, severity: str = "error"):
        self.category = category
        self.field = field
        self.message = message
        self.severity = severity  # 'error', 'warning'

    def __str__(self):
        symbol = "✗" if self.severity == "error" else "⚠"
        if self.field:
            return f"  {symbol} [{self.category}.{self.field}] {self.message}"
        return f"  {symbol} [{self.category}] {self.message}"


class KnowledgeSourcesValidator:
    """知识源配置验证器"""

    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.errors: List[ValidationError] = []
        self.warnings: List[ValidationError] = []
        self.data: Dict[str, Any] = {}

    def validate(self) -> bool:
        """
        执行完整验证流程

        Returns:
            True if validation passes, False otherwise
        """
        # 1. JSON 格式验证
        if not self._validate_json_format():
            return False

        # 2. 四大类别完整性验证
        if not self._validate_categories():
            return False

        # 3. 字段完整性验证
        self._validate_fields()

        # 4. 占位符一致性验证
        self._validate_placeholder_consistency()

        # 5. ENV 引用验证
        self._validate_env_references()

        # 6. response_parser 安全性验证
        self._validate_response_parser_security()

        return len(self.errors) == 0

    def _validate_json_format(self) -> bool:
        """验证 JSON 格式"""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                self.data = json.load(f)

            if not isinstance(self.data, dict):
                self.errors.append(
                    ValidationError("root", "", "配置文件根必须为对象 (JSON object)")
                )
                return False

            return True

        except FileNotFoundError:
            self.errors.append(ValidationError("file", "", f"配置文件不存在: {self.config_path}"))
            return False

        except json.JSONDecodeError as e:
            self.errors.append(ValidationError("json", "", f"JSON 格式错误: {e}"))
            return False

        except Exception as e:
            self.errors.append(ValidationError("file", "", f"读取文件失败: {e}"))
            return False

    def _validate_categories(self) -> bool:
        """验证四大类别完整性"""
        missing_categories = []

        for category in REQUIRED_CATEGORIES:
            if category not in self.data:
                missing_categories.append(category)

        if missing_categories:
            self.errors.append(
                ValidationError("structure", "", f"缺少必需类别: {', '.join(missing_categories)}")
            )
            return False

        # 验证每个类别的基本结构
        for category in REQUIRED_CATEGORIES:
            cat_data = self.data[category]

            if not isinstance(cat_data, dict):
                self.errors.append(ValidationError(category, "", "类别必须为对象 (JSON object)"))
                continue

            if "enabled" not in cat_data:
                self.errors.append(ValidationError(category, "enabled", "enabled 字段缺失"))

            elif not isinstance(cat_data["enabled"], bool):
                self.errors.append(
                    ValidationError(
                        category,
                        "enabled",
                        f"enabled 必须为布尔值，当前为: {type(cat_data['enabled']).__name__}",
                    )
                )

            if "sources" not in cat_data:
                self.errors.append(ValidationError(category, "sources", "sources 字段缺失"))

            elif not isinstance(cat_data["sources"], list):
                self.errors.append(
                    ValidationError(
                        category,
                        "sources",
                        f"sources 必须为数组，当前为: {type(cat_data['sources']).__name__}",
                    )
                )

        return len(self.errors) == 0

    def _validate_fields(self):
        """验证字段完整性"""
        for category in REQUIRED_CATEGORIES:
            if category not in self.data:
                continue

            cat_data = self.data[category]
            if "sources" not in cat_data or not isinstance(cat_data["sources"], list):
                continue

            required_fields = REQUIRED_FIELDS[category]

            for idx, source in enumerate(cat_data["sources"]):
                if not isinstance(source, dict):
                    self.errors.append(
                        ValidationError(
                            category,
                            f"sources[{idx}]",
                            f"条目必须为对象，当前为: {type(source).__name__}",
                        )
                    )
                    continue

                # 检查必需字段
                missing_fields = []
                for field in required_fields:
                    if field not in source:
                        missing_fields.append(field)

                if missing_fields:
                    source_id = source.get("id", f"index-{idx}")
                    self.errors.append(
                        ValidationError(
                            category,
                            f"sources[{idx}] (id={source_id})",
                            f"缺少必需字段: {', '.join(missing_fields)}",
                        )
                    )

                # 验证字段类型
                self._validate_field_types(category, idx, source)

    def _validate_field_types(self, category: str, idx: int, source: dict):
        """验证字段类型"""
        source_id = source.get("id", f"index-{idx}")

        # enabled 字段必须为布尔值
        if "enabled" in source and not isinstance(source["enabled"], bool):
            self.errors.append(
                ValidationError(
                    category,
                    f"sources[{idx}].enabled (id={source_id})",
                    f"enabled 必须为布尔值，当前为: {type(source['enabled']).__name__}",
                )
            )

        # year 字段必须为整数 (standards, company_kb)
        if category in ["standards", "company_kb"] and "year" in source:
            if not isinstance(source["year"], int):
                self.errors.append(
                    ValidationError(
                        category,
                        f"sources[{idx}].year (id={source_id})",
                        f"year 必须为整数，当前为: {type(source['year']).__name__}",
                    )
                )

        # deprecated 字段必须为布尔值 (standards)
        if category == "standards" and "deprecated" in source:
            if not isinstance(source["deprecated"], bool):
                self.errors.append(
                    ValidationError(
                        category,
                        f"sources[{idx}].deprecated (id={source_id})",
                        f"deprecated 必须为布尔值，当前为: {type(source['deprecated']).__name__}",
                    )
                )

        # authors 字段必须为数组 (company_kb)
        if category == "company_kb" and "authors" in source:
            if not isinstance(source["authors"], list):
                self.errors.append(
                    ValidationError(
                        category,
                        f"sources[{idx}].authors (id={source_id})",
                        f"authors 必须为数组，当前为: {type(source['authors']).__name__}",
                    )
                )

        # key_parameters 字段必须为对象 (reference_designs)
        if category == "reference_designs" and "key_parameters" in source:
            if not isinstance(source["key_parameters"], dict):
                self.errors.append(
                    ValidationError(
                        category,
                        f"sources[{idx}].key_parameters (id={source_id})",
                        f"key_parameters 必须为对象，当前为: {type(source['key_parameters']).__name__}",
                    )
                )

        # headers, body_template, response_parser 字段类型 (web)
        if category == "web":
            if "headers" in source and not isinstance(source["headers"], dict):
                self.errors.append(
                    ValidationError(
                        category,
                        f"sources[{idx}].headers (id={source_id})",
                        f"headers 必须为对象，当前为: {type(source['headers']).__name__}",
                    )
                )

            if "body_template" in source and not isinstance(source["body_template"], (dict, str)):
                self.errors.append(
                    ValidationError(
                        category,
                        f"sources[{idx}].body_template (id={source_id})",
                        f"body_template 必须为对象或字符串，当前为: {type(source['body_template']).__name__}",
                    )
                )

            if "response_parser" in source and not isinstance(
                source["response_parser"], (dict, str)
            ):
                self.errors.append(
                    ValidationError(
                        category,
                        f"sources[{idx}].response_parser (id={source_id})",
                        f"response_parser 必须为对象或字符串，当前为: {type(source['response_parser']).__name__}",
                    )
                )

    def _validate_placeholder_consistency(self):
        """验证占位符一致性 (per FR-014 L929, L933)"""
        for category in REQUIRED_CATEGORIES:
            if category not in self.data:
                continue

            cat_data = self.data[category]
            if "sources" not in cat_data or not isinstance(cat_data["sources"], list):
                continue

            for idx, source in enumerate(cat_data["sources"]):
                if not isinstance(source, dict):
                    continue

                source_id = source.get("id", f"index-{idx}")
                enabled = source.get("enabled", False)

                # 如果 enabled=true，检查是否有占位符
                if enabled:
                    placeholders_found = []

                    for key, value in source.items():
                        if self._contains_placeholder(value):
                            placeholders_found.append(key)

                    if placeholders_found:
                        self.errors.append(
                            ValidationError(
                                category,
                                f"sources[{idx}] (id={source_id})",
                                f"enabled=true 但以下字段仍包含占位符: {', '.join(placeholders_found)}",
                            )
                        )

    def _contains_placeholder(self, value: Any) -> bool:
        """检查值是否包含 {{PLACEHOLDER: 字符串"""
        if isinstance(value, str):
            return "{{PLACEHOLDER:" in value

        elif isinstance(value, dict):
            return any(self._contains_placeholder(v) for v in value.values())

        elif isinstance(value, list):
            return any(self._contains_placeholder(item) for item in value)

        return False

    def _validate_env_references(self):
        """验证 ENV 引用格式"""
        env_pattern = re.compile(r"^ENV:[A-Z_][A-Z0-9_]*$")

        for category in REQUIRED_CATEGORIES:
            if category not in self.data:
                continue

            cat_data = self.data[category]
            if "sources" not in cat_data or not isinstance(cat_data["sources"], list):
                continue

            for idx, source in enumerate(cat_data["sources"]):
                if not isinstance(source, dict):
                    continue

                source_id = source.get("id", f"index-{idx}")

                # 检查 api_key 字段的 ENV 引用 (web)
                if category == "web" and "api_key" in source:
                    api_key = source["api_key"]
                    if isinstance(api_key, str) and api_key.startswith("ENV:"):
                        if not env_pattern.match(api_key):
                            self.warnings.append(
                                ValidationError(
                                    category,
                                    f"sources[{idx}].api_key (id={source_id})",
                                    f"ENV 引用格式不规范: {api_key} (建议格式: ENV:VARIABLE_NAME)",
                                    severity="warning",
                                )
                            )

    def _validate_response_parser_security(self):
        """验证 response_parser 安全性 (per FR-015 L936-939)"""
        for category in REQUIRED_CATEGORIES:
            if category not in self.data:
                continue

            cat_data = self.data[category]
            if "sources" not in cat_data or not isinstance(cat_data["sources"], list):
                continue

            for idx, source in enumerate(cat_data["sources"]):
                if not isinstance(source, dict):
                    continue

                source_id = source.get("id", f"index-{idx}")

                # 只检查 web 类别的 response_parser
                if category == "web" and "response_parser" in source:
                    response_parser = source["response_parser"]
                    dangerous_chars = self._check_dangerous_patterns(response_parser)

                    if dangerous_chars:
                        self.errors.append(
                            ValidationError(
                                category,
                                f"sources[{idx}].response_parser (id={source_id})",
                                f"包含危险字符或函数调用: {', '.join(dangerous_chars)}",
                            )
                        )

    def _check_dangerous_patterns(self, value: Any) -> List[str]:
        """检查危险模式"""
        dangerous_found = []

        if isinstance(value, str):
            for pattern in DANGEROUS_PATTERNS:
                if re.search(pattern, value, re.IGNORECASE):
                    # 提取匹配的文本
                    match = re.search(pattern, value, re.IGNORECASE)
                    if match:
                        dangerous_found.append(match.group(0))

        elif isinstance(value, dict):
            for v in value.values():
                dangerous_found.extend(self._check_dangerous_patterns(v))

        elif isinstance(value, list):
            for item in value:
                dangerous_found.extend(self._check_dangerous_patterns(item))

        return dangerous_found

    def print_summary(self):
        """打印验证摘要"""
        if len(self.errors) == 0 and len(self.warnings) == 0:
            print("✓ 验证通过")
            print()
            self._print_statistics()
            return

        print("验证结果:")
        print()

        if self.errors:
            print(f"错误 ({len(self.errors)}):")
            for error in self.errors:
                print(str(error))
            print()

        if self.warnings:
            print(f"警告 ({len(self.warnings)}):")
            for warning in self.warnings:
                print(str(warning))
            print()

        self._print_statistics()

    def _print_statistics(self):
        """打印统计信息"""
        if not self.data:
            return

        print("配置统计:")
        for category in REQUIRED_CATEGORIES:
            if category not in self.data:
                continue

            cat_data = self.data[category]
            enabled = cat_data.get("enabled", False)
            sources = cat_data.get("sources", [])
            sources_count = len(sources)

            enabled_sources = sum(
                1 for s in sources if isinstance(s, dict) and s.get("enabled", False)
            )
            placeholder_sources = sum(
                1 for s in sources if isinstance(s, dict) and self._contains_placeholder(s)
            )

            status = "启用" if enabled else "禁用"
            print(
                f"  {category}: {status}, {sources_count} 个条目 ({enabled_sources} 已启用, {placeholder_sources} 包含占位符)"
            )


def main():
    """主函数"""
    if len(sys.argv) != 2:
        print("Usage: python kbconfig_validate.py <config_file>")
        print("Example: python kbconfig_validate.py .elecspecify/memory/knowledge-sources.json")
        sys.exit(1)

    config_path = Path(sys.argv[1])

    print(f"验证配置文件: {config_path}")
    print()

    validator = KnowledgeSourcesValidator(config_path)
    is_valid = validator.validate()

    validator.print_summary()

    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
