import requests
import json
import time
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import webbrowser


webhook_url = ""  # Global variable to hold the webhook URL
monitoring_threads = []  # List to hold monitoring threads
products = []  # List to store product information (URL and Name)

def open_github():
    webbrowser.open_new("https://github.com/alperkyoruk")

def get_product_name_cimri(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    product_name = soup.find('h1', {'class': 's1wytv2f-2 jTAVuj'}).text
    return product_name

def get_product_info_cimri(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    price_div = soup.find('span', {'class': 's1wl91l5-4 cBVHJG'})
    if price_div:
        price = price_div.text.strip()
    else:
        price = "Price not available"

    return price

def get_product_name_itopya(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    product_name_element = soup.find('div', {'class': 'col-12 col-xl-7'})
    if product_name_element:
        product_name = product_name_element.text.strip()
    else:
        product_name = "Product name not available"
    return product_name

def get_product_info_itopya(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    price_div = soup.find('div', {'class': 'amount my-3'})
    if price_div:
        price = price_div.text.strip()
    

    return price

def get_product_name_trendyol(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    product_name = soup.find('h1', {'class': 'pr-new-br'}).text
    return product_name

def get_product_info_trendyol(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    price_div = soup.find('div', {'class': 'pr-bx-w'})

    if price_div:
        price = price_div.text.strip()
    else:
        price = "Price not available"

    return price

def send_message(webhook_url, message):
    data = {'content': message}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
    if response.status_code != 204:
        print("Failed to send Discord message")

def start_monitoring():
    if not products:
        messagebox.showwarning("Warning", "Please import a product list first.")
        return

    webhook_url = webhook_entry.get()
    if not webhook_url:
        messagebox.showwarning("Warning", "Please enter the webhook URL.")
        return

    webhook_entry.config(state=tk.DISABLED)

    def monitor(product):
        url = product["url"]
        product_name = product["name"]
        interval = int(interval_entry.get()) * 60

        try:
            # Fetch initial product information
            if "cimri" in url:
                initial_price = get_product_info_cimri(url)
            elif "itopya" in url:
                initial_price = get_product_info_itopya(url)
            elif "trendyol" in url:
                initial_price = get_product_info_trendyol(url)
            else:
                messagebox.showwarning("Warning", f"No site selected for {url}.")
                return

            send_message(webhook_url, f"Product Name: {product_name}\nProduct Price: {initial_price}\n URL: {url}")

            while True:
                current_price = ""

                if "cimri" in url:
                    current_price = get_product_info_cimri(url)
                elif "trendyol" in url:
                    current_price = get_product_info_trendyol(url)
                elif "itopya" in url:
                    current_price = get_product_info_itopya(url)

                if current_price and current_price != initial_price:
                    send_message(webhook_url, f"Product price has changed!\nNew Price for {product_name}: {current_price} Here: {url}")
                    initial_price = current_price



                time_remaining = interval
                while time_remaining > 0 and not stop_flag.is_set():
                    mins, secs = divmod(time_remaining, 60)
                    timer_label.configure(text=f"Next check in {mins:02d}:{secs:02d}")
                    time.sleep(1)
                    time_remaining -= 1

                if stop_flag.is_set():
                    break

        except Exception as e:
            messagebox.showerror("Error", str(e))

    global monitoring_threads, stop_flag
    stop_flag = threading.Event()
    monitoring_threads = []
    for product in products:
        monitoring_thread = threading.Thread(target=monitor, args=(product,))
        monitoring_thread.daemon = True
        monitoring_thread.start()
        monitoring_threads.append(monitoring_thread)

def stop_monitoring():
    global stop_flag, monitoring_threads
    if stop_flag:
        stop_flag.set()
        for thread in monitoring_threads:
            if thread and thread.is_alive():
                thread.join()
        timer_label.configure(text="Monitoring stopped")

def import_product_list():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            with open(file_path, "r") as file:
                global products
                products = []
                product_listbox.delete(0, tk.END)
                for line in file:
                    url = line.strip()
                    if url:
                        product_name = ""
                        if cimri_var.get() and "cimri" in url:
                            product_name = get_product_name_cimri(url)
                        elif itopya_var.get() and "itopya" in url:
                            product_name = get_product_name_itopya(url)
                        elif trendyol_var.get() and "trendyol" in url:
                            product_name = get_product_name_trendyol(url)
                        else:
                            messagebox.showwarning("Warning", f"No site selected for {url}.")
                            continue

                        products.append({"url": url, "name": product_name})
                        product_listbox.insert(tk.END, product_name)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import product list:\n{str(e)}")

# GUI Setup
root = tk.Tk()
root.title("Product Price Monitor")
root.geometry("400x600")

webhook_label = tk.Label(root, text="Webhook URL:")
webhook_label.pack()
webhook_entry = tk.Entry(root, width=50)
webhook_entry.pack()

url_label = tk.Label(root, text="Product URL:")
url_label.pack()
url_entry = tk.Entry(root, width=50)
url_entry.pack()

interval_label = tk.Label(root, text="Monitoring Interval (minutes):")
interval_label.pack()
interval_entry = tk.Entry(root, width=50)
interval_entry.pack()

discount_label = tk.Label(root, text="Discount Percentage:")
discount_label.pack()
discount_entry = tk.Entry(root, width=50)
discount_entry.pack()

import_button = tk.Button(root, text="Import TXT", command=import_product_list)
import_button.pack()

start_button = tk.Button(root, text="Start Monitoring", command=start_monitoring)
start_button.pack()

stop_button = tk.Button(root, text="Stop Monitoring", command=stop_monitoring)
stop_button.pack()

product_list_label = tk.Label(root, text="Product List:")
product_list_label.pack()

product_listbox = tk.Listbox(root, width=40, height=10)
product_listbox.pack()

timer_label = tk.Label(root, text="Next check in: -")
timer_label.pack()

# Checkboxes for different sites
sites_frame = tk.Frame(root)
sites_frame.pack()

cimri_var = tk.IntVar()
itopya_var = tk.IntVar()
trendyol_var = tk.IntVar()

cimri_checkbox = tk.Checkbutton(sites_frame, text="Cimri", variable=cimri_var)
itopya_checkbox = tk.Checkbutton(sites_frame, text="İtopya", variable=itopya_var)
trendyol_checkbox = tk.Checkbutton(sites_frame, text="Trendyol", variable=trendyol_var)

cimri_checkbox.pack()
itopya_checkbox.pack()
trendyol_checkbox.pack()

stop_flag = None

built_by_label = tk.Label(root, text="Built By alperkyoruk", font=("Arial", 10), fg="blue", cursor="hand2")
built_by_label.pack(side=tk.BOTTOM)

built_by_label.bind("<Button-1>", lambda e: open_github())

root.mainloop()
