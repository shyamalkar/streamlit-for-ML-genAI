import streamlit as st 

from st_link_analysis import st_link_analysis, NodeStyle, EdgeStyle
from st_link_analysis.component.icons import SUPPORTED_ICONS
import json


st.set_page_config(layout="wide")

# st.write(",". join(Supported_ICONS))

with open("/Users/shyamalkar/Desktop/Python_project/py_project_st_lit/network.json", 'r') as f:
    elements = json.load(f)

edge_style = [
    EdgeStyle['Founde']
]
