"""Exercise content validation and build behavior in isolated repositories."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest
import yaml

from kb import cli


SCHEMAS = Path(__file__).resolve().parents[1] / "schemas"


def metadata(**changes):
    value = {
        "id": "overview.index",
        "title": "Overview",
        "type": "index",
        "domain": "overview",
        "status": "draft",
        "platforms": ["generic"],
        "source_refs": [],
        "updated_at": "2026-09-29",
    }
    return {**value, **changes}


def write_document(root, relative="knowledge/00-overview/index.md", *, meta=None, body=""):
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "---\n" + yaml.safe_dump(meta if meta is not None else metadata())
        + "---\n\n# Content\n\n" + body,
        encoding="utf-8",
    )
    return path


def source(source_id="src.example.docs"):
    return {
        "id": source_id,
        "title": "Example documentation",
        "url": "https://example.org/docs",
        "kind": "documentation",
        "registered_at": "2026-09-29",
        "license": {"status": "unknown", "notes": "Not inspected.", "scopes": []},
        "notes": "Test source; no external requests are required.",
    }


def write_registry(root, sources):
    (root / "sources/registry.yaml").write_text(
        yaml.safe_dump({"schema_version": 1, "sources": sources}), encoding="utf-8"
    )


@pytest.fixture
def repository(tmp_path):
    shutil.copytree(SCHEMAS, tmp_path / "schemas")
    (tmp_path / "config").mkdir()
    (tmp_path / "sources").mkdir()
    (tmp_path / "config/taxonomy.yaml").write_text(
        "schema_version: 1\ndomains:\n"
        "  - id: overview\n    directory: 00-overview\n",
        encoding="utf-8",
    )
    write_registry(tmp_path, [])
    write_document(tmp_path)
    return tmp_path


def errors_for(root):
    return "\n".join(cli.collect(root)[1])


@pytest.mark.parametrize(
    ("text", "message"),
    [
        ("# Missing metadata\n", "missing YAML front matter"),
        ("", "missing YAML front matter"),
        ("---\nid: overview.index\n", "unclosed YAML front matter"),
        ("---\nid: overview.index\nid: other.index\n---\n", "unique string"),
        ("---\n7: unexpected\n---\n", "unique string"),
        ("---\nplatforms: [\n---\n", "expected"),
    ],
)
def test_frontmatter_failures_are_reported(repository, text, message):
    (repository / "knowledge/00-overview/index.md").write_text(text, encoding="utf-8")
    assert message in errors_for(repository)


@pytest.mark.parametrize(
    ("changes", "message"),
    [
        ({"updated_at": "2026-02-30"}, "updated_at"),
        ({"platforms": ["unregistered-device"]}, "platforms"),
        ({"domain": "unknown-domain"}, "domain"),
        ({"domain": "hardware"}, "domain does not match"),
        ({"source_refs": ["src.unknown.docs"]}, "unknown source ID"),
        ({"related_ids": ["unknown.content"]}, "unknown related ID"),
        ({"applicability": {"environment_refs": ["unknown.environment"], "notes": "Unknown."}},
         "unknown environment_refs ID"),
        ({"verification": {"status": "source_checked", "evidence_refs": ["unknown.evidence"],
                           "notes": "Unknown."}}, "unknown evidence_refs ID"),
    ],
)
def test_invalid_metadata_and_references(repository, changes, message):
    write_document(repository, meta=metadata(**changes))
    assert message in errors_for(repository)


def test_duplicate_content_and_source_ids(repository):
    write_document(repository, "knowledge/00-overview/duplicate.md")
    item = source()
    write_registry(repository, [item, item])
    issues = errors_for(repository)
    assert "duplicate content IDs" in issues
    assert "duplicate source IDs" in issues


def test_valid_source_related_and_path_references(repository):
    write_registry(repository, [source()])
    write_document(repository, meta=metadata(source_refs=["src.example.docs"]))
    write_document(
        repository, "paths/platforms/example.md",
        meta=metadata(id="path.example", type="path", related_ids=["overview.index"]),
        body="[Overview](../../knowledge/00-overview/index.md)",
    )
    records, errors, _ = cli.collect(repository)
    assert errors == []
    assert [record["id"] for record in records] == ["overview.index", "path.example"]


@pytest.mark.parametrize("kind", ["procedure", "case", "experiment"])
def test_operational_content_requires_applicability_and_verification(repository, kind):
    write_document(repository, meta=metadata(type=kind))
    issues = errors_for(repository)
    assert "applicability" in issues
    assert "verification" in issues


def test_reproduced_claim_requires_evidence(repository):
    write_document(repository, meta=metadata(
        type="procedure",
        applicability={"environment_refs": [], "notes": "Scope to be established."},
        verification={"status": "reproduced", "evidence_refs": [], "notes": "No evidence."},
    ))
    assert "evidence_refs" in errors_for(repository)


def test_unverified_procedure_can_be_recorded_as_draft(repository):
    write_document(repository, meta=metadata(
        type="procedure",
        applicability={"environment_refs": [], "notes": "Scope to be established."},
        verification={"status": "not_verified", "evidence_refs": [], "notes": "Not run."},
    ))
    assert errors_for(repository) == ""


def test_directory_rules_and_missing_chapter_index(repository):
    (repository / "knowledge/00-overview/index.md").unlink()
    write_document(repository, "knowledge/99-unknown/item.md", meta=metadata(id="unknown.item"))
    write_document(repository, "paths/example.md", meta=metadata(id="path.example"))
    issues = errors_for(repository)
    assert "required chapter index missing" in issues
    assert "domain does not match chapter directory" in issues
    assert "paths/ entries must have type: path" in issues


@pytest.mark.parametrize(
    ("relative", "contents", "message"),
    [
        ("schemas/content.schema.json", "{broken-json", "configuration:"),
        ("schemas/sources.schema.json", None, "configuration:"),
        ("sources/registry.yaml", "sources: [", "configuration:"),
        ("sources/registry.yaml", "{}\n", "sources/registry.yaml"),
        ("config/taxonomy.yaml", "domains: null\n", "configuration:"),
    ],
)
def test_unreadable_or_invalid_configuration(repository, relative, contents, message):
    path = repository / relative
    if contents is None:
        path.unlink()
    else:
        path.write_text(contents, encoding="utf-8")
    records, errors, _ = cli.collect(repository)
    assert records == []
    assert message in "\n".join(errors)


def test_links_ignore_remote_fragment_and_code_examples(repository):
    (repository / "docs").mkdir()
    (repository / "docs/reference notes.md").write_text("# Notes\n", encoding="utf-8")
    write_document(repository, body="""
[Remote](https://example.org/not-fetched)
[Protocol relative](//example.org/not-fetched)
[Email](mailto:test@example.org)
[Fragment](#not-checked)
[Local](../../docs/reference%20notes.md#heading)
[Local angle link](<../../docs/reference notes.md>)
`[Inline example](does-not-exist.md)`
```markdown
[Example](missing-in-example.md)
~~~
[Still inside original fence](also-missing.md)
```
~~~markdown
[Tilde example](missing-too.md)
~~~
""")
    assert errors_for(repository) == ""


def test_dead_and_outside_repository_links_include_root_documents(repository):
    write_document(repository, body="[Missing](missing.md)\n![Missing image](missing.png)")
    (repository / "README.md").write_text("[Outside](../outside.md)", encoding="utf-8")
    issues = errors_for(repository)
    assert "missing.md" in issues
    assert "missing.png" in issues
    assert "README.md: missing or outside-repository link: ../outside.md" in issues


def test_check_and_build_are_deterministic(repository, capsys):
    write_registry(repository, [source()])
    write_document(repository, meta=metadata(title="A | [B]", source_refs=["src.example.docs"]))
    assert cli.main(["check", "--root", str(repository)]) == 0
    checked = capsys.readouterr()
    assert "PASS: 1 content entries; 1 sources." in checked.out
    assert checked.err == ""
    assert not (repository / "build").exists()

    assert cli.main(["build", "--root", str(repository)]) == 0
    first = {p.name: p.read_bytes() for p in (repository / "build").iterdir()}
    catalog = json.loads(first["catalog.json"])
    assert catalog["documents"][0]["id"] == "overview.index"
    assert len(catalog["documents"][0]["sha256"]) == 64
    assert len(catalog["input_sha256"]) == 4
    assert "A \\| \\[B\\]" in first["catalog.md"].decode()

    assert cli.main(["build", "--root", str(repository)]) == 0
    assert {p.name: p.read_bytes() for p in (repository / "build").iterdir()} == first
    assert "Built build/catalog.json and build/catalog.md." in capsys.readouterr().out


@pytest.mark.parametrize("command", ["check", "build"])
def test_failed_cli_does_not_produce_a_catalog(repository, capsys, command):
    write_document(repository, meta=metadata(source_refs=["src.unknown.docs"]))
    assert cli.main([command, "--root", str(repository)]) == 1
    captured = capsys.readouterr()
    assert "unknown source ID" in captured.err
    assert "FAILED:" in captured.err
    assert "PASS:" not in captured.out
    assert not (repository / "build/catalog.json").exists()
    assert not (repository / "build/catalog.md").exists()
