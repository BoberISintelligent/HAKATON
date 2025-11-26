import gspread
from gspread.exceptions import SpreadsheetNotFound

SPREADSHEET_NAME = "Eesti lastelaagrid"

def upload_to_google_sheets(data, spreadsheet_name=SPREADSHEET_NAME):

    gc = gspread.oauth(credentials_filename="credentials.json")

    try:

        sh = gc.open(spreadsheet_name)
        print("Arvutiarvutustabel leiti, andmeid kirjutatakse üle...")
    except SpreadsheetNotFound:

        print("Tabelit ei leitud, luuakse uus...")
        sh = gc.create(spreadsheet_name)

        sh.share("romansav1229@gmail.com", perm_type="user", role="writer")

    ws = sh.sheet1


    ws.clear()


    ws.update(data)

    print("Tabelit on uuendatud.")
    print("URL Google Sheets:", sh.url)
    myurl = sh.url
    return myurl
