"""
Unit tests for Task 3: Automated File Organizer & Cleanup Utility.
"""

import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "task3_file_organizer"))

from organizer import FileOrganizer, CATEGORY_MAP


def test_category_mapping():
    assert CATEGORY_MAP[".pdf"] == "Documents"
    assert CATEGORY_MAP[".jpg"] == "Images"
    assert CATEGORY_MAP[".mp4"] == "Videos"
    assert CATEGORY_MAP[".zip"] == "Archives"
    assert CATEGORY_MAP[".py"] == "Code"
    assert CATEGORY_MAP[".exe"] == "Executables"


def test_file_organization_and_sorting(tmp_path):
    # Setup mock files
    (tmp_path / "document.pdf").write_text("dummy", encoding="utf-8")
    (tmp_path / "picture.png").write_text("dummy", encoding="utf-8")
    (tmp_path / "source.py").write_text("dummy", encoding="utf-8")
    (tmp_path / "archive.zip").write_text("dummy", encoding="utf-8")

    organizer = FileOrganizer(tmp_path, dry_run=False)
    stats = organizer.organize()

    assert stats["scanned"] == 4
    assert stats["relocated"] == 4
    assert stats["errors"] == 0

    assert (tmp_path / "Documents" / "document.pdf").exists()
    assert (tmp_path / "Images" / "picture.png").exists()
    assert (tmp_path / "Code" / "source.py").exists()
    assert (tmp_path / "Archives" / "archive.zip").exists()


def test_collision_resolution(tmp_path):
    dest_dir = tmp_path / "Documents"
    dest_dir.mkdir()
    (dest_dir / "report.pdf").write_text("existing", encoding="utf-8")

    (tmp_path / "report.pdf").write_text("new incoming file", encoding="utf-8")

    organizer = FileOrganizer(tmp_path, dry_run=False)
    stats = organizer.organize()

    assert stats["collisions_resolved"] == 1
    assert (dest_dir / "report.pdf").exists()
    assert (dest_dir / "report_1.pdf").exists()
    assert (dest_dir / "report.pdf").read_text(encoding="utf-8") == "existing"
    assert (dest_dir / "report_1.pdf").read_text(encoding="utf-8") == "new incoming file"


def test_dry_run_mode(tmp_path):
    test_file = tmp_path / "sample.pdf"
    test_file.write_text("preview", encoding="utf-8")

    organizer = FileOrganizer(tmp_path, dry_run=True)
    stats = organizer.organize()

    assert stats["relocated"] == 1
    # In dry run, file must remain in original location and no category dir created
    assert test_file.exists()
    assert not (tmp_path / "Documents" / "sample.pdf").exists()
