@ECHO OFF
cd %~dp0\
pip install -r requirements.txt
call streamlit run app.py
