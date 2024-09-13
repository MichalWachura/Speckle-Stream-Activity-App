#--------------------
# IMPORTING LIBRARIES
#import streamlit
import streamlit as st
import streamlit.components.v1
#import speackle 
from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_account_from_token
#import pandas
import pandas as pd
#import plotly
import plotly.express as px
#--------------------

#--------------------
#PAGE CONGIG
st.set_page_config(
    page_title="Speckle Stream Activity",
    page_icon="📊"
)
#--------------------
#CONTAINERS
header = st.container()
input = st.container()
viewer = st.container()
report = st.container()
graphs = st.container()
#--------------------
#--------------------
#HEADER
#Page Header
with header:
    st.title("Speckle Stream Activity App 📊")
#about the app
with header.expander("About this app 🔽",expanded=True):
    st.markdown("""
This is a beginner web app developed using Streamlit.My goal was to understand how to interact with SpeckleAPI using SpecklePy,analyze what is received and its structure.This was interesting experiment 
    """)
#--------------------

#--------------------
#INPUTS
with input:
    st.subheader("Inputs")
    #------
    #Columns for inputs
    serverCol,tokenCol = st.columns([1,2])
    #User inputs boxes
    speckleServer = serverCol.text_input("server URL","speckle.xyz")
    speckleToken = tokenCol.text_input('Speckle Token',"377e12e1b5244da052946597d28c8ff75b1436d322")

    #------
    #Client 
    client  = SpeckleClient(host = speckleServer)
    #get account from tocken
    account = get_account_from_token(speckleToken,speckleServer)
    #Authenticate
    client.authenticate_with_account(account)
    #------
    # streams list👇
    streams = client.stream.list()
    #Get Strem Names
    streamsNames = [s.name for s in streams]
    #Drop down for stream selection 
    selectedName = st.selectbox(label = "Select your stream ",options = streamsNames )
    #selected Stream
    stream = client.stream.search(selectedName)[0]
    #stream Branches🌳
    branches = client.branch.list(stream.id)
    #stream Commits 🏹
    commits = client.commit.list(stream.id,limit=100)
   
    #------
#--------------------
#DEFINITIONS
#python list to markdown lists (already provided)
def listToMarkdown(list,column):
     list = ["-"+ i + "\n" for i in list]
     list = "".join(list)
     return column.markdown(list)

#creates iframe form commit
#--------------------
def commit2viewer():
       embed_src = "https://app.speckle.systems/projects/8e72066ad8/models/31db6b4639#embed=%7B%22isEnabled%22%3Atrue%7D"
       
       return st.components.v1.iframe(src = embed_src,height=400)


#--------------------

#--------------------
#SPECKLE VIEWER

with viewer:
    st.subheader("Latest Commit 👇")
    commit2viewer()#commits[0])
#https://app.speckle.systems/projects/8e72066ad8/models/#embed=%7B%22isEnabled%22%3Atrue%7D

#--------------------

#--------------------
#Report
with report:
    st.subheader("Statistics")
    #------
    #Columns for cards
    branchCol,commitCol,connectorCol,contributorCol = st.columns(4)
    #------

    #------
    #Branch Card💳
    branchCol.metric(label="Number of braches", value = stream.branches.totalCount )
    #list of Branches
    
    listToMarkdown([b.name for b in branches],branchCol)
    #------

    #------
    #Commits Carts💳
    commitCol.metric(label="Number of Commits", value = len(commits))
    #st.write(commits)
    #------

    #Connector Carts💳
    #connector list
    connectorList = [c.sourceApplication for c in commits]
    #conectors names
    connectorNames = list(dict.fromkeys(connectorList))
    connectorCol.metric(label="Number of Connectors ", value = len(dict.fromkeys(connectorList)))
    listToMarkdown(connectorNames,connectorCol)
    #------

    #------
    #Contributor Carts💳
    contributorCol.metric(label="Number of Contributtors ", value = len(stream.collaborators))
    #contributors name
    contributorsName = list(dict.fromkeys([col.name for col in stream.collaborators]))
    #contributor list
    listToMarkdown(contributorsName,contributorCol)
    #------

#--------------------
with graphs:
     st.subheader("Graphs")
     #columns for Charts
     branch_graph_col,connector_graph_col,collaborator_graph_col = st.columns([2,1,1])
    #------
    #branch graph📊
     branch_counts = pd.DataFrame([[b.name,b.commits.totalCount] for b in branches])
    #rename clumns 
     branch_counts.columns = ['branchName',"totalCommits"]
    #create graph 
     branch_count_graph = px.bar(branch_counts,x = branch_counts.branchName, y= branch_counts.totalCommits,color = branch_counts.branchName)
     branch_count_graph.update_layout(showlegend = False,height=220,margin = dict(l=1,r=1,t=1,b=1))
     branch_graph_col.plotly_chart(branch_count_graph,use_container_width=True)
    #------

    #------
    #Connector Chart
     commits = pd.DataFrame.from_dict([c.dict() for c in commits])
    #get apps form data frame
     apps = commits['sourceApplication']
    #reset index apps
     apps = apps.value_counts().reset_index()
     #rename columns
     apps.columns = ["app","count"]
     #donut chart
     fig = px.pie(apps,names=apps['app'],values = apps['count'],hole=0.5 )
     fig.update_layout(
          showlegend = False,
          margin=dict(l=2,r=2,t=2,b=2),
          height = 200
        )
     connector_graph_col.plotly_chart(fig,use_container_width=True)
    #------
    #------
    #Collaborator Chart
     authors = commits["authorName"].value_counts().reset_index()
     #rename columns
     authors.columns = ['author','count']
     #create chart
     authorFig = px.pie(authors,names=authors['author'],values=authors['count'],hole=0.5)
     authorFig.update_layout(
          showlegend = False,
          margin=dict(l=1,r=1,t=1,b=1),
          height = 200
        )
     collaborator_graph_col.plotly_chart(authorFig,use_container_width=True)
    #------





#--------------------
