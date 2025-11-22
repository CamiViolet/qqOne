"""
Script to concatenate all .txt files in a directory into a single file.
Usage: python txt_to_1bf.py <input_dir>
"""

import sys
import os
from docx import Document

def excepthook(type, value, tb):
    import traceback, pdb
    traceback.print_exception (type, value, tb)
    print
    pdb.pm ()


def txt_to_1bf(input_dir):
    """
    Read all .txt files from a directory and concatenate them into a single file.
    
    Args:
        input_dir (str): Directory containing the input .txt files
    """
    # Check if input directory exists
    if not os.path.isdir(input_dir):
        print(f"Error: Input directory '{input_dir}' not found.")
        sys.exit(1)

    output_dir = input_dir.replace("_txt", "") + "_1bf"     # Directory where the output file will be saved
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Find all .txt files in the input directory (no recursion)
    txt_files = [f for f in os.listdir(input_dir) if f.endswith('.txt') and os.path.isfile(os.path.join(input_dir, f))]
    
    if not txt_files:
        print(f"No .txt files found in '{input_dir}'")
        sys.exit(0)
    
    print(f"Found {len(txt_files)} .txt file(s) to concatenate...")
    
    # Sort files for consistent ordering
    txt_files.sort()
    
    # Concatenate all text files
    all_content = []
    all_content.append(f"\nL'autore di queste note è Carlo.\n\n")
    for txt_file in txt_files:
        txt_path = os.path.join(input_dir, txt_file)
        
        # Read the .txt file
        with open(txt_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # Add filename separator before content
            all_content.append(f"\nFile: {txt_file}\n\n{content}")
        
        print(f"Read '{txt_file}'")
    
    # Join all content with double newlines between files
    concatenated_content = '\n\n'.join(all_content)
    
    # Create output filename based on input directory name
    dir_name = os.path.basename(input_dir.rstrip(os.sep)).replace("_txt", "")
    output_file = os.path.join(output_dir, f"{dir_name}.1bf.txt")
    
    # Write to single output file
    with open(output_file, 'w', encoding='utf-8') as output:
        output.write(concatenated_content)
    
    print(f"\nSuccessfully concatenated {len(txt_files)} file(s) into '{output_file}'")


if __name__ == "__main__":
    sys.excepthook = excepthook

    input_directory = r"C:\Dev_TTT\DTech-20251122T165535Z-1-001\DTech_txt"
    txt_to_1bf(input_directory)

# import pdb; pdb.set_trace()
