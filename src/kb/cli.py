"""Local content checks; these checks do not verify technical correctness."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml
from jsonschema import Draft202012Validator, FormatChecker


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject duplicate keys instead of silently discarding earlier metadata."""


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str) or key in result:
            raise ValueError(f"YAML key must be a unique string: {key!r}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping
)


def read_yaml(text):
    return yaml.load(text, Loader=UniqueKeyLoader)


def frontmatter(text):
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("missing YAML front matter")
    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise ValueError("unclosed YAML front matter") from error
    return read_yaml("\n".join(lines[1:end]))


def schema_errors(value, schema, label):
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        f"{label}: {'/'.join(map(str, error.absolute_path)) or '(root)'}: {error.message}"
        for error in validator.iter_errors(value)
    ]


def prose(text):
    """Exclude fenced examples and inline code from simple link checks."""
    output = []
    fence = None
    for line in text.splitlines():
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        if fence is None:
            output.append(re.sub(r"`[^`]*`", "", line))
    return "\n".join(output)


def link_errors(path, root):
    # Standard inline links/images; fragments and remote contents are not checked.
    pattern = r"!?\[[^\]\n]*\]\(\s*(?:<([^>]+)>|([^\s)]+))"
    errors = []
    for match in re.finditer(pattern, prose(path.read_text(encoding="utf-8"))):
        target = match.group(1) or match.group(2)
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        destination = (path.parent / unquote(parsed.path)).resolve()
        label = path.relative_to(root)
        if not destination.is_relative_to(root) or not destination.exists():
            errors.append(f"{label}: missing or outside-repository link: {target}")
    return errors


def collect(root):
    """Return metadata records and structural errors, with no external access."""
    errors = []
    records = []
    try:
        content_schema = json.loads((root / "schemas/content.schema.json").read_text())
        sources_schema = json.loads((root / "schemas/sources.schema.json").read_text())
        registry = read_yaml((root / "sources/registry.yaml").read_text())
        taxonomy = read_yaml((root / "config/taxonomy.yaml").read_text())
        folders = {entry["directory"]: entry["id"] for entry in taxonomy["domains"]}
    except (OSError, ValueError, TypeError, KeyError, yaml.YAMLError) as error:
        return [], [f"configuration: {error}"], {}

    errors.extend(schema_errors(registry, sources_schema, "sources/registry.yaml"))
    if errors:
        return [], errors, {}
    source_ids = [source["id"] for source in registry["sources"]]
    if len(source_ids) != len(set(source_ids)):
        errors.append("sources/registry.yaml: duplicate source IDs")
    for folder in folders:
        if not (root / "knowledge" / folder / "index.md").is_file():
            errors.append(f"knowledge/{folder}/index.md: required chapter index missing")

    paths = sorted(
        list((root / "knowledge").rglob("*.md")) + list((root / "paths").rglob("*.md"))
    )
    for path in paths:
        relative = path.relative_to(root)
        try:
            text = path.read_text(encoding="utf-8")
            metadata = frontmatter(text)
            issues = schema_errors(metadata, content_schema, str(relative))
        except (ValueError, yaml.YAMLError) as error:
            errors.append(f"{relative}: {error}")
            continue
        errors.extend(issues)
        if issues:
            continue
        if relative.parts[0] == "knowledge":
            expected = folders.get(relative.parts[1])
            if expected is None or metadata["domain"] != expected:
                errors.append(f"{relative}: domain does not match chapter directory")
        elif metadata["type"] != "path":
            errors.append(f"{relative}: paths/ entries must have type: path")
        for source in metadata["source_refs"]:
            if source not in source_ids:
                errors.append(f"{relative}: unknown source ID: {source}")
        records.append({
            **metadata,
            "path": relative.as_posix(),
            "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        })

    ids = [record["id"] for record in records]
    if len(ids) != len(set(ids)):
        errors.append("content: duplicate content IDs")
    for record in records:
        for related in record.get("related_ids", []):
            if related not in ids:
                errors.append(f"{record['path']}: unknown related ID: {related}")
        for field, refs in (
            ("environment_refs", record.get("applicability", {}).get("environment_refs", [])),
            ("evidence_refs", record.get("verification", {}).get("evidence_refs", [])),
        ):
            for ref in refs:
                if ref not in ids and ref not in source_ids:
                    errors.append(f"{record['path']}: unknown {field} ID: {ref}")

    local_markdown = list(root.glob("*.md"))
    for directory in ("knowledge", "paths", "docs", "sources"):
        local_markdown.extend((root / directory).rglob("*.md"))
    for path in sorted(local_markdown):
        errors.extend(link_errors(path, root))
    return sorted(records, key=lambda record: record["id"]), errors, registry


def build(root, records, registry):
    """Create reproducible artifacts only after callers have validated inputs."""
    inputs = (
        "config/taxonomy.yaml", "sources/registry.yaml",
        "schemas/content.schema.json", "schemas/sources.schema.json",
    )
    catalog = {
        "schema_version": 1,
        "notice": "结构校验和导航清单不证明技术结论正确、版本兼容或经过现场验证。",
        "input_sha256": {
            name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in inputs
        },
        "documents": records,
        "sources": registry["sources"],
    }
    lines = [
        "# 自动生成的内容清单", "",
        "来源为 knowledge/ 与 paths/，请修改源文件后重新运行 make build。", "",
        "结构校验不代表技术结论、兼容性或现场行为已验证。", "",
        "| ID | 标题 | 类型 | 平台 | 审核状态 |", "|---|---|---|---|---|",
    ]
    for record in records:
        title = record["title"].replace("|", "\\|").replace("[", "\\[").replace("]", "\\]")
        lines.append(
            f"| {record['id']} | [{title}](../{record['path']}) | {record['type']} | "
            f"{', '.join(record['platforms'])} | {record['status']} |"
        )
    output = root / "build"
    output.mkdir(exist_ok=True)
    (output / "catalog.json").write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (output / "catalog.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check", "build"))
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args(argv)
    root = args.root.resolve()
    records, errors, registry = collect(root)
    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        print(f"FAILED: {len(errors)} structural issue(s).", file=sys.stderr)
        return 1
    print(f"PASS: {len(records)} content entries; {len(registry['sources'])} sources.")
    print("Checked structure and local file links; not technical correctness or remote links.")
    if args.command == "build":
        build(root, records, registry)
        print("Built build/catalog.json and build/catalog.md.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
