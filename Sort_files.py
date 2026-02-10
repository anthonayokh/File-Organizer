import os
import shutil
from pathlib import Path

def organize_downloads():
    # Define source and destination directories
    downloads_path = Path.home() / "Downloads"
    
    # Define destination folders
    folders = {
        "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".xlsx", ".xls", ".ppt", ".pptx"],
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".tiff"],
        "Programs": [".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm", ".app"],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
        "Videos": [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv"],
        "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"],
        "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".json", ".xml"],
        "Others": []  # For uncategorized files
    }
    
    # Create destination folders if they don't exist
    for folder in folders:
        folder_path = downloads_path / folder
        folder_path.mkdir(exist_ok=True)
    
    # Track organized files
    organized_count = {folder: 0 for folder in folders}
    
    # Organize files
    for item in downloads_path.iterdir():
        # Skip directories and hidden files
        if item.is_dir() and item.name in folders:
            continue
        if item.name.startswith('.'):
            continue
        
        # Get file extension
        file_extension = item.suffix.lower()
        
        # Find appropriate category
        moved = False
        for category, extensions in folders.items():
            if file_extension in extensions:
                # Handle duplicate file names
                dest_path = downloads_path / category / item.name
                counter = 1
                while dest_path.exists():
                    stem = item.stem
                    if f"({counter-1})" in stem:
                        stem = stem.replace(f"({counter-1})", "")
                    new_name = f"{stem}({counter}){item.suffix}"
                    dest_path = downloads_path / category / new_name
                    counter += 1
                
                # Move the file
                try:
                    shutil.move(str(item), str(dest_path))
                    organized_count[category] += 1
                    moved = True
                    break
                except Exception as e:
                    print(f"Error moving {item.name}: {e}")
        
        # If file doesn't match any category, move to "Others"
        if not moved and item.is_file():
            dest_path = downloads_path / "Others" / item.name
            counter = 1
            while dest_path.exists():
                stem = item.stem
                if f"({counter-1})" in stem:
                    stem = stem.replace(f"({counter-1})", "")
                new_name = f"{stem}({counter}){item.suffix}"
                dest_path = downloads_path / "Others" / new_name
                counter += 1
            
            try:
                shutil.move(str(item), str(dest_path))
                organized_count["Others"] += 1
            except Exception as e:
                print(f"Error moving {item.name}: {e}")
    
    # Print summary
    print("\n" + "="*50)
    print("FILE ORGANIZATION COMPLETE")
    print("="*50)
    
    total_moved = 0
    for category, count in organized_count.items():
        if count > 0:
            print(f"{category}: {count} file(s)")
            total_moved += count
    
    print(f"\nTotal files organized: {total_moved}")
    print(f"Source: {downloads_path}")

def main():
    print("Starting Downloads folder organization...")
    print("This will organize files into categorized folders.")
    print("Original files will be moved, not copied.\n")
    
    response = input("Do you want to proceed? (y/n): ").lower()
    
    if response == 'y':
        organize_downloads()
        print("\nOrganization complete!")
    else:
        print("Operation cancelled.")

if __name__ == "__main__":
    main()
