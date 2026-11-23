# Task 3: Automated File Organizer & Cleanup Utility

## Overview & Goal
Automate filesystem operations and directory sorting using Python OS libraries (`os`, `shutil`, `pathlib`). The utility autonomously organizes cluttered directories into intuitive category subfolders while safeguarding against naming collisions and file locks.

## Features
- **Dynamic Category Mapping**:
  - `/Documents`: `.pdf`, `.docx`, `.txt`, `.xlsx`, `.csv`, `.md`, `.pptx`
  - `/Images`: `.jpg`, `.jpeg`, `.png`, `.gif`, `.svg`, `.webp`
  - `/Videos`: `.mp4`, `.mkv`, `.mov`, `.avi`, `.webm`
  - `/Audio`: `.mp3`, `.wav`, `.aac`, `.flac`, `.ogg`
  - `/Archives`: `.zip`, `.tar`, `.gz`, `.rar`, `.7z`
  - `/Code`: `.py`, `.js`, `.ts`, `.html`, `.css`, `.json`, `.sql`, `.sh`
  - `/Executables`: `.exe`, `.msi`, `.dmg`, `.pkg`
  - `/Other`: Unmapped file extensions
- **Collision Resolution Engine**: Automatically resolves destination filename collisions by appending sequential numbering (e.g. `report.pdf` -> `report_1.pdf`) without overwriting existing data.
- **Dry-Run Preview**: Preview proposed file transfers without committing writes to disk.
- **Exception Protection**: Handles `PermissionError` and OS-level file locking gracefully with clear logging output.
- **Audit Summary**: Displays total files scanned, relocated, collisions resolved, and category breakdown.

## File Manifest
- `organizer.py`: Core reorganization script and CLI entrypoint.
- `demo_run.py`: Isolated sandbox test suite validating file sorting and collision renaming.

## How to Run
```bash
# Preview organization without moving files
python task3_file_organizer/organizer.py path/to/target/folder --dry-run

# Execute organization
python task3_file_organizer/organizer.py path/to/target/folder

# Run automated validation demo
python task3_file_organizer/demo_run.py
```
