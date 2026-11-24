
import tkinter as tk
from tkinter import ttk, messagebox

pizza_prices = {
    "Overload Pepperoni": 260,
    "Bacon Mushroom": 290,
    "Ham and Cheese": 230,
    "Cheese Mania": 320
}

size_prices = {
    "Small": 0,
    "Medium": 60,
    "Large": 120
}

topping_prices = {
    "Extra Cheese": 35,
    "Mushrooms": 45,
    "Olives": 40
}

window = tk.Tk()
window.title("Pizza ni Lucky")
window.geometry("650x850")
window.resizable(True, True)
window.configure(bg="#8B2525")

pizza_var = tk.StringVar(value="Overload Pepperoni")
size_var = tk.StringVar(value="Small")
quantity_var = tk.IntVar(value=1)

topping_vars = {
    topping: tk.BooleanVar(value=False)
    for topping in topping_prices
}

title = tk.Label(
    window,
    text="Pizza ni Lucky",
    font=("Arial", 22, "bold"),
    bg="#8B2525",
    fg="#FFE6B3"
)
title.pack(pady=20)

order_frame = tk.Frame(window, bg="#FFF1D6", padx=25, pady=20)
order_frame.pack(padx=25, fill="x")

tk.Label(
    order_frame,
    text="Select Pizza Flavor:",
    font=("Arial", 12, "bold"),
    bg="#2a2a45",
    fg="white"
).pack(anchor="w")

pizza_dropdown = ttk.Combobox(
    order_frame,
    textvariable=pizza_var,
    values=list(pizza_prices.keys()),
    state="readonly",
    font=("Arial", 11)
)
pizza_dropdown.pack(fill="x", pady=8)


pizza_price_label = tk.Label(
    order_frame,
    text=f"Price: ₱{pizza_prices[pizza_var.get()]:,.2f}",
    font=("Arial", 12, "bold"),
    bg="#2a2a45",
    fg="#ffcc00"
)
pizza_price_label.pack(anchor="w")



def update_pizza_price(event=None):
    selected_pizza = pizza_var.get()
    price = pizza_prices[selected_pizza]
    pizza_price_label.config(text=f"Price: ₱{price:,.2f}")


pizza_dropdown.bind(
    "<<ComboboxSelected>>",
    update_pizza_price
)

tk.Label(
    order_frame,
    text="Select Pizza Size:",
    font=("Arial", 12, "bold"),
    bg="#2a2a45",
    fg="white"
).pack(anchor="w", pady=(12, 5))

for size, price in size_prices.items():
    tk.Radiobutton(
        order_frame,
        text=f"{size} (+₱{price})",
        variable=size_var,
        value=size,
        font=("Arial", 11),
        bg="#2a2a45",
        fg="white",
        selectcolor="#444466",
        activebackground="#2a2a45",
        activeforeground="white"
    ).pack(anchor="w")

tk.Label(
    order_frame,
    text="Select Extra Toppings:",
    font=("Arial", 12, "bold"),
    bg="#2a2a45",
    fg="white"
).pack(anchor="w", pady=(12, 5))

for topping, price in topping_prices.items():
    tk.Checkbutton(
        order_frame,
        text=f"{topping} (+₱{price})",
        variable=topping_vars[topping],
        font=("Arial", 11),
        bg="#2a2a45",
        fg="white",
        selectcolor="#444466",
        activebackground="#2a2a45",
        activeforeground="white"
    ).pack(anchor="w")

tk.Label(
    order_frame,
    text="Quantity:",
    font=("Arial", 12, "bold"),
    bg="#2a2a45",
    fg="white"
).pack(anchor="w", pady=(12, 5))

quantity_spinbox = tk.Spinbox(
    order_frame,
    from_=1,
    to=50,
    textvariable=quantity_var,
    font=("Arial", 12),
    width=10
)
quantity_spinbox.pack(anchor="w")


def calculate_total():

    pizza = pizza_var.get()
    size = size_var.get()

    try:
        quantity = int(quantity_var.get())

        if quantity < 1 or quantity > 50:
            raise ValueError

    except (ValueError, tk.TclError):
        messagebox.showerror(
            "Invalid Quantity",
            "Please enter a quantity between 1 and 50."
        )
        return

    confirm = messagebox.askyesno(
        "Confirm Order",
        "Are you sure you want to place this order?"
    )

    if not confirm:
        return

    pizza_price = pizza_prices[pizza]
    size_price = size_prices[size]

    selected_toppings = [
        topping
        for topping, variable in topping_vars.items()
        if variable.get()
    ]

    topping_price = sum(
        topping_prices[topping]
        for topping in selected_toppings
    )

    total_per_pizza = pizza_price + size_price + topping_price
    total = total_per_pizza * quantity

    receipt_text.config(state="normal")
    receipt_text.delete("1.0", tk.END)

    receipt_text.insert(
        tk.END,
        "========== ORDER RECEIPT ==========\n\n"
    )

    receipt_text.insert(tk.END, f"Pizza Flavor: {pizza} (₱{pizza_price})\n")
    receipt_text.insert(tk.END, f"Pizza Size: {size} (+₱{size_price})\n")

    if selected_toppings:
        for topping in selected_toppings:
            receipt_text.insert(
                tk.END,
                f"{topping}: ₱{topping_prices[topping]}\n"
            )
    else:
        receipt_text.insert(tk.END, "No extra toppings\n")

    receipt_text.insert(tk.END, "\n")
    receipt_text.insert(tk.END, f"Price per Pizza: ₱{total_per_pizza:,.2f}\n")
    receipt_text.insert(tk.END, f"Quantity: {quantity}\n")
    receipt_text.insert(tk.END, "-----------------------------------\n")
    receipt_text.insert(tk.END, f"TOTAL AMOUNT: ₱{total:,.2f}\n")
    receipt_text.insert(tk.END, "\nThank you for ordering!\n")

    receipt_text.config(state="disabled")


def reset_order():

    pizza_var.set("Overload Pepperoni")
    size_var.set("Small")
    quantity_var.set(1)

    for variable in topping_vars.values():
        variable.set(False)

   
    update_pizza_price()

    receipt_text.config(state="normal")
    receipt_text.delete("1.0", tk.END)
    receipt_text.config(state="disabled")


button_frame = tk.Frame(window, bg="#1b1b2f")
button_frame.pack(pady=15)

calculate_button = tk.Button(
    button_frame,
    text="PLACE ORDER",
    font=("Arial", 11, "bold"),
    bg="#ffcc00",
    fg="black",
    width=18,
    command=calculate_total
)
calculate_button.grid(row=0, column=0, padx=8)

reset_button = tk.Button(
    button_frame,
    text="RESET",
    font=("Arial", 11, "bold"),
    bg="#555577",
    fg="white",
    width=12,
    command=reset_order
)
reset_button.grid(row=0, column=1, padx=8)

tk.Label(
    window,
    text="ORDER SUMMARY",
    font=("Arial", 14, "bold"),
    bg="#1b1b2f",
    fg="#ffcc00"
).pack(pady=5)

receipt_text = tk.Text(
    window,
    height=14,
    width=65,
    font=("Consolas", 11),
    bg="#2a2a45",
    fg="white",
    insertbackground="white"
)
receipt_text.pack(padx=25, pady=10)

receipt_text.config(state="disabled")

window.mainloop()
