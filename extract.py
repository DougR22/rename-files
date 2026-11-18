"""
This program is part 1 of 2

This program extracts PDF filenames from the current directory into extract_filenames.txt, feed this into ChatGPT to get better filenames.

Part 2 is replace.py -- which replaces filenames using mappings from the output of this program (extract_filenames.txt) plus another file replace_filenames.txt

This program was created by Claude Haiku 4.5 in VSCode.
Pylance warnings fixed by GPT-6.2 Sol (medium effort mode).
"""

import os
import argparse

# Directory containing files to process
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
EXTRACT_FILE = "extract_filenames.txt"

def extract_filenames(ext: str = 'pdf'):
    """
    Extract all filenames in current directory that end in .pdf (or other given extension, such as "epub") 
    Save list of filenames to file named "extract_filenames.txt".
    """
    try:
        # List all files in the directory
        files = os.listdir(DIRECTORY)

        extracted_data: list[dict[str, str]] = []

        for filename in files:
            if filename.endswith(f'.{ext}'):
                extracted_data.append({
                    'filename': filename,
                    'extracted': filename
                })
                print(f"Extracted: {filename}\n")
        
        # Save results to a file
        output_file = os.path.join(DIRECTORY, EXTRACT_FILE)
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
    parser = argparse.ArgumentParser(description='Extract filenames by extension')
    parser.add_argument('--ext', default='pdf', help='File extension to extract (default: pdf)')
    args = parser.parse_args()
    extract_filenames(ext=args.ext)
