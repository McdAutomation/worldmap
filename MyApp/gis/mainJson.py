from flask import Flask, render_template, request, jsonify, session
from MyApp.gis.WorldJson import World, WorldCircleColumnDataSource
from elasticsearch import Elasticsearch
import pandas as pd
from geopy.geocoders import Nominatim
import numpy as np
from flask import g

key = 'AIzaSyCl9gfvmpQoyisgz-lt1epZkU5iVMaoLM0'
app = Flask(__name__)

app.secret_key = key

restaurant_data_AU = pd.read_csv("C:/Users/atrivedy/Documents/proj/AU.txt",sep="\t")
restaurant_data_BR = pd.read_csv("C:/Users/atrivedy/Documents/proj/BR.txt",sep="\t")
restaurant_data_CN = pd.read_csv("C:/Users/atrivedy/Documents/proj/CN.txt",sep="\t")
restaurant_data_FR = pd.read_csv("C:/Users/atrivedy/Documents/proj/FR.txt",sep="\t")
restaurant_data_US = pd.read_csv("C:/Users/atrivedy/Documents/proj/US.txt",sep="\t")


@app.route("/")
def jsonWorld():
    session['searchbody_session'] =  {  # default search P1
        "size": 1000,
        "query": {
            "term": {
                "error": 5
            }
        }
    }
    session['errorcode_session'] = 1
    with World() as world:
        script1, div1 = world.returnFigureComponents()
        return render_template("WorldJson.html", script=script1, div=div1)


stored_coordinates = {}

# ----------------redundant func below
@app.route('/data/', methods=['POST'])
def post_data():
    set_address = set()
    dict_time = {}

    es = Elasticsearch()
    response = es.search(index="coutry", body={
                                                "query": {
                                                    "term": {
                                                        "error": "cant"
                                                    }
                                                }
                                             }
                        )
    if response["hits"]["total"] >= 1:
        for hit in response['hits']['hits']:
            set_address.add(hit['_source']['name'])
            dict_time[hit['_source']['name']] = hit['_source']['timestamp']

    variable = {'x': [], 'y': [], 'name': [], 'time': []}
    geopy = Nominatim()
    for name in set_address:
        try: # if the name is already stored, fetch the coordinates, else geocode this name in the except block and also storing the coordinates
            variable['x'].append(stored_coordinates[name][0])
            variable['y'].append(stored_coordinates[name][1])
            #variable['name'].append(name)
        except:
            cir = geopy.geocode(name)
            variable['x'].append(cir.longitude)
            variable['y'].append(cir.latitude)
            stored_coordinates[name] = [cir.longitude, cir.latitude]  # store so that no need to use geocode again

        variable['name'].append(name)
        variable['time'].append(dict_time[name])
    return jsonify(variable)


# -------------global searchbody, errorcode

# --------------


@app.route('/stores/', methods=['GET','POST'])
def post_data_stores():
    print(session['searchbody_session'])
    es = Elasticsearch()
    variable = {'x': [], 'y': [],'nsn':[],'addressline':[], 'name': [], 'time': [], 'color': []}
    prioritycolors = {}
    prioritycolors[1] = "red"
    prioritycolors[2] = "yellow"
    prioritycolors[3] = 'fuchsia'
    prioritycolors[4] = 'aqua'
   # global errorcode
    if request.method == 'GET':
        errorcode = request.args.get('d')
    #    global searchbody
        # if errorcode == '1':
        searchbody = {
            "size": 1000,
            "query": {
                "term": {
                    "error": int(errorcode)
                }
            }
        }
        session['searchbody_session'] = searchbody
        session['errorcode_session'] = errorcode

    response = es.search(index="stores_ecp", body=session['searchbody_session'],request_timeout=30)
    if response["hits"]["total"] >= 1:
        for hit in response['hits']['hits']:
            if hit['_source']['ISO2'] == 'AU':
                variable['x'].append(float(restaurant_data_AU.loc[restaurant_data_AU['NatlStrNumber'] == int(hit['_source']['nsn'])]['Longitude']))
                variable['y'].append(float(restaurant_data_AU.loc[restaurant_data_AU['NatlStrNumber'] == int(hit['_source']['nsn'])]['Latitude']))
            elif hit['_source']['ISO2'] == 'BR':
                variable['x'].append(float(restaurant_data_BR.loc[restaurant_data_AU['NatlStrNumber'] == int(hit['_source']['nsn'])]['Longitude']))
                variable['y'].append(float(restaurant_data_BR.loc[restaurant_data_AU['NatlStrNumber'] == int(hit['_source']['nsn'])]['Latitude']))
            elif hit['_source']['ISO2'] == 'CN':
                variable['x'].append(float(restaurant_data_CN.loc[restaurant_data_CN['NatlStrNumber'] == int(hit['_source']['nsn'])]['Longitude']))
                variable['y'].append(float(restaurant_data_CN.loc[restaurant_data_CN['NatlStrNumber'] == int(hit['_source']['nsn'])]['Latitude']))
            elif hit['_source']['ISO2'] == 'FR':
                variable['x'].append(float(restaurant_data_FR.loc[restaurant_data_FR['NatlStrNumber'] == int(hit['_source']['nsn'])]['Longitude']))
                variable['y'].append(float(restaurant_data_FR.loc[restaurant_data_FR['NatlStrNumber'] == int(hit['_source']['nsn'])]['Latitude']))
            elif hit['_source']['ISO2'] == 'US':
                variable['x'].append(float(restaurant_data_US.loc[restaurant_data_US['NatlStrNumber'] == int(hit['_source']['nsn'])]['Longitude']))
                variable['y'].append(float(restaurant_data_US.loc[restaurant_data_US['NatlStrNumber'] == int(hit['_source']['nsn'])]['Latitude']))
            variable['name'].append(hit['_source']['name'])
            variable['time'].append(hit['_source']['timestamp'])
            variable['color'].append(prioritycolors[int(session['errorcode_session'])])
            variable['nsn'].append(hit['_source']['nsn'])
            variable['addressline'].append(hit['_source']['addressline'])

    return jsonify(variable)


@app.route('/circleAsCDS')
def worldJsonWithCircleCds():
    with WorldCircleColumnDataSource() as world:
        script, div = world.returnFigureComponents()
        return render_template("WorldJson.html", script=script, div=div)


@app.route('/storesCDS/', methods=['GET','POST'])
def post_data_storesCDS():
    es = Elasticsearch()
    variable = {'x': [], 'y': [],'nsn':[],'addressline':[], 'name': [], 'time': [], 'color': [], 'ISO2':[]}
    prioritycolors = {}
    # red yellow fuchsia aqua
    prioritycolors[1] = "blue"
    prioritycolors[2] = "blue"
    prioritycolors[3] = 'blue'
    prioritycolors[4] = 'blue'
   # global errorcode
    if request.method == 'GET':
        errorcode = request.args.get('d')
    #    global searchbody
        # if errorcode == '1':
        searchbody = {
            "size": 1000,
            "query": {
                "term": {
                    "error": int(errorcode)
                }
            }
        }
        response = es.search(index="stores_ecp", body=searchbody,request_timeout=30)
        if response["hits"]["total"] >= 1:
            for hit in response['hits']['hits']:
                #variable['x'].append(float(restaurant_data.loc[restaurant_data['NatlStrNumber'] == int(hit['_source']['nsn'])]['Longitude']))
                #variable['y'].append(float(restaurant_data.loc[restaurant_data['NatlStrNumber'] == int(hit['_source']['nsn'])]['Latitude']))
                if hit['_source']['ISO2'] == 'AU':
                    variable['ISO2'].append('AU')
                    variable['x'].append(float(
                        restaurant_data_AU.loc[restaurant_data_AU['NatlStrNumber'] == int(hit['_source']['nsn'])][
                            'Longitude']))
                    variable['y'].append(float(
                        restaurant_data_AU.loc[restaurant_data_AU['NatlStrNumber'] == int(hit['_source']['nsn'])][
                            'Latitude']))
                elif hit['_source']['ISO2'] == 'BR':
                    variable['ISO2'].append('BR')
                    variable['x'].append(float(
                        restaurant_data_BR.loc[restaurant_data_BR['NatlStrNumber'] == int(hit['_source']['nsn'])][
                            'Longitude']))
                    variable['y'].append(float(
                        restaurant_data_BR.loc[restaurant_data_BR['NatlStrNumber'] == int(hit['_source']['nsn'])][
                            'Latitude']))
                elif hit['_source']['ISO2'] == 'CN':
                    variable['ISO2'].append('CN')
                    variable['x'].append(float(
                        restaurant_data_CN.loc[restaurant_data_CN['NatlStrNumber'] == int(hit['_source']['nsn'])][
                            'Longitude']))
                    variable['y'].append(float(
                        restaurant_data_CN.loc[restaurant_data_CN['NatlStrNumber'] == int(hit['_source']['nsn'])][
                            'Latitude']))
                elif hit['_source']['ISO2'] == 'FR':
                    variable['ISO2'].append('FR')
                    variable['x'].append(float(
                        restaurant_data_FR.loc[restaurant_data_FR['NatlStrNumber'] == int(hit['_source']['nsn'])][
                            'Longitude']))
                    variable['y'].append(float(
                        restaurant_data_FR.loc[restaurant_data_FR['NatlStrNumber'] == int(hit['_source']['nsn'])][
                            'Latitude']))
                elif hit['_source']['ISO2'] == 'US':
                    variable['ISO2'].append('US')
                    variable['x'].append(float(
                        restaurant_data_US.loc[restaurant_data_US['NatlStrNumber'] == int(hit['_source']['nsn'])][
                            'Longitude']))
                    variable['y'].append(float(
                        restaurant_data_US.loc[restaurant_data_US['NatlStrNumber'] == int(hit['_source']['nsn'])][
                            'Latitude']))

                variable['name'].append(hit['_source']['name'])
                variable['time'].append(hit['_source']['timestamp'])
                variable['color'].append(prioritycolors[int(errorcode)])
                variable['nsn'].append(hit['_source']['nsn'])
                variable['addressline'].append(hit['_source']['addressline'])

        return jsonify(variable)


@app.teardown_appcontext
def initialize(obj):
    print("teardown")


@app.route('/popup')
def popup_template():
    return render_template("popup.html")


if __name__ == '__main__':
    app.run(debug=False)
