#!/usr/bin/env python3
"""
Script to generate a sample ODS file for testing the table viewer
"""

from odf.opendocument import OpenDocumentSpreadsheet
from odf.table import Table, TableRow, TableCell
from odf.text import P

def create_sample_ods():
    # Create a new spreadsheet
    doc = OpenDocumentSpreadsheet()
    
    # Create first sheet - Schedule
    schedule_table = Table(name="Schedule")
    
    # Header row
    header_row = TableRow()
    headers = ["Time", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    for header in headers:
        cell = TableCell()
        cell.addElement(P(text=header))
        header_row.addElement(cell)
    schedule_table.addElement(header_row)
    
    # Data rows
    schedule_data = [
        ["9:00", "Math", "English", "Science", "History", "Art"],
        ["10:00", "Physics", "Chemistry", "Biology", "Geography", "Music"],
        ["11:00", "Literature", "Programming", "Statistics", "Economics", "PE"]
    ]
    
    for row_data in schedule_data:
        row = TableRow()
        for cell_data in row_data:
            cell = TableCell()
            cell.addElement(P(text=cell_data))
            row.addElement(cell)
        schedule_table.addElement(row)
    
    doc.spreadsheet.addElement(schedule_table)
    
    # Create second sheet - Student Grades
    grades_table = Table(name="Student Grades")
    
    # Header row
    header_row = TableRow()
    headers = ["Student Name", "Math", "Science", "English", "Average"]
    for header in headers:
        cell = TableCell()
        cell.addElement(P(text=header))
        header_row.addElement(cell)
    grades_table.addElement(header_row)
    
    # Data rows
    grades_data = [
        ["Alice Smith", "95", "88", "92", "91.7"],
        ["Bob Johnson", "87", "91", "85", "87.7"],
        ["Carol White", "92", "95", "89", "92.0"],
        ["David Brown", "78", "82", "80", "80.0"],
        ["Emma Davis", "91", "87", "94", "90.7"]
    ]
    
    for row_data in grades_data:
        row = TableRow()
        for cell_data in row_data:
            cell = TableCell()
            cell.addElement(P(text=cell_data))
            row.addElement(cell)
        grades_table.addElement(row)
    
    doc.spreadsheet.addElement(grades_table)
    
    # Save the file
    doc.save("sample.ods")
    print("Sample ODS file created: sample.ods")

if __name__ == "__main__":
    create_sample_ods()
