import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from dotenv import load_dotenv
import datetime
import os

load_dotenv('environment/invoicing/.env')

def get_config():
    return {
        'CUSTOMER_SHORTCODE': os.getenv('CUSTOMER_SHORTCODE'),
        'CUSTOMER_NAME': os.getenv('CUSTOMER_NAME'),
        'INVOICE_AMOUNT': float(os.getenv('INVOICE_AMOUNT')),
        'FILE_ID': os.getenv('FILE_ID'),
        'FOLDER_ID': os.getenv('FOLDER_ID'),
        'SCOPES': [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive',
        ]
    }

def setup_services(scopes):
    creds = Credentials.from_service_account_file('environment/invoicing/credentials.json', scopes=scopes)
    sheets_client = gspread.authorize(creds)
    drive_service = build('drive', 'v3', credentials=creds)
    return sheets_client, drive_service

def get_invoice_dates():
    today = datetime.date.today()
    expiration = datetime.date(today.year, today.month, 10)
    return today, expiration

def update_template(sheets_client, file_id, customer_name, invoice_amount, today, expiration):
    sheet = sheets_client.open_by_key(file_id).sheet1
    sheet.update('B9', [[f'Submitted on {today.strftime("%Y/%m/%d")}' ]])
    sheet.update('B13', [[ customer_name ]])
    sheet.update('F12', [[float(sheet.acell('F12').value) + 1]])
    sheet.update('F15', [[expiration.strftime('%Y/%m/%d')]])
    sheet.update('F19', [[invoice_amount]])

def export_to_pdf(drive_service, file_id, customer_shortcode, expiration):
    invoice_name = f'{expiration.year}{expiration.month:02d}{expiration.day:02d}-invoice-roberts-{customer_shortcode}.pdf'
    request = drive_service.files().export_media(
        fileId=file_id,
        mimeType='application/pdf'
    )
    with open(invoice_name, 'wb') as f:
        f.write(request.execute())
    return invoice_name

def upload_to_drive(drive_service, file_name, folder_id):
    media = MediaFileUpload(file_name, mimetype='application/pdf')
    _ = drive_service.files().create(
        body={'name': file_name, 'parents': [folder_id]},
        media_body=media,
        fields='id'
    ).execute()

def main():
    config = get_config()
    CUSTOMER_SHORTCODE = config['CUSTOMER_SHORTCODE']
    CUSTOMER_NAME = config['CUSTOMER_NAME']
    INVOICE_AMOUNT = config['INVOICE_AMOUNT']
    FILE_ID = config['FILE_ID']
    FOLDER_ID = config['FOLDER_ID']
    SCOPES = config['SCOPES']

    sheets_client, drive_service = setup_services(SCOPES)
    today, expiration = get_invoice_dates()

    update_template(sheets_client, FILE_ID, CUSTOMER_NAME, INVOICE_AMOUNT, today, expiration)
    invoice_name = export_to_pdf(drive_service, FILE_ID, CUSTOMER_SHORTCODE, expiration)

    upload_to_drive(drive_service, invoice_name, FOLDER_ID)

    os.remove(invoice_name)  # Clean up local file

    print(f'Invoice for {CUSTOMER_NAME} ({CUSTOMER_SHORTCODE}) of ${INVOICE_AMOUNT} created successfully.')
