import streamlit as st
import time
#st.set_page_config(page_title="Smart Coffee Kiosk Application")
st.title("Smart Coffee Kiosk Application")
import json
from pathlib import Path

json_file = Path("inventory.json")

if json_file.exists():
    with open(json_file, "r") as f:
        inventory = json.load(f)
else:
    inventory = [] 

json_file_orders = Path("orders.json")

if json_file_orders.exists():
    with open(json_file_orders, "r") as f:
        orders = json.load(f)
else:
    orders = [] 

tab1, tab2, tab3, tab4 = st.tabs(["Create", "Read", "Update","Delete/Cancel"])

with tab1:
    st.header("Place Your Order!")
    order_type = st.selectbox("Choose your product!", ["Espresso", "Latte", "Cold Brew","Mocha","Blueberry Muffin"])
    order_quantity = st.number_input("How many do you want?")
    order_name = st.text_input("What name is the order under?",placeholder="Ex. Jane Doe",key="Order_Name")
    submit_button = st.button("Submit Order",disabled=False)
    if submit_button:
        if not order_name:
            st.warning("Must have a name!")
        for order in inventory:
            if order_type == order["name"]:
                if order_quantity <= order["stock"]:
                    order['stock'] -= order_quantity
                    order_total_price = order['price'] * order_quantity
                    new_order = {"order_id": order["id"], "customer": order_name, "item": order_type, 
                    "total": order_total_price, "quantity": order_quantity, "status": "Placed" }
                    orders.append(new_order)
                    with open(json_file, "w") as f:
                        json.dump(orders, f, indent=4)
                    with open(json_file, "w") as f:
                        json.dump(inventory, f, indent=4)
                    st.success("Order placed! Here is your receipt.")
                    receipt_id = new_order['order_id']
                    st.markdown(f'ID: {receipt_id}')
                    st.markdown(" ")
                    receipt_name = new_order['customer']
                    st.markdown(f'Name: {receipt_name}')
                    st.markdown(" ")
                    receipt_item = new_order['item']
                    st.markdown(f'Item: {receipt_item}')
                    st.markdown(" ")
                    receipt_quantity = new_order['quantity']
                    st.markdown(f'Quantity: {receipt_quantity}')
                    st.markdown(" ")
                    receipt_total = new_order['total']
                    st.markdown(f'Total: ${receipt_total}')
                    st.markdown(" ")
                    receipt_status = new_order['status']
                    st.markdown(f'Status: {receipt_status}')
                    st.markdown(" ")
                    time.sleep(5.0)
                    st.rerun
                else:
                    st.error("Out of Stock!")
                    time.sleep(5.0)
                    st.rerun




with tab2:
    st.subheader("Current Items List")
    view_mode = st.radio("View Mode", 
                ["View All", "Search Items"], horizontal=True)
    if view_mode == "View All":
        with st.container(border=True):
            st.metric(label="Total Items", value=len(inventory))
            if len(inventory) > 0:
                for item in inventory:
                    with st.expander(item.get('name')):
                        st.write(f"**ID:** {item.get('id')}")
                        st.write(f"**Name:** {item.get('name')}")
                        st.write(f"**Price:** {item.get('price')}")
                        st.write(f"**Stock**: {item.get('stock')}")
            else:
                st.info("No Items found.")
    elif view_mode == "Search Items":
        st.markdown("### Search")
        items = [order["name"] for order in inventory]
        selected_item = st.text_input("Quick Search (Type to filter)",key="quick_search")
        if selected_item:
            st.divider()
            selected_inventory = None
            for item in items:
                if item == selected_item:
                    selected_inventory = item
                    break
            if selected_inventory:
                st.success(f"Details for: {selected_item}")
                for order in inventory:
                    if item == order['name']:
                        with st.expander(item):
                            st.write(f"**ID:** {order.get('id')}")
                            st.write(f"**Name:** {order.get('name')}")
                            st.write(f"**Price:** {order.get('price')}")
                            st.write(f"**Stock**: {order.get('stock')}")
            else:
                st.warning("Item details not found.")

with tab3:
    st.subheader("Edit Inventory")
    if len(inventory) > 0:
        items = [item["name"] for item in inventory]
        selected_item = st.selectbox("Select Item to Update",
        items, key="update_select")
# Find the assignment object in the list
        selected_inventory = None
        for item in items:
            if item == selected_item:
                selected_inventory = item
                break
        if selected_inventory:
            for order in inventory:
                if selected_item == order["name"]:
                    with st.container(border=True):
                        st.write(f"Editing: {selected_item}")
                        new_stock = st.number_input("New Stock")
                        btn_update = st.button("Update Info", use_container_width=True,
                        type="primary")
                        if btn_update:
                            order["stock"] = new_stock
                            with open(json_file, "w") as f:
                                json.dump(inventory, f, indent=4)
                            st.success("Updated!")
                            time.sleep(5.0)
                            st.rerun()
    else:
        st.info("No items to update.")

with tab4:
    st.subheader("Delete Order")
    if len(orders) > 0:
        order_names = [order["customer"] for order in orders]
        selected_order_to_delete = st.selectbox("Select Your Name to Delete Your Order",
        order_names, key="delete_select")
        selected_name_to_delete = None
        for order in orders:
            if order == selected_order_to_delete:
                selected_name_to_delete = order
                break
        if selected_name_to_delete:
            with st.container(border=True):
                if st.button("Delete Order", type="primary", use_container_width=True):
                    if order['customer'] == selected_name_to_delete:
                        for item in inventory:
                            if order['item'] == item['name']:
                                item['stock'] += order['quantity']
                        orders.remove(selected_name_to_delete)
                        with open(json_file, "w") as f:
                            json.dump(orders, f, indent=4)
                        st.success("Order Deleted Successfully!")
                        time.sleep(5.0)
                        st.rerun()
    else:
        st.info("No orders to delete.")