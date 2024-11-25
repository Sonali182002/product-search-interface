

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from capture_detect_image import capture_image, classify_image
from product_search_API import search_product_on_ebay, search_product
import webbrowser

class ProductSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Product Search Interface")
        self.root.geometry("400x500")

        # Heading Label
        self.label = tk.Label(root, text="Product Search Interface", font=("Arial", 18))
        self.label.pack(pady=10)

        # Search entry
        self.search_entry = tk.Entry(root, width=30)
        self.search_entry.pack(pady=5)

        # Search button
        self.search_button = tk.Button(root, text="Search by text", command=self.search_by_text)
        self.search_button.pack(pady=5)

        # Capture image button
        self.capture_button = tk.Button(root, text="Search by image", command=self.search_by_image)
        self.capture_button.pack(pady=5)

        # Results label
        self.result_label = tk.Label(root, text="Results", font=("Arial", 14))
        self.result_label.pack(pady=10)

        #result are to display links
        self.result_frame=tk.Frame(self.root)
        self.result_frame.pack(fill="both",expand=True,padx=20,pady=20)

    def search_by_text(self):
        product_name = self.search_entry.get()
        if product_name:
            self.search_product_on_sites(product_name)
        else:
            messagebox.showwarning("Input Error", "Please enter a product name.")

    def search_by_image(self):
        image_path = capture_image()
        if image_path:
         self.perform_image_recognition(image_path)
        else:
         messagebox.showwarning("Input Error", "Please click a product photo.")
         
        
    def perform_image_recognition(self, image_path):
        detected_labels = classify_image(image_path)
        if detected_labels:
            #product_name = detected_labels[0] 
            self.search_product_on_sites(detected_labels)
             # Use the first label as product name
        else:
            messagebox.showwarning("Recognition Error", "No recognizable product found in the image.")

    def search_product_on_sites(self, detected_labels):
        # Get product links from eBay
        ebay_links = search_product_on_ebay(detected_labels)
        # Get product links from Google search
        google_search_links = search_product(detected_labels)
        # Display both sets of product links
        self.display_product_links(ebay_links)
        self.display_product_links(google_search_links)

    def display_product_links(self, product_links):
        for index,item in enumerate(product_links):
            title=item.get("title")
            link=item.get("link")

            result_label=tk.Label(self.result_frame,text=f"{title}:{link}",fg="blue",cursor="hand2")
            result_label.grid(row=index,column=0,sticky="w",pady=5)

            result_label.bind("<Button-1>",lambda e, url=link: self.open_link(url))
    def open_link(self, url):
        webbrowser.open(url)

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductSearchApp(root)
    root.mainloop()
   