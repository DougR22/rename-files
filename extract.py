"""
Part 1 of 2: this program: extract PDF filenames from the current directory to extract_filenames.txt.

Note that part 2 is replace.py which replaces filenames using mappings from the ouptut of this app (extract_filenames.txt) and replace_filenames.txt
"""

import os
import re

# Directory containing files to process
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

def extract_filenames():
    """
    Extract all filenames in current directory that end in .pdf and save them to a file named "extract_filenames.txt". 
    Each line in the output file will contain the filename.
    """
    try:
        # List all files in the directory
        files = os.listdir(DIRECTORY)

        extracted_data = []

        for filename in files:
            if filename.endswith('.pdf'):
                extracted_data.append({
                    'filename': filename,
                    'extracted': filename
                })
                print(f"Extracted: {filename}\n")
        
        # Save results to a file
        output_file = os.path.join(DIRECTORY, "extract_filenames.txt")
        with open(output_file, 'w') as f:
            for item in extracted_data:
                f.write(f"{item['extracted']}\n")
        
        print(f"\nTotal files processed: {len(extracted_data)}")
        print(f"Results saved to: {output_file}")
    
    except FileNotFoundError:
        print(f"Error: Directory not found: {DIRECTORY}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    extract_filenames()
