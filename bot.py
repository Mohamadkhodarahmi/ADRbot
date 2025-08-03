from telegram.ext import Updater, MessageHandler, Filters import gspread from oauth2client.service_account
import ServiceAccountCredentials 
from datetime import datetime 
import re 
import os 

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"] 
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope) 
client = gspread.authorize(creds) 
sheet = client.open("ADR Log").sheet

def parse_adr(text):
     adr = {} 
     for field in ['Title', 'Context', 'Decision', 'Consequences', 'Author', 'Date']:
         match = re.search(rf"{field}:\s*(.*)", text) adr[field] = match.group(1).strip() if match else '' return adr # Message Handler

def handle_message(update, context):
     text = update.message.text 
     if text.startswith("ADR"):
         adr = parse_adr(text) sheet.append_row([ 
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            adr['Title'], 
            adr['Context'], 
            adr['Decision'], 
            adr['Consequences'], 
            adr['Author'], 
            adr['Date'] ]) update.message.reply_text("✅ ADR saved to Google Sheet.") 
    else: update.message.reply_text("Please start your message with 'ADR:'")

def main(): token = os.getenv("BOT_TOKEN") # Better security
    updater = Updater(token, use_context=True) 
    dp = updater.dispatcher 
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message)) 
    updater.start_polling() 
    updater.idle()
     if __name__ == '__main__': main()    