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
    st.write(stream)
    #------
#--------------------
#DEFINITIONS
#python list to markdown lists
def listToMarkdown(list,column):
     list = ["-"+ i + "\n" for i in list]
     list = "".join(list)
     return column.markdown(list)

#creates iframe form commit
#--------------------
def commit2viewer():
       embed_src = "https://app.speckle.systems/projects/8e72066ad8/models/31db6b4639#embed=%7B%22isEnabled%22%3Atrue%7D"
       st.write(embed_src)
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
    conncetorList = len([c.sourceApplication for c in commits])
    connectorCol.metric(label="Number of Connectors", value = conncetorList)
    #st.write([c.sourceApplication for c in commits])
    #------

    #------
    #Contributor Carts💳
    contributorCol.metric(label="Number of Contributtors ", value = len(stream.collaborators))
    #------


#--------------------