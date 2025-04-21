#!/usr/bin/env python3
import os
import glob
from pathlib import Path
import re

def main():
    # Create autocombined directory if it doesn't exist
    os.makedirs("autocombined", exist_ok=True)
    
    # Get all markdown files from by-use-case and to-format directories
    use_case_format_files = []
    use_case_format_files.extend(glob.glob("by-use-case/**/*.md", recursive=True))
    use_case_format_files.extend(glob.glob("to-format/**/*.md", recursive=True))
    
    # Get all markdown files from to-style directory
    style_files = glob.glob("to-style/*.md")
    
    # Counter for generated files
    count = 0
    
    # Process each combination
    for use_case_format_file in use_case_format_files:
        # Get the base name without extension
        use_case_format_name = os.path.splitext(os.path.basename(use_case_format_file))[0]
        
        # Read the content of the use-case/format file
        with open(use_case_format_file, 'r', encoding='utf-8') as f:
            use_case_format_content = f.read()
        
        for style_file in style_files:
            # Get the base name without extension
            style_name = os.path.splitext(os.path.basename(style_file))[0]
            
            # Read the content of the style file
            with open(style_file, 'r', encoding='utf-8') as f:
                style_content = f.read().strip()
            
            # Remove the first line from the style content
            style_lines = style_content.split('\n')
            if len(style_lines) > 0:
                # Remove the first line (which typically contains "Reformat the following text...")
                style_lines = style_lines[1:]
                # Join the remaining lines
                style_content = '\n'.join(style_lines).strip()
            
            # Add the prefix to the style content
            processed_style_content = f"Apply the following style:\n{style_content}"
            
            # Create the combined content
            combined_content = f"{use_case_format_content}\n\n{processed_style_content}"
            
            # Create the output file name
            output_file_name = f"{use_case_format_name}_{style_name}.md"
            output_path = os.path.join("autocombined", output_file_name)
            
            # Write the combined content to the output file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(combined_content)
            
            count += 1
    
    print(f"Generated {count} combined prompt files in the 'autocombined' directory.")

if __name__ == "__main__":
    main()