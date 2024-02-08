import os
import smtplib
import numlookupapi
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

carriers = {
    'att': '@mms.att.net',
    'tmobile': '@tmomail.net',
    'verizon': '@vtext.com',
    'unknown': 'unknown',
    'error': 'error'
}


def lookup(number):
    if isinstance(number, str):
        number = int(number)

    def apiLookup(number):
        key = os.getenv('LOOKUP-API-KEY')
        client = numlookupapi.Client(key)
        apiResult = client.validate(number, country_code='US')
        print("API lookup result:", apiResult)
        if 'at&t' in apiResult['carrier'].lower() or 'att' in apiResult['carrier'].lower():
            return "att"
        elif 'tmobile' in apiResult['carrier'].lower() or 't-mobile' in apiResult['carrier'].lower():
            return "tmobile"
        elif 'verizon' in apiResult['carrier'].lower():
            return "verizon"
        elif 'sprint' in apiResult['carrier'].lower():
            return "tmobile"
        elif 'mint' in apiResult['carrier'].lower():
            return "tmobile"
        elif '' in apiResult['carrier'].lower():
            return "error"
        else:
            return "unknown"

    df = pd.read_csv('contacts.csv')
    if number in df['Phone'].values:
        print("Number found in CSV file")
        if df.loc[df['Phone'] == number, 'Carrier'].values[0] in carriers:
            return df.loc[df['Phone'] == number, 'Carrier'].values[0]
        else:
            print("Looking up carrier using API")
            result = apiLookup(number)
            print("API lookup result:", result)
            df.loc[df['Phone'] == number, 'Carrier'] = result
            df.to_csv('contacts.csv', index=False)
            return result


def send(messageData):
    email = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')
    auth = (email, password)

    # Establish a secure session with gmail's outgoing SMTP server using your gmail account
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])

    for items in messageData:
        number = items['number']
        carrier = carriers[lookup(number)]
        if carrier == "unknown":
            return f'ERR: can not find carrier for number {number}'
        message = items['message']

        to_number = (number + carrier)
        server.sendmail(auth[0], to_number, message)
        print(f"Sent message \n{message} \nto {number}")
