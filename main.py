import csv
import PySimpleGUI as sg
from dotenv import load_dotenv
import os
import sms
load_dotenv()

# Read the CSV file
with open('contacts.csv', 'r') as file:
    reader = csv.reader(file)
    contacts = [row[0] for row in reader]  # Extract names

# Create the GUI
layout = [
    [sg.Listbox(values=contacts, size=(20, 10), key='-CONTACTS-', enable_events=True),
     sg.Listbox(values=[], size=(20, 10), key='-INVITEES-')],
    [sg.Button('Add to Party'), sg.Button('Send Invites')]
]
window = sg.Window('Party Invites', layout)

party_list = []

# Event loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'Add to Party':
        if values['-CONTACTS-']:
            party_list.append(values['-CONTACTS-'][0])
            window['-INVITEES-'].update(party_list)
    elif event == 'Send Invites':
        for invitee in party_list:
            messageData = {
                'number': invitee[2],  # Invitee's phone number
                'subject': 'Party Invitation',
                'message': 'You are invited to the party!'
            }
            sms.send(messageData)

window.close()
