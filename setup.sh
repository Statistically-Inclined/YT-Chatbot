#!/bin/bash
pip install -r requirements.txt
streamlit run app.py --server.port=10000 --server.enableCORS=false