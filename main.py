from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from datetime import datetime
import cv2
import time
import os

# Görsellerin kaydedileceği klasör
output_dir = "images"
os.makedirs(output_dir, exist_ok=True)

def crop_center(image_path, timestamp, crop_width=1000, crop_height=800, offset_x=-150, offset_y=0):
    img = cv2.imread(image_path)
    height, width, _ = img.shape

    center_x = (width // 2) + offset_x
    center_y = (height // 2) + offset_y

    x1 = center_x - crop_width // 2
    y1 = center_y - crop_height // 2
    x2 = center_x + crop_width // 2
    y2 = center_y + crop_height // 2

    cropped = img[y1:y2, x1:x2]
    cropped_path = os.path.join(output_dir, f"map_{timestamp}_cropped.png")
    cv2.imwrite(cropped_path, cropped)

    return cropped_path

def take_and_crop():
    # Otomatik doğru sürüm chromedriver yükle
    chromedriver_autoinstaller.install()

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--force-device-scale-factor=0.8")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    # Harita linki (senin verdiğin)
    maps_url = "https://www.google.com/maps/@21.4245033,39.8768942,11012m/data=!3m1!1e3!5m1!1e1"
    driver.get(maps_url)
    time.sleep(10)  # Haritanın yüklenmesi için bekleme

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    raw_path = os.path.join(output_dir, f"map_{timestamp}.png")
    driver.save_screenshot(raw_path)
    driver.quit()

    cropped_path = crop_center(raw_path, timestamp)
    print(f"✔ Kırpıldı ve kaydedildi: {cropped_path}")

if __name__ == "__main__":
    take_and_crop()
