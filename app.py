#!flask/bin/python
from flask import Flask, jsonify, abort, request
from sklearn import tree
import pandas as pd

app = Flask(__name__)

data = pd.read_csv('thLotto_49-59.csv')
day = list(zip(data['day'],data['month'],data['year']))
first = data['first']
digit3 = data['3digit']
last_2digit_top = data['last_2digit_top']
first_3digit_1 = data['first_3digit_1']
first_3digit_2 = data['first_3digit_2']
last_3digit_1 = data['last_3digit_1']
last_3digit_2 = data['last_3digit_2']
last_2digit_down = data['last_2digit_down']
iD = int(16)
iM = int(04)
iY = int(2014)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/lottery/get', methods=['POST'])
def create_task():
    print(request.json)
    if not request.json or not 'day' or not 'month' or not 'year' in request.json:
        abort(400)
    iD = int(int(request.json['day']))
    iM = int(int(request.json['month']))
    iY = int(int(request.json['year']))
    message_parts = {
            "first":"%s"% perdictLotto(iD,iM,iY,day,first),
            "tree":"%s"%perdictLotto(iD,iM,iY,day,digit3),
            "first_tree1":"%s"%perdictLotto(iD,iM,iY,day,first_3digit_1),
            "first_tree2":"%s"%perdictLotto(iD,iM,iY,day,first_3digit_2),
            "last_tree1":"%s"%perdictLotto(iD,iM,iY,day,last_3digit_1),
            "last_tree2":"%s"%perdictLotto(iD,iM,iY,day,last_3digit_2),
            "two_1":"%s"%perdictLotto(iD,iM,iY,day,last_2digit_top),
            "two_2":"%s"%perdictLotto(iD,iM,iY,day,last_2digit_down)
        }
    return jsonify(message_parts), 200

def perdictLotto(d,m,y,data1,data2):
	classifier = tree.DecisionTreeClassifier()
	classifier.fit(data1,data2)
	return classifier.predict([[d,m,y]])[0]

if __name__ == '__main__':
    app.run(debug=True)

