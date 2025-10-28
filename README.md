# tim3
Links para defesas remotas ou salas para defesas presenciais

## Table Viewer

A web application for displaying tables from LibreOffice spreadsheets (.ods) or Markdown files (.md).

### Features

- **Markdown Support**: Display tables from markdown files
- **LibreOffice Spreadsheet Support**: Display tables from .ods files
- **Multiple Tables**: View multiple tables from a single markdown file
- **Multiple Sheets**: Switch between different sheets in an ODS file
- **Responsive Design**: Clean, modern interface that works on all devices

### Usage

1. Open `index.html` in a web browser
2. Click "Choose File" to upload either:
   - A markdown file (.md) containing tables
   - A LibreOffice spreadsheet file (.ods)
3. The tables will be displayed automatically
4. For ODS files with multiple sheets, use the dropdown to switch between sheets

### Sample Files

Two sample files are included:
- `sample.md` - A markdown file with example tables
- `sample.ods` - A LibreOffice spreadsheet with multiple sheets

### Running Locally

Simply open `index.html` in a web browser. No server required!

For better experience, you can use a local server:
```bash
python3 -m http.server 8000
```
Then navigate to `http://localhost:8000`
