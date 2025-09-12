# pages/1_Image_Analyzer.py

import streamlit as st
from PIL import Image
import google.generativeai as genai
import io
import re
import dbm as db # Import your database module

def parse_response(response_text):
    """Parses the bulleted list from the Gemini response."""
    items = []
    # Regex to find item name and number, assuming format: * Item Name: Quantity
    lines = response_text.strip().split('\n')
    for line in lines:
        match = re.match(r"\*\s*(.*?):\s*(\d+)", line)
        if match:
            item_name = match.group(1).strip()
            # Clean up the name by removing common punctuation if needed
            item_name = item_name.strip(':- ') 
            quantity = int(match.group(2).strip())
            items.append({"item_name": item_name, "quantity": quantity})
    return items

st.title("📸 Image Inventory Analyzer")
st.write("Upload an image of your inventory to get an automated count.")

# --- API Configuration ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Error configuring API. Check your `.streamlit/secrets.toml` file.")
    st.stop()
# --- End API Configuration ---

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    st.write("Analyzing...")

    # Prepare data
    with io.BytesIO() as buffer:
        image.save(buffer, format=image.format)
        image_bytes = buffer.getvalue()
    
    mime_type = f"image/{image.format.lower()}"
    
    # Generate content
    with st.spinner('Contacting Gemini API...'):
        response = model.generate_content([
            "You are an inventory management bot. Your only goal is to output a bulleted list of item names and numbers based on the input image. Format as: '* Item Name: Quantity'. Do not include any other text, headings, or commentary.",
            {"mime_type": mime_type, "data": image_bytes}
        ])

    st.subheader("Inventory List from Image Analysis")
    st.code(response.text, language='text')

    # Parse and store the data
    inventory_items = parse_response(response.text)
    
    st.subheader("Confirm and Update Database")
    if inventory_items:
        df = st.dataframe(inventory_items, use_container_width=True)
        
        if st.button("Update Database with Above Items"):
            for item in inventory_items:
                # Assuming the app always inserts, not updates, for simplicity.
                # For a real system, you'd check if the item exists and update quantity.
                db.insert_item(item['item_name'], item['quantity'], uploaded_file.name)
            
            st.success("Database updated successfully! Navigate to the 'Inventory Manager' page to view changes.")
            
    else:
        st.warning("Could not parse any items from the image response. Please ensure the model output is in the requested format.")
