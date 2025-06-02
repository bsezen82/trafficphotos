from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import cv2
import time
import os

output_dir = "images"
os.makedirs(output_dir, exist_ok=True)

def take_and_crop():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--force-device-scale-factor=0.8")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/google-chrome"  # Gerçek Chrome

    driver = webdriver.Chrome(options=options)

    maps_url = "https://www.google.com/maps/@21.4245033,39.8768942,11012m/data=!3m1!1e3!5m1!1e1"
    driver.get(maps_url)
    time.sleep(10)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    raw_path = f"{output_dir}/map_{timestamp}.png"
    cropped_path = f"{output_dir}/map_{timestamp}_cropped.png"
    driver.save_screenshot(raw_path)
    driver.quit()

    # Crop center + offset
    img = cv2.imread(raw_path)
    h, w, _ = img.shape
    cx, cy = (w // 2) + 100, h // 2
    cw, ch = 800, 500
    cropped = img[cy - ch//2:cy + ch//2, cx - cw//2:cx + cw//2]
    cv2.imwrite(cropped_path, cropped)

    print(f"✔ Kırpıldı ve kaydedildi: {cropped_path}")

if __name__ == "__main__":
    take_and_crop()
