import requests, re, time
from pathlib import Path

BASE = "https://ftp.ncbi.nlm.nih.gov/geo/series"

def list_dir(url):
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    links = re.findall(r'href="([^"?/][^"]*)"', r.text)
    return [l for l in links if not l.startswith("..") and "://" not in l]

def download(url, dest, retries=5):
    dest = Path(dest)
    if dest.exists() and dest.stat().st_size > 0:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    for i in range(retries):
        try:
            r = requests.get(url, timeout=60, stream=True)
            r.raise_for_status()
            with open(dest, "wb") as f:
                for chunk in r.iter_content(8192):
                    f.write(chunk)
            print("OK", dest)
            return
        except Exception as e:
            print("retry", i, dest.name, e)
            time.sleep(3)
    print("FAILED", url)

def crawl(url, local_root):
    for name in list_dir(url):
        if name.endswith("/"):
            crawl(url + name, local_root / name)
        else:
            download(url + name, local_root / name)

for gse in ["GSE186527", "GSE130438", "GSE279540"]:
    prefix = gse[:-3] + "nnn"
    suppl_url = f"{BASE}/{prefix}/{gse}/suppl/"
    local = Path(f"./data/raw/{gse}/suppl_https")
    print("=== ", gse)
    crawl(suppl_url, local)