from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify, redirect,url_for
import atexit
import cf_deployment_tracker
import os
import json

# Emit Bluemix deployment event
cf_deployment_tracker.track()

app = Flask(__name__)

db_name = 'mydb'
db1_name = 'Users'
client = None
db = None

if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.getenv('VCAP_SERVICES'))
    print('Found VCAP_SERVICES')
    if 'cloudantNoSQLDB' in vcap:
        creds = vcap['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)
elif os.path.isfile('vcap-local.json'):
    with open('vcap-local.json') as f:
        vcap = json.load(f)
        print('Found local VCAP_SERVICES')
        creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)
        

# On Bluemix, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/heatmap')
def heatmap1():
    return render_template('bk.html')    

# /* Endpoint to greet and add a new visitor to database.
# * Send a POST request to localhost:8000/api/visitors with body
# * {
# *     "name": "Bob"
# * }
# */
@app.route('/api/visitors', methods=['GET'])
def get_visitor():
    if client:
        return jsonify([])
    else:
        print('No database')
        return jsonify([])

# /**
#  * Endpoint to get a JSON array of all the visitors in the database
#  * REST API example:
#  * <code>
#  * GET http://localhost:8000/api/visitors
#  * </code>
#  *
#  * Response:
#  * [ "Bob", "Jane" ]
#  * @return An array of all the visitor names
#  */
@app.route('/api/visitors', methods=['POST'])
def put_visitor():
    user = request.json['name']
    if client:
        data = {'name':user}
        db.create_document(data)
        return 'Hello %s! I added you to the database.' % user
    else:
        print('No database')
        return 'Hello %s!' % user



'''class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    gender = db.Column(db.String(120))
    age = db.Column(db.Integer)

    def __init__(self, username, email , gender , age):
        self.username = username
        self.email = email
        self.gender = gender
        self.age = age

    def __repr__(self):
        return '<User %r>' % self.username

class Pills1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    name = db.Column(db.String(80))
    count = db.Column(db.Integer)
    partition_number = db.Column(db.Integer)

    def __init__(self, user_id, name , count , partition_number):
        self.user_id = user_id
        self.name = name
        self.count = count
        self.partition_number = partition_number

    def __repr__(self):
        return '<User %r>' % self.username

class Histories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    pillname = db.Column(db.String(80))
    pill_id = db.Column(db.Integer)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
	# updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate = db.func.now())


class Dosage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pill_id = db.Column(db.Integer)
    cycle = db.Column(db.String(5))
    
    def __init__(self, pill_id, cycle ):
        self.pill_id = pill_id
        self.cycle = cycle

    def __repr__(self):
        return '<User %r>' % self.username


    def __init__( self, user_id, pillname , pill_id ):
        self.user_id = user_id
        self.pillname = pillname
        self.pill_id = pill_id
    
    def __repr__(self):
        return '<User %r>' % self.username        

'''

@app.route('/showhistory',methods=['GET'])
def gethistory():
	#history = list(map(lambda doc:{doc['_id'],doc['user_id'],doc['pillname'],doc['pill_id'],doc['created_on'] }, history_db))
	selector = {'type':{'$eq':'history'}}
	history = db.get_query_result(selector)
	return render_template('history.html', history = history )
	'''history = Histories.query.all()
	return render_template('history.html', history = history )'''


@app.route('/gethistorybyid',methods=['GET'])
def gethistorybyid():
	user_id = request.args.get('user_id')
	selector = {'user_id':{'$eq':user_id},'type':{'$eq':'history'}}
	history = db.get_query_result(selector)

	historyhash = {}
	counter = 1

	for temp in history:
		temphash = {}
		temphash['pill_id'] = temp['pill_id']
		temphash['user_id'] = temp['user_id']
		temphash['pillname'] = temp['pillname']
		temphash['time'] = temp['created_on']
		historyhash[counter] = temphash
		counter = counter+1

	historyhash['size']=counter-1
	return jsonify(historyhash)	



@app.route('/pilltaken',methods=['GET'])
def pilltaken():
	pill_id = request.args.get('pill_id')
	selector = {'_id':{'$eq':pill_id},'type':{'$eq':'pills'}}
	pill = db.get_query_result(selector,limit=1)
	pill['count'] = pill['count']-1
	db.save()
	data = {
		'user_id': pill['user_id'],
		'name': pill['name'],
		'_id': pill['_id'],
		'type':'pills'
	}

	db.create_document(data)
	db.save()
	return redirect(url_for('index'))


@app.route('/show_user')
def show_user():
	#users = list(map(lambda doc: {doc['username'],doc['email'],doc['gender'],doc['age']}, user_db))
	#users = Users.query.all()
	selector = {'type':{'$eq':'user'}}
	users = db.get_query_result(selector)
	return render_template('show_users.html', user = users )

@app.route('/show_pills')
def show_pills():
	#pills = list(map(lambda doc: {doc['user_id'],doc['name'],doc['partition_number']},pills_db))
	selector = {'type':{'$eq':'pills'}}
	pills = db.get_query_result(selector)
	return render_template('show_pills.html', pill = pills )

@app.route('/show_dosage')
def show_dosage():
	selector = {'type':{'$eq':'dosage'}}
	dosage = db.get_query_result(selector)
	return render_template('show_dosage.html', dosage = dosage )


@app.route('/adduser', methods=['GET'])
def adduser():
	data = {
		'username' : request.args.get('username'),
		'email':request.args.get('email'),
		'gender':request.args.get('gender'),
		'age':request.args.get('age'),
		'type':'user'
	}

	db.create_document(data)

	#admin = Users( request.args.get('username'), request.args.get('email') , request.args.get('gender') , request.args.get('age') )
	#db.session.add(admin)
	#db.session.commit()
	return redirect(url_for('index'))

@app.route('/addpill', methods=['GET'])
def addpill():
	data ={
		'user_id':request.args.get('user_id'),
		'name':request.args.get('name'),
		'count':request.args.get('count'),
		'partition_number':request.args.get('partition_number'),
		'type':'pills'
	}

	db.create_document(data)
	#box = Pills1( request.args.get('user_id'), request.args.get('name') , request.args.get('count') , request.args.get('partition_number') )
	#db.session.add(box)
	#db.session.commit()
	return redirect(url_for('index'))

# todo
@app.route('/addpillanddosage', methods=['GET'])
def addpillanddosage():
	data ={
		'user_id':request.args.get('user_id'),
		'name':request.args.get('name'),
		'count':request.args.get('count'),
		'partition_number':request.args.get('partition_number'),
		'type':'pills'
	}

	db.create_document(data)

	selector = {'user_id': {'$eq': request.args.get('user_id')},
		'name':{'$eq': request.args.get('name')},
		'count':{'$eq': request.args.get('count')},
		'partition_number':{'$eq': request.args.get('partition_number'),'type':{'$eq':'pills'}}}

	doc = db.get_query_result(selector,limit=1)

	for d in doc:
		data2={
			'pill_id': doc['_id'],
	    	'timing': request.args.get('timing'),
	    	'type': 'dosage'
		}

		db.create_document(data2)

	#box = Pills1.query.filter_by(user_id=request.args.get('user_id')).filter_by(name = request.args.get('name')).filter_by(count=request.args.get('count')).first()
	#osage = Dosage( box.id , request.args.get('cycle') )
	#b.session.add(dosage)
	#db.session.commit()
	return redirect(url_for('index'))

@app.route('/adddosage', methods=['GET'])
def adddosage():
	data2={
		'pill_id': request.args.get('pill_id'),
		'timing': request.args.get('timing'),
		'type': 'dosage'
	}
	db.create_document(data2)
	return redirect(url_for('index'))

@app.route('/delete_dosage_by_pill_id', methods=['GET'])
def deletedosage():
	pill_id = request.args.get('pill_id')

	selector = {'pill_id': {'$eq': pill_id},'type': {'$eq': 'dosage'}}

	box = db.get_query_result(selector)
	
	if box:
		for temp in box:
			temp.delete()

	return redirect(url_for('index'))

@app.route('/get_pill_by_user_for_pi',methods=['GET'])
def get_pill_by_user_for_pi():
	user_id = request.args.get('user_id')
	selector = {'user_id':{'$eq':user_id},'type': {'$eq': 'pills'}}
	#pill = Pills1.query.filter_by(user_id=user_id).all()
	pill = db.get_query_result(selector)
	final = {}
	counter = 1

	for temp in pill:
		selector = {'pill_id':{"$eq":temp['_id']},'type': {'$eq': 'dosage'}}
		dosage = db.get_query_result(selector,limit=1)
		temphash = {}
		if dosage:
			temphash['timing'] = dosage['timing']
		temphash['pill_id'] = temp['_id']
		temphash['user_id'] = temp['user_id']
		temphash['count'] = temp['count']
		temphash['partition_number'] = temp['partition_number']
		temphash['name'] = temp['name']
		final[counter] = temphash
		counter = counter + 1

	final['size'] = counter-1
	return jsonify(final)	


@app.route('/getuser_id', methods=['GET'])
def getuser_id():
	name = request.args.get('name')
	selector = {'type',{'$eq':'user'},'username',{'$eq':name}}
	user = db.get_query_result(selector,limit=1)
	userHash = {}
	userHash['id']=user.id
	userHash['username']=user.username
	userHash['gender']=user.gender
	userHash['email']=user.email	
	return jsonify(userHash)

@app.route('/getpill_id', methods=['GET'])
def getpill_id():
	user_id = request.args.get('user_id')
	selector = {'user_id':{'$eq':user_id},'type':{'$eq':'types'}}
	pills = db.get_query_result(selector)
	#pills = Pills1.query.filter_by(user_id=user_id).all()
	
	pillHash = {}
	
	counter = 1

	for temp in pills:
		tempHash = {}
		tempHash['name'] = temp['name']
		tempHash['user_id'] = temp['user_id']
		tempHash['id'] = temp['id']
		tempHash['count'] = temp['count']
		pillHash[counter] = tempHash
		counter = counter + 1

	pillHash['size'] = counter-1

	return jsonify(pillHash)

@app.route('/getdosage_id', methods=['GET'])
def getdosage_id():
	pill_id = request.args.get('pill_id')
	selector = {'pill_is',{'$eq':pill_id},'type',{'$eq':'dosage'}}

	dosage = db.get_query_result(selector)
	#dosage = Dosage.query.filter_by(pill_id=pill_id).all()
	
	dosageHash = {}
	
	counter = 1

	for temp in dosage:
		tempHash = {}
		tempHash['timing'] = temp['timing']
		dosageHash[counter] = tempHash
		counter = counter + 1
	
	dosageHash['size']=counter-1

	return jsonify(dosageHash)

@atexit.register
def shutdown():
    if client:
        client.disconnect()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)