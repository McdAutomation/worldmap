from flask import Flask, render_template, request
from bokeh.embed import components
from MyApp.gis.getFigGeography import figGeography
from MyApp.gis.WorldJson import ptch,figPatch

app = Flask(__name__)


@app.route("/")
def jsonWorld():
    script1, div1 = components(figPatch)
    return render_template("WorldJson.html", script=script1, div=div1, )


if __name__ == '__main__':
    app.run(debug=True)