from flask import Flask, render_template, request, jsonify
from bokeh.embed import components
from MyApp.gis.getFigGeography import figGeography
from MyApp.gis.WorldJson import ptch, figPatch
from geopandas.tools import geocode
from elasticsearch import Elasticsearch

key = 'AIzaSyCl9gfvmpQoyisgz-lt1epZkU5iVMaoLM0'

app = Flask(__name__)


@app.route("/")
def jsonWorld():
    script1, div1 = components(figPatch)
    return render_template("WorldJson.html", script=script1, div=div1, )


@app.route('/data/', methods=['POST'])
def post_data():
    global index

    list_address = set()
    es = Elasticsearch()
    response = es.search(index="country", body={
        "query": {
            "term": {
                "error": "missing"
            }
        }
    }
                         )
    if response["hits"]["total"] >= 1:
        for hit in response['hits']['hits']:
            list_address.add(hit['_source']['address'])

    variable = {'x': [], 'y': []}
    for name in list_address:
        cir = geocode(name, api_key=key)
        temp = cir['geometry'].apply(lambda p: (p.x, p.y))
        variable['x'].append(temp[0][0])
        variable['y'].append(temp[0][1])
        # print(variable[0][0])
    return jsonify(variable)


if __name__ == '__main__':
    app.run(debug=True)