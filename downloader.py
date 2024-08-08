from google_images_search import GoogleImagesSearch
from hidden import my_api, project_cx
import tkinter 
from tkinter import filedialog,messagebox
import os


# Initialize GoogleImagesSearch with API key and CX
gis = GoogleImagesSearch(my_api, project_cx)



class Google_downloader:
    def __init__(self,root):
        self.root=root
        self.root.title("Google images")
        self.root.geometry("1000x800")
        self.root.config(bg="#f0f0f0")

        self.search_successful = False

        self.label = tkinter.Label(self.root, text="Enter your search term:")
        self.label.pack(pady=15)

        self.query_entry = tkinter.Entry(self.root, width=40)
        self.query_entry.pack(pady=5)

        self.num_label = tkinter.Label(self.root, text="Enter number of images to download:")
        self.num_label.pack(pady=10)


        self.num_entry = tkinter.Entry(self.root, width=10)
        self.num_entry.pack(pady=5)
        
        self.search_button=tkinter.Button(self.root,text="search",command=self.search_images)
        self.search_button.pack(pady=5)

        self.result_text = tkinter.Text(root, height=10, width=50)
        self.result_text.pack(pady=10)

        self.save_button = tkinter.Button(self.root, text="Save Images", command=self.save_images)
        self.save_button.pack(pady=10)

    search_query_entry=None


    def search_images(self):
        query = self.query_entry.get()
        if not query:
            messagebox.showwarning("Input Error", "Please enter a search term.")
            return
        

        self.result_text.delete(1.0, tkinter.END)
        self.result_text.insert(tkinter.END, f"Searching images for: {query}\n")

        num= self.num_entry.get()
        num=int(num)
        search_query_entry=self.query_entry

        try:
            
            _search_params = {
                'q': query,
                'num': num,  
                'fileType': 'jpg',
                'rights': 'cc_publicdomain',
                'safe': 'active',
            }
            self.search_results = gis.search(search_params=_search_params)
            self.result_text.insert(tkinter.END, "Search completed successfully. You can now save the images.\n")
            self.search_successful = True
        

        except Exception as e:
            messagebox.showerror("Search Error", f"An error occurred: {str(e)}")
            self.search_successful = False
        

    def save_images(self):
        if not self.search_successful:
            messagebox.showwarning("Save Error", "Please perform a search first.")
            return

        # Get the search query from the entry widget
        self.search_query = self.query_entry.get()
        
        if not self.search_query:
            messagebox.showwarning("Save Error", "Search query is empty. Cannot save images.")
            return

        # Use filedialog to select the directory to save images
        base_directory = filedialog.askdirectory()
        
        if not base_directory:
            messagebox.showwarning("Save Error", "No directory selected. Cannot save images.")
            return

        # Create a new directory for the images based on the search query
        folder_name = self.search_query.replace(" ", "_")  # Replace spaces with underscores
        save_directory = os.path.join(base_directory, folder_name)

        try:
            os.makedirs(save_directory, exist_ok=True)
            
            # Update search parameters and call the search method with the new directory
            _search_params = {
                'q': self.search_query,
                'num': self.num_entry,  # Number of images to download
                'fileType': 'jpg',
                'rights': 'cc_publicdomain',
                'safe': 'active',
            }
            gis.search(search_params=_search_params, path_to_dir=save_directory)
            messagebox.showinfo("Success", f"Images successfully downloaded to {save_directory}")
        except Exception as e:
            messagebox.showerror("Save Error", f"An error occurred while saving images: {str(e)}")



    
if __name__ == "__main__":
    root = tkinter.Tk()
    app = Google_downloader(root)
    root.mainloop()


    

