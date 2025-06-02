from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from datetime import datetime
import cv2
import time
import os

# === Çıktı klasörü ===
output_dir = "images"
os.makedirs(output_dir, exist_ok=True)

# === Görsel Ayarları ===
WINDOW_WIDTH = 3840
WINDOW_HEIGHT = 2160
DEVICE_SCALE = 1.25

CROP_WIDTH = 2000    
CROP_HEIGHT = 1500
OFFSET_X = -400  # daha geniş görüntüde sola orantılı kaydırma
OFFSET_Y = 0

def take_and_crop():
    # Otomatik olarak uyumlu chromedriver kurar
    chromedriver_autoinstaller.install()

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument(f"--window-size={WINDOW_WIDTH},{WINDOW_HEIGHT}")
    options.add_argument(f"--force-device-scale-factor={DEVICE_SCALE}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    # Harita linkin (trafik katmanlı, 3D)
    maps_url = "https://www.google.com/maps/@21.4245033,39.8768942,14012m/data=!3m1!1e3!5m1!1e1"
    driver.get(maps_url)
    time.sleep(10)  # yüklenmesi için bekle

    # Dosya isimleri
    timestamp = (datetime.utcnow() + timedelta(hours=3)).strftime("%Y%m%d_%H%M%S")
    raw_path = f"{output_dir}/map_{timestamp}.png"
    cropped_path = f"{output_dir}/map_{timestamp}_cropped.png"

    # Görüntüyü kaydet
    driver.save_screenshot(raw_path)
    driver.quit()

    # Görüntüyü kırp
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
