document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('fileInput');
    const fileName = document.getElementById('fileName');
    const tableContainer = document.getElementById('tableContainer');
    const errorMessage = document.getElementById('errorMessage');

    fileInput.addEventListener('change', handleFileSelect);

    function handleFileSelect(event) {
        const file = event.target.files[0];
        
        if (!file) {
            return;
        }

        fileName.textContent = file.name;
        clearError();
        tableContainer.innerHTML = '';

        const fileExtension = file.name.split('.').pop().toLowerCase();

        if (fileExtension === 'md') {
            handleMarkdownFile(file);
        } else if (fileExtension === 'html' || fileExtension === 'htm') {
            handleHTMLFile(file);
        } else if (fileExtension === 'ods') {
            handleODSFile(file);
        } else {
            showError('Unsupported file format. Please upload a .md, .html, or .ods file.');
        }
    }

    function handleHTMLFile(file) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            const content = e.target.result;
            
            try {
                // Create a temporary container to parse the HTML
                const tempDiv = document.createElement('div');
                tempDiv.innerHTML = content;
                
                // Find all tables
                const tables = tempDiv.querySelectorAll('table');
                
                if (tables.length === 0) {
                    showError('No tables found in the HTML file.');
                    return;
                }
                
                // Display all tables
                tables.forEach((table, index) => {
                    if (index > 0) {
                        const title = document.createElement('h2');
                        title.className = 'table-title';
                        title.textContent = `Table ${index + 1}`;
                        tableContainer.appendChild(title);
                    }
                    tableContainer.appendChild(table.cloneNode(true));
                });
                
            } catch (error) {
                showError('Error parsing HTML file: ' + error.message);
            }
        };
        
        reader.onerror = function() {
            showError('Error reading file.');
        };
        
        reader.readAsText(file);
    }

    function handleMarkdownFile(file) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            const content = e.target.result;
            
            try {
                const tables = parseMarkdownTables(content);
                
                if (tables.length === 0) {
                    showError('No tables found in the markdown file.');
                    return;
                }
                
                // Display all tables
                tables.forEach((tableData, index) => {
                    if (index > 0) {
                        const title = document.createElement('h2');
                        title.className = 'table-title';
                        title.textContent = `Table ${index + 1}`;
                        tableContainer.appendChild(title);
                    }
                    const table = createHTMLTable(tableData);
                    tableContainer.appendChild(table);
                });
                
            } catch (error) {
                showError('Error parsing markdown file: ' + error.message);
            }
        };
        
        reader.onerror = function() {
            showError('Error reading file.');
        };
        
        reader.readAsText(file);
    }

    function parseMarkdownTables(markdown) {
        const tables = [];
        const lines = markdown.split('\n');
        let i = 0;
        
        while (i < lines.length) {
            const line = lines[i].trim();
            
            // Check if this line looks like a table row (contains |)
            if (line.startsWith('|') && line.endsWith('|')) {
                const tableData = [];
                
                // Parse the header row
                const headerCells = line.split('|').map(cell => cell.trim()).filter(cell => cell);
                tableData.push(headerCells);
                
                i++;
                
                // Check for separator row
                if (i < lines.length) {
                    const separatorLine = lines[i].trim();
                    if (separatorLine.match(/^\|[\s\-:|]+\|$/)) {
                        i++; // Skip separator row
                        
                        // Parse data rows
                        while (i < lines.length) {
                            const dataLine = lines[i].trim();
                            if (dataLine.startsWith('|') && dataLine.endsWith('|')) {
                                const dataCells = dataLine.split('|').map(cell => cell.trim()).filter(cell => cell);
                                tableData.push(dataCells);
                                i++;
                            } else {
                                break;
                            }
                        }
                        
                        if (tableData.length > 1) {
                            tables.push(tableData);
                        }
                    } else {
                        i++;
                    }
                } else {
                    i++;
                }
            } else {
                i++;
            }
        }
        
        return tables;
    }

    function createHTMLTable(data) {
        const table = document.createElement('table');
        
        // Create header
        if (data.length > 0) {
            const thead = document.createElement('thead');
            const headerRow = document.createElement('tr');
            
            data[0].forEach(cellText => {
                const th = document.createElement('th');
                th.textContent = cellText;
                headerRow.appendChild(th);
            });
            
            thead.appendChild(headerRow);
            table.appendChild(thead);
        }
        
        // Create body
        if (data.length > 1) {
            const tbody = document.createElement('tbody');
            
            for (let i = 1; i < data.length; i++) {
                const row = document.createElement('tr');
                
                data[i].forEach(cellText => {
                    const td = document.createElement('td');
                    td.textContent = cellText;
                    row.appendChild(td);
                });
                
                tbody.appendChild(row);
            }
            
            table.appendChild(tbody);
        }
        
        return table;
    }

    function handleODSFile(file) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            try {
                const arrayBuffer = e.target.result;
                parseODSFile(arrayBuffer);
            } catch (error) {
                showError('Error parsing ODS file: ' + error.message);
            }
        };
        
        reader.onerror = function() {
            showError('Error reading file.');
        };
        
        reader.readAsArrayBuffer(file);
    }

    async function parseODSFile(arrayBuffer) {
        try {
            // ODS files are ZIP archives containing XML files
            // Parsing them in the browser without libraries is complex
            
            clearError();
            
            const instructions = document.createElement('div');
            instructions.style.marginTop = '20px';
            instructions.style.padding = '20px';
            instructions.style.background = '#e3f2fd';
            instructions.style.borderRadius = '8px';
            instructions.style.border = '2px solid #2196F3';
            instructions.innerHTML = `
                <h3 style="color: #1976D2; margin-top: 0;">How to View ODS Files:</h3>
                <p>ODS file support requires a Python conversion script. Follow these steps:</p>
                <ol style="line-height: 1.8;">
                    <li>Save your ODS file to the project directory</li>
                    <li>Run: <code style="background: #fff; padding: 4px 8px; border-radius: 3px;">python3 convert_ods_to_html.py yourfile.ods output.html</code></li>
                    <li>Upload the generated HTML file here</li>
                </ol>
                <p><strong>Alternative:</strong> Open your ODS file in LibreOffice Calc and save it as a CSV or HTML file.</p>
                <hr style="margin: 15px 0; border: none; border-top: 1px solid #90CAF9;">
                <p><strong>For testing:</strong> Try uploading <code style="background: #fff; padding: 4px 8px; border-radius: 3px;">sample.md</code> or <code style="background: #fff; padding: 4px 8px; border-radius: 3px;">sample_from_ods.html</code> instead.</p>
            `;
            tableContainer.appendChild(instructions);
            
        } catch (error) {
            showError('Error processing ODS file: ' + error.message);
        }
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.classList.add('show');
    }

    function clearError() {
        errorMessage.textContent = '';
        errorMessage.classList.remove('show');
    }
});
