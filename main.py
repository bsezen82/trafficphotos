from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from datetime import datetime
import cv2
import time
import os

# === Klasör ayarı ===
output_dir = "images"
os.makedirs(output_dir, exist_ok=True)

# === Kaydırma ayarı ===
OFFSET_X = -80  # sola kaydırmak için negatif değer
OFFSET_Y = 0
CROP_WIDTH = 800
CROP_HEIGHT = 500

def take_and_crop():
    # Otomatik olarak uyumlu chromedriver kur
    chromedriver_autoinstaller.install()

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--force-device-scale-factor=0.8")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    # Trafik + uydu harita linkin
    maps_url = "https://www.google.com/maps/@21.4245033,39.8768942,11012m/data=!3m1!1e3!5m1!1e1"
    driver.get(maps_url)
    time.sleep(10)  # Yüklenmesini bekle

    # Zaman damgası ile dosya isimleri
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    raw_path = f"{output_dir}/map_{timestamp}.png"
    cropped_path = f"{output_dir}/map_{timestamp}_cropped.png"

    # Ekran görüntüsü al
    driver.save_screenshot(raw_path)
    driver.quit()

    # Görseli oku ve kırp
    img = cv2.imread(raw_path)
    h, w, _ = img.shape
    cx = (w // 2) + OFFSET_X
    cy = (h // 2) + OFFSET_Y

    cropped = img[cy - CROP_HEIGHT//2 : cy + CROP_HEIGHT//2,
                  cx - CROP_WIDTH//2  : cx + CROP_WIDTH//2]

    cv2.imwrite(cropped_path, cropped)
    print(f"✔ Kırpıldı ve kaydedildi: {cropped_path}")

if __name__ == "__main__":
    take_and_crop()
