import pandas as pd
from bokeh.plotting import figure, output_file, show, curdoc
from bokeh.models import Plot, LinearInterpolator, CategoricalColorMapper, ColumnDataSource, HoverTool, BoxZoomTool, ResetTool, PanTool, Circle, NumeralTickFormatter, DatetimeTickFormatter
from bokeh.models.glyphs import Line, MultiLine
from bokeh.models.markers import Circle
from bokeh.layouts import widgetbox, column
from bokeh.models.widgets import Dropdown
from bokeh.models.tickers import FixedTicker

full = pd.read_csv('b16to19.csv')


full.fillna(value=0, inplace=True)  #Turns NaN data into entries of zero
full.set_index(['total2016', 'total2017', 'total2018', 'total'])
full['depid'] =full['class_id'].map(str)+ full['department']
full= full.T   #Flips columns and rows in dataframe

entriescounter = list(range(0, 551))
depo = ""
circleyvals = []
for val in entriescounter:
    if depo == "":
        for value in full.iloc[4:8][val].values:
            circleyvals.append(value)
    if full.iloc[2][val] == depo:
        for value in full.iloc[4:8][val].values:
            circleyvals.append(value)
yvals= []
for valu in entriescounter:
    temp = []
    stre = str(full.iloc[2][valu])
    if depo == "":
        for val in full.iloc[4:8][valu].values:
            temp.append(val)
        yvals.append(temp)
        temp = []
    if stre == depo:
        for val in full.iloc[4:8][valu].values:
            temp.append(val)
        yvals.append(temp)
        temp = []
circlesource = ColumnDataSource(dict(   #instanstiates data for dots on the plot
    x = [2016, 2017, 2018, 2019]*(int(len(circleyvals)/4)),
    y = circleyvals
))
source = ColumnDataSource(dict(     #instantiates data for lines on the plot
    x=[[2016, 2017, 2018, 2019]]*len(full.columns),
    y=yvals,
    department = full.iloc[2],
    depid = full.iloc[3],
    fund = full.iloc[1]

))

hover = HoverTool(tooltips=[('Department: ', '@department'), ('For ', '@depid'), ('Amount', '$y{($ 0.00 a)}'), ('Fund ','@fund')])
p = figure(
    title = "Philadelphia City Budget 2016-2019",
    tools=[hover, BoxZoomTool(), ResetTool(), PanTool()])


deplist = []       #creates a list of Departments that data is provided for
for dep in list(full.iloc[2].unique()):
    dep = dep, dep
    deplist.append(tuple(dep))



p.circle(x='x', y='y',   #creates dotted plot
         size=7,
         source=circlesource)

p.multi_line(xs='x', ys='y', source=source)   #creates line plot
p.yaxis[0].formatter = NumeralTickFormatter(format="$0.00 a")    #formats y and x axes
p.xaxis[0].formatter = NumeralTickFormatter(format= "00")
p.xaxis.ticker = FixedTicker(ticks=[2016, 2017, 2018, 2019])
menu = sorted(deplist) #Alphabetizes Department list
dropdown = Dropdown(label="Department", button_type="warning", width=425, menu=menu)


def update(attr, old, new):
    depo = dropdown.value
    new = dropdown.value
    p.title.text = str(new)
    entriescounter = list(range(0, 551))
    circleyvals = []
    for val in entriescounter:
        if full.iloc[2][val] == depo:
            for value in full.iloc[4:8][val].values:
                circleyvals.append(value)
    yvals = []
    for valu in entriescounter:
        temp = []
        stre = str(full.iloc[2][valu])
        if stre == depo:
            for val in full.iloc[4:8][valu].values:
                temp.append(val)
        yvals.append(temp)
        temp = []
    new_dataml = dict(x=[[2016, 2017, 2018, 2019]]*len(full.columns), y=yvals, department = full.iloc[2], depid = full.iloc[3], fund = full.iloc[1])
    new_datac = dict(x = [2016, 2017, 2018, 2019]*(int(len(circleyvals)/4)),
    y = circleyvals)
    source.data = new_dataml
    circlesource.data = new_datac


dropdown.on_change('value', update)

curdoc().add_root(column(p, dropdown))



plot = figure()
plot.circle([1,2], [3,4])

