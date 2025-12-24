import os
from pathlib import Path

def combine_markdown_files(directory_path='.', output_file='combined_book.txt', separator='\n\n---\n\n'):
    """
    Combine multiple markdown files into a single text file.
    
    Args:
        directory_path: Path to directory containing .md files
        output_file: Name of the output file
        separator: Text to insert between chapters (default: horizontal rule with spacing)
    """
    md_files = sorted(Path(directory_path).glob('*.md'))
    
    if not md_files:
        print(f"No .md files found in {directory_path}")
        return
    
    print(f"Found {len(md_files)} markdown files:")
    for f in md_files:
        print(f"  - {f.name}")
    
    print(f"\nCombining into {output_file}...")
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for i, file_path in enumerate(md_files):
            # Read the content
            with open(file_path, 'r', encoding='utf-8') as infile:
                content = infile.read()
            
            # Write chapter header
            outfile.write(f"# {file_path.name}\n\n")
            
            # Write content
            outfile.write(content)
            
            # Add separator between chapters (but not after the last one)
            if i < len(md_files) - 1:
                outfile.write(separator)
    
    # Get file size
    file_size = os.path.getsize(output_file)
    file_size_kb = file_size / 1024
    
    print(f"\n✓ Successfully combined {len(md_files)} files")
    print(f"✓ Output file: {output_file}")
    print(f"✓ File size: {file_size_kb:.1f} KB")
    
    # Count total lines and words
    with open(output_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        words = sum(len(line.split()) for line in lines)
    
    print(f"✓ Total lines: {len(lines):,}")
    print(f"✓ Total words: {words:,}")

if __name__ == "__main__":
    # Configuration
    book_directory = './chapters'  # Change to your directory path
    output_filename = 'combined_book.txt'
    
    # You can customize the separator between chapters:
    # Option 1: Horizontal rule with spacing (default)
    chapter_separator = '\n\n---\n\n'
    
    # Option 2: Page break style
    # chapter_separator = '\n\n\n=== NEW CHAPTER ===\n\n\n'
    
    # Option 3: Simple spacing
    # chapter_separator = '\n\n\n\n'
    
    combine_markdown_files(book_directory, output_filename, chapter_separator)