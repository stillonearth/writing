#!/usr/bin/env python3
"""
Convert a directory of markdown files into a PDF book with fiction formatting.
Each markdown file becomes a chapter starting on a new page.

Requirements:
    pip install markdown weasyprint

Usage:
    python md_to_pdf.py <input_directory> <output_pdf>
    python md_to_pdf.py ./chapters book.pdf
"""

import os
import sys
from pathlib import Path
import markdown
from weasyprint import HTML, CSS

# HTML template with fiction book styling
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page {{
            size: 5.5in 8.5in;  /* Standard fiction book size */
            margin: 0.75in 0.5in;
            
            @top-center {{
                content: string(book-title);
                font-family: 'Crimson Text', 'Georgia', serif;
                font-size: 10pt;
                font-style: italic;
            }}
            
            @bottom-center {{
                content: counter(page);
                font-family: 'Crimson Text', 'Georgia', serif;
                font-size: 10pt;
            }}
        }}
        
        @page :first {{
            @top-center {{ content: none; }}
            @bottom-center {{ content: none; }}
        }}
        
        body {{
            font-family: 'Crimson Text', 'Georgia', serif;
            font-size: 12pt;
            line-height: 1.6;
            text-align: justify;
            hyphens: auto;
            color: #222;
        }}
        
        h1 {{
            string-set: book-title content();
            page-break-before: always;
            text-align: center;
            font-size: 24pt;
            font-weight: normal;
            margin-top: 2in;
            margin-bottom: 1in;
            font-variant: small-caps;
            letter-spacing: 0.05em;
        }}
        
        h1:first-of-type {{
            page-break-before: avoid;
        }}
        
        h2 {{
            font-size: 14pt;
            font-weight: bold;
            margin-top: 1.5em;
            margin-bottom: 0.75em;
            page-break-after: avoid;
        }}
        
        p {{
            margin: 0;
            text-indent: 1.5em;
            orphans: 2;
            widows: 2;
        }}
        
        p:first-of-type,
        h1 + p,
        h2 + p {{
            text-indent: 0;
        }}
        
        p + p {{
            margin-top: 0;
        }}
        
        /* Scene breaks */
        hr {{
            border: none;
            text-align: center;
            margin: 2em 0;
        }}
        
        hr:after {{
            content: "* * *";
            letter-spacing: 1em;
        }}
        
        blockquote {{
            margin: 1em 2em;
            font-style: italic;
        }}
        
        em {{
            font-style: italic;
        }}
        
        strong {{
            font-weight: bold;
        }}
        
        code {{
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }}
        
        pre {{
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            white-space: pre-wrap;
            margin: 1em 0;
            padding: 0.5em;
            background: #f5f5f5;
        }}
    </style>
</head>
<body>
{content}
</body>
</html>
"""


def get_chapter_files(directory):
    """Get all markdown files sorted naturally."""
    path = Path(directory)
    md_files = list(path.glob("*.md")) + list(path.glob("*.markdown"))
    
    # Sort files naturally (e.g., ch1, ch2, ch10)
    def natural_sort_key(filepath):
        import re
        parts = re.split(r'(\d+)', filepath.stem)
        return [int(p) if p.isdigit() else p.lower() for p in parts]
    
    return sorted(md_files, key=natural_sort_key)


def markdown_to_html(md_files):
    """Convert markdown files to HTML chapters."""
    md = markdown.Markdown(extensions=[
        'extra',
        'nl2br',
        'sane_lists',
        'smarty'
    ])
    
    chapters_html = []
    
    for i, md_file in enumerate(md_files, 1):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Convert markdown to HTML
        html_content = md.convert(content)
        
        # If no h1 heading exists, add chapter title
        if '<h1>' not in html_content:
            chapter_title = md_file.stem.replace('_', ' ').replace('-', ' ').title()
            html_content = f'<h1>Chapter {i}: {chapter_title}</h1>\n{html_content}'
        
        chapters_html.append(html_content)
        md.reset()
    
    return '\n\n'.join(chapters_html)


def create_pdf(input_dir, output_pdf):
    """Create PDF book from markdown files."""
    print(f"📚 Converting markdown files from '{input_dir}' to PDF...")
    
    # Get all chapter files
    md_files = get_chapter_files(input_dir)
    
    if not md_files:
        print(f"❌ No markdown files found in '{input_dir}'")
        sys.exit(1)
    
    print(f"📖 Found {len(md_files)} chapters:")
    for f in md_files:
        print(f"   - {f.name}")
    
    # Convert to HTML
    print("\n🔄 Converting markdown to HTML...")
    content_html = markdown_to_html(md_files)
    
    # Create complete HTML
    full_html = HTML_TEMPLATE.format(content=content_html)
    
    # Generate PDF
    print("📄 Generating PDF...")
    HTML(string=full_html).write_pdf(output_pdf)
    
    print(f"✅ PDF book created successfully: {output_pdf}")
    
    # Show file size
    size_mb = Path(output_pdf).stat().st_size / (1024 * 1024)
    print(f"📊 File size: {size_mb:.2f} MB")


def main():
    if len(sys.argv) < 3:
        print("Usage: python md_to_pdf.py <input_directory> <output_pdf>")
        print("Example: python md_to_pdf.py ./chapters my_book.pdf")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_pdf = sys.argv[2]
    
    if not os.path.isdir(input_dir):
        print(f"❌ Error: '{input_dir}' is not a directory")
        sys.exit(1)
    
    if not output_pdf.endswith('.pdf'):
        output_pdf += '.pdf'
    
    create_pdf(input_dir, output_pdf)


if __name__ == "__main__":
    main()