"""
Script to convert a .docx file to a plain text file.
Usage: python docx_to_txt.py <input_dir> <output_dir>
"""

import sys
import os
from docx import Document

def excepthook(type, value, tb):
    import traceback, pdb
    traceback.print_exception (type, value, tb)
    print
    pdb.pm ()


def docx_to_txt(input_dir):
    """
    Read all .docx files from a directory and export their content to .txt files.
    
    Args:
        input_dir (str): Directory containing the input .docx files
    """

    output_dir = input_dir + "_txt"     # Directory where the output .txt files will be saved
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Find all .docx files in the input directory and subfolders (recursive)
    docx_files = []
    for root, dirs, files in os.walk(input_dir):
        for f in files:
            if f.endswith('.docx'):
                docx_files.append(os.path.join(root, f))
    
    print(f"Found {len(docx_files)} .docx file(s) to convert...")
    
    # Process each .docx file
    for docx_path in docx_files:
        docx_file = os.path.basename(docx_path)
        txt_file = os.path.splitext(docx_file)[0] + '.txt'
        
        txt_path = os.path.join(output_dir, txt_file)
        
        # Load the .docx file
        doc = Document(docx_path)
        
        # Extract text from all paragraphs
        full_text = []
        for paragraph in doc.paragraphs:
            full_text.append(paragraph.text)
        
        # Join paragraphs with newlines
        content = '\n'.join(full_text)
        
        # Write to text file
        with open(txt_path, 'w', encoding='utf-8') as txt_file_obj:
            txt_file_obj.write(content)
    
    print(f"\nSuccessfully converted {len(docx_files)} file(s)")


if __name__ == "__main__":
    sys.excepthook = excepthook

    input_directory = r"C:\Dev_TTT\DTech-20251226T145049Z-3-001\DTech"
    docx_to_txt(input_directory)

# import pdb; pdb.set_trace()
