import streamlit as st
import dbm as db

def display_inventory_manager():
    st.title("📋 Inventory Manager")
    st.write("View, manually update, or delete inventory items.")

    # --- Display the current inventory ---
    st.header("Current Inventory")
    items = db.get_all_items()
    
    if items:
        # Create a list of dictionaries that Streamlit can easily handle
        # The database returns a tuple, so we need to convert it.
        # This is a good way to handle dynamic data.
        item_list = []
        for row in items:
            item_list.append({
                "ID": row[0],
                "Item Name": row[1],
                "Quantity": row[2],
                "Image Path": row[3]
            })

        # Use st.dataframe with column_config to set display names
        st.dataframe(item_list, use_container_width=True, hide_index=True)

    else:
        st.info("Your inventory is empty. Go to the 'Image Analyzer' page to start.")

    # --- Section for manual update/delete ---
    st.header("Manual Update / Delete")
    st.markdown("Use the **ID** from the table above to make changes.")
    
    with st.form("manual_form"):
        # The IDs from your database start at 1
        item_id = st.number_input("Item ID:", min_value=1, step=1, help="Enter the ID (first column) of the item to modify.")
        new_quantity = st.number_input("New Quantity:", min_value=0, step=1)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.form_submit_button("Update Quantity"):
                if item_id:
                    db.update_item_quantity(item_id, new_quantity)
                    st.success(f"Item ID {item_id} quantity updated to {new_quantity}.")
                    st.experimental_rerun()
                else:
                    st.warning("Please enter a valid Item ID.")
        
        with col2:
            if st.form_submit_button("Delete Item"):
                if item_id:
                    db.delete_item(item_id)
                    st.success(f"Item ID {item_id} deleted successfully.")
                    st.experimental_rerun()
                else:
                    st.warning("Please enter a valid Item ID.")

if __name__ == "__main__":
    display_inventory_manager()