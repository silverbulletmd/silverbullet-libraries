#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

def run_command(cmd, cwd=None):
    """Helper function to run shell commands"""
    import subprocess
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            shell=True,
            check=True,
            text=True,
            capture_output=True
        )
        return (True, result.stdout.strip())
    except subprocess.CalledProcessError as e:
        return (False, f"Error: {e.stderr.strip()}")

def sync_custom_libraries():
    # Base directories
    current_dir = Path('.').resolve()
    source_dir = current_dir.parent / 'silverbullet_backup' / 'z-custom'
    src_dir = current_dir / 'src'
    
    if not source_dir.exists():
        print(f"Error: Source directory not found: {source_dir}")
        return False
        
    # Update source repository
    print("Updating source repository...")
    success, output = run_command("git pull", cwd=source_dir)
    if not success:
        print(f"Warning: Failed to update source repository: {output}")
    else:
        print("Source repository updated successfully")
    

    # Remove src folder
    print("\nRemoving src/ folder...")
    try:
        shutil.rmtree(src_dir)
        print("src/ folder removed successfully")
    except FileNotFoundError:
        print(f"src/ folder not found")
    except Exception as e:
        print(f"Error removing src/ folder: {e}")
   
    # Create src directory if it doesn't exist
    src_dir = current_dir / 'src'
    src_dir.mkdir(exist_ok=True)
    
    # First, collect all files to copy (excluding test files and Templates folder)
    print("\nScanning for files to copy...")
    files_to_copy = []
    for src_file in source_dir.rglob('*.md'):
        # Skip test files, Templates, and import folders
        skip_patterns = ['test', 'Templates', 'import']
        if any(pattern.lower() in str(src_file).lower() for pattern in skip_patterns):
            print(f"Skipping: {src_file.relative_to(source_dir)}")
            continue
        files_to_copy.append(src_file)
    
    if not files_to_copy:
        print("No files to copy after filtering.")
        return True
        
    # Now copy the files
    print(f"\nCopying {len(files_to_copy)} files to src/...")
    for src_file in files_to_copy:
        try:
            # Get the relative path and create destination path in src/
            rel_path = src_file.relative_to(source_dir)
            dest_file = src_dir / rel_path
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy file
            shutil.copy2(src_file, dest_file)
            print(f"Copied to src/: {rel_path}")
        except Exception as e:
            print(f"Error copying {src_file}: {e}")
    
    print("\nSync completed!")
    return True

if __name__ == "__main__":
    sync_custom_libraries()
