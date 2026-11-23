"""
Task 3: Automated File Organizer & Cleanup Utility
Author: Seebiraj V (Datheon Python Programming Internship)
Track: Python & AI Applications

Features:
- Inspects file extensions across cluttered directories (Downloads, Desktop, etc.).
- Dynamically provisions category folders (/Documents, /Images, /Videos, /Audio, /Archives, /Code, /Executables, /Other).
- Implements collision-safe renaming (e.g., invoice.pdf -> invoice_1.pdf) when filenames collide.
- Graceful exception handling for PermissionError, FileExistsError, and OS-level locking.
- Dry-run capability to preview organizational operations before executing.
- Execution summary report with category distribution and relocation statistics.
"""

import argparse
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Comprehensive Extension Mapping Taxonomy
CATEGORY_MAP: Dict[str, str] = {
    # Images
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".bmp": "Images",
    ".svg": "Images",
    ".webp": "Images",
    ".ico": "Images",
    # Documents
    ".pdf": "Documents",
    ".docx": "Documents",
    ".doc": "Documents",
    ".txt": "Documents",
    ".rtf": "Documents",
    ".pptx": "Documents",
    ".ppt": "Documents",
    ".xlsx": "Documents",
    ".xls": "Documents",
    ".csv": "Documents",
    ".odt": "Documents",
    ".md": "Documents",
    # Videos
    ".mp4": "Videos",
    ".mkv": "Videos",
    ".mov": "Videos",
    ".avi": "Videos",
    ".wmv": "Videos",
    ".flv": "Videos",
    ".webm": "Videos",
    # Audio
    ".mp3": "Audio",
    ".wav": "Audio",
    ".aac": "Audio",
    ".flac": "Audio",
    ".ogg": "Audio",
    ".m4a": "Audio",
    # Archives
    ".zip": "Archives",
    ".tar": "Archives",
    ".gz": "Archives",
    ".bz2": "Archives",
    ".rar": "Archives",
    ".7z": "Archives",
    # Code & Development
    ".py": "Code",
    ".js": "Code",
    ".ts": "Code",
    ".html": "Code",
    ".css": "Code",
    ".json": "Code",
    ".xml": "Code",
    ".yaml": "Code",
    ".yml": "Code",
    ".sql": "Code",
    ".sh": "Code",
    ".ps1": "Code",
    ".cpp": "Code",
    ".c": "Code",
    ".java": "Code",
    # Executables & Installers
    ".exe": "Executables",
    ".msi": "Executables",
    ".dmg": "Executables",
    ".pkg": "Executables",
    ".apk": "Executables",
}

DEFAULT_CATEGORY = "Other"


class FileOrganizer:
    """Autonomous filesystem reorganization engine."""

    def __init__(self, target_directory: Path, dry_run: bool = False):
        self.target_dir = Path(target_directory).resolve()
        self.dry_run = dry_run
        self.stats = {
            "scanned": 0,
            "relocated": 0,
            "skipped": 0,
            "collisions_resolved": 0,
            "errors": 0,
            "category_counts": {}
        }
        self.relocation_log: List[Tuple[str, str]] = []

    def get_category_for_file(self, file_path: Path) -> str:
        """Determines target category folder based on extension."""
        ext = file_path.suffix.lower()
        return CATEGORY_MAP.get(ext, DEFAULT_CATEGORY)

    def resolve_destination_collision(self, dest_folder: Path, filename: str) -> Path:
        """
        Generates a non-colliding destination path if filename already exists.
        Example: data.csv -> data_1.csv -> data_2.csv
        """
        candidate = dest_folder / filename
        if not candidate.exists():
            return candidate

        stem = candidate.stem
        suffix = candidate.suffix
        counter = 1

        while True:
            new_candidate = dest_folder / f"{stem}_{counter}{suffix}"
            if not new_candidate.exists():
                self.stats["collisions_resolved"] += 1
                return new_candidate
            counter += 1

    def organize(self) -> dict:
        """Executes the file organization pipeline across the target directory."""
        if not self.target_dir.exists() or not self.target_dir.is_dir():
            raise FileNotFoundError(f"Target directory '{self.target_dir}' does not exist or is not a directory.")

        # Identify category folder names to avoid self-reorganizing category directories
        category_folder_names = set(CATEGORY_MAP.values()) | {DEFAULT_CATEGORY}

        # Scan files using os.scandir for high performance
        with os.scandir(self.target_dir) as entries:
            for entry in entries:
                # Skip subdirectories (including existing category folders)
                if entry.is_dir():
                    continue

                self.stats["scanned"] += 1
                source_path = Path(entry.path)
                category = self.get_category_for_file(source_path)
                category_dir = self.target_dir / category

                target_path = self.resolve_destination_collision(category_dir, source_path.name)

                # Skip if already in place
                if source_path == target_path:
                    self.stats["skipped"] += 1
                    continue

                try:
                    if not self.dry_run:
                        # Ensure category folder exists
                        category_dir.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(source_path), str(target_path))

                    self.stats["relocated"] += 1
                    self.stats["category_counts"][category] = self.stats["category_counts"].get(category, 0) + 1
                    self.relocation_log.append((str(source_path), str(target_path)))

                except PermissionError as pe:
                    self.stats["errors"] += 1
                    print(f"⚠️ Permission Denied: Could not move '{source_path.name}'. File may be locked by another process.")
                except Exception as e:
                    self.stats["errors"] += 1
                    print(f"❌ Error moving '{source_path.name}': {e}")

        return self.stats

    def format_summary(self) -> str:
        """Returns a formatted execution audit report."""
        lines = []
        mode = "[DRY-RUN PREVIEW]" if self.dry_run else "[LIVE EXECUTION]"
        lines.append("=" * 70)
        lines.append(f"     🗂️ DATHEON AUTOMATED FILE ORGANIZER SUMMARY {mode}")
        lines.append("=" * 70)
        lines.append(f"Target Directory     : {self.target_dir}")
        lines.append(f"Total Files Scanned  : {self.stats['scanned']}")
        lines.append(f"Files Relocated      : {self.stats['relocated']}")
        lines.append(f"Collisions Resolved  : {self.stats['collisions_resolved']}")
        lines.append(f"Files Skipped        : {self.stats['skipped']}")
        lines.append(f"Encountered Errors   : {self.stats['errors']}")
        lines.append("-" * 70)
        lines.append("Category Breakdown:")
        if self.stats["category_counts"]:
            for cat, count in sorted(self.stats["category_counts"].items()):
                lines.append(f"  📁 /{cat:<15} : {count:>4} file(s)")
        else:
            lines.append("  (No files organized)")
        lines.append("=" * 70)
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Datheon File Organizer & Cleanup Utility")
    parser.add_argument("directory", nargs="?", default=".", help="Target directory to organize (default: current directory)")
    parser.add_argument("--dry-run", action="store_true", help="Preview relocations without physically moving files")
    args = parser.parse_args()

    target_path = Path(args.directory).resolve()
    print(f"\n🚀 Initializing file organization on: {target_path}")
    if args.dry_run:
        print("💡 Dry-run mode enabled: No files will be modified.")

    organizer = FileOrganizer(target_path, dry_run=args.dry_run)
    organizer.organize()
    print("\n" + organizer.format_summary())


if __name__ == "__main__":
    main()
