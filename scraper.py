import os
import requests

def force_download():
    output_dir = "Others"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Add headers to trick the server into thinking you are a logged-in user
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": "https://joining.indraganesan.org/",
        "Accept": "application/pdf,application/xhtml+xml,text/html"
    }

    # Example: List of the hex-style files you found
    targets = [
        "https://igceng.com/Others/228e67_00360e8d022d45469642239833ae26b6.pdf",
        "https://igceng.com/Others/01_NSS_2018-2019.pdf"
    ]

    for url in targets:
        filename = url.split('/')[-1]
        print(f"Downloading {filename}...")
        
        try:
            r = requests.get(url, headers=headers, stream=True)
            if r.status_code == 200:
                with open(f"{output_dir}/{filename}", 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024):
                        f.write(chunk)
                print(f"Success: {os.path.getsize(f'{output_dir}/{filename}')} bytes")
            else:
                print(f"Failed: HTTP {r.status_code}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    force_download()
