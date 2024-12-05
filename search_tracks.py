import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from googleapiclient.discovery import build
from youtube_downloader import YouTubeDownloader
import font_manager as fonts

class SearchTracks:
    def __init__(self, window):
        # Initialize the main window
        self.window = window
        window.title("Track Finder")
        window.geometry("850x650")
        
        # YouTube API setup
        self.API_KEY = 'AIzaSyABr15ZATckpKWHrw4RcbLq3RdJFryl-FI'
        self.youtube = build('youtube', 'v3', developerKey=self.API_KEY)
        
        # Initialize the downloader
        self.downloader = YouTubeDownloader()
        
        self.create_ui()

    def create_ui(self):
        # Create the main container frame
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Search bar frame
        self.search_area = ctk.CTkFrame(self.main_frame)
        self.search_area.pack(fill=tk.X, padx=10, pady=10)

        # Search input field
        self.query_var = tk.StringVar()
        self.search_input = ctk.CTkEntry(
            self.search_area, 
            width=450,
            placeholder_text="Search your favorite songs...",
            textvariable=self.query_var
        )
        self.search_input.pack(side=tk.LEFT, padx=5)
        
        # Search button
        self.search_button = ctk.CTkButton(
            self.search_area,
            text="Find Tracks",
            fg_color="#1DB954",
            hover_color="#168d40",
            command=self.fetch_videos
        )
        self.search_button.pack(side=tk.LEFT, padx=5)
        
        # Frame to display the search results
        self.result_area = ctk.CTkFrame(self.main_frame)
        self.result_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Keyboard shortcut for quick search (Enter key)
        self.window.bind('<Return>', lambda e: self.fetch_videos())

    def fetch_videos(self):
        search_term = self.query_var.get()
        if not search_term:
            return
        
        # Clear previous results before displaying new search results
        for widget in self.result_area.winfo_children():
            widget.destroy()

        try:
            # Query the YouTube API for videos based on the search term
            request = self.youtube.search().list(
                part="snippet",
                maxResults=5,
                q=search_term,
                type="video"
            )
            response = request.execute()

            # Display video results
            for item in response['items']:
                video_frame = ctk.CTkFrame(self.result_area)
                video_frame.pack(fill=tk.X, padx=5, pady=5)
                
                # Get and display the video thumbnail
                thumbnail_url = item['snippet']['thumbnails']['default']['url']
                response = requests.get(thumbnail_url)
                img = Image.open(BytesIO(response.content))
                resized_img = img.resize((220, 110))
                photo = ImageTk.PhotoImage(resized_img)

                thumbnail_label = tk.Label(video_frame, image=photo)
                thumbnail_label.image = photo
                thumbnail_label.pack(side=tk.LEFT, padx=10, pady=10)
                
                # Display the video title
                video_title = item['snippet']['title']
                title_label = ctk.CTkLabel(
                    video_frame,
                    text=video_title,
                    wraplength=420
                )
                title_label.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.BOTH)
                
                # Button to add video to library
                add_button = ctk.CTkButton(
                    video_frame,
                    text="Add to Library",
                    fg_color="#1DB954",
                    hover_color="#168d40",
                    width=110,
                    command=lambda vid_id=item['id']['videoId'], title=video_title: self.add_track_to_library(vid_id, title)
                )
                add_button.pack(side=tk.RIGHT, padx=10)

        except Exception as e:
            error_message = ctk.CTkLabel(
                self.result_area,
                text=f"Failed to fetch videos: {str(e)}"
            )
            error_message.pack(padx=10, pady=10)

    def add_track_to_library(self, video_id, title):
        self.window.update()
        
        # Download the video and save it
        track_id = self.downloader.download_and_save(video_id, title)

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")
    
    root = ctk.CTk()
    fonts.configure()
    app = SearchTracks(root)
    root.mainloop()
