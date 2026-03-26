#!/usr/bin/env python3
"""
Generate PDF documentation from Markdown
Requires: markdown, weasyprint
"""
import os
import sys
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    missing = []
    
    try:
        import markdown
    except ImportError:
        missing.append("markdown")
    
    try:
        import weasyprint
    except ImportError:
        missing.append("weasyprint")
    
    return missing

def install_dependencies(packages):
    """Install missing packages"""
    import subprocess
    
    for package in packages:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def generate_pdf():
    """Generate PDF from markdown file"""
    
    # Check dependencies
    missing = check_dependencies()
    if missing:
        print(f"Missing packages: {', '.join(missing)}")
        print("Installing...")
        install_dependencies(missing)
    
    # Import after installation
    import markdown
    from weasyprint import HTML, CSS
    
    # Read markdown file
    md_file = Path("FluxUI_Language_Reference.md")
    if not md_file.exists():
        print(f"Error: {md_file} not found")
        return False
    
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert markdown to HTML
    html = markdown.markdown(
        md_content,
        extensions=[
            'tables',
            'fenced_code',
            'codehilite',
            'toc',
            'nl2br'
        ]
    )
    
    # Add CSS styling
    css = """
    <style>
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.6;
        color: #333;
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #2c3e50;
        margin-top: 30px;
        margin-bottom: 15px;
    }
    
    h1 {
        border-bottom: 3px solid #3498db;
        padding-bottom: 10px;
    }
    
    h2 {
        border-bottom: 2px solid #3498db;
        padding-bottom: 8px;
    }
    
    code {
        background-color: #f8f9fa;
        padding: 2px 4px;
        border-radius: 3px;
        font-family: 'Courier New', monospace;
        border: 1px solid #e9ecef;
    }
    
    pre {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 5px;
        overflow-x: auto;
        border: 1px solid #e9ecef;
    }
    
    pre code {
        background-color: transparent;
        padding: 0;
        border: none;
    }
    
    blockquote {
        border-left: 4px solid #3498db;
        padding-left: 20px;
        margin-left: 0;
        font-style: italic;
        color: #666;
    }
    
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 20px 0;
    }
    
    th, td {
        border: 1px solid #ddd;
        padding: 12px;
        text-align: left;
    }
    
    th {
        background-color: #3498db;
        color: white;
        font-weight: bold;
    }
    
    ul, ol {
        padding-left: 20px;
    }
    
    li {
        margin-bottom: 5px;
    }
    
    a {
        color: #3498db;
        text-decoration: none;
    }
    
    a:hover {
        text-decoration: underline;
    }
    
    .toc {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        padding: 20px;
        border-radius: 5px;
        margin-bottom: 30px;
    }
    
    .toc ul {
        list-style-type: none;
        padding-left: 0;
    }
    
    .toc li {
        margin-bottom: 5px;
    }
    
    .toc a {
        color: #3498db;
        font-weight: 500;
    }
    
    @page {
        margin: 2cm;
        @bottom-center {
            content: counter(page);
            font-size: 10pt;
            color: #666;
        }
    }
    
    .page-break {
        page-break-before: always;
    }
    </style>
    """
    
    # Create complete HTML document
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>FluxUI Language Reference</title>
        {css}
    </head>
    <body>
        {html}
    </body>
    </html>
    """
    
    # Generate PDF
    output_file = "FluxUI_Language_Reference.pdf"
    
    try:
        HTML(string=full_html).write_pdf(output_file)
        print(f"PDF generated successfully: {output_file}")
        return True
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return False

def main():
    print("FluxUI PDF Documentation Generator")
    print("=" * 40)
    
    if generate_pdf():
        print("\nPDF documentation created successfully!")
        print("File: FluxUI_Language_Reference.pdf")
    else:
        print("\nFailed to generate PDF documentation")
        sys.exit(1)

if __name__ == "__main__":
    main()
