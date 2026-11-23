"""
Demonstration runner for Task 3: Automated File Organizer & Cleanup Utility.
Constructs a temporary cluttered sandbox, creates mock files across various extensions,
tests collision resolution, and validates proper sorting into category subfolders.
"""

import shutil
import tempfile
from pathlib import Path
from organizer import FileOrganizer, CATEGORY_MAP


def run_organizer_demo():
    print("\n--- Running Automated File Organizer Sandbox Demo ---")
    temp_dir = Path(tempfile.mkdtemp(prefix="datheon_clutter_"))
    try:
        # Create test mock files
        test_files = [
            "quarterly_report.pdf",
            "vacation_photo.jpg",
            "screenshot.png",
            "financial_model.xlsx",
            "dataset_extract.csv",
            "project_backup.zip",
            "background_track.mp3",
            "demo_walkthrough.mp4",
            "pipeline_script.py",
            "setup_installer.exe",
            "notes.txt",
            "unknown_archive.bin"
        ]

        for fname in test_files:
            file_path = temp_dir / fname
            file_path.write_text(f"Mock content for {fname}", encoding="utf-8")

        # Also create a pre-existing destination file to test collision resolution!
        docs_dir = temp_dir / "Documents"
        docs_dir.mkdir(parents=True, exist_ok=True)
        colliding_file = docs_dir / "quarterly_report.pdf"
        colliding_file.write_text("Existing document in target folder", encoding="utf-8")

        print(f"Created {len(test_files)} mock files in sandbox directory:\n  {temp_dir}")

        # Execute organization
        organizer = FileOrganizer(temp_dir, dry_run=False)
        stats = organizer.organize()

        # Print audit report
        print("\n" + organizer.format_summary())

        # Assertions
        assert stats["relocated"] == len(test_files), f"Expected {len(test_files)} relocations, got {stats['relocated']}"
        assert stats["collisions_resolved"] == 1, f"Expected 1 collision resolved, got {stats['collisions_resolved']}"

        # Verify destination files
        assert (docs_dir / "quarterly_report.pdf").exists()
        assert (docs_dir / "quarterly_report_1.pdf").exists()  # collision renamed!
        assert (temp_dir / "Images" / "vacation_photo.jpg").exists()
        assert (temp_dir / "Code" / "pipeline_script.py").exists()
        assert (temp_dir / "Archives" / "project_backup.zip").exists()
        assert (temp_dir / "Videos" / "demo_walkthrough.mp4").exists()
        assert (temp_dir / "Audio" / "background_track.mp3").exists()

        print("\nAll category directories, file relocations, and collision-safe renames verified successfully!")

    finally:
        # Cleanup temporary sandbox
        shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    run_organizer_demo()
