#!/usr/bin/env python3
import os
import re
import json
import subprocess
from pathlib import Path
import time

def find_markdown_files(base_dir):
    """Find all markdown files in the repository."""
    markdown_files = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.md') and file != 'index.md' and file != 'README.md':
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, base_dir)
                markdown_files.append(rel_path)
    
    # Sort alphabetically
    markdown_files.sort()
    return markdown_files

def extract_content(file_path, max_chars=1000):
    """Extract content from a markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Truncate content if it's too long
            if len(content) > max_chars:
                content = content[:max_chars] + "..."
            return content
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

def generate_description(file_path, content):
    """Generate a short description using Ollama with LLAMA 3.2."""
    prompt = f"""
    You are analyzing a text transformation prompt file named '{os.path.basename(file_path)}' located at '{file_path}'.
    
    Here's the content of the file:
    
    {content}
    
    Please provide a very concise one-line description (maximum 10-15 words) of what this text transformation prompt does.
    Focus only on the main purpose of the prompt. Be direct and specific.
    """
    
    try:
        # Call Ollama API
        result = subprocess.run(
            ["ollama", "run", "llama3.2", prompt],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Extract the description from the output
        description = result.stdout.strip()
        
        # Clean up the description (remove quotes, etc.)
        description = re.sub(r'^["\'`]|["\'`]$', '', description)
        description = re.sub(r'\n+', ' ', description)
        
        # Ensure it's not too long
        if len(description) > 100:
            description = description[:97] + "..."
            
        return description
    except subprocess.CalledProcessError as e:
        print(f"Error generating description for {file_path}: {e}")
        return "No description available"

def create_index(markdown_files, base_dir):
    """Create the index markdown file with a table of contents."""
    index_content = "# Text Transformation Prompts Index\n\n"
    index_content += "This is an automatically generated index of all text transformation prompts in this repository.\n\n"
    index_content += "| Prompt | Description |\n"
    index_content += "|--------|-------------|\n"
    
    total_files = len(markdown_files)
    
    for i, file_path in enumerate(markdown_files):
        print(f"Processing file {i+1}/{total_files}: {file_path}")
        
        full_path = os.path.join(base_dir, file_path)
        content = extract_content(full_path)
        
        # Generate description
        description = generate_description(file_path, content)
        
        # Create a link to the file
        file_name = os.path.basename(file_path)
        file_name_without_ext = os.path.splitext(file_name)[0]
        
        # Add to index
        index_content += f"| [{file_path}]({file_path}) | {description} |\n"
        
        # Sleep a bit to avoid overwhelming Ollama
        time.sleep(0.5)
    
    return index_content

def main():
    base_dir = os.getcwd()
    print(f"Searching for markdown files in {base_dir}")
    
    markdown_files = find_markdown_files(base_dir)
    print(f"Found {len(markdown_files)} markdown files")
    
    index_content = create_index(markdown_files, base_dir)
    
    # Write the index file
    with open("index.md", "w", encoding="utf-8") as f:
        f.write(index_content)
    
    print(f"Index generated successfully at {os.path.join(base_dir, 'index.md')}")

if __name__ == "__main__":
    main()