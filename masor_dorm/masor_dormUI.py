import json
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from ttkthemes import ThemedStyle
# import math


def view_all_rooms():
    with open('room.json') as file:
        room_data = json.load(file)

    root = tk.Tk()
    root.title("All Rooms")

    tree = ttk.Treeview(root)
    tree["columns"] = ("price", "vacancy", "tenant_id", "floor")
    tree.heading("#0", text="Room Number")
    tree.heading("price", text="Price")
    tree.heading("vacancy", text="Vacancy")
    tree.heading("tenant_id", text="Tenant ID")
    tree.heading("floor", text="Floor")

    for room in room_data['room']:
        room_number = room['room_num']
        price = room['price']
        vacancy = 'Yes' if room['vacancy'] else 'No'
        tenant_id = room['tenent_id'] if room['tenent_id'] is not None else '--'
        floor = room['floor']

        tree.insert("", tk.END, text=room_number, values=(price, vacancy, tenant_id, floor))

    tree.pack()

    root.mainloop()


def delete_tenant():
    def delete_selected_tenant():
        selected_item = tree.selection()
        if selected_item:
            tenant_id = tree.item(selected_item)["values"][0]

            try:
                with open('tenant.json') as file:
                    data = json.load(file)

                tenants = data["tenant"]

                updated_tenants = [tenant for tenant in tenants if tenant["id"] != tenant_id]

                data["tenant"] = updated_tenants

                with open('tenant.json', 'w') as file:
                    json.dump(data, file, indent=4)

                messagebox.showinfo("Success", f"Tenant with ID {tenant_id} has been deleted!")
                window.destroy()

            except FileNotFoundError:
                messagebox.showerror("Error", "File not found!")
        else:
            messagebox.showwarning("No Tenant Selected", "Please select a tenant to delete.")

    try:
        with open('tenant.json') as file:
            data = json.load(file)

        # Create a new window
        window = tk.Toplevel(root)
        window.title("Delete Tenant")
        window.geometry("300x400")  # Set the size of the window

        # Create a Treeview to display the tenants
        tree = ttk.Treeview(window)
        tree["columns"] = ("ID", "Name", "Surname", "Contract")
        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("ID", anchor=tk.CENTER, width=100)
        tree.column("Name", anchor=tk.CENTER, width=100)
        tree.column("Surname", anchor=tk.CENTER, width=100)
        tree.column("Contract", anchor=tk.CENTER, width=100)

        tree.heading("#0", text="")
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Surname", text="Surname")
        tree.heading("Contract", text="Contract")

        tenants = data["tenant"]

        for tenant in tenants:
            tree.insert("", tk.END, values=(tenant["id"], tenant["name"], tenant["surname"], tenant["contract"]))

        tree.pack()

        delete_button = ttk.Button(window, text="Delete Tenant", command=delete_selected_tenant)
        delete_button.pack(pady=10)

    except FileNotFoundError:
        messagebox.showerror("Error", "File not found!")

def view_all_tenants():
    try:
        with open('tenant.json') as file:
            data = json.load(file)

        # Create a new window
        window = tk.Toplevel(root)
        window.title("All Tenants")
        window.geometry("300x400")  # Set the size of the window

        # Create a Treeview to display the tenants
        tree = ttk.Treeview(window)
        tree["columns"] = ("ID", "Name", "Surname", "Contract")
        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("ID", anchor=tk.CENTER, width=100)
        tree.column("Name", anchor=tk.CENTER, width=100)
        tree.column("Surname", anchor=tk.CENTER, width=100)
        tree.column("Contract", anchor=tk.CENTER, width=100)

        tree.heading("#0", text="")
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Surname", text="Surname")
        tree.heading("Contract", text="Contract")

        tenants = data["tenant"]

        for tenant in tenants:
            tree.insert("", tk.END, values=(tenant["id"], tenant["name"], tenant["surname"], tenant["contract"]))

        tree.pack()

    except FileNotFoundError:
        messagebox.showerror("Error", "File not found!")

def add_new_tenant():
    def save_tenant():
        id = id_entry.get()
        name = name_entry.get()
        surname = surname_entry.get()
        contract = int(contract_entry.get())

        try:
            with open('tenant.json') as file:
                data = json.load(file)

            if 'tenant' not in data:
                data['tenant'] = []

            new_tenant = {
                "id": id,
                "name": name,
                "surname": surname,
                "contract": contract
            }
            data["tenant"].append(new_tenant)

            with open('tenant.json', 'w') as file:
                json.dump(data, file, indent=4)
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found!")

        # Show a messagebox to indicate that the tenant has been saved
        messagebox.showinfo("Success", "The tenant has been saved!")

    window = tk.Toplevel(root)
    window.title("Add New Tenant")
    window.geometry("300x400")  # Set the size of the window

    frame = ttk.Frame(window)
    frame.pack(pady=20)

    id_label = ttk.Label(frame, text="ID:")
    id_label.grid(row=0, column=0, padx=10)

    id_entry = ttk.Entry(frame)
    id_entry.grid(row=0, column=1, padx=10)

    name_label = ttk.Label(frame, text="Name:")
    name_label.grid(row=1, column=0, padx=10)

    name_entry = ttk.Entry(frame)
    name_entry.grid(row=1, column=1, padx=10)

    surname_label = ttk.Label(frame, text="Surname:")
    surname_label.grid(row=2, column=0, padx=10)

    surname_entry = ttk.Entry(frame)
    surname_entry.grid(row=2, column=1, padx=10)

    contract_label = ttk.Label(frame, text="Contract Duration:")
    contract_label.grid(row=3, column=0, padx=10)

    contract_entry = ttk.Entry(frame)
    contract_entry.grid(row=3, column=1, padx=10)

    button = ttk.Button(window, text="Save Tenant", command=save_tenant)
    button.pack(pady=10)

    window.mainloop()



def find_tenants_with_long_contract():
    def display_result():
        # Read JSON data from file
        try:
            with open('tenant.json') as file:
                data = json.load(file)
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found!")

        # Get contract duration from entry field
        contract_duration = int(contract_entry.get())

        # Find tenants with contract duration greater than the specified value
        tenants = data["tenant"]
        long_contract_tenants = []

        for tenant in tenants:
            if tenant["contract"] > contract_duration:
                long_contract_tenants.append(tenant)

        # Create a new window
        window = tk.Toplevel(root)
        window.title("Results")
        window.geometry("300x400")  # Set the size of the window

        # Create a Treeview to display the results
        tree = ttk.Treeview(window)
        tree["columns"] = ("ID", "Name", "Surname", "Contract")
        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("ID", anchor=tk.CENTER, width=100)
        tree.column("Name", anchor=tk.CENTER, width=100)
        tree.column("Surname", anchor=tk.CENTER, width=100)
        tree.column("Contract", anchor=tk.CENTER, width=100)

        tree.heading("#0", text="")
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Surname", text="Surname")
        tree.heading("Contract", text="Contract")

        for tenant in long_contract_tenants:
            tree.insert("", tk.END, values=(tenant["id"], tenant["name"], tenant["surname"], tenant["contract"]))

        tree.pack()

    window = tk.Toplevel(root)
    window.title("Find Tenants")
    window.geometry("300x400")  # Set the size of the window

    frame = ttk.Frame(window)
    frame.pack(pady=20)

    contract_label = ttk.Label(frame, text="Contract Duration:")
    contract_label.grid(row=0, column=0, padx=10)

    contract_entry = ttk.Entry(frame)
    contract_entry.grid(row=0, column=1, padx=10)

    button = ttk.Button(window, text="Find Tenants", command=display_result)
    button.pack(pady=10)

    window.mainloop()

def add_water_electric():
    def save_bill():
        room = room_entry.get()
        water = int(water_entry.get())
        elect = int(electric_entry.get())
        date = date_entry.get()

        try:
            with open('bill.json') as file:
                bill = json.load(file)

            if 'bill' not in bill:
                bill['bill'] = []

            new_bill = {
                "room_num": room,
                "water": water,
                "electric": elect,
                "pay": False,
                "date": date
            }
            bill["bill"].append(new_bill)

            with open('bill.json', 'w') as file:
                json.dump(bill, file, indent=4)
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found!")

        # Show a messagebox to indicate that the bill has been saved
        messagebox.showinfo("Success", "The bill has been saved!")

    window = tk.Toplevel(root)
    window.title("Add Water and Electric Bill")
    window.geometry("300x400")  # Set the size of the window

    frame = ttk.Frame(window)
    frame.pack(pady=20)

    room_label = ttk.Label(frame, text="Room Number:")
    room_label.grid(row=0, column=0, padx=10)

    room_entry = ttk.Entry(frame)
    room_entry.grid(row=0, column=1, padx=10)

    water_label = ttk.Label(frame, text="Water Bill:")
    water_label.grid(row=1, column=0, padx=10)

    water_entry = ttk.Entry(frame)
    water_entry.grid(row=1, column=1, padx=10)

    electric_label = ttk.Label(frame, text="Electric Bill:")
    electric_label.grid(row=2, column=0, padx=10)

    electric_entry = ttk.Entry(frame)
    electric_entry.grid(row=2, column=1, padx=10)

    date_label = ttk.Label(frame, text="Date:")
    date_label.grid(row=3, column=0, padx=10)

    date_entry = ttk.Entry(frame)
    date_entry.grid(row=3, column=1, padx=10)

    button = ttk.Button(window, text="Save Bill", command=save_bill)
    button.pack(pady=10)

    window.mainloop()


def sum_bills_by_room(bill_data, room_num):
    electric_total = 0
    water_total = 0

    for bill in bill_data["bill"]:
        if "room_num" in bill and bill["room_num"] == room_num and  bill.get("pay", False):
            if "electric" in bill:
                electric_total += bill["electric"]
            if "water" in bill:
                water_total += bill["water"]

    return electric_total, water_total

def sum_bills_by_room_wrapper():
    def display_result():
        room_num = int(room_entry.get())
        with open('bill.json') as file:
            bill_data = json.load(file)
        electric_total, water_total = sum_bills_by_room(bill_data, room_num)
        result_label.config(text=f"Total electric bill for room {room_num}: {electric_total}")
        result_label2.config(text=f"Total water bill for room {room_num}: {water_total}")
        result_label3.config(text=f"Total expense for room {room_num}: {water_total+electric_total}")

    window = tk.Toplevel(root)
    window.title("Sum Bills by Room")
    window.geometry("300x200")  # Set the size of the window

    frame = ttk.Frame(window)
    frame.pack(pady=20)

    room_label = ttk.Label(frame, text="Room Number:")
    room_label.grid(row=0, column=0, padx=10)

    room_entry = ttk.Entry(frame)
    room_entry.grid(row=0, column=1, padx=10)

    button = ttk.Button(window, text="Calculate", command=display_result)
    button.pack(pady=10)

    result_label = ttk.Label(window, text="")
    result_label.pack()

    result_label2 = ttk.Label(window, text="")
    result_label2.pack()
    result_label3 = ttk.Label(window, text="")
    result_label3.pack()
    window.mainloop()

root = tk.Tk()
root.title("Apartment Management System")
root.geometry("400x400")

style = ThemedStyle(root)
style.set_theme("arc")

frame = ttk.Frame(root)
frame.pack(pady=20)

find_tenants_button = ttk.Button(frame, text="Find Tenants with Long Contract", command=find_tenants_with_long_contract)
find_tenants_button.grid(row=0, column=0, padx=10)



add_tenant_button = ttk.Button(frame, text="Add New Tenant", command=add_new_tenant)
add_tenant_button.grid(row=1, column=0, columnspan=2, pady=10)

view_tenants_button = ttk.Button(frame, text="View All Tenants", command=view_all_tenants)
view_tenants_button.grid(row=2, column=0, columnspan=2, pady=10)

delete_tenant_button = ttk.Button(frame, text="Delete Tenant", command=delete_tenant)
delete_tenant_button.grid(row=3, column=0, columnspan=2, pady=10)

sum_bills_button = ttk.Button(frame, text="Sum Bills by Room", command=sum_bills_by_room_wrapper)
sum_bills_button.grid(row=4, column=0, columnspan=2, pady=10)

view_rooms_button = ttk.Button(frame, text="View All Rooms", command=view_all_rooms)
view_rooms_button.grid(row=5, column=0, columnspan=2, pady=10)

add_bill_button = ttk.Button(frame, text="Add Water and Electric Bill", command=add_water_electric)
add_bill_button.grid(row=6, column=0, padx=10)

root.mainloop()
