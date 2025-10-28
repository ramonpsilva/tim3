#!/usr/bin/env python3
"""
Convert ODS file to HTML table that can be viewed in the table viewer
"""

import sys
from odf import opendocument, table, text


def convert_ods_to_html(ods_path, html_path):
    """Convert ODS file to HTML with tables"""
    doc = opendocument.load(ods_path)
    
    html_parts = []
    html_parts.append('<!DOCTYPE html>')
    html_parts.append('<html lang="en">')
    html_parts.append('<head>')
    html_parts.append('    <meta charset="UTF-8">')
    html_parts.append('    <meta name="viewport" content="width=device-width, initial-scale=1.0">')
    html_parts.append(f'    <title>Tables from {ods_path}</title>')
    html_parts.append('    <style>')
    html_parts.append('        body { font-family: Arial, sans-serif; margin: 20px; }')
    html_parts.append('        table { border-collapse: collapse; width: 100%; margin: 20px 0; }')
    html_parts.append('        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }')
    html_parts.append('        th { background-color: #4CAF50; color: white; }')
    html_parts.append('        tr:nth-child(even) { background-color: #f2f2f2; }')
    html_parts.append('        h2 { color: #333; margin-top: 30px; }')
    html_parts.append('    </style>')
    html_parts.append('</head>')
    html_parts.append('<body>')
    
    for sheet in doc.spreadsheet.getElementsByType(table.Table):
        sheet_name = sheet.getAttribute('name')
        html_parts.append(f'    <h2>{sheet_name}</h2>')
        html_parts.append('    <table>')
        
        first_row = True
        for row in sheet.getElementsByType(table.TableRow):
            cells_data = []
            for cell in row.getElementsByType(table.TableCell):
                cell_text = ''
                for p in cell.getElementsByType(text.P):
                    cell_text += str(p)
                cells_data.append(cell_text)
            
            if any(cells_data):  # Only add non-empty rows
                if first_row:
                    html_parts.append('        <thead>')
                    html_parts.append('            <tr>')
                    for cell_text in cells_data:
                        html_parts.append(f'                <th>{cell_text}</th>')
                    html_parts.append('            </tr>')
                    html_parts.append('        </thead>')
                    html_parts.append('        <tbody>')
                    first_row = False
                else:
                    html_parts.append('            <tr>')
                    for cell_text in cells_data:
                        html_parts.append(f'                <td>{cell_text}</td>')
                    html_parts.append('            </tr>')
        
        html_parts.append('        </tbody>')
        html_parts.append('    </table>')
    
    html_parts.append('</body>')
    html_parts.append('</html>')
    
    with open(html_path, 'w') as f:
        f.write('\n'.join(html_parts))
    
    print(f'Converted {ods_path} to {html_path}')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 convert_ods_to_html.py <input.ods> <output.html>')
        sys.exit(1)
    
    ods_file = sys.argv[1]
    html_file = sys.argv[2]
    
    convert_ods_to_html(ods_file, html_file)
