import requests
import streamlit as st
import time


st.set_page_config(page_title="Team Generator", layout="wide")

st.title("Team Generator")


project_details = st.text_area("Project Details")
if st.button("Generate Team"):
    with st.spinner("Generating team..."):
        start_time = time.time()
        api_url = "http://localhost:8000/project_details"
        
        response = requests.post(api_url, params={"project_details": project_details})
        
        if response.status_code == 200 and response.json().get("status") == "success":
            team_info = response.json().get("project_details")
            st.success(f"Team generated successfully in {int(time.time() - start_time)} seconds :)")
            st.write(team_info)
        else:
            st.error(f"Failed to generate team. Team cannot be found for the project details: {project_details}")