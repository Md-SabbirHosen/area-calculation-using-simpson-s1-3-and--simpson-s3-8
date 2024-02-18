import geopandas as gpd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

latitude_entry = None
longitude_entry = None
map_canvas = None
error_label = None
result_label = None

def simpsons_one_third_area(areas):
    n = len(areas)
    h = 1
    result = h / 3 * (areas[0] + 4 * sum(areas[1:-1:2]) + 2 * sum(areas[2:-2:2]) + areas[-1])
    num_evals = n - 1
    return result, num_evals

def simpsons_three_eighth_area(areas):
    n = len(areas)
    h = 1
    result = 3 * h / 8 * (areas[0] + 3 * sum(areas[1:-1:3]) + 3 * sum(areas[2:-2:3]) + 2 * sum(areas[3:-3:3]) + areas[-1])
    num_evals = n - 1
    return result, num_evals

def main(latitude_range, longitude_range, method):
    shapefile_path = "./BGD_adm2.shx"
    try:
        gdf = gpd.read_file(shapefile_path)
        filtered_gdf = gdf.cx[longitude_range[0]:longitude_range[1], latitude_range[0]:latitude_range[1]]
        if filtered_gdf.empty:
            update_gui_error("Filtered GeoDataFrame is empty. No data available within the specified latitude and longitude range.")
            return
        fig, ax = plt.subplots()
        filtered_gdf.plot(ax=ax)
        traditional_area = filtered_gdf.geometry.area.sum()
        areas = filtered_gdf.geometry.area.tolist()
        if method == "Simpson's 1/3":
            area, num_evals = simpsons_one_third_area(areas)
        elif method == "Simpson's 3/8":
            area, num_evals = simpsons_three_eighth_area(areas)
        else:
            area, num_evals = None, None
        if area is not None:
            filtered_gdf.iloc[0:1].plot(facecolor='none', edgecolor='yellow', linewidth=2, ax=ax)
            title = "Area calculated using {} method: {:.4f}\nTotal area using traditional GIS methods: {:.4f}".format(method, area, traditional_area)
            ax.set_title(title)
            ax.set_xlabel("Longitude")
            ax.set_ylabel("Latitude")
            global map_canvas
            map_canvas = FigureCanvasTkAgg(fig, master=root)
            map_canvas.draw()
            map_canvas.get_tk_widget().grid(row=0, column=3, rowspan=5, padx=1, pady=1, sticky="nsew")
            accuracy = abs(traditional_area - area)
            result_label.config(text="Accuracy: {:.4f}\nEfficiency: {} evaluations".format(accuracy, num_evals))
        else:
            update_gui_error("Invalid method selected!")
    except IndexError:
        update_gui_error("Index out of range!")
    except Exception as e:
        update_gui_error("Error: {}".format(e))

def on_submit():
    latitude_range = [latitude_slider.get(), latitude_slider2.get()]
    longitude_range = [longitude_slider.get(), longitude_slider2.get()]
    method = method_combobox.get()
    main(latitude_range, longitude_range, method)

def update_latitude_entry(value):
    latitude_entry.config(state="normal")
    latitude_entry.delete(0, tk.END)
    latitude_entry.insert(0, "{:.2f}".format(float(value)))
    latitude_entry.config(state="readonly")

def update_longitude_entry(value):
    longitude_entry.config(state="normal")
    longitude_entry.delete(0, tk.END)
    longitude_entry.insert(0, "{:.2f}".format(float(value)))
    longitude_entry.config(state="readonly")

def update_gui_error(error_message):
    global map_canvas
    global error_label
    if map_canvas:
        map_canvas.get_tk_widget().grid_forget()
    error_label.config(text=error_message)
    if "empty" in error_message.lower():
        tk.messagebox.showinfo("Empty GeoDataFrame", "No data available within the specified latitude and longitude range.")

root = tk.Tk()
root.title("GIS Data Visualization")

submit_button = ttk.Button(root, text="Submit", command=on_submit, width=10)
submit_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

result_label = ttk.Label(root, text="", foreground="blue")
result_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

latitude_label = ttk.Label(root, text="Latitude Range:")
latitude_label.grid(row=0, column=0, padx=5, pady=5)
latitude_slider = ttk.Scale(root, from_=20.34, to=26.38, length=300, orient="horizontal", command=update_latitude_entry)
latitude_slider.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
latitude_slider.set(20.34)
latitude_slider2 = ttk.Scale(root, from_=20.34, to=26.38, length=300, orient="horizontal", command=update_latitude_entry)
latitude_slider2.grid(row=0, column=3, columnspan=2, padx=5, pady=5)
latitude_slider2.set(26.38)
latitude_entry = ttk.Entry(root, state="readonly")
latitude_entry.grid(row=0, column=5, padx=5, pady=5)
latitude_entry.insert(0, "20.34 - 26.38")

longitude_label = ttk.Label(root, text="Longitude Range:")
longitude_label.grid(row=1, column=0, padx=5, pady=5)
longitude_slider = ttk.Scale(root, from_=88.01, to=92.41, length=300, orient="horizontal", command=update_longitude_entry)
longitude_slider.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
longitude_slider.set(88.01)
longitude_slider2 = ttk.Scale(root, from_=88.01, to=92.41, length=300, orient="horizontal", command=update_longitude_entry)
longitude_slider2.grid(row=1, column=3, columnspan=2, padx=5, pady=5)
longitude_slider2.set(92.41)
longitude_entry = ttk.Entry(root, state="readonly")
longitude_entry.grid(row=1, column=5, padx=5, pady=5)
longitude_entry.insert(0, "88.01 - 92.41")

method_label = ttk.Label(root, text="Calculation Method:")
method_label.grid(row=2, column=0, padx=5, pady=5)
method_combobox = ttk.Combobox(root, values=["Simpson's 1/3", "Simpson's 3/8"], state="readonly")
method_combobox.current(0)
method_combobox.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

error_label = ttk.Label(root, text="", foreground="red")
error_label.grid(row=5, column=0, columnspan=6, padx=15, pady=5)

root.mainloop()
