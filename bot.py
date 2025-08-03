from telegram.ext import Updater, MessageHandler, Filters
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import re
import os

# Setup Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
google_creds_str = os.getenv("GOOGLE_CREDENTIALS")
google_creds_dict = json.loads(google_creds_str)
creds = ServiceAccountCredentials.from_json_keyfile_dict(google_creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open("ADR Log").sheet1  # Make sure 'sheet1' matches your sheet/tab name

# Function to parse ADR fields
def parse_adr(text):
    adr = {}
    for field in ['Title', 'Context', 'Decision', 'Consequences', 'Author', 'Date']:
        match = re.search(rf"{field}:\s*(.*)", text)
        adr[field] = match.group(1).strip() if match else ''
    return adr

# Message handler
def handle_message(update, context):
    text = update.message.text
    if text.startswith("ADR"):
        adr = parse_adr(text)
        sheet.append_row([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            adr['Title'],
            adr['Context'],
            adr['Decision'],
            adr['Consequences'],
            adr['Author'],
            adr['Date']
        ])
        update.message.reply_text("✅ ADR saved to Google Sheet.")
    else:
        update.message.reply_text("Please start your message with 'ADR:'")

# Main function
def main():
    token = os.getenv("BOT_TOKEN")  # Set this in Railway secrets
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
