import json
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk

class ContactManager:
    def __init__(self, filename="contacts.json"):
        self.filename = filename
        self.load_contacts()

    def load_contacts(self):
        try:
            with open(self.filename, "r") as file:
                self.contacts = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.contacts = []

    def save_contacts(self):
        with open(self.filename, "w") as file:
            json.dump(self.contacts, file, indent=4)

    def add_contact(self, name, phone, email, address):
        self.contacts.append({"name": name, "phone": phone, "email": email, "address": address})
        self.save_contacts()
        messagebox.showinfo("Success", "Contact added successfully!")

    def view_contacts(self):
        contact_list.delete(*contact_list.get_children())
        for contact in self.contacts:
            contact_list.insert("", "end", values=(contact['name'], contact['phone'], contact['email'], contact['address']))

    def search_contact(self, keyword):
        contact_list.delete(*contact_list.get_children())
        results = [c for c in self.contacts if keyword.lower() in c["name"].lower() or keyword in c["phone"]]
        if results:
            for contact in results:
                contact_list.insert("", "end", values=(contact['name'], contact['phone'], contact['email'], contact['address']))
        else:
            messagebox.showinfo("Info", "No contacts found.")

    def update_contact(self, name, new_phone=None, new_email=None, new_address=None):
        for contact in self.contacts:
            if contact["name"].lower() == name.lower():
                if new_phone:
                    contact["phone"] = new_phone
                if new_email:
                    contact["email"] = new_email
                if new_address:
                    contact["address"] = new_address
                self.save_contacts()
                messagebox.showinfo("Success", "Contact updated successfully!")
                return
        messagebox.showerror("Error", "Contact not found.")

    def delete_contact(self, name):
        for contact in self.contacts:
            if contact["name"].lower() == name.lower():
                self.contacts.remove(contact)
                self.save_contacts()
                messagebox.showinfo("Success", "Contact deleted successfully!")
                return
        messagebox.showerror("Error", "Contact not found.")

# GUI Setup
def add_contact_gui():
    name = simpledialog.askstring("Input", "Enter name:")
    phone = simpledialog.askstring("Input", "Enter phone:")
    email = simpledialog.askstring("Input", "Enter email:")
    address = simpledialog.askstring("Input", "Enter address:")
    if name and phone:
        manager.add_contact(name, phone, email, address)
        manager.view_contacts()

def search_contact_gui():
    keyword = simpledialog.askstring("Search", "Enter name or phone number:")
    if keyword:
        manager.search_contact(keyword)

def delete_contact_gui():
    name = simpledialog.askstring("Delete", "Enter the name of the contact to delete:")
    if name:
        manager.delete_contact(name)
        manager.view_contacts()

def update_contact_gui():
    name = simpledialog.askstring("Update", "Enter the name of the contact to update:")
    if name:
        new_phone = simpledialog.askstring("Update", "Enter new phone (leave blank to keep current):") or None
        new_email = simpledialog.askstring("Update", "Enter new email (leave blank to keep current):") or None
        new_address = simpledialog.askstring("Update", "Enter new address (leave blank to keep current):") or None
        manager.update_contact(name, new_phone, new_email, new_address)
        manager.view_contacts()

app = tk.Tk()
app.title("Contact Management System")
app.geometry("700x500")
app.configure(bg="#ADD8E6")
manager = ContactManager()

frame = tk.Frame(app, bg="#E6E6FA")
frame.pack(pady=10)

contact_list = ttk.Treeview(frame, columns=("Name", "Phone", "Email", "Address"), show="headings")
contact_list.heading("Name", text="Name")
contact_list.heading("Phone", text="Phone")
contact_list.heading("Email", text="Email")
contact_list.heading("Address", text="Address")
contact_list.pack()
manager.view_contacts()

tk.Button(app, text="Add Contact", command=add_contact_gui, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), width=20).pack(pady=5)
tk.Button(app, text="Search Contact", command=search_contact_gui, bg="#2196F3", fg="white", font=("Arial", 12, "bold"), width=20).pack(pady=5)
tk.Button(app, text="Update Contact", command=update_contact_gui, bg="#FFC107", fg="black", font=("Arial", 12, "bold"), width=20).pack(pady=5)
tk.Button(app, text="Delete Contact", command=delete_contact_gui, bg="#F44336", fg="white", font=("Arial", 12, "bold"), width=20).pack(pady=5)
tk.Button(app, text="Exit", command=app.quit, bg="#9E9E9E", fg="white", font=("Arial", 12, "bold"), width=20).pack(pady=5)

app.mainloop()