from moviepy.editor import VideoFileClip, AudioFileClip

# Define the paths of the input video and audio files
video_path = "/Users/samir/Desktop/Youtube Videos/3 Michelin star Araki vlog/Araki vlog.fcpbundle/15-04-2023 1/Original Media/20230415_C0567.mp4"
audio_path = "/Users/samir/Desktop/Youtube Videos/3 Michelin star Araki vlog/Araki vlog.fcpbundle/15-04-2023 1/Original Media/DJI_05_20230415_193126.wav"

# Load the video and audio files
video = VideoFileClip(video_path)
audio = AudioFileClip(audio_path)

# Set the audio of the video to the synchronized audio
video = video.set_audio(audio)

# Define the output video file path
output_path = "output.mp4"

# Save the synchronized video with the new audio
video.write_videofile(output_path, codec="libx264", audio_codec="aac")