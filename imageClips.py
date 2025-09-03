import sys
import os
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QFileDialog,
    QLabel,
    QLineEdit,
    QMessageBox,
)
from moviepy import *


class VideoGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("MoviePy Video Generator")
        self.setGeometry(100, 100, 500, 350)

        # Main layout
        layout = QVBoxLayout()

        # Image folder selection
        self.image_folder_label = QLabel("Select Images Folder:")
        layout.addWidget(self.image_folder_label)

        self.image_folder_button = QPushButton("Browse")
        self.image_folder_button.clicked.connect(self.select_image_folder)
        layout.addWidget(self.image_folder_button)

        # FFmpeg path selection
        self.ffmpeg_path_label = QLabel("FFmpeg Path:")
        layout.addWidget(self.ffmpeg_path_label)

        self.ffmpeg_path_input = QLineEdit()
        layout.addWidget(self.ffmpeg_path_input)

        self.ffmpeg_path_button = QPushButton("Browse")
        self.ffmpeg_path_button.clicked.connect(self.select_ffmpeg_path)
        layout.addWidget(self.ffmpeg_path_button)

        # FFplay path selection
        self.ffplay_path_label = QLabel("FFplay Path:")
        layout.addWidget(self.ffplay_path_label)

        self.ffplay_path_input = QLineEdit()
        layout.addWidget(self.ffplay_path_input)

        self.ffplay_path_button = QPushButton("Browse")
        self.ffplay_path_button.clicked.connect(self.select_ffplay_path)
        layout.addWidget(self.ffplay_path_button)

        # Generate video button
        self.generate_button = QPushButton("Generate Video")
        self.generate_button.clicked.connect(self.generate_video)
        layout.addWidget(self.generate_button)

        # Play video button
        self.play_button = QPushButton("Play Video")
        self.play_button.clicked.connect(self.play_video)
        layout.addWidget(self.play_button)

        # Set layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Variables
        self.image_folder = None
        self.video_path = "output_video.mp4"

    def select_image_folder(self):
        self.image_folder = QFileDialog.getExistingDirectory(self, "Select Images Folder")
        if self.image_folder:
            self.image_folder_label.setText(f"Selected Folder: {self.image_folder}")

    def select_ffmpeg_path(self):
        ffmpeg_path, _ = QFileDialog.getOpenFileName(self, "Select FFmpeg Executable", "", "Executable Files (*.exe)")
        if ffmpeg_path:
            self.ffmpeg_path_input.setText(ffmpeg_path)

    def select_ffplay_path(self):
        ffplay_path, _ = QFileDialog.getOpenFileName(self, "Select FFplay Executable", "", "Executable Files (*.exe)")
        if ffplay_path:
            self.ffplay_path_input.setText(ffplay_path)

    def generate_video(self):
        if not self.image_folder:
            QMessageBox.warning(self, "Error", "Please select an images folder.")
            return

        ffmpeg_path = self.ffmpeg_path_input.text().strip()
        ffplay_path = self.ffplay_path_input.text().strip()

        if not ffmpeg_path or not ffplay_path:
            QMessageBox.warning(self, "Error", "Please provide paths for FFmpeg and FFplay.")
            return

        # Set MoviePy's FFmpeg and FFplay paths
        os.environ["FFMPEG_BINARY"] = ffmpeg_path
        os.environ["FFPLAY_BINARY"] = ffplay_path

        try:
            # Get list of images from the folder
            images = sorted(
                [
                    os.path.join(self.image_folder, img)
                    for img in os.listdir(self.image_folder)
                    if img.endswith((".png", ".jpg", ".jpeg"))
                ]
            )

            if not images:
                QMessageBox.warning(self, "Error", "No images found in the selected folder.")
                return

            # Create video from images
            clip = ImageSequenceClip(images, fps=1)  # 1 frame per second

            font = "./SweetieSummer.ttf"

            # Add subtitle text
            text_clip = TextClip(
                font=font, text="MoviePy example", font_size=50, color="white", bg_color="black", duration=clip.duration
            )

            # Combine video and text
            final_clip = CompositeVideoClip([clip, text_clip])

            # Save the video
            final_clip.write_videofile(self.video_path, codec="libx264")

            QMessageBox.information(self, "Success", f"Video saved as {self.video_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def play_video(self):
        if not os.path.exists(self.video_path):
            QMessageBox.warning(self, "Error", "No video found. Please generate a video first.")
            return

        ffplay_path = self.ffplay_path_input.text().strip()
        if not ffplay_path:
            QMessageBox.warning(self, "Error", "Please provide the path to FFplay.")
            return

        try:
            # Play the video using FFplay
            os.system(f'"{ffplay_path}" {self.video_path}')
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while playing the video: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoGeneratorApp()
    window.show()
    sys.exit(app.exec_())