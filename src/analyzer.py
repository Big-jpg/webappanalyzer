import os
import json
import re
import requests
from bs4 import BeautifulSoup

TECH_DIR = os.path.join(os.path.dirname(__file__), "technologies")

class Analyzer:
    def __init__(self):
        self.technologies = self.load_fingerprints()

    def load_fingerprints(self):
        fingerprints = []
        for fname in os.listdir(TECH_DIR):
            if fname.endswith(".json"):
                with open(os.path.join(TECH_DIR, fname), "r", encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                        fingerprints.extend(data.values())
                    except Exception as e:
                        print(f"Error loading {fname}: {e}")
        return fingerprints

    def analyze(self, url):
        try:
            response = requests.get(url, timeout=10)
            html = response.text
            headers = {k.lower(): v for k, v in response.headers.items()}
        except Exception as e:
            return {"url": url, "error": str(e)}

        detected = []

        for tech in self.technologies:
            name = tech.get("name")
            implies = tech.get("implies", [])
            detected_flag = False

            # HTML regex match
            for key in ["html", "script", "meta"]:
                for entry in tech.get(key, []):
                    pattern = entry.get("regex")
                    if pattern and re.search(pattern, html, re.IGNORECASE):
                        detected_flag = True
                        break

            # Headers
            for hname, hdata in tech.get("headers", {}).items():
                if hname.lower() in headers:
                    pattern = hdata.get("regex")
                    if pattern and re.search(pattern, headers[hname.lower()], re.IGNORECASE):
                        detected_flag = True
                        break

            if detected_flag:
                detected.append({"name": name, "implies": implies})

        return {"url": url, "technologies": detected}
