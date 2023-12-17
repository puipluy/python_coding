import tkinter as tk
import json

class masorhusnaUI:
    def __init__(self):
        self.root = tk.Tk()
        self.menu = self.load_menu()
        self.orders = []
        self.order_counter = 1

        self.root.title("ร้านมซอ")
        self.root.geometry("500x400")

        self.create_menu_buttons()

        self.root.mainloop()

    def load_menu(self):
        with open('menu.json', encoding='utf-8') as file:
            menu_data = json.load(file)
        return menu_data['menu']
    
    def create_order_window(self):
        order_window = tk.Toplevel(self.root)
        order_window.title(f"ลูกค้า คนที่ #{self.order_counter}")
        order_window.geometry("400x500")

        order_label = tk.Label(order_window, text="รายการอาหารที่สั่ง:", font=("Arial", 14, "bold"))
        order_label.pack(pady=10)

        total_cost_label = tk.Label(order_window, text="ยอดรวมค่าอาหาร: 0 บาท", font=("Arial", 12))
        total_cost_label.pack(pady=10)

        finish_button = tk.Button(order_window, text="คิดเงิน", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                                  command=lambda: self.summary_total_cost(order_window))
        finish_button.pack(pady=10)

        order = {
            'window': order_window,
            'order_items': [],
            'total_cost_label': total_cost_label
        }

        self.orders.append(order)

        self.order_counter += 1


    def create_menu_buttons(self):
        for item in self.menu:
            button = tk.Button(self.root, text=item['name'], font=("Arial", 12), width=15, height=2,
                               command=lambda item=item: self.open_add_item_window(item))
            button.pack(pady=5)

        new_order_button = tk.Button(self.root, text="สั่งอาหารใหม่", font=("Arial", 12, "bold"), bg="#2196F3", fg="white",
                                     command=self.create_order_window)
        new_order_button.pack(pady=10)

    def open_add_item_window(self, item):
        add_item_window = tk.Toplevel(self.root)
        add_item_window.title("Add Item")
        add_item_window.geometry("300x200")

        order_label = tk.Label(add_item_window, text="เลือกลูกค้า:", font=("Arial", 12))
        order_label.pack(pady=10)

        order_var = tk.StringVar(add_item_window)
        order_options = [f"คนที่ #{i}" for i, order in enumerate(self.orders, start=1)]
        order_dropdown = tk.OptionMenu(add_item_window, order_var, *order_options)
        order_dropdown.config(font=("Arial", 12), width=10)
        order_dropdown.pack(pady=5)

        add_button = tk.Button(add_item_window, text="เพิ่มรายการอาหาร", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                               command=lambda: self.add_item_to_order(item, order_var.get()))
        add_button.pack(pady=10)

    def add_item_to_order(self, item, selected_order):
        order_index = int(selected_order.split("#")[1]) - 1
        selected_order = self.orders[order_index]
        selected_order['order_items'].append(item)
        selected_order['total_cost_label'].config(text="ค่าอาหารรวม: {:.2f} บาท".format(self.calculate_total_cost(selected_order['order_items'])))

        item_label = tk.Label(selected_order['window'], text=item['name'], font=("Arial", 12))
        item_label.pack()

    def calculate_total_cost(self, order_items):
        total_cost = sum(item['price'] for item in order_items)
        return total_cost

    def summary_total_cost(self, order_window):
        current_order = next((order for order in self.orders if order['window'] == order_window), None)
        total_cost = self.calculate_total_cost(current_order['order_items'])

        summary_window = tk.Toplevel(self.root)
        summary_window.title("Summary")
        summary_window.geometry("300x200")

        summary_label = tk.Label(summary_window, text="ราคารวม: {:.2f} บาท ".format(total_cost), font=("Arial", 14, "bold"))
        summary_label.pack(pady=20)

        current_order['order_items'] = []
        current_order['total_cost_label'].config(text="ราคารวม: 0 บาท")
        self.orders.remove(current_order)
        order_window.destroy()

if __name__ == "__main__":
    masorhusnaUI()
