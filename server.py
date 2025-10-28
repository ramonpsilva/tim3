#!/usr/bin/env python3
"""
Simple HTTP server that can serve the table viewer and convert ODS files to HTML
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os
from odf import opendocument, table, text
import cgi
from urllib.parse import parse_qs

class TableViewerHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        """Handle file uploads and conversion"""
        if self.path == '/convert_ods':
            content_type = self.headers.get('Content-Type', '')
            
            if 'multipart/form-data' not in content_type:
                self.send_error(400, 'Bad Request')
                return
            
            # Parse multipart form data
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    'REQUEST_METHOD': 'POST',
                    'CONTENT_TYPE': self.headers['Content-Type'],
                }
            )
            
            if 'file' not in form:
                self.send_error(400, 'No file uploaded')
                return
            
            file_item = form['file']
            
            try:
                # Save uploaded file temporarily using a secure method
                import tempfile
                with tempfile.NamedTemporaryFile(mode='wb', suffix='.ods', delete=False) as temp_file:
                    temp_path = temp_file.name
                    temp_file.write(file_item.file.read())
                
                # Convert ODS to table data
                tables_data = self.convert_ods_to_data(temp_path)
                
                # Send response
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(tables_data).encode())
                
                # Clean up
                os.remove(temp_path)
                
            except Exception as e:
                self.send_error(500, f'Error processing file: {str(e)}')
    
    def convert_ods_to_data(self, filepath):
        """Convert ODS file to table data structure"""
        doc = opendocument.load(filepath)
        sheets = []
        
        for sheet in doc.spreadsheet.getElementsByType(table.Table):
            sheet_name = sheet.getAttribute('name')
            rows_data = []
            
            for row in sheet.getElementsByType(table.TableRow):
                cells_data = []
                for cell in row.getElementsByType(table.TableCell):
                    # Get cell text properly
                    cell_text = ''
                    for p in cell.getElementsByType(text.P):
                        # Get text content from paragraph
                        for node in p.childNodes:
                            if hasattr(node, 'data'):
                                cell_text += node.data
                    cells_data.append(cell_text)
                
                if any(cells_data):  # Only add non-empty rows
                    rows_data.append(cells_data)
            
            if rows_data:
                sheets.append({
                    'name': sheet_name,
                    'data': rows_data
                })
        
        return sheets

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, TableViewerHandler)
    print(f'Server running on http://localhost:{port}/')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
