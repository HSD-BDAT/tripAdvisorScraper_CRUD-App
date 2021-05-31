'''
Homepage, it reads the data present in the MongoDB database.
It contains everything required for the project.
1. Data table
2. Create/Add 
3. Read
4. Update/Edit
5. Delete (one/many)

The main content is in the `app.html` file.
We used Boostrap for fonts and forms.
DataTables to show the data.
JavaScript, jQuery, AJAX to read data from forms and buttons into Python.
'''

# load necessary packages
from flask import Flask, request, render_template
from pymongo import MongoClient
from datetime import datetime

# create flask app
app = Flask(__name__)

# connect with mongoDB atlas
client = MongoClient("mongodb+srv://bdatAdmin:HCjquZSkonIiojmi@cluster0.zbfiq.mongodb.net/trip?retryWrites=true&w=majority")
db = client.socialMining_01

# Homepage, READ
@app.route('/')
def home():
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    scraped = db.scraped.find()
    b = [todo for todo in scraped]   
    return render_template('app.html', products = b, **locals())

# To delete observations, DELETE
@app.route('/delete_products', methods=['POST'])
def delete():	
    ids = request.json['ids']
    ids = ids.split(',')
    [db.scraped.remove({'_id': id1}) for id1 in ids]

# To add data entry, CREATE     
@app.route('/add', methods=['POST', 'GET'])
def add():	
    dict1 = dict()

    dict1['Rank'] = ''.join(request.json['Rank'])
    dict1['Name'] = ''.join(request.json['Name'])
    dict1['Group'] = ''.join(request.json['Group'])
    dict1['Rating'] = ''.join(request.json['Rating'])
    dict1['# of Reviews'] = ''.join(request.json['# of Reviews'])
    dict1['Perfect Reviews %'] = ''.join(request.json['Perfect Reviews %'])
    dict1['Address'] = ''.join(request.json['Address'])
    dict1['Neighbourhood'] = ''.join(request.json['Neighbourhood'])  
    dict1['Suggested Duration'] = ''.join(request.json['Suggested Duration'])
    dict1['Timings'] = ''.join(request.json['Timings'])
    dict1['Open'] = ''.join(request.json['Open'])  
    dict1['Website'] = ''.join(request.json['Website'])
    dict1['Phone'] = ''.join(request.json['Phone'])
    dict1['Email'] = ''.join(request.json['Email'])
    dict1['Summary'] = ''.join(request.json['Summary'])
    dict1['Link'] = ''.join(request.json['Link'])
    dict1['timeScraped'] = ''.join(request.json['timeScraped'])
    dict1['_id'] = dict1['Name']
    
    db.scraped.insert_one(dict1)
    
# run the flask app   
if __name__ == "__main__":
    app.run()