import customtkinter as ctk
from tkinter import messagebox
from track_library import get_name, set_rating, get_play_count
import font_manager as fonts

class UpdateTracks:
    def __init__(self, window):
        window.title("Update Tracks")
        window.geometry("500x400")

        # Configure appearance mode (Light/Dark)
        ctk.set_default_color_theme("green")

        # Entry for track number
        self.track_label = ctk.CTkLabel(window, text="Enter Track Number (e.g., 01):")
        self.track_label.grid(row=0, column=0, padx=(10, 5), pady=5, sticky="w")

        self.track_entry = ctk.CTkEntry(window, placeholder_text="Track Number")
        self.track_entry.grid(row=0, column=1, padx=(5, 10), pady=5)

        # Create Rating label and entry on the same row
        self.rating_label = ctk.CTkLabel(window, text="Enter New Rating (1-5):")
        self.rating_label.grid(row=1, column=0, padx=(10, 5), pady=5, sticky="w")

        self.rating_entry = ctk.CTkEntry(window, placeholder_text="Rating")
        self.rating_entry.grid(row=1, column=1, padx=(5, 10), pady=5)

        # Button to update the track's rating (centered on a new row)
        self.update_button = ctk.CTkButton(window, text="Update Rating", command=self.update_rating)
        self.update_button.grid(row=2, columnspan=2, pady=(15, 5))

        # Frame for result display with scrollbars
        self.result_frame = ctk.CTkFrame(window)
        self.result_frame.grid(row=3, columnspan=2, pady=(10, 5), padx=10, sticky="nsew")

        # Scrollable text area for results
        self.result_display = ctk.CTkTextbox(self.result_frame, height=10, width=50, wrap="word")
        self.result_display.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # Configure the window to expand properly
        window.grid_rowconfigure(3, weight=1)
        window.grid_columnconfigure(0, weight=1)
        window.grid_columnconfigure(1, weight=1)

    def update_rating(self):
        """Update the rating of the track and display the result."""
        track_number = self.track_entry.get()

        # Validate that the track number is numeric
        if not track_number.isdigit():
            messagebox.showerror("Error", "Track number must be numeric.")
            self.clear_entries()
            return

        # Validate the rating input
        try:
            new_rating = int(self.rating_entry.get())
            if not (1 <= new_rating <= 5):
                messagebox.showerror("Error", "Rating must be between 1 and 5.")
                self.clear_entries()
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid rating.")
            self.clear_entries()
            return

        # Check if the track number is valid
        track_name = get_name(track_number)
        if track_name:
            set_rating(track_number, new_rating)
            play_count = get_play_count(track_number)
            self.result_display.delete("1.0", "end")
            self.result_display.insert("1.0", f"{track_number}: {track_name}\nNew Rating: {new_rating}\nPlay Count: {play_count}")
            messagebox.showinfo("Success", f"Track {track_number}: {track_name} rating has been updated.")
        else:
            messagebox.showerror("Error", "Invalid track number")

        # Clear the entries in all cases
        self.clear_entries()

    def clear_entries(self):
        """Clear the track number and rating entry fields."""
        self.track_entry.delete(0, "end")
        self.rating_entry.delete(0, "end")


# GUI initialization
if __name__ == "__main__":
    root = ctk.CTk()
    fonts.configure()
    gui = UpdateTracks(root)
    root.mainloop()
