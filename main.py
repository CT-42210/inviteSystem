from flask import Flask, request, render_template, redirect
import csv
import pandas as pd
import os
import sms
from dotenv import load_dotenv

load_dotenv()

# Read the CSV file
df = pd.read_csv('contacts.csv')

# Group by 'Group' and sort names within each group
contacts = df.groupby('Group')['Name'].apply(lambda x: x.sort_values().values.tolist()).to_dict()

app = Flask(__name__)

party_list = {}
batch1 = {}
batch2 = {}
batch3 = {}


@app.route('/')
def home():
    print(party_list)
    print(batch1)
    print(batch2)
    print(batch3)
    return render_template('index.html', contacts=contacts, invitees=party_list)

@app.route('/groups')
def group():
    return render_template('groups.html', contacts=contacts, invitees=party_list)


@app.route('/add_group', methods=['POST'])
def add_group():
    groups = request.form.getlist('groups')
    for group in groups:
        if group not in party_list:
            party_list[group] = contacts[group]
    return redirect('/groups')

@app.route('/batches')
def batches():
    batches = [batch1, batch2, batch3]
    return render_template('batch.html', batches=batches)

@app.route('/add_to_party', methods=['POST'])
def add_to_party():
    invitees = request.form.getlist('invitees')
    for invitee in invitees:
        for group, names in contacts.items():
            if invitee in names:
                if group not in party_list:
                    party_list[group] = []
                if invitee not in party_list[group]:
                    party_list[group].append(invitee)
    return redirect('/')


@app.route('/add_to_batch', methods=['POST'])
def add_to_batch():
    groupInvitees = request.form.getlist('group_invitees')
    groupButton = request.form['group_button']
    if groupButton == 'batch 1':
        batch_number = batch1
    elif groupButton == 'batch 2':
        batch_number = batch2
    elif groupButton == 'batch 3':
        batch_number = batch3

    for invitee in groupInvitees:
        for group, names in contacts.items():
            if invitee in names:
                if group not in batch_number:
                    batch_number[group] = []
                if invitee not in batch_number[group]:
                    batch_number[group].append(invitee)

    return redirect('/')



@app.route('/send_invites', methods=['POST'])
def send_invites():
    for invitee in party_list:
        messageData = {
            'number': invitee[2],  # Invitee's phone number
            'subject': 'Party Invitation',
            'message': 'You are invited to the party!'
        }
        sms.send(messageData)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
