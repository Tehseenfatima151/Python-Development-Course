import tkinter as tk

window = tk.Tk()
window.title("Mile to Km Converter")
window.config(padx=20, pady=20)


def miles_to_km():
    try:
        miles = float(miles_input.get())
    except ValueError:
        km_result_label.config(text="Invalid input")
    else:
        km = round(miles * 1.609, 2)
        km_result_label.config(text=f"{km}")


# Miles input
miles_input = tk.Entry(width=7)
miles_input.grid(column=1, row=0)

miles_label = tk.Label(text="Miles")
miles_label.grid(column=2, row=0)

# Result row
km_result_label = tk.Label(text="0")
km_result_label.grid(column=1, row=1)

is_equal_label = tk.Label(text="is equal to")
is_equal_label.grid(column=0, row=1)

km_label = tk.Label(text="Km")
km_label.grid(column=2, row=1)

# Calculate button
calculate_button = tk.Button(text="Calculate", command=miles_to_km)
calculate_button.grid(column=1, row=2)

window.mainloop()