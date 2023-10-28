import os
import subprocess
import requests
from pydub import AudioSegment

# Function to download audio from a YouTube video using youtube-dl
def download_audio(youtube_url, output_file):
    subprocess.call(['youtube-dl', '--extract-audio', '--audio-format', 'wav', '-o', output_file, youtube_url])

# Function to transcribe audio using PocketSphinx
def transcribe_audio(audio_file):
    # Convert the audio file to 16 kHz, 16-bit PCM format (required by PocketSphinx)
    audio = AudioSegment.from_file(audio_file)
    audio = audio.set_frame_rate(16000).set_sample_width(2).set_channels(1)

    # Export the converted audio to a temporary WAV file
    temp_wav_file = 'temp_audio.wav'
    audio.export(temp_wav_file, format='wav')

    # Perform speech recognition using PocketSphinx
    cmd = f'pocketsphinx_continuous -infile {temp_wav_file} -hmm en-us -lm en-us.lm.dmp -dict cmudict-en-us.dict'
    output = subprocess.check_output(cmd, shell=True, universal_newlines=True)

    # Print the transcribed text
    print(output)

    # Clean up temporary WAV file
    os.remove(temp_wav_file)

if __name__ == '__main__':
    youtube_url = input('Enter the YouTube URL: ')
    output_file = 'audio.wav'
    
    download_audio(youtube_url, output_file)
    transcribe_audio(output_file)
