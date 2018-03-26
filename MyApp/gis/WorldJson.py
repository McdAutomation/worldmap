import geopandas as gpd
from bokeh.plotting import figure

from MyApp.gis.conversions.returnCircleBokeh import returnCircle
from MyApp.gis.conversions.returnPolygonBokeh import returnPDS
from bokeh.models import HoverTool, TapTool, OpenURL
from bokeh.models.callbacks import CustomJS

filePath = r"./data/world_dest.json"

outFile = "./templates/patches.html"
p = gpd.read_file(filePath)

bokPatch = returnPDS(p)

figPatch = figure(title="first map with geocoding polygon", sizing_mode='stretch_both')
figPatch.axis.visible = False
ptch = figPatch.patches('x', 'y', source=bokPatch, line_color='black', line_width=0.3, legend='Patches')


def create_hover_tool_india():
    """Generates the HTML for the Bokeh's hover data tool on our graph."""
    hover_html = """
      <div>
        <span class="hover-tooltip">Country: @NAME
      </div>
        """
    return HoverTool(renderers=[ptch], tooltips=hover_html)


url = "http://www.colors.commutercreative.com/"

figPatch.add_tools(create_hover_tool_india())

#add points to map:

temp_points = gpd.read_file('./data/ne_110m_populated_places.json')
points = returnCircle(temp_points)
pt = figPatch.circle('x', 'y', source=points, size=5, color='yellow')


def create_hover_tool_points():
    hover_html = """
          <div>
            <span class="hover-tooltip">City: @NAME
          </div>
            """
    return HoverTool(renderers=[pt], tooltips=hover_html)


def create_pop_up():  # remember bokPatch is the source here which is ColumnDataSource
    tap_to_get = CustomJS(args=dict(source=bokPatch), code="""
        data = source.data;

        //var inds = cb_obj.source.attributes.selected['1d'].indices; 
        //d = cb_obj.data;
        var myWindow = window.open("", "MsgWindow", "top=200, left=200, width=500, height=500");


        var a = myWindow.document.createElement('a');
        var linkText = myWindow.document.createTextNode("Click Here!!");
        a.appendChild(linkText);
        a.title = "my title text";
        a.href = "http://www.google.com";
        myWindow.document.body.appendChild(a);

        selectedVariable = source.selected['1d'].indices;
        d = cb_obj.data;

        console.log(cb_data);
        console.log(cb_obj);
        console.log(selectedVariable);
        console.log(data["NAME"][selectedVariable[0]]); //extraction of attributes of selected glyph done!!!

        //myWindow.document.write(cb_data.geometries);

        //var ind = cb_obj.selected['1d'].index;
        //var country = cb_obj.get('NAME');
        //var st="anupam";     
        //myWindow.document.write("<p>hey there</p>");
        
        hr = 8;
        min=5;
        
        displayClock();
        drawClock();
    """)
    return TapTool(renderers=[pt], callback=tap_to_get)


figPatch.add_tools(create_hover_tool_points())
figPatch.add_tools(create_pop_up())

def sampleFunct():
    print("executed")


