import geopandas as gpd
from bokeh.plotting import figure
from flask import request
from MyApp.gis.conversions.returnPolygonBokeh import returnPDS
from bokeh.models import HoverTool, TapTool, OpenURL
from bokeh.models.callbacks import CustomJS
from bokeh.embed import components
from bokeh.models import AjaxDataSource, ColumnDataSource

url = "http://www.colors.commutercreative.com/"


class World:

    def __init__(self):
        self.figPatch = figure(title="World Map", sizing_mode='stretch_both')
        self.figPatch.axis.visible = False
        self.renderedBy = {}

    def __enter__(self):
        print("entered")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("exited")
        pass

    def drawMap(self):
        filePath = r"./data/world_dest.json"
        p = gpd.read_file(filePath)
        bokPatch = returnPDS(p)
        self.ptch = self.figPatch.patches('x', 'y', source=bokPatch, line_color='black', line_width=0.3, legend='Patches')

    def create_hover_tool_map(self):
        """Generates the HTML for the Bokeh's hover data tool on our graph."""
        hover_html = """
          <div>
            <span class="hover-tooltip">Country: @NAME
          </div>
            """
        return HoverTool(renderers=[self.renderedBy['patch']], tooltips=hover_html)


    def returnFigureComponents(self):
        filePath = r"./data/world_dest.json"
        p = gpd.read_file(filePath)
        bokPatch = returnPDS(p)

        self.renderedBy['patch'] = self.figPatch.patches('x', 'y', source=bokPatch, line_color='black', line_width=0.3,
                                                    legend='World', name='patchCustomName')


        #  for Ajax calls

        cir = AjaxDataSource(data_url=request.url_root + 'stores/', #change to listen to different endpoints
                             polling_interval=3000, mode='replace', name='circleAjax')

        cir.data = dict(x=[], y=[], name=[], color=[])

        pt = self.figPatch.circle(x='x', y='y', source=cir, size=5, color='color', legend='Restaurant')


        def create_pop_up_marker():  # remember bokPatch is the source here which is ColumnDataSource
            tap_to_get = CustomJS(args=dict(source=cir), code="""
            
                window.toBeClearedTimer = 1; // clear timer on next click
                window.drawnTimer = 1;
                
                data = source.data;

                //var inds = cb_obj.source.attributes.selected['1d'].indices; 
                //d = cb_obj.data;
                var popupWindow = window.open("/popup", "MsgWindow", "top=200, left=200, width=800, height=500");


                /*var a = myWindow.document.createElement('a');
                var linkText = myWindow.document.createTextNode("Click Here!!");
                a.appendChild(linkText);
                a.title = "my title text";
                a.href = "http://www.google.com";
                myWindow.document.body.appendChild(a);*/
                

                selectedVariable = source.selected['1d'].indices;
                //d = cb_obj.data;

                //console.log(cb_data);
                //console.log(cb_obj);
                //console.log(selectedVariable);
                //console.log(data["NAME"][selectedVariable[0]]); //extraction of attributes of selected glyph done!!!

                //myWindow.document.write(cb_data.geometries);

                //var ind = cb_obj.selected['1d'].index;
                //var country = cb_obj.get('NAME');
                //var st="anupam";     
                //myWindow.document.write("<p>hey there</p>");
                //ctry_name = data['name'][selectedVariable];
                //console.log(ctry_name);

                var arr_timedata= data['time'][selectedVariable].split(':');
                hr = parseInt(arr_timedata[0]);
                min = parseInt(arr_timedata[1]);

                //ctx.restore();
                ctx.clearRect(-100, -100, canvas.width, canvas.height);
                window.color = JSON.stringify(data['color'][selectedVariable]);
                console.log(window.color);
                if (window.color == JSON.stringify("red")){
    window.minuteSLA = 15;
                }else if(window.color == JSON.stringify("yellow")){
                    window.minuteSLA = 45;
                }else if(window.color == JSON.stringify("fuchsia")){
                    window.minuteSLA = 90;
                }else if(window.color == JSON.stringify("aqua")){
                    window.minuteSLA = 120;
                }
                ctx.fillStyle = JSON.parse(window.color);
                console.log(window.minuteSLA);
                ctx.beginPath();
                ctx.moveTo(0,0);
                var now = new Date();
                var hour = now.getHours();
                var minute = now.getMinutes();
                var second = now.getSeconds();
                
                var timeMinutes = (hour - hr)*60*60 + (minute - min)*60+second;
                
                if( (timeMinutes/60 >= window.minuteSLA ) || (hour<hr) || ((minute<min) && (hour==hr)) ){
                    //clearInterval(window.refreshIntervalId);
                    ctx.clearRect(-radius-5, -radius-5, canvas.width, canvas.height);
                    animCtx.clearRect(-radius-5, -radius-5, canvas.width, canvas.height);
                    clearInterval(window.refreshIntervalId);
                    ctx.arc(0, 0, radius, -Math.PI/2, 3*Math.PI/2);
                    console.log(window.color);
                    ctx.fillStyle = window.color;
                    ctx.fill();
                    console.log("cleared");
                    console.log(hr+" "+hour+" "+timeMinutes/60);
                  }
                else{
                     window.refreshIntervalId = setInterval(drawClock, 1000/60); // to stop later
                     console.log("started");
                }              
                
                //set data to pop up window in following code
                console.log(data['name'][selectedVariable]);
                //popupWindow.document.getElementById("area").innerHTML = data['name'][selectedVariable];
                
                popupWindow.window.onload = function() {
                    popupWindow.document.getElementById('nsn').innerHTML = data['nsn'][selectedVariable];
                    popupWindow.document.getElementById('area').innerHTML = data['name'][selectedVariable];
                    popupWindow.document.getElementById('time').innerHTML = data['time'][selectedVariable];
                    popupWindow.document.getElementById('fullName').innerHTML = data['addressline'][selectedVariable];           
                }
            """)
            return TapTool(renderers=[pt], callback=tap_to_get)

        def create_hover_tool_marker():
            hover_html = """
                  <div>
                    <span class="hover-tooltip">City: @name
                  </div>
                    """
            hover_to_get = CustomJS(args=dict(source=cir), code="""
            var hovered_ind = cb_data.index['1d'].indices[0];
            data = source.data;
            if(hovered_ind != undefined){
                //console.log('inside', hovered_ind);
                //console.log('inside', cb_data['geometry']);
                
                //console.log("this is the end , my only friend"+data['time'][hovered_ind]);
                             
                var arr_timedata= data['time'][hovered_ind].split(':');
                hr = parseInt(arr_timedata[0]);
                min = parseInt(arr_timedata[1]);

                //ctx.restore();
                ctx.clearRect(-100, -100, canvas.width, canvas.height);
                window.color = JSON.stringify(data['color'][hovered_ind]);
                console.log(window.color);
                if (window.color == JSON.stringify("red")){
    window.minuteSLA = 15;
                }else if(window.color == JSON.stringify("yellow")){
                    window.minuteSLA = 45;
                }else if(window.color == JSON.stringify("fuchsia")){
                    window.minuteSLA = 90;
                }else if(window.color == JSON.stringify("aqua")){
                    window.minuteSLA = 120;
                }
                ctx.fillStyle = JSON.parse(window.color);
                console.log(window.minuteSLA);
                ctx.beginPath();
                ctx.moveTo(0,0);
                var now = new Date();
                var hour = now.getHours();
                var minute = now.getMinutes();
                var second = now.getSeconds();
                
                var timeMinutes = (hour - hr)*60*60 + (minute - min)*60+second;
                
                if( (timeMinutes/60 >= window.minuteSLA ) || (hour<hr) || ((minute<min) && (hour==hr)) ){
                    //clearInterval(window.refreshIntervalId);
                    ctx.clearRect(-radius-5, -radius-5, canvas.width, canvas.height);
                    animCtx.clearRect(-radius-5, -radius-5, canvas.width, canvas.height);
                    clearInterval(window.refreshIntervalId);
                    ctx.arc(0, 0, radius, -Math.PI/2, 3*Math.PI/2);
                    console.log(window.color);
                    ctx.fillStyle = window.color;
                    ctx.fill();
                    console.log("cleared");
                    console.log(hr+" "+hour+" "+timeMinutes/60);
                  }
                else{
                     window.refreshIntervalId = setInterval(drawClock, 1000/60); // to stop later
                     console.log("started");
                }              
                
                
            }
            """)
            return HoverTool(renderers=[pt], tooltips=hover_html, callback=hover_to_get)

        self.figPatch.add_tools(create_pop_up_marker())
        return components(self.figPatch)


class WorldCircleColumnDataSource:
    def __init__(self):
        self.figPatch = figure(sizing_mode='stretch_both',output_backend="webgl")
        self.figPatch.axis.visible = False
        self.renderedBy = {}

    def __enter__(self):
        print("entered")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("exited")

    def drawMap(self):
        filePath = r"./data/world_dest.json"
        p = gpd.read_file(filePath)
        bokPatch = returnPDS(p)
        self.ptch = self.figPatch.patches('x', 'y', source=bokPatch, line_color='black', line_width=0.3,
                                          legend='Patches')

    def create_hover_tool_map(self):
        """Generates the HTML for the Bokeh's hover data tool on our graph."""
        hover_html = """
          <div>
            <span class="hover-tooltip">Country: @NAME
          </div>
            """
        return HoverTool(renderers=[self.renderedBy['patch']], tooltips=hover_html)

    def returnFigureComponents(self):
        filePath = r"./data/world_dest_withcolor/world_dest_withcolor.shp"
        p = gpd.read_file(filePath)
        bokPatch = returnPDS(p)
        #color='COLOR' removed below, COLOR is a column in columndatasource bokeh
        # #DCDCDC
        self.renderedBy['patch'] = self.figPatch.patches('x', 'y', source=bokPatch, line_color='black', color='COLOR', line_width=0.3,
                                                         legend='World', name='bokehPatch')

        #  for Ajax calls

        cir = ColumnDataSource(dict(x=[], y=[], name=[], color=[], addressline=[], nsn=[], time=[]))

        pt = self.figPatch.circle(x='x', y='y', size=5, source=cir, color='color', legend='Restaurant', name='circleCDS')

        def create_pop_up_marker():  # remember bokPatch is the source here which is ColumnDataSource
            tap_to_get = CustomJS(args=dict(source=cir), code="""
            window.toBeClearedTimer = 1; // clear timer on next click
                window.drawnTimer = 1;
                
                data = source.data;

                //var inds = cb_obj.source.attributes.selected['1d'].indices; 
                //d = cb_obj.data;
                var popupWindow = window.open("/popup", "MsgWindow", "top=200, left=200, width=800, height=500");
                

                /*var a = myWindow.document.createElement('a');
                var linkText = myWindow.document.createTextNode("Click Here!!");
                a.appendChild(linkText);
                a.title = "my title text";
                a.href = "http://www.google.com";
                myWindow.document.body.appendChild(a);*/
                

                selectedVariable = source.selected['1d'].indices;
                console.log(Bokeh);
                //d = cb_obj.data;

                //console.log(cb_data);
                //console.log(cb_obj);
                //console.log(selectedVariable);
                //console.log(data["NAME"][selectedVariable[0]]); //extraction of attributes of selected glyph done!!!

                //myWindow.document.write(cb_data.geometries);

                //var ind = cb_obj.selected['1d'].index;
                //var country = cb_obj.get('NAME');
                //var st="anupam";     
                //myWindow.document.write("<p>hey there</p>");
                //ctry_name = data['name'][selectedVariable];
                //console.log(ctry_name);

                var arr_timedata= data['time'][selectedVariable].split(':');
                hr = parseInt(arr_timedata[0]);
                min = parseInt(arr_timedata[1]);

                //ctx.restore();
                ctx.clearRect(-100, -100, canvas.width, canvas.height);
                window.color = JSON.stringify(data['color'][selectedVariable]);
                console.log(window.color);
                if (window.color == JSON.stringify("red")){
    window.minuteSLA = 15;
                }else if(window.color == JSON.stringify("yellow")){
                    window.minuteSLA = 45;
                }else if(window.color == JSON.stringify("fuchsia")){
                    window.minuteSLA = 90;
                }else if(window.color == JSON.stringify("aqua")){
                    window.minuteSLA = 120;
                }
                ctx.fillStyle = JSON.parse(window.color);
                console.log(window.minuteSLA);
                ctx.beginPath();
                ctx.moveTo(0,0);
                var now = new Date();
                var hour = now.getHours();
                var minute = now.getMinutes();
                var second = now.getSeconds();
                
                var timeMinutes = (hour - hr)*60*60 + (minute - min)*60+second;
                
                if( (timeMinutes/60 >= window.minuteSLA ) || (hour<hr) || ((minute<min) && (hour==hr)) ){
                    //clearInterval(window.refreshIntervalId);
                    ctx.clearRect(-radius-5, -radius-5, canvas.width, canvas.height);
                    animCtx.clearRect(-radius-5, -radius-5, canvas.width, canvas.height);
                    clearInterval(window.refreshIntervalId);
                    ctx.arc(0, 0, radius, -Math.PI/2, 3*Math.PI/2);
                    console.log(window.color);
                    ctx.fillStyle = window.color;
                    ctx.fill();
                    console.log("cleared");
                    console.log(hr+" "+hour+" "+timeMinutes/60);
                  }
                else{
                     window.refreshIntervalId = setInterval(drawClock, 1000/60); // to stop later
                     console.log("started");
                }              
                
                //set data to pop up window in following code
                console.log(data['name'][selectedVariable]);
                //popupWindow.document.getElementById("area").innerHTML = data['name'][selectedVariable];
                
                popupWindow.window.onload = function() {
                    popupWindow.document.getElementById('nsn').innerHTML = data['nsn'][selectedVariable];
                    popupWindow.document.getElementById('area').innerHTML = data['name'][selectedVariable];
                    popupWindow.document.getElementById('time').innerHTML = data['time'][selectedVariable];
                    popupWindow.document.getElementById('fullName').innerHTML = data['addressline'][selectedVariable];           
                }
                console.log(selectedVariable);
            """)
            return TapTool(renderers=[pt], callback=tap_to_get)

        self.figPatch.add_tools(create_pop_up_marker())
        return components(self.figPatch)