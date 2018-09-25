from flask import Flask, jsonify, request
from gcsproxy import GCSProxy
import json

G = GCSProxy()
app = Flask(__name__)

servers = ['active_server', 'backup_server']

@app.route('/')
def index():
    return 'Welcome to Geo Decoding Proxy!'

@app.route('/api/v1', methods=["GET"])
def info_view():
    """List of routes for this API."""
    output = {
        'info': 'GET /api/v1',
        'backend_geo_servers': 'GET /api/v1/servers',
        'location': 'POST /api/v1/location?addr=<address>',
    }
    return jsonify(output)

@app.route('/api/v1/servers', methods=["GET"])
def servers():
    return 'The backup servers used are  %s' % str(servers)

@app.route('/api/v1/location', methods=["GET"])
def location():
    print("Got location")
    address = request.args.get('addr', default='*', type=str)
    if address == '*':
        return 'No address provided'
    print ('The location of the address you have passed is %s' % str(address))
    location, active = G.request_location(address)
    loc = dict()
    
    if active == 1:
        loc['Latitude'] = location['Response']['View'][0]['Result'][0]\
                                    ['Location']['NavigationPosition'][0]['Latitude']
        loc['Longitude'] = location['Response']['View'][0]['Result'][0]\
                                    ['Location']['NavigationPosition'][0]['Longitude']
    elif active == 2:
        loc['Latitude'] = location['results'][0]['geometry']['location']['lat']
        loc['Longitude'] = location['results'][0]['geometry']['location']['lng']
    
    return jsonify(loc)

G.start()

if __name__ == '__main__':
    #start the backend proxy and establish the key

    app.run()
