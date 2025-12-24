import os
import re
from pathlib import Path

def count_words_in_markdown(file_path):
    """Count words in a markdown file, excluding code blocks and metadata."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove code blocks
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    content = re.sub(r'`[^`]+`', '', content)
    
    # Remove YAML front matter
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    
    # Remove markdown syntax but keep the text
    content = re.sub(r'#+\s', '', content)  # Headers
    content = re.sub(r'\*\*([^*]+)\*\*', r'\1', content)  # Bold
    content = re.sub(r'\*([^*]+)\*', r'\1', content)  # Italic
    content = re.sub(r'__([^_]+)__', r'\1', content)  # Bold
    content = re.sub(r'_([^_]+)_', r'\1', content)  # Italic
    content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)  # Links
    content = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', '', content)  # Images
    
    # Count words
    words = content.split()
    return len(words)

def estimate_pages(directory_path='./chapters', words_per_page=250):
    """
    Estimate total pages from markdown files in a directory.
    
    Args:
        directory_path: Path to directory containing .md files
        words_per_page: Average words per page (250 is standard for novels,
                       300-350 for technical books, 200-250 for large print)
    """
    md_files = sorted(Path(directory_path).glob('*.md'))
    
    if not md_files:
        print(f"No .md files found in {directory_path}")
        return
    
    total_words = 0
    chapter_stats = []
    
    print(f"Analyzing {len(md_files)} markdown files...\n")
    print(f"{'File':<40} {'Words':>10} {'Pages':>8}")
    print("-" * 60)
    
    for file_path in md_files:
        word_count = count_words_in_markdown(file_path)
        pages = word_count / words_per_page
        total_words += word_count
        chapter_stats.append((file_path.name, word_count, pages))
        print(f"{file_path.name:<40} {word_count:>10,} {pages:>8.1f}")
    
    total_pages = total_words / words_per_page
    
    print("-" * 60)
    print(f"{'TOTAL':<40} {total_words:>10,} {total_pages:>8.1f}")
    print(f"\nEstimated book length: {total_pages:.0f} pages")
    print(f"Total word count: {total_words:,} words")
    print(f"\nAssumptions: {words_per_page} words per page")
    print("\nNote: Typical page counts vary by format:")
    print("  - Novel (standard): 250 words/page")
    print("  - Technical book: 300-350 words/page")
    print("  - Large print: 200-250 words/page")

if __name__ == "__main__":
    # Change this to your directory path, or use '.' for current directory
    book_directory = './chapters'
    
    # Adjust words_per_page based on your book format
    estimate_pages(book_directory, words_per_page=250)