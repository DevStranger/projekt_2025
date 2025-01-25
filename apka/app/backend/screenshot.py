import os
import subprocess
import logging
import hashlib
import cv2
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


def detect_presentation_area(image_path):
    """
    Wykrywa obszar prezentacji w zrzucie ekranu i przycina go.
    """
    try:
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Progowanie w celu wykrycia jasnego obszaru (często prezentacje są na białym tle)
        _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Wybierz największy kontur 
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)

            # Przytnij obraz do wykrytego obszaru
            cropped_image = image[y:y+h, x:x+w]
            cv2.imwrite(image_path, cropped_image)  # Nadpisz plik
    except Exception as e:
        print(f"Błąd podczas wykrywania obszaru prezentacji: {e}")


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

            detect_presentation_area(screenshot_path)

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

