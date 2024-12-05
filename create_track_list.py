import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
import time
import threading
import pygame
import os
from mutagen.mp3 import MP3
from track_library import increment_play_count, get_name

class CreateTrackList:
    def __init__(self, window):
        self.window = window
        window.title("Create Track List")
        window.geometry("1300x700")

        # Initialize pygame mixer
        pygame.mixer.init()

        # Initialize player variables
        self.playlist = []
        self.current_track_index = 0
        self.is_playing = False
        self.progress = 0
        self.current_track_length = 0
        self.manually_skipped = False
        self.skip_position = 0
        self.start_time = 0
        self.elapsed_time = 0

        # Create main container
        self.main_container = ctk.CTkFrame(window, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=30, pady=20)

        # Create header
        self.create_header()

        # Initialize horizontal container for playlist and player sections
        self.horizontal_container = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.horizontal_container.pack(fill="x", pady=(10, 20))
        
        # Create playlist section
        self.create_playlist_section()
        
        # Create player section
        self.create_player_section()

        # Start progress update thread
        self.start_progress_thread()

        # Bind window close event
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_header(self):
        header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))

        title_label = ctk.CTkLabel(
            header_frame,
            text   ="CREATE TRACK LIST",
            font=("Inter", 24, "bold"),
            text_color="#1DB954"  # Spotify-like green
        )
        title_label.pack(pady=(0, 10))

        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Create and manage your playlists with style",
            font=("Inter", 14),
            text_color="#666666"
        )
        subtitle_label.pack()

    def create_playlist_section(self):
        """Create a modern playlist input section"""
        # Playlist Container with shadow effect
        playlist_container = ctk.CTkFrame(
            self.horizontal_container,
            corner_radius=15,
            border_width=1,
            border_color="#E0E0E0"
        )
        playlist_container.pack(side="left", fill="y", expand=True, padx=10, pady=0)

        # Track input section with modern layout
        input_frame = ctk.CTkFrame(playlist_container, fg_color="transparent")
        input_frame.pack(pady=20, padx=30)

        # track number input
        self.track_entry = ctk.CTkEntry(
            input_frame,
            width=250,
            height=45,
            corner_radius=25,
            placeholder_text="Enter Track Number (e.g., 01)",
            font=("Inter", 13),
            border_color="#1DB954"
        )
        self.track_entry.pack(side="left", padx=(0, 10))

        # Modern add button
        self.add_button = ctk.CTkButton(
            input_frame,
            text="Add to Playlist",
            height=45,
            corner_radius=25,
            font=("Inter", 13, "bold"),
            fg_color="#1DB954",
            hover_color="#18A64B",
            command=self.add_to_playlist
        )
        self.add_button.pack(side="left")

        # Playlist display with Modern styling
        self.playlist_display = ctk.CTkTextbox(
            playlist_container,
            width=600,
            height=200,
            corner_radius=10,
            font=("Inter", 12),
            border_width=1,
            border_color="#1DB954"
        )
        self.playlist_display.pack(pady=(10, 20), padx=30)

        # Modern reset button
        self.reset_button = ctk.CTkButton(
            playlist_container,
            text="Reset Playlist",
            width=150,
            height=40,
            corner_radius=20,
            font=("Inter", 13),
            fg_color="#FF5252",
            hover_color="#FF1744",
            command=self.reset_playlist
        )
        self.reset_button.pack(pady=(0, 20))

    def create_player_section(self):
        """Create a Modern media player section"""
        # Player container with shadow effect
        player_container = ctk.CTkFrame(
            self.horizontal_container,
            corner_radius=15,
            border_width=1,
            border_color="#E0E0E0"
        )
        player_container.pack(side="left", fill="both", expand=True, padx=10)

        # Now playing section
        self.now_playing_label = ctk.CTkLabel(
            player_container,
            text="NOW PLAYING",
            font=("Inter", 14, "bold"),
            text_color="#666666"
        )
        self.now_playing_label.pack(pady=(20, 5))

        # Track info with Modern font
        self.track_info = ctk.CTkLabel(
            player_container,
            text="",
            font=("Inter", 18, "bold"),
            text_color="#1DB954"
        )
        self.track_info.pack(pady=(0, 20))

        # Progress section
        progress_frame = ctk.CTkFrame(player_container, fg_color="transparent")
        progress_frame.pack(fill="x", padx=30)

        # Modern progress bar
        self.progress_bar = ctk.CTkProgressBar(
            progress_frame,
            width=600,
            height=6,
            corner_radius=3,
            progress_color="#1DB954",
            fg_color="#E0E0E0"
        )
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0)
        self.progress_bar.bind("<Button-1>", self.skip_in_track)

        # Time labels with Modern font
        time_frame = ctk.CTkFrame(progress_frame, fg_color="transparent")
        time_frame.pack(fill="x")

        self.current_time = ctk.CTkLabel(
            time_frame,
            text="0:00",
            font=("Inter", 12),
            text_color="#666666"
        )
        self.current_time.pack(side="left")

        self.total_time = ctk.CTkLabel(
            time_frame,
            text="0:00",
            font=("Inter", 12),
            text_color="#666666"
        )
        self.total_time.pack(side="right")

        # Control Buttons Frame
        self.controls_frame = ctk.CTkFrame(player_container, fg_color="transparent")
        self.controls_frame.pack(pady=10)

        # Previous Button
        self.prev_button = ctk.CTkButton(
            self.controls_frame,
            text="⏮",
            width=60,
            command=self.previous_track,
            corner_radius=20,
            fg_color="green"
        )
        self.prev_button.pack(side="left", padx=10)

        # Play/Pause Button
        self.play_button = ctk.CTkButton(
            self.controls_frame,
            text="▶️",
            width=60,
            command=self.toggle_play_pause,
            corner_radius=20,
            fg_color="green"
        )
        self.play_button.pack(side="left", padx=10)

        # Next Button
        self.next_button = ctk.CTkButton(
            self.controls_frame,
            text="⏭",
            width=60,
            command=self.next_track,
            corner_radius=20,
             fg_color="green"
        )
        self.next_button.pack(side="left", padx=10)

        # Volume control with Modern styling
        volume_frame = ctk.CTkFrame(player_container, fg_color="transparent")
        volume_frame.pack(pady=20)

        self.volume_label = ctk.CTkLabel(
            volume_frame,
            text="🔊",
            font=("Inter", 14)
        )
        self.volume_label.pack(side="left", padx=5)

        self.volume_slider = ctk.CTkSlider(
            volume_frame,
            from_=0,
            to=1,
            number_of_steps=100,
            width=200,
            progress_color="#1DB954",
            button_color="#1DB954",
            button_hover_color="#18A64B",
            command=self.update_volume
        )
        self.volume_slider.pack(side="left", padx=5)
        self.volume_slider.set(0.5)

        # Control buttons frame
        controls_frame = ctk.CTkFrame(player_container, fg_color="transparent")
        controls_frame.pack(pady=(0, 20))

    def add_to_playlist(self):
        track_number = self.track_entry.get()

        if not track_number.isdigit():
            messagebox.showerror("Error", "Track number must be numeric.")
            return

        track_name = get_name(track_number)

        if track_name:
            if track_number in self.playlist:
                messagebox.showwarning("Warning", f"Track {track_number} is already in the playlist.")
            else:
                self.playlist.append(track_number)
                self.update_playlist_display()
                messagebox.showinfo("Success", f"Track {track_number}: {track_name} added to playlist.")

                if len(self.playlist) == 1:
                    self.play_current_track()
        else:
            messagebox.showerror("Error", "Invalid track number")

        self.track_entry.delete(0, ctk.END)

    def update_playlist_display(self):
        self.playlist_display.delete("1.0", ctk.END)
        for track_number in self.playlist:
            track_name = get_name(track_number)
            if track_name:
                self.playlist_display.insert(ctk.END, f"{track_number}: {track_name}\n")

    def reset_playlist(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.play_button.configure(text="▶️")
        
        self.playlist.clear()
        self.playlist_display.delete("1.0", ctk.END)
        self.track_info.configure(text="")
        self.reset_progress()
        
        messagebox.showinfo("Playlist Reset", "The playlist has been cleared.")
        self.track_entry.delete(0, ctk.END)

    def get_track_path(self, track_number):
        return os.path.join("tracks", f"{track_number}.mp3")

    def play_current_track(self):
        self.reset_progress()

        if 0 <= self.current_track_index < len(self.playlist):
            track_number = self.playlist[self.current_track_index]
            track_path = self.get_track_path(track_number)

            if os.path.exists(track_path):
                track_name = get_name(track_number)
                self.track_info.configure(text=f"{track_number}: {track_name}")

                audio = MP3(track_path)
                self.current_track_length = audio.info.length

                total_min = int(self.current_track_length) // 60
                total_sec = int(self.current_track_length) % 60
                self.total_time.configure(text=f"{total_min}:{total_sec:02d}")

                pygame.mixer.music.stop()
                pygame.mixer.music.load(track_path)
                pygame.mixer.music.play()

                self.is_playing = True
                self.play_button.configure(text="⏸")
                
                increment_play_count(track_number)
            else:
                messagebox.showerror("Error", f"Track file not found: {track_path}")
                self.next_track()

    def toggle_play_pause(self):
        if not self.playlist:
            messagebox.showwarning("Warning", "Please add tracks to the playlist first.")
            return

        if self.is_playing:
            pygame.mixer.music.pause()
            self.play_button.configure(text="▶️")
        else:
            pygame.mixer.music.unpause()
            self.play_button.configure(text="⏸")
        self.is_playing = not self.is_playing

    def reset_progress(self):
        self.progress = 0
        self.progress_bar.set(0)
        self.current_time.configure(text="0:00")
        self.manually_skipped = False
        self.elapsed_time = 0
        self.start_time = 0

    def next_track(self):
        if not self.playlist:
            return

        if self.current_track_index < len(self.playlist) - 1:
            self.current_track_index += 1
        else:
            self.current_track_index = 0

        self.play_current_track()

    def previous_track(self):
        if not self.playlist:
            return

        if self.current_track_index > 0:
            self.current_track_index -= 1
            self.play_current_track()

    def update_volume(self, value):
        pygame.mixer.music.set_volume(float(value))

    def skip_in_track(self, event):
        if not self.is_playing or self.current_track_length <= 0:
            return

        progress_width = self.progress_bar.winfo_width()
        click_x = event.x
        fraction = click_x / progress_width
        new_time = fraction * self.current_track_length
        pygame.mixer.music.set_pos(new_time)

        self.progress = fraction
        self.progress_bar.set(self.progress)

        current_min = int(new_time) // 60
        current_sec = int(new_time) % 60
        self.current_time.configure(text=f"{current_min}:{current_sec:02d}")

        self.manually_skipped = True
        self.skip_position = new_time
        self.start_time = time.time()

    def update_progress(self):
        """Update progress bar and time labels based on actual playback position."""
        while True:
            if self.is_playing and self.current_track_length > 0:
                if self.manually_skipped:
                    self.elapsed_time = time.time() - self.start_time
                    current_pos = self.skip_position + self.elapsed_time
                else:
                    current_pos = pygame.mixer.music.get_pos() / 1000

                if self.window.winfo_exists():
                    self.progress = current_pos / self.current_track_length

                    if self.progress_bar.winfo_exists():
                        self.progress_bar.set(self.progress)

                    current_min = int(current_pos) // 60
                    current_sec = int(current_pos) % 60
                    if self.current_time.winfo_exists():
                        self.current_time.configure(text=f"{current_min}:{current_sec:02d}")

                    if not pygame.mixer.music.get_busy() and self.is_playing:
                        self.next_track()

            time.sleep(0.1)

    def start_progress_thread(self):
        """Start a separate thread for updating progress"""
        progress_thread = threading.Thread(target=self.update_progress, daemon=True)
        progress_thread.start()

    def on_closing(self):
        """Handle window closing"""
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        self.window.destroy()

# GUI initialization
if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")