import os
import platform
import json
from datetime import datetime
from yt_dlp import YoutubeDL
from pydub import AudioSegment



first_message = """
  _____                      _                 _   _ 
 |  __ \                    | |               | | | |
 | |  | | _____      ___ __ | | ___   __ _  __| | | |
 | |  | |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` | | |
 | |__| | (_) \ V  V /| | | | | (_) | (_| | (_| | |_|
 |_____/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_| (_)                                       
"""
copyrights = """
By Ahmed Hesham..... 

discord: ahmhesham
"""
# ANSI color escape sequences
class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


config_file_path = 'config.json'
download_history_file_path = 'download_history.json'

def load_config():
    try:
        if os.path.exists(config_file_path) and os.path.getsize(config_file_path) > 0:
            with open(config_file_path, 'r') as config_file:
                return json.load(config_file)
        else:
            return {"download_path": get_download_path()}
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"{Color.FAIL}Error loading config file: {e}{Color.ENDC}")
        return {"download_path": get_download_path()}

def save_config(config):
    try:
        with open(config_file_path, 'w') as config_file:
            json.dump(config, config_file, indent=4)
        print(f"{Color.OKGREEN}Config file saved successfully.{Color.ENDC}")
    except Exception as e:
        print(f"{Color.FAIL}Error saving config file: {e}{Color.ENDC}")

def load_download_history():
    try:
        if os.path.exists(download_history_file_path) and os.path.getsize(download_history_file_path) > 0:
            with open(download_history_file_path, 'r') as history_file:
                return json.load(history_file)
        else:
            return []
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"{Color.FAIL}Error loading download history file: {e}{Color.ENDC}")
        return []

def save_download_history(history):
    try:
        with open(download_history_file_path, 'w') as history_file:
            json.dump(history, history_file, indent=4)
        print(f"{Color.OKGREEN}Download history saved successfully.{Color.ENDC}")
    except Exception as e:
        print(f"{Color.FAIL}Error saving download history: {e}{Color.ENDC}")

def add_to_download_history(entry):
    history = load_download_history()
    history.append(entry)
    save_download_history(history)

def get_download_path():
    if platform.system() == 'Windows':
        return os.path.join(os.getenv('USERPROFILE'), 'Downloads')
    else:
        return os.path.join(os.getenv('HOME'), 'Downloads')

def create_initial_files():
    try:
        if not os.path.exists(config_file_path):
            save_config({"download_path": get_download_path()})
        if not os.path.exists(download_history_file_path):
            save_download_history([])
    except Exception as e:
        print(f"{Color.FAIL}Error creating initial files: {e}{Color.ENDC}")

def download_youtube_video_as_mp3(url, config):
    output_path = config["download_path"]
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s')
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', 'Video')
            ydl.download([url])
        
        print(f"{Color.OKGREEN}Downloaded and converted to MP3: {video_title}{Color.ENDC}")
        add_to_download_history({
            "name": video_title,
            "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "platform": "YouTube",
            "path": output_path,
            "url": url
        })
    except Exception as e:
        print(f"{Color.FAIL}An error occurred: {e}{Color.ENDC}")

def download_spotify_song(url, config):
    try:
        output_path = config["download_path"]
        
        command = f"spotdl --output {output_path} {url}"
        os.system(command)
        
        song_title = os.path.basename(url)
        
        print(f"{Color.OKGREEN}Downloaded from Spotify: {song_title}{Color.ENDC}")
        
        # Adding to download history
        add_to_download_history({
            "name": song_title,
            "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "platform": "Spotify",
            "path": output_path,
            "url": url
        })
    except Exception as e:
        print(f"{Color.FAIL}An error occurred: {e}{Color.ENDC}")

def settings_menu(config):
    while True:
        print(f"\n{Color.HEADER}Settings Menu:{Color.ENDC}")
        print(f"{Color.BOLD}Current download path is {config['download_path']}.{Color.ENDC}")
        print(f"{Color.OKBLUE}1- Change download path{Color.ENDC}")
        print(f"{Color.OKBLUE}2- Go back{Color.ENDC}")
        
        choice = input(f"{Color.WARNING}Enter your choice: {Color.ENDC}")
        
        if choice == '1':
            new_path = input(f"{Color.OKBLUE}Current download path is {config['download_path']}. Enter new download path: {Color.ENDC}")
            if os.path.isdir(new_path):
                config["download_path"] = new_path
                save_config(config)
                print(f"{Color.OKGREEN}Download path updated to: {new_path}{Color.ENDC}")
            else:
                print(f"{Color.FAIL}Invalid path. Please try again.{Color.ENDC}")
        elif choice == '2':
            print(f"{Color.WARNING}Returning to main menu.{Color.ENDC}")
            break
        else:
            print(f"{Color.FAIL}Invalid choice. Please try again.{Color.ENDC}")

def main():
    create_initial_files()
    config = load_config()
    download_path = config["download_path"]
    
    while True:
        print(f"{Color.WARNING}{first_message}{Color.ENDC}")
        print(f"\n{Color.HEADER}Menu:{Color.ENDC}")
        print(f"{Color.OKBLUE}1- YouTube download{Color.ENDC}")
        print(f"{Color.OKBLUE}2- Spotify download{Color.ENDC}")
        print(f"{Color.OKBLUE}3- Settings{Color.ENDC}")
        print(f"{Color.OKBLUE}4- View Download History{Color.ENDC}")
        print(f"{Color.OKBLUE}5- Exit{Color.ENDC}")
        print(f"{Color.HEADER}{copyrights}{Color.ENDC}")
        
        choice = input(f"{Color.WARNING}Enter your choice: {Color.ENDC}")
        
        if choice == '1':
            youtube_url = input(f"{Color.OKBLUE}Enter YouTube URL: {Color.ENDC}")
            download_youtube_video_as_mp3(youtube_url, config) 
        elif choice == '2':
            spotify_url = input(f"{Color.OKBLUE}Enter Spotify URL: {Color.ENDC}")
            download_spotify_song(spotify_url, config)  
        elif choice == '3':
            settings_menu(config)
        elif choice == '4':
            history = load_download_history()
            print(f"\n{Color.HEADER}Download History:{Color.ENDC}")
            for entry in history:
                print(f"\n{Color.OKGREEN}[\nName: {entry['name']}, \nTime: {entry['time']}, \nPlatform: {entry['platform']}, \nURL: {entry.get('url', '-')}, \nPath: {entry['path']}\n]{Color.ENDC}\n")
        elif choice == '5':
            print(f"{Color.WARNING}Exiting...{Color.ENDC}")
            break
        else:
            print(f"{Color.FAIL}Invalid choice. Please try again.{Color.ENDC}")


if __name__ == "__main__":
    main()