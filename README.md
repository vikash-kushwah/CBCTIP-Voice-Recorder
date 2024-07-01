Voice Recorder Application
This Python application allows you to record, play, and save audio using the sounddevice module for audio capture and playback, and wavio for saving audio files in WAV format.

Features
Record Audio: Start and stop recording with the ability to capture audio for up to 30 minutes.
Play Audio: Playback recorded audio with play and stop functionalities.
Save Audio: Save recorded audio as a WAV file with a timestamped filename.
Progress Tracking: Real-time display of recording and playback progress.
User Interface: Simple GUI using Tkinter for intuitive interaction.
Installation
Ensure you have Python 3.x installed along with the necessary modules:

bash
Copy code
pip install sounddevice wavio
Usage
Run the application by executing the main.py script:

bash
Copy code
python main.py
Interface
Record Button: Click to start or stop recording.
Play Button: Click to start or stop playback of the recorded audio.
Save Button: Click to save the recorded audio as a WAV file.
Progress Display: Shows current recording or playback progress.
Dependencies
sounddevice: Used for recording and playing audio.
wavio: Used for writing WAV files.
Notes
Ensure your system's microphone is correctly configured and accessible by the application.
The application uses non-blocking recording for smooth interaction and responsiveness.
Author
Name: Vikash Kushwaha
Contact: [Your Contact Information]
GitHub: [Your GitHub Profile]
