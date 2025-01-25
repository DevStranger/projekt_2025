import os
import subprocess
import logging
import hashlib
from PIL import Image
import imagehash
from PIL import Image

def calculate_image_hash(image_path):
    """
    Oblicza perceptual hash dla obrazu.
    """
    image = Image.open(image_path)
    return str(imagehash.average_hash(image))




def is_duplicate_image(new_image_path, last_image_path):
    """
    Sprawdza, czy nowy obraz jest duplikatem ostatniego obrazu na podstawie hashy.
    """
    try:
        new_hash = calculate_image_hash(new_image_path)
        last_hash = calculate_image_hash(last_image_path)

        return new_hash == last_hash
    except Exception as e:
        print(f"Błąd podczas porównywania obrazów: {e}")
        return False  # Domyślnie uznaj, że obrazy są różne w przypadku błędu



def extract_screenshots_from_video(video_path, output_folder, fps=1):
    """
    Generuje unikalne zrzuty ekranu z wideo w regularnych odstępach czasu.
    """
    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        output_pattern = os.path.join(output_folder, "temp_screenshot_%04d.png")
        subprocess.run(
            [
                "ffmpeg",
                "-i", video_path,
                "-vf", f"fps={fps}",
                output_pattern
            ],
            check=True
        )

        # Usuń duplikaty screenshotów
        last_image_path = None
        for screenshot in sorted(os.listdir(output_folder)):
            screenshot_path = os.path.join(output_folder, screenshot)

            # Sprawdź, czy obraz jest duplikatem
            if last_image_path and is_duplicate_image(screenshot_path, last_image_path):
                logging.info(f"Usuwam duplikat: {screenshot_path}")
                os.remove(screenshot_path)
            else:
                last_image_path = screenshot_path

        print(f"Unikalne zrzuty ekranu zapisane w folderze: {output_folder}")
    except subprocess.CalledProcessError as e:
        print(f"Błąd podczas generowania zrzutów ekranu: {e}")
    except Exception as e:
        print(f"Nieoczekiwany błąd: {e}")

