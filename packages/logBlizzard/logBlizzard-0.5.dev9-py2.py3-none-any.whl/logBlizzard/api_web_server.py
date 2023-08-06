#!flask/bin/python
from flask import Flask, jsonify, abort, make_response
import search_api
import json

def api_server():
    app = Flask('logBlizzard')
    @app.route('/logblizzard/api/v0.5/logs/<search>/<oper>/<stype>/<tmin>/<tmax>', methods=['GET'])
    def log_search(search,oper,stype,tmin,tmax):
        search=search.split(',')
        tmin=float(tmin)
        tmax=float(tmax)
        result=search_api.apiReq(search,oper,stype,tmin,tmax)

        return(jsonify(result))
    with open('network_cfg.json','r') as nwc:
        nw=json.load(nwc)
    API_IP=nw["API_IP"]
    app.run(host=API_IP, debug=True)

if __name__ == '__main__':
    api_server()
