import customtkinter as ctk
from view_tracks import TrackViewer
from create_track_list import CreateTrackList
from update_tracks import UpdateTracks
from search_tracks import SearchTracks

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")  # Switch to dark mode
ctk.set_default_color_theme("blue")  # Blue theme for a sleek look

class JukeBoxApp:
    def __init__(self):
        # Main window configuration
        self.window = ctk.CTk()
        self.window.geometry("400x600")
        self.window.title("JukeBox")

        # Configure grid layout for a single column
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_rowconfigure(2, weight=1)
        self.window.grid_rowconfigure(3, weight=1)
        self.window.grid_rowconfigure(4, weight=1)
        self.window.grid_rowconfigure(5, weight=1)

        # Header with bold font
        self.header_lbl = ctk.CTkLabel(
            self.window,
            text="Welcome to JukeBox!",
            font=("Helvetica", 20, "bold"),
            text_color="white"
        )
        self.header_lbl.grid(row=0, column=0, padx=20, pady=30, sticky="nsew")

        # Description Label
        self.description_lbl = ctk.CTkLabel(
            self.window,
            text="Choose an option below to manage your tracks.",
            font=("Helvetica", 14),
            text_color="white"
        )
        self.description_lbl.grid(row=1, column=0, padx=50, pady=10, sticky="nsew")

        # View Tracks Button
        self.view_tracks_btn = ctk.CTkButton(
            self.window,
            text="View Tracks",
            font=("Helvetica", 14),
            command=self.view_tracks_clicked,
            fg_color="#1E90FF",  # Bright blue color
            hover_color="#4682B4",  # Darker blue on hover
            corner_radius=15
        )
        self.view_tracks_btn.grid(row=2, column=0, padx=50, pady=20, sticky="nsew")

        # Create Track List Button
        self.create_track_list_btn = ctk.CTkButton(
            self.window,
            text="Create Track List",
            font=("Helvetica", 14),
            command=self.create_track_list_clicked,
            fg_color="#32CD32",  # Lime green color
            hover_color="#228B22",  # Dark green on hover
            corner_radius=15
        )
        self.create_track_list_btn.grid(row=3, column=0, padx=50, pady=20, sticky="nsew")

        self.search_tracks_btn = ctk.CTkButton(
            self.window,
            text="Search",
            font=("Helvetica", 14),
            command=self.search_tracks_clicked,
            fg_color="#FF007F",  # Lime pink color
            hover_color="#E75480",  # Dark pink on hover
            corner_radius=15
        )
        self.search_tracks_btn.grid(row=4, column=0, padx=50, pady=20, sticky="nsew")

        # Update Tracks Button
        self.update_tracks_btn = ctk.CTkButton(
            self.window,
            text="Update Tracks",
            font=("Helvetica", 14),
            command=self.update_tracks_clicked,
            fg_color="#FF6347",  # Tomato red color
            hover_color="#FF4500",  # Orange red on hover
            corner_radius=15
        )
        self.update_tracks_btn.grid(row=5, column=0, padx=50, pady=20, sticky="nsew")

        # Status Label to show actions
        self.status_lbl = ctk.CTkLabel(
            self.window,
            text="Please select an action.",
            font=("Helvetica", 12),
            text_color="lightgray"
        )
        self.status_lbl.grid(row=6, column=0, padx=10, pady=10, sticky="nsew")

    def view_tracks_clicked(self):
        """Handle the 'View Tracks' button click."""
        self.status_lbl.configure(text="Opening View Tracks...")
        self.create_and_show_toplevel(TrackViewer)

    def create_track_list_clicked(self):
        """Handle the 'Create Track List' button click."""
        self.status_lbl.configure(text="Opening Create Track List...")
        self.create_and_show_toplevel(CreateTrackList)

    def update_tracks_clicked(self):
        """Handle the 'Update Tracks' button click."""
        self.status_lbl.configure(text="Opening Update Tracks...")
        self.create_and_show_toplevel(UpdateTracks)

    def search_tracks_clicked(self):
        """Handle the 'Search Tracks' button click."""
        self.status_lbl.configure(text="Opening Search Tracks...")
        self.create_and_show_toplevel(SearchTracks)

    def create_and_show_toplevel(self, view_class):
        """Create and display a new Toplevel window with the given view class."""
        new_window = ctk.CTkToplevel(self.window)
        new_window.lift()  # Bring the new window to the front
        new_window.attributes('-topmost', True)  # Make sure it's on top
        new_window.focus_set()  # Focus on the new window
        new_window.grab_set()  # Modal window (block interaction with main window)
        new_window.attributes('-topmost', False)  # Reset the topmost behavior
        view_class(new_window)  # Display the new view in the toplevel window

    def run(self):
        """Start the main loop."""
        self.window.mainloop()

# Run the application
if __name__ == "__main__":
    app = JukeBoxApp()
    app.run()
