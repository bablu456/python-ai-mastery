import sys
import time
from pathlib import Path

try:
    import pygame
except ImportError:
    pygame = None


def print_lyric(text, char_delay, post_delay):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(char_delay)  # Har ek letter type hone ki speed

    time.sleep(post_delay)  # Agli line aane se pehle ka wait
    print()  # Nayi line ke liye


def start_music(audio_file):
    audio_path = Path(__file__).with_name(audio_file)

    if pygame is None:
        print("Music playback disabled: pygame is not installed.")
        print("Run 'pip install pygame' if you want audio support.\n")
        return False

    if not audio_path.exists():
        print(f"Music playback disabled: '{audio_file}' was not found.")
        print("Add the MP3 file in the same folder as lyrics.py to enable audio.\n")
        return False

    try:
        pygame.mixer.init()
        pygame.mixer.music.load(str(audio_path))
        print("Starting the magic...\n")
        time.sleep(1)
        pygame.mixer.music.play()
        return True
    except Exception as exc:
        print(f"Audio file error: {exc}")
        print("Continuing without music.\n")
        return False


def start_karaoke():
    # Yahan apne gaane ka exact naam daalna
    audio_file = "infinity.mp3"
    music_started = start_music(audio_file)

    if music_started:
        # Gaane ke start hone aur in lyrics ke aane ke beech ka gap.
        # Agar ye lyrics gaane ke beech me aate hain, toh yahan utne seconds ka sleep laga do.
        # Example: time.sleep(45) # Agar ye lines 45 seconds baad aati hain
        time.sleep(2)

    # Format: ("Lyrics", Letter_Typing_Speed, Wait_Before_Next_Line)
    # Timing maine original song ke flow ke hisaab se set ki hai
    lyrics_data = [
        ("cause youre the", 0.07, 0.1),
        ("reason i believe in fate", 0.06, 1.2),
        ("Youre my paradise", 0.07, 1.5),
        ("And ill do anything", 0.06, 0.2),
        ("to be your love or be", 0.06, 0.4),
        ("your sacrifice", 0.08, 1.5),
        ("cause i love you", 0.06, 0.2),
        ("for infinity", 0.11, 1.8),
        ("I love you for infinity", 0.07, 1.5),
        ("cause i love you", 0.08, 2.0),
    ]

    print("\n" + "=" * 30 + "\n")

    # Magic loop
    for text, char_delay, post_delay in lyrics_data:
        print_lyric(text, char_delay, post_delay)

    print("\n" + "=" * 30 + "\n")

    # Gaana khatam hone tak console khula rakhne ke liye
    if music_started:
        while pygame.mixer.music.get_busy():
            time.sleep(1)


if __name__ == "__main__":
    start_karaoke()
