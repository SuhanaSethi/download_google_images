from google_images_search import GoogleImagesSearch
from hidden import my_api, project_cx, sender_email, sender_password  
import tkinter
from tkinter import messagebox
import smtplib
from email.message import EmailMessage
from io import BytesIO


gis = GoogleImagesSearch(my_api, project_cx)

class GoogleDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("Google Images to Email")
        self.root.geometry("600x400")
        self.root.config(bg="#f0f0f0")

        self.search_results = [] 


        tkinter.Label(self.root, text="Enter your search term:").pack(pady=10)
        self.query_entry = tkinter.Entry(self.root, width=40)
        self.query_entry.pack(pady=5)

        tkinter.Label(self.root, text="Enter number of images to download:").pack(pady=10)
        self.num_entry = tkinter.Entry(self.root, width=10)
        self.num_entry.pack(pady=5)

        tkinter.Label(self.root, text="Enter recipient's email:").pack(pady=10)
        self.email_entry = tkinter.Entry(self.root, width=40)
        self.email_entry.pack(pady=5)


        tkinter.Button(self.root, text="Search", command=self.search_images).pack(pady=5)
        tkinter.Button(self.root, text="Send to Email", command=self.send_images_to_email).pack(pady=10)

        self.result_text = tkinter.Text(self.root, height=10, width=50)
        self.result_text.pack(pady=10)

    def search_images(self):
        query = self.query_entry.get()
        num = self.num_entry.get()

        if not query or not num.isdigit():
            messagebox.showwarning("Input Error", "Please enter a valid search term and number of images.")
            return

        num = int(num)
        self.result_text.delete(1.0, tkinter.END)
        self.result_text.insert(tkinter.END, f"Searching for {num} images of '{query}'...\n")

        try:
            search_params = {
                'q': query,
                'num': num,
                'fileType': 'jpg',
                'rights': 'cc_publicdomain',
                'safe': 'active',
            }
            gis.search(search_params=search_params)
            self.search_results = gis.results()  

            if not self.search_results:
                raise ValueError("No images found for the given search query.")

            self.result_text.insert(tkinter.END, "Search successful! Ready to send the images via email.\n")
        except Exception as e:
            messagebox.showerror("Search Error", f"An error occurred: {str(e)}")
            self.search_results = []  

    def send_images_to_email(self):
        if not self.search_results:
            messagebox.showwarning("Error", "Please search for images first.")
            return

        recipient_email = self.email_entry.get()
        if not recipient_email:
            messagebox.showwarning("Input Error", "Please enter a valid email address.")
            return

        try:
       
            msg = EmailMessage()
            msg['Subject'] = f"Images of {self.query_entry.get()}"
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg.set_content(f"Attached are the images for '{self.query_entry.get()}' you requested.")

         
            for image in self.search_results:
                image_data = BytesIO()
                image.copy_to(image_data)  
                image_name = image.url.split("/")[-1]
                msg.add_attachment(image_data.getvalue(), maintype='image', subtype='jpeg', filename=image_name)


            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(sender_email, sender_password)
                smtp.send_message(msg)


            messagebox.showinfo("Success", f"Images sent to {recipient_email} successfully!")
        except Exception as e:
            messagebox.showerror("Email Error", f"An error occurred while sending email: {str(e)}")

if __name__ == "__main__":
    root = tkinter.Tk()
    app = GoogleDownloader(root)
    root.mainloop()
