from django.shortcuts import render
import requests
import json
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import io
import urllib,base64
import plotly.graph_objs as go


# Create your views here.
def home(request):
    # search = ""
    # if 'search' in request.GET and request.GET['search']:
    #     search = request.GET['search']
    # print(search)
    url = "https://covid-193.p.rapidapi.com/statistics"

    headers = {
        'x-rapidapi-host': "covid-193.p.rapidapi.com",
        'x-rapidapi-key': "8e22026da2mshafdd0174440b8c0p1f1001jsned5eb3513fd1"
        }

    response = requests.request("GET", url, headers=headers).json()

    # print(response)

    data = response['response']
    # print(data)
    print("length of data: ",len(data))
    c = []
    t = []
    for i in range(8):
        c.append(data[i]['country'])
        t.append(data[i]['cases']['total'])
    print("countries",c)
    print("total cases: ",t)
    plt.bar(c,t,color = 'blue',width = 0.2)
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf,format = 'png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    fig1 = go.Figure(data=go.Scatter(x=c, y=t))
    graph1 = fig1.to_html(full_html=False, default_height=400, default_width=500)

    return render(request,'home.html',{'data':uri,'data1':graph1})

def search(request):
    url = "https://covid-193.p.rapidapi.com/statistics"

    querystring = {"country":request.GET['search']}

    headers = {
        'x-rapidapi-host': "covid-193.p.rapidapi.com",
        'x-rapidapi-key': "8e22026da2mshafdd0174440b8c0p1f1001jsned5eb3513fd1"
        }

    response = requests.request("GET", url, headers=headers, params=querystring).json()

    data = response['response']

    d = data[0]
    print(d)

    c = request.GET['search']
    l = ['recovered','deaths','new','critical']
    v = [d['cases']['recovered'],d['deaths']['total'],d['cases']['new'],d['cases']['critical']]
    print(c,l,v)
    
    colors= ['violet','grey','blue','red']
    data = [go.Bar(
   x = l,
   y = v,
   marker_color=colors
    )]
    #BarGraph
    fig = go.Figure(data=data)
    graph = fig.to_html(full_html=False, default_height=500, default_width=300)

    #LineGraph
    fig1 = go.Figure(data=go.Scatter(x=l, y=v))
    graph1 = fig1.to_html(full_html=False, default_height=500, default_width=300)

    #PieCHart
    fig2 = go.Figure(data=[go.Pie(labels=l, values=v)])
    graph2 = fig2.to_html(full_html=False, default_height=500, default_width=700)


    context = {
        'country':request.GET['search'],
        'all':d['cases']['total'],
        'recovered':d['cases']['recovered'],
        'deaths':d['deaths']['total'],
        'new':d['cases']['new'],
        'critical':d['cases']['critical'],
        'uri': graph,
        'uri1': graph1,
        'uri2': graph2

    }
    return render(request, 'index.html',context)