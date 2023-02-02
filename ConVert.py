import openpyxl as xl
import pandas as pd
from tabula import io as tb


def pdf_to_csv_to_data_frame(filename):
    tb.convert_into(filename + ".pdf", filename + ".csv", output_format="csv", pages='all')

    try:
        file_frame = pd.read_csv(filename + ".csv")
    except FileNotFoundError:
        return f'The file "{filename + ".csv"}" does not exist'
    except UnicodeDecodeError:
        return f'Error reading file "{filename + ".csv"}"'

    # delete the second column and th e last two columns
    file_frame = file_frame.drop(file_frame.columns[1], axis=1)
    file_frame = file_frame.drop(file_frame.columns[-2:], axis=1)

    # name the columns
    file_frame.columns = ['Date', 'Supplier', 'Amount1', 'Amount2']

    # any row in the date column that is not a date is removed
    file_frame = file_frame[file_frame['Date'].str.contains(r'\d{2}/\d{2}/\d{4}')]

    # remove the '€' and ',' from the Amount1 and Amount2 columns
    file_frame['Amount1'] = file_frame['Amount1'].str.replace('€', '')
    file_frame['Amount1'] = file_frame['Amount1'].str.replace(',', '')
    file_frame['Amount2'] = file_frame['Amount2'].str.replace('€', '')
    file_frame['Amount2'] = file_frame['Amount2'].str.replace(',', '')

    # convert the Amount1 and Amount2 columns to float
    file_frame['Amount1'] = file_frame['Amount1'].astype(float)
    file_frame['Amount2'] = file_frame['Amount2'].astype(float)

    # replace all NaN values with 0
    file_frame = file_frame.fillna(0)

    # sum the Amount1 and Amount2 replacing both columns with the sum
    file_frame['Amount1'] = file_frame['Amount1'] + file_frame['Amount2']
    file_frame = file_frame.drop(file_frame.columns[-1], axis=1)

    return file_frame


# using openpyxl create a function that takes a list and writes it to a new Excel file
def write_to_excel(filename, data):
    wb = xl.Workbook()
    ws = wb.active

    # create a table in the Excel file with headers [DATE, CODE, SUPPLIER, TOTAL, CREDITOR, SAVINGS, PAYE, WAGES,
    # BANK, PENSION, CREDIT-CA, TAX/INS, SUNDRIES, TOTAL]
    ws.append(
        ['DATE', 'CODE', 'SUPPLIER', 'TOTAL', 'CREDITOR', 'SAVINGS', 'PAYE', 'WAGES', 'BANK', 'PENSION', 'CREDIT-CA',
         'TAX/INS', 'SUNDRIES', 'TOTAL'])

    # write the data to the Excel file with column 1 under A, column 2 under C and column 3 under D
    for row in data:
        row.insert(1, '')
        ws.append(row)

    wb.save(filename + ".xlsx")


# Function to be performed on the PDF file
def process_pdf(pdf_file):
    # Insert code here to process the PDF file
    text = pdf_file
    text = text[:-4]
    write_to_excel('uploads/CONVERTED-PDF', pdf_to_csv_to_data_frame(text).values.tolist())



