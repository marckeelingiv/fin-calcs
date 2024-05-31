import os
import streamlit as st
# Get the Google Adds link from environment variables
google_adds_link = os.getenv("GOOGLE_ADDS_LINK")

def add_script_to_header():
    add_script_js = f"""
    <script>
    (function() {{
        var script = document.createElement('script');
        script.src = '{google_adds_link}';
        script.crossOrigin = 'anonymous';
        script.async = true;
        document.head.appendChild(script);
    }})();
    </script>
    """
    
    st.markdown(add_script_js, unsafe_allow_html=True)