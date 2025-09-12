# app.py
import streamlit as st

st.set_page_config(
    page_title="Multi-Page Inventory App",
    page_icon="📦"
)

st.title("📦 Welcome to the Smart Inventory System")
st.sidebar.success("Select a page above.")

st.markdown("""
This application uses the Gemini API to analyze inventory from an image and stores the data in a local SQLite database.

**Pages:**
1.  **Image Analyzer:** Upload an image of your inventory (e.g., shelves, boxes) to automatically count items and populate the database.
2.  **Inventory Manager:** View, manually update, and delete items from your stored inventory list.
""")