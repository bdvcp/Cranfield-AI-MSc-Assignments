import pandas as pd
import matplotlib.pyplot as plt
import networkx as netx
import cartopy.crs as ccrs
import cartopy.feature as cfeature

'''################ LOAD DATA ####################'''
dataAirports = pd.read_csv("Cleaned_Airports_Data.csv",encoding="unicode_escape")#
dataAirports = dataAirports.set_index("id")#
FlightsData = pd.read_csv("Cleaned_Flights_Data.csv")
Flights_us = FlightsData[(FlightsData.Target_Country == "USA")#
                          & (FlightsData.Source_Country == "USA")#
                          & (FlightsData.TimeSeries == 200307)]

Flights_uk = FlightsData[(FlightsData.Target_Country == "UK")#
                          & (FlightsData.Source_Country == "UK")#
                          & (FlightsData.TimeSeries == 200307)]#

Flights_au = FlightsData[(FlightsData.Target_Country == "Australia")#
                          & (FlightsData.Source_Country == "Australia")#
                          & (FlightsData.TimeSeries == 200307)]#

Flights_ch = FlightsData[(FlightsData.Target_Country == "China")#
                          & (FlightsData.Source_Country == "China")#
                          & (FlightsData.TimeSeries == 200307)]#

data =     {"Country":       ["USA", "China", "UK", "Australia"],#
            "Minimum Label": [500000,52000,55000,11000],#
            "Edge Width":    [0.4,1,2,5],#
            "Location": [[-177,-66,19,59.2],[73, 135, 18, 50],#
                         [-8.3,1.8,49,60],[113, 155, -42, -9]]}#

plotData = pd.DataFrame(data).set_index("Country").transpose()#.
'''##############################################'''

def CreateGraph(country, airportData, connections, plotInfo):

    set_weights = connections[["Source","Target","Weight"]].values#
    graph = netx.Graph()#
    graph.add_weighted_edges_from(set_weights)#
    
    airports = airportData[(airportData.country == country)]#
    
    position = {airport: (x["Lon"], x["Lat"])#
                for airport, x in airports.to_dict(#
                        "index").items()}#
    
    degree = netx.degree(graph, weight="weight")#
    masses = [degree[node] for node in graph.nodes]#
    sizes = [(((degree[node] - min(masses)) * 283) / (#
        max(masses) - min(masses))) + 1 for node in graph.nodes]#
       
    labels = {node: node if degree[node] >= plotInfo[country][0] else ""#
              for node in graph.nodes}#
    
    all_masses = [data["weight"] for nodes1, nodes2, data in graph.edges(data=True)]#
    edgeWidth = [(((weight - min(all_masses)) * (plotInfo[country][1] - 0.075)) / (#
        max(all_masses) - min(all_masses))) + 0.075#
                  for weight in all_masses]#
    
    crs = ccrs.PlateCarree()#
    fig, ax = plt.subplots(1,1 ,figsize=(17, 8) ,subplot_kw =dict(projection=crs))#
    ax.coastlines()#
    ax.add_feature(cfeature.BORDERS)#
    ax.set_extent(plotInfo[country][2])#
    ax.gridlines()#
    netx.draw_networkx(graph, ax=ax,font_size=17,alpha=0.6,#
                       width=edgeWidth,node_size=sizes,labels=labels,pos=position,#
                     node_color=sizes,#
                     cmap=plt.cm.plasma)#
    plt.show()#
    return graph#
    
def DistributionDegree(country, G):#
    degree = netx.degree(G, weight="weight")#
    seq = sorted([x for y, x in degree],reverse = True )#
    plt.semilogy(seq,marker = ".",label= "July 2003", color="green")#
    plt.ylabel(" Weighted Degree ")#
    plt.xlabel(" Rank ")#
    plt.title(" Degree Distribution" + " for " + str(country))#
    plt.show()#

def BetweenDegree(country, G):#
    a = list(netx.betweenness_centrality( G, endpoints=False ,normalized = False ).items())#
    w = [f for m,f in  sorted(G.degree, key = lambda w:w[0], reverse  = False)]#
    y = [f for m,f in  sorted(a, key= lambda w:w[0], reverse=False)]#
    plt.plot( w ,y,"." )#
    plt.xlabel( " Weighted-Degree ")#
    plt.xscale( "log" )#
    plt.title("Degree - Betweenness "+"for " +str( country ))#
    plt.ylabel( " Betweenness " )#
    plt.yscale( "log" )#
    plt.show()#

def assortativity(graph):#
    return netx.degree_pearson_correlation_coefficient( graph,weight= "weight" )#

def CommunityCore(country, G):#
    figure,x =plt.subplots(#
        1,1, figsize=(16,7))#
    label="07/2003"#
    listC=[]#
    try:#
        coreC = netx.k_core(#
            G,core_number#
            = netx.core_number(G))#
    except netx.exception.NetworkXError:#
        g=G#
        g.remove_edges_from( list( netx.selfloop_edges( g )))#
        coreC = netx.k_core(g, core_number=netx.core_number(g))#
    listC.append( len( coreC ))#
    netx.draw_networkx( coreC,ax=x ,label=label,alpha =0.8, node_color ="yellow", edge_color ="green")#
    plt.title(country + "  Core  Community ")#
    plt.show()#
    return listC#

def CommunityCoreK(country, G, s):#S is input from CommunityCore
    a = pd.DataFrame([(e,r) for (e,r) in sorted(G.degree, key =lambda z: z[1],#
                                                reverse=True) ] ).rename( columns={0: "id", 1:"degree"#
                                                                                   },inplace =False)#
    a["rank"] = a["degree"].rank(ascending = False)#
    ll =[]#
    for id in a["id"]:#
        c= 0#
        for i in G.neighbors( id):###
            if a[ a["id"]==i ].iloc[0]["degree"]>a[ a["id"]==id ].iloc[0]["degree"]:#
                c+=1#
        ll.append(c)#
    z= pd.DataFrame([r for (e,r) in sorted(G.degree, key = lambda z: z[1]#
                                            , reverse = False)]).rank( #
                                                axis=0, method ="first" ).to_numpy()#
    w= ll#
    plt.plot( z,w, color = "green")#
    plt.xscale( "linear" )#
    plt.yscale( "linear" )#
    plt.title(country + "  Core  Community ")#
    plt.legend(["The  " + country + "  Core  Community  Size  is:  {}".format(s)])#
    plt.xlabel(" Ranked  Node  Number ")#
    plt.ylabel(" Connections  to  Nodes  with  higher  degree ")#
    plt.show()#
                  
USA = CreateGraph("USA",dataAirports,Flights_us, plotData)
DistributionDegree("USA", USA)
BetweenDegree("USA", USA)
print("the assortativity of the USA is: "+str(assortativity(USA)))
x = CommunityCore("USA", USA)
CommunityCoreK("USA", USA, x)

UK = CreateGraph("UK",dataAirports,Flights_uk, plotData)
DistributionDegree("UK", UK)
BetweenDegree("UK", UK)
print("the assortativity of the UK is: "+str(assortativity(UK)))
x = CommunityCore("UK", UK)
CommunityCoreK("UK", UK, x)

Australia = CreateGraph("Australia",dataAirports,Flights_au, plotData)
DistributionDegree("Australia", Australia)
BetweenDegree("Australia", Australia)
print("the assortativity of Australia is: "+str(assortativity(Australia)))
x = CommunityCore("Australia", Australia)
CommunityCoreK("Australia", Australia, x)

China = CreateGraph("China",dataAirports,Flights_ch, plotData)
DistributionDegree("China", China)
BetweenDegree("China", China)
print("the assortativity of China is: "+str(assortativity(China)))
x = CommunityCore("China", China)
CommunityCoreK("China", China, x)

