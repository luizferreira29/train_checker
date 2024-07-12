import streamlit as st
import requests
import json
import pprint
apikey = "W2MXFgz1fxg54B518oUO1lpfLVVbxUZy"
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import numpy as np

from json2xml import json2xml

from bs4 import BeautifulSoup
from datetime import datetime


st.title("Train checker for Vernouillet-Verneuil")
st.caption("This app allows you to check if your train is on time.")

def handle_train_check(url_param):
    url = f"https://prim.iledefrance-mobilites.fr/marketplace/stop-monitoring?MonitoringRef={url_param}"
    headers = {'Accept': 'application/json', 'apikey': apikey}
    req = requests.get(url, headers=headers).json()
    print('Status:',req)
    response_xml = json2xml.Json2xml(req, wrapper="all", pretty=True).to_xml()
    soup = BeautifulSoup(response_xml, features="xml")
    destination = []
    time_arrival = []
    status = []
    date_format = "%Y-%m-%dT%H:%M:%S.000Z"
    for train in soup.find_all("MonitoredVehicleJourney"):
        destination.append(train.find('DestinationName').text.strip())
        time = train.find('ExpectedArrivalTime').text
        date_obj = datetime.strptime(time, date_format)
        date = str(date_obj.hour) + "h", str(date_obj.minute) + "min"
        time_arrival.append(date)
        status.append(train.find('DepartureStatus').text)
    df = pd.DataFrame({"destination" : destination, "heure de passage" : time_arrival, "ok" : status})
    st.table(df)

if st.button("Vernouillet-Verneuil", type="primary"):
    handle_train_check("STIF:StopPoint:Q:41198:")

if st.button("Les clairières de Verneuil", type="primary"):
    handle_train_check("STIF:StopPoint:Q:41199:")
