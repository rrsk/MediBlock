from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify
import atexit
import cf_deployment_tracker
import os
import json

# Emit Bluemix deployment event
cf_deployment_tracker.track()

app = Flask(__name__)

db_name = 'mydb'
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
def home():
    return render_template('index.html')

# /* Endpoint to greet and add a new visitor to database.
# * Send a POST request to localhost:8000/api/visitors with body
# * {
# *     "name": "Bob"
# * }
# */
@app.route('/api/visitors', methods=['GET'])
def get_visitor():
    if client:
        return jsonify(list(map(lambda doc: doc['name'], db)))
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

user_db = client.create_database('Users',throw_on_exists=False)
pills_db = client.create_database('Pills',throw_on_exists=False)
dosage_db = client.create_database('Dosage',throw_on_exists=False)
history_db = client.create_database('Histories',throw_on_exists=False)


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
    if client:
	history = list(map(lambda doc: doc['name'], history_db))
        return render_template('history.html', history = history )
    else:
        return render_template('history.html', history = [] )
	'''history = Histories.query.all()
	return render_template('history.html', history = history )'''


@app.route('/gethistorybyid',methods=['GET'])
def gethistorybyid():
	user_id = request.args.get('user_id')
	history = history_db[user_id]

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
	pill = pills_db[pill_id]
	pill['count'] = pill['count']-1
	pills_db.save()
	history = Histories( pill.user_id , pill.name , pill.id )
	db.session.add(history)
	db.session.commit()
	return redirect(url_for('index'))


@app.route('/show_user')
def show_user():
	users = Users.query.all()
	return render_template('show_users.html', user = users )

@app.route('/show_pills')
def show_pills():
	pills = Pills1.query.all()
	return render_template('show_pills.html', pill = pills )

@app.route('/show_dosage')
def show_dosage():
	dosage = Dosage.query.all()
	return render_template('show_dosage.html', dosage = dosage )


@app.route('/adduser', methods=['GET'])
def adduser():
	admin = Users( request.args.get('username'), request.args.get('email') , request.args.get('gender') , request.args.get('age') )
	db.session.add(admin)
	db.session.commit()
	return redirect(url_for('index'))

@app.route('/addpill', methods=['GET'])
def addpill():
	box = Pills1( request.args.get('user_id'), request.args.get('name') , request.args.get('count') , request.args.get('partition_number') )
	db.session.add(box)
	db.session.commit()
	return redirect(url_for('index'))

# todo
@app.route('/addpillanddosage', methods=['GET'])
def addpillanddosage():
	box = Pills1( request.args.get('user_id'), request.args.get('name') , request.args.get('count') , request.args.get('partition_number') )
	db.session.add(box)
	db.session.commit()
	box = Pills1.query.filter_by(user_id=request.args.get('user_id')).filter_by(name = request.args.get('name')).filter_by(count=request.args.get('count')).first()
	dosage = Dosage( box.id , request.args.get('cycle') )
	db.session.add(dosage)
	db.session.commit()
	return redirect(url_for('index'))

@app.route('/adddosage', methods=['GET'])
def adddosage():
	box = Dosage( request.args.get('pill_id'), request.args.get('cycle') )
	db.session.add(box)
	db.session.commit()
	return redirect(url_for('index'))

@app.route('/delete_dosage_by_pill_id', methods=['GET'])
def deletedosage():
	pill_id = request.args.get('pill_id')
	box = Dosage.query.filter_by(pill_id=pill_id).all()
	
	if box:
		for temp in box:
			db.session.delete(temp)
			db.session.commit()

	return redirect(url_for('index'))

@app.route('/get_pill_by_user_for_pi',methods=['GET'])
def get_pill_by_user_for_pi():
	user_id = request.args.get('user_id')
	pill = Pills1.query.filter_by(user_id=user_id).all()

	final = {}
	counter = 1

	for temp in pill:
		dosage = Dosage.query.filter_by( pill_id = temp.id ).first()
		temphash = {}
		if dosage:
			temphash['cycle'] = dosage.cycle
		temphash['pill_id'] = temp.id
		temphash['user_id'] = temp.user_id
		temphash['count'] = temp.count
		temphash['partition_number'] = temp.partition_number
		temphash['name'] = temp.name
		final[counter] = temphash
		counter = counter + 1

	final['size'] = counter-1
	return jsonify(final)	


@app.route('/getuser_id', methods=['GET'])
def getuser_id():
	name = request.args.get('name')
	user = Users.query.first()
	userHash = {}
	userHash['id']=user.id
	userHash['name']=user.username
	userHash['gender']=user.gender
	userHash['email']=user.email	
	return jsonify(userHash)

@app.route('/getpill_id', methods=['GET'])
def getpill_id():
	user_id = request.args.get('user_id')
	pills = Pills1.query.filter_by(user_id=user_id).all()
	
	pillHash = {}
	
	counter = 1

	for temp in pills:
		tempHash = {}
		tempHash['name'] = temp.name
		tempHash['user_id'] = temp.user_id
		tempHash['id'] = temp.id
		tempHash['count'] = temp.count
		pillHash[counter] = tempHash
		counter = counter + 1

	pillHash['size'] = counter-1

	return jsonify(pillHash)

@app.route('/getdosage_id', methods=['GET'])
def getdosage_id():
	pill_id = request.args.get('pill_id')
	dosage = Dosage.query.filter_by(pill_id=pill_id).all()
	
	dosageHash = {}
	
	counter = 1

	for temp in dosage:
		tempHash = {}
		tempHash['cycle'] = temp.cycle
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
