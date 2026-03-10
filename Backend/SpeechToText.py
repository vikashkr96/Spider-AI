from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import time
import mtranslate as mt

# ================= ENV =================
env_vars = dotenv_values(".env")
InputLanguage = env_vars.get("InputLanguage", "en")

# ================= PATHS =================
BASE_DIR = os.getcwd()
DATA_DIR = os.path.join(BASE_DIR, "Data")
FRONTEND_DIR = os.path.join(BASE_DIR, "Frontend", "Files")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(FRONTEND_DIR, exist_ok=True)

HTML_PATH = os.path.join(DATA_DIR, "Voice.html")

# ================= HTML =================
HtmlCode = f"""
<!DOCTYPE html>
<html>
<body>
<button id="start">Start</button>
<button id="end">Stop</button>
<p id="output"></p>

<script>
let recognition;
document.getElementById("start").onclick = () => {{
    recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = "{InputLanguage}";
    recognition.continuous = true;
    recognition.onresult = (event) => {{
        document.getElementById("output").innerText =
        event.results[event.results.length - 1][0].transcript;
    }};
    recognition.start();
}};
document.getElementById("end").onclick = () => recognition.stop();
</script>
</body>
</html>
"""

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(HtmlCode)

# ================= CHROME =================
options = Options()
options.add_argument("--use-fake-ui-for-media-stream")
options.add_argument("--use-fake-device-for-media-stream")
options.add_argument("--disable-infobars")
options.add_argument("--disable-notifications")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# ================= HELPERS =================
def QueryModifier(text):
    text = text.strip()
    if not text.endswith(('.', '?', '!')):
        text += '?'
    return text.capitalize()

def UniversalTranslator(text):
    return mt.translate(text, "en", "auto").capitalize()

# ================= MAIN FUNCTION =================
def SpeechRecognition():
    driver.get("file:///" + HTML_PATH.replace("\\", "/"))
    time.sleep(1)

    driver.find_element(By.ID, "start").click()

    for _ in range(30):  # wait max 30 seconds
        try:
            text = driver.find_element(By.ID, "output").text.strip()
            if text:
                driver.find_element(By.ID, "end").click()

                if InputLanguage.lower().startswith("en"):
                    return QueryModifier(text)
                else:
                    return QueryModifier(UniversalTranslator(text))
        except:
            pass
        time.sleep(10)

    return "No speech detected."

# ================= RUN =================
if __name__ == "__main__":
    try:
        result = SpeechRecognition()
        print("Recognized:", result)
    finally:
        driver.quit()
