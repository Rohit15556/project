from tkinter import*
from PIL import ImageTk,Image
import tkinter.font as font
from tkcalendar import DateEntry
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
root = tk.Tk()
root.attributes("-fullscreen",True)
root.configure(background='#b6ac89')
screen_width = root.winfo_screenwidth()
screen_height= root.winfo_screenheight()

def min():
    root.iconify()
def enter(i):
    btn2['background']="red"
def leave(i):
    btn2['background']="#b6ac89"
def max():
    msg_box =messagebox.askquestion('Exit Application', 'Are you sure you want to close the application?',icon='warning')
    if msg_box == 'yes':
        root.destroy()
label1=LabelFrame(root,height=35,fg="blue",bg="#57a1f8").place(x=0,y=0)
buttonFont = font.Font(size=14)

btn2=Button(root,text="✕", command=max,width=4,bg="#b6ac89",border=0,font=buttonFont)
btn2.place(x=1485,y=0)
btn2.bind('<Enter>',enter)
btn2.bind('<Leave>',leave)

btn=Button(root,text="-", command=min,width=4,bg="#b6ac89",border=0,font=buttonFont)
btn.place(x=screen_width-100,y=0)
def enter(i):
    btn['background']="red"
def leave(i):
    btn['background']="#b6ac89"
btn.bind('<Enter>',enter)
btn.bind('<Leave>',leave)

def log_out():
    msg_box = messagebox.askquestion('LOG OUT', 'Are you sure you want to Log Out?', icon='warning')
    if msg_box == 'yes':
        root.destroy()
    import start

log=Button(root,text="LOG OUT",bg='red', fg='white',font=('Arial', '12', ''),command=log_out)
log.place(x=screen_width-185,y=0)
# Connect to SQLite database
conn = sqlite3.connect("products.db")
cursor = conn.cursor()

# Create product table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS products
                  (id INTEGER PRIMARY KEY, name TEXT, price REAL)''')
conn.commit()

# Sample product list
products = []

def get_products_from_db():
    cursor.execute("SELECT * FROM products")
    return cursor.fetchall()

def populate_treeview():
    tree.delete(*tree.get_children())
    for product in products:
        tree.insert('', 'end', values=product[1:])

def add_product_dialog():
    dialog = tk.Toplevel(root)
    dialog.title("Add Product")
    dialog.geometry("300x150")
    dialog.configure(background='#b6ac89')

    tk.Label(dialog, text="Product Name:", font=("Arial", 12), background='#b6ac89').pack()
    product_name_entry = tk.Entry(dialog, font=("Arial", 12))
    product_name_entry.pack()

    tk.Label(dialog, text="Product Price:", font=("Arial", 12), background='#b6ac89').pack()
    product_price_entry = tk.Entry(dialog, font=("Arial", 12))
    product_price_entry.pack()

    add_product_btn = tk.Button(dialog, text="Add Product", command=lambda: add_product(product_name_entry.get(), product_price_entry.get()), font=("Arial", 12), bg='purple', fg='white')
    add_product_btn.pack(pady=10)

def add_product(name, price):
    if not name or not price:
        messagebox.showwarning("Warning", "Please enter both name and price for the product.")
        return

    try:
        price = float(price)
    except ValueError:
        messagebox.showwarning("Warning", "Price must be a number.")
        return

    cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
    conn.commit()

    # Update local products list and treeview
    products.clear()
    products.extend(get_products_from_db())
    populate_treeview()

def add_to_cart():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a product to add to cart.")
        return

    price = float(tree.item(selected_item, 'values')[1])
    cart.append((get_product_name(price), price))

    # Update total price
    update_total_price()

def view_cart():
    if not cart:
        messagebox.showwarning("Warning", "Your cart is empty. Please add products to your cart.")
        return

    cart_window = tk.Toplevel(root)
    cart_window.title("Shopping Cart")
    cart_window.geometry("600x400")
    cart_window.configure(background='#b6ac89')

    # Create a frame for the cart items
    cart_frame = tk.Frame(cart_window, bg='#b6ac89')
    cart_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Create a treeview to display cart items
    cart_tree = ttk.Treeview(cart_frame, columns=('Name', 'Price'), show='headings', selectmode='browse')
    cart_tree.heading('Name', text='Name')
    cart_tree.heading('Price', text='Price')
    cart_tree.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

    for item in cart:
        cart_tree.insert('', 'end', values=item)

    # Create a button to place order
    place_order_btn = tk.Button(cart_frame, text="Place Order", command=place_order, font=("Arial", 14), bg='red', fg='white')
    place_order_btn.pack(pady=10)

def get_product_name(price):
    for product in products:
        if product[2] == price:
            return product[1]
    return "Unknown"  # Return a default value if product name is not found

def place_order():
    if not cart:
        messagebox.showwarning("Warning", "Your cart is empty. Please add products to your cart.")
        return

    # Display bill receipt
    bill_window = tk.Toplevel(root)
    bill_window.title("Bill Receipt")
    bill_window.geometry("400x300")
    bill_window.configure(background='#b6ac89')

    total_price = sum(item[1] for item in cart)
    order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    tk.Label(bill_window, text="Order Date: " + order_date, font=("Helvetica", 12), background='#b6ac89').pack()
    tk.Label(bill_window, text="------------------------------------------", font=("Arial", 12), background='#b6ac89').pack()

    for item in cart:
        tk.Label(bill_window, text=f"Product: {item[0]} - ${item[1]}", font=("Arial", 12), background='#b6ac89').pack()

    tk.Label(bill_window, text="------------------------------------------", font=("Arial", 12), background='#b6ac89').pack()
    tk.Label(bill_window, text="Total Price: $" + str(total_price), font=("Arial", 12), background='#b6ac89').pack()

    tk.Button(bill_window, text="Close", command=bill_window.destroy, font=("Arial", 12), bg='red').pack(pady=10)

    # Reset cart and total price
    cart.clear()
    update_total_price()

def delete_product():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a product to delete.")
        return

    # Extract the index from the selected item
    selected_index = int(tree.index(selected_item))

    if selected_index < 0 or selected_index >= len(products):
        messagebox.showwarning("Warning", "Invalid product selected.")
        return

    product_id = products[selected_index][0]
    confirm = messagebox.askyesno("Confirmation", "Are you sure you want to delete this product?")

    if confirm:
        cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
        conn.commit()

        # Update local products list and treeview
        products.clear()
        products.extend(get_products_from_db())
        populate_treeview()

def update_total_price():
    total_price.set(sum(item[1] for item in cart))

cart = []  # Initialize cart list
total_price = tk.DoubleVar()
total_price.set(0.0)

# Create a frame for the products
products_frame = tk.Frame(root, bg='#b6ac89')
products_frame.pack(padx=10, pady=35,fill=tk.BOTH, expand=True)

# Create a treeview to display products
tree = ttk.Treeview(products_frame, columns=('Name', 'Price'), show='headings', selectmode='browse')
tree.heading('Name', text='Name')
tree.heading('Price', text='Price')
tree.pack(side=tk.LEFT, padx=10, pady=25, fill=tk.BOTH, expand=True)

# Populate the treeview with products
products.extend(get_products_from_db())
populate_treeview()

# Create a label to display total price
tk.Label(root, text="Total Price:", font=("Arial", 16), background='#b6ac89').pack()
tk.Label(root, textvariable=total_price, font=("Arial", 16), background='#b6ac89').pack()

# Create a button to add selected product to cart
add_to_cart_btn = tk.Button(root, text="Add to Cart", command=add_to_cart, font=("Arial", 14), bg='green', fg='white')
add_to_cart_btn.pack(pady=10)

# Create a button to view cart
view_cart_btn = tk.Button(root, text="View Cart", command=view_cart, font=("Arial", 14), bg='blue', fg='white')
view_cart_btn.pack(pady=10)

# Create a button to add a new product
add_product_btn = tk.Button(root, text="Add Product", command=add_product_dialog, font=("Arial", 14), bg='orange', fg='white')
add_product_btn.pack(pady=10)

# Create a button to delete selected product
delete_product_btn = tk.Button(root, text="Delete Product", command=delete_product, font=("Arial", 14), bg='red', fg='white')
delete_product_btn.pack(pady=10)

root.mainloop()

# Close the database connection when the application exits
conn.close()

root.mainloop()


