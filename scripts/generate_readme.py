#!/usr/bin/env python3
import os
from pathlib import Path

def get_markdown_files(directory, exclude=None):
    if exclude is None:
        exclude = []
    markdown_files = []
    for file_path in Path(directory).glob('**/*.md'):
        if file_path.name not in exclude and not any(part.startswith('.') for part in file_path.parts):
            markdown_files.append(file_path)
    return sorted(markdown_files)

def generate_readme():
    # Get all markdown files from src directory (excluding README.md and hidden directories)
    lib_files = get_markdown_files('src', ['README.md'])
    
    # Sort files alphabetically
    lib_files.sort(key=lambda x: str(x).lower())
    
    # Generate README content
    content = [
        "# 🚀 SilverBullet Libraries",
        "\nA curated collection of plugins, templates, and utilities for [SilverBullet](https://silverbullet.md/).\n",
        "## 📦 Available Libraries",
        ""
    ]
    
    # Add all library files in a single list
    for file in lib_files:
        rel_path = file.relative_to('./src')
        
        # Skip template files in the listing
        if 'template' in str(rel_path).lower():
            continue
            
        # Format the display name (convert kebab-case to Title Case)
        display_name = ' '.join(word.capitalize() for word in rel_path.stem.split('-'))
        content.append(f"- [{display_name}](https://github.com/malys/silverbullet-libraries/blob/main/src/{rel_path.as_posix().replace('\\', '/')})")
    

    # Add usage instructions
    content.extend([
        "\n## 🛠️ Installation",
        "1. Browse the libraries above and find one you'd like to use\n"
        "2. Click on the library to view its contents\n"
        "3. Copy the file URL (e.g., `https://github.com/malys/silverbullet-libraries/blob/main/src/example.md`)\n"
        "4. In SilverBullet, run the `Import: URL` command\n"
        "5. Paste the URL and select `Github: Repo file` as the source\n"
        "6. Run `System: Reload` to activate the library\n",
        "## 🤝 Contributing",
        "We welcome contributions! Here's how you can help:",
        "- Add new libraries or improve existing ones",
        "- Fix bugs or improve documentation",
        "- Suggest new features or report issues\n",
        "To contribute:",
        "1. Fork this repository",
        "2. Create a new branch for your changes",
        "3. Submit a pull request\n",
        "## 📜 License",
        "This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details."
    ])
    
    # Write to README.md
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))

if __name__ == "__main__":
    generate_readme()
