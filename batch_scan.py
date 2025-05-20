import yaml
import csv
from src.analyzer import Analyzer

def load_config(path="job-config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def scan_urls(urls):
    analyzer = Analyzer()
    results = []
    for url in urls:
        print(f"Scanning {url}...")
        result = analyzer.analyze(url)
        results.append({
            "url": url,
            "technologies": ", ".join([t["name"] for t in result.get("technologies", [])])
        })
    return results

def save_to_csv(results, out_path="output.csv"):
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["url", "technologies"])
        writer.writeheader()
        for row in results:
            writer.writerow(row)

if __name__ == "__main__":
    config = load_config()
    urls = config.get("urls", [])
    output = config.get("output", "output.csv")
    results = scan_urls(urls)
    save_to_csv(results, output)
