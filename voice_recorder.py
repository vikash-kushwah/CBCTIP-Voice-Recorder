# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 00:09:50 2024

@author: vikash kushwaha
"""

import sounddevice as sd
import wavio
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import datetime
import threading

# Constants
FS = 44100  # Sample rate
MAX_DURATION = 30 * 60  # 30 minutes in seconds

class VoiceRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Recorder")
        self.root.geometry("300x200")
        self.root.resizable(False, False)

        self.recording = None
        self.is_recording = False
        self.is_playing = False
        self.duration = 0

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # Button styling
        button_style = {"padx": 10, "pady": 5, "width": 15, "bg": "#E0E0E0", "fg": "#333333"}

        # Record button
        self.record_button = tk.Button(self.root, text="Record", command=self.toggle_record, **button_style)
        self.record_button.pack(pady=10)

        # Play button
        self.play_button = tk.Button(self.root, text="Play", command=self.toggle_play, state=tk.DISABLED, **button_style)
        self.play_button.pack(pady=10)

        # Save button
        self.save_button = tk.Button(self.root, text="Save", command=self.save_audio, state=tk.DISABLED, **button_style)
        self.save_button.pack(pady=10)

        # Progress label
        self.progress_label = tk.Label(self.root, text="", bg="white", fg="#333333")
        self.progress_label.pack(pady=10)

        # Progress scale
        self.progress = ttk.Scale(self.root, orient="horizontal", length=200, from_=0, to=MAX_DURATION, state=tk.DISABLED)
        self.progress.pack(pady=10)

    def toggle_record(self):
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        try:
            self.recording = sd.rec(int(MAX_DURATION * FS), samplerate=FS, channels=2, blocking=False)
            self.is_recording = True
            self.duration = 0
            self.record_button.config(text="Stop", bg="#FF6347", fg="white")
            self.play_button.config(state=tk.DISABLED)
            self.save_button.config(state=tk.DISABLED)
            self.progress.config(state=tk.DISABLED)
            self.update_recording_progress()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start recording: {e}")

    def stop_recording(self):
        try:
            sd.stop()
            self.is_recording = False
            self.record_button.config(text="Record", bg="#E0E0E0", fg="#333333")
            self.play_button.config(state=tk.NORMAL)
            self.save_button.config(state=tk.NORMAL)
            self.progress.config(state="normal", to=self.duration)
            self.progress_label.config(text="Recording finished")
            self.recording = self.recording[:int(self.duration * FS)]  # Trim the recording to actual duration
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop recording: {e}")

    def update_recording_progress(self):
        if self.is_recording:
            self.duration += 1
            self.progress_label.config(text=f"Recording: {self.duration}s")
            if self.duration < MAX_DURATION:
                self.root.after(1000, self.update_recording_progress)
            else:
                self.stop_recording()

    def toggle_play(self):
        if not self.is_playing:
            self.start_playing()
        else:
            self.stop_playing()

    def start_playing(self):
        if self.recording is not None:
            try:
                self.is_playing = True
                self.play_button.config(text="Stop", bg="#FF6347", fg="white")
                self.progress.set(0)
                self.progress_label.config(text="Playing...")
                threading.Thread(target=self.play_audio).start()  # Play audio in a separate thread
            except Exception as e:
                messagebox.showerror("Error", f"Failed to play audio: {e}")
        else:
            messagebox.showwarning("Warning", "No recording found!")

    def play_audio(self):
        try:
            sd.play(self.recording, FS)
            sd.wait()  # Wait until playback is finished
            self.is_playing = False
            self.play_button.config(text="Play", bg="#E0E0E0", fg="#333333")
            self.progress_label.config(text="Playback stopped")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop playback: {e}")

    def stop_playing(self):
        try:
            sd.stop()
            self.is_playing = False
            self.play_button.config(text="Play", bg="#E0E0E0", fg="#333333")
            self.progress_label.config(text="Playback stopped")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop playback: {e}")

    def save_audio(self):
        if self.recording is not None:
            try:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                default_filename = f"Recording_{timestamp}.wav"

                file_path = filedialog.asksaveasfilename(defaultextension=".wav", initialfile=default_filename,
                                                        filetypes=[("WAV files", "*.wav")])
                if file_path:
                    wavio.write(file_path, self.recording, FS, sampwidth=2)
                    messagebox.showinfo("Info", f"Audio saved as {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save audio: {e}")
        else:
            messagebox.showwarning("Warning", "No recording found!")

# Main function
def main():
    root = tk.Tk()
    app = VoiceRecorderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
