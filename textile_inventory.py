import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import datetime

CSV_FILE = "textile_products.csv"

# Initialize CSV
def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Name", "Type", "Quantity", "Date"])

def get_next_id():
    if not os.path.exists(CSV_FILE):
        return 1
    with open(CSV_FILE, 'r') as file:
        rows = list(csv.reader(file))[1:]
        return len(rows) + 1

class TextileInventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Textile Industry Inventory")
        self.root.geometry("850x550")
        init_csv()
        self.setup_ui()

    def setup_ui(self):
        title = tk.Label(self.root, text="Textile Inventory Management", font=("Helvetica", 18, "bold"))
        title.pack(pady=10)

        tabs = ttk.Notebook(self.root)
        self.receive_tab = ttk.Frame(tabs)
        self.sell_tab = ttk.Frame(tabs)
        self.view_tab = ttk.Frame(tabs)
        self.stats_tab = ttk.Frame(tabs)

        tabs.add(self.receive_tab, text="Receive Products")
        tabs.add(self.sell_tab, text="Sell Products")
        tabs.add(self.view_tab, text="View All Records")
        tabs.add(self.stats_tab, text="View Summary")
        tabs.pack(expand=1, fill="both")

        self.create_receive_tab()
        self.create_sell_tab()
        self.create_view_tab()
        self.create_stats_tab()

    # ---------- Receive Tab ----------
    def create_receive_tab(self):
        tk.Label(self.receive_tab, text="Product Name:").pack(pady=5)
        self.rec_name = tk.Entry(self.receive_tab)
        self.rec_name.pack()

        tk.Label(self.receive_tab, text="Quantity:").pack(pady=5)
        self.rec_qty = tk.Entry(self.receive_tab)
        self.rec_qty.pack()

        tk.Button(self.receive_tab, text="Add Received Product", command=self.add_received).pack(pady=10)

    def add_received(self):
        name = self.rec_name.get()
        qty = self.rec_qty.get()
        if not name or not qty.isdigit():
            messagebox.showerror("Error", "Enter valid product name and quantity.")
            return
        self.write_to_csv(name, "Received", int(qty))
        self.rec_name.delete(0, tk.END)
        self.rec_qty.delete(0, tk.END)
        messagebox.showinfo("Success", "Received product added.")

    # ---------- Sell Tab ----------
    def create_sell_tab(self):
        tk.Label(self.sell_tab, text="Product Name:").pack(pady=5)
        self.sell_name = tk.Entry(self.sell_tab)
        self.sell_name.pack()

        tk.Label(self.sell_tab, text="Quantity:").pack(pady=5)
        self.sell_qty = tk.Entry(self.sell_tab)
        self.sell_qty.pack()

        tk.Button(self.sell_tab, text="Add Sold Product", command=self.add_sold).pack(pady=10)

    def add_sold(self):
        name = self.sell_name.get()
        qty = self.sell_qty.get()
        if not name or not qty.isdigit():
            messagebox.showerror("Error", "Enter valid product name and quantity.")
            return
        self.write_to_csv(name, "Sold", int(qty))
        self.sell_name.delete(0, tk.END)
        self.sell_qty.delete(0, tk.END)
        messagebox.showinfo("Success", "Sold product added.")

    # ---------- CSV Write ----------
    def write_to_csv(self, name, type_, qty):
        with open(CSV_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([get_next_id(), name, type_, qty, datetime.now().strftime("%Y-%m-%d")])

    # ---------- View Tab ----------
    def create_view_tab(self):
        self.tree = ttk.Treeview(self.view_tab, columns=("ID", "Name", "Type", "Quantity", "Date"), show="headings")
        for col in ["ID", "Name", "Type", "Quantity", "Date"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(fill="both", expand=True)

        tk.Button(self.view_tab, text="Refresh Records", command=self.load_records).pack(pady=5)

    def load_records(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            with open(CSV_FILE, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.tree.insert("", tk.END, values=(row["ID"], row["Name"], row["Type"], row["Quantity"], row["Date"]))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------- Stats Tab ----------
    def create_stats_tab(self):
        self.stats_label = tk.Label(self.stats_tab, font=("Arial", 14))
        self.stats_label.pack(pady=20)

        tk.Button(self.stats_tab, text="Show Summary", command=self.show_stats).pack(pady=10)

    def show_stats(self):
        data = {}
        try:
            with open(CSV_FILE, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    name = row["Name"]
                    qty = int(row["Quantity"])
                    type_ = row["Type"]

                    if name not in data:
                        data[name] = {"Received": 0, "Sold": 0}

                    if type_ == "Received":
                        data[name]["Received"] += qty
                    elif type_ == "Sold":
                        data[name]["Sold"] += qty

            output = "Product Summary:\n\n"
            for product, counts in data.items():
                received = counts["Received"]
                sold = counts["Sold"]
                stock = received - sold
                output += f"{product} → Received: {received}, Sold: {sold}, Remaining: {stock}\n"

            self.stats_label.config(text=output)
        except Exception as e:
            messagebox.showerror("Error", str(e))


# ---------- Run App ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = TextileInventoryApp(root)
    root.mainloop()

