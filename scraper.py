import os
import requests
import time

def download_file(url, folder):
    # Set a real User-Agent so the server doesn't block the GitHub Runner
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        # Use allow_redirects=True to follow Wayback Machine hops
        response = requests.get(url, headers=headers, stream=True, timeout=30, allow_redirects=True)
        
        if response.status_code == 200:
            filename = url.split('/')[-1] if not url.endswith('/') else "index.html"
            # Clean filename
            filename = filename.split('?')[0]
            
            filepath = os.path.join(folder, filename)
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            # Verify file size
            size = os.path.getsize(filepath)
            print(f"Downloaded: {filename} ({size} bytes)")
            
            if size == 0:
                print(f"Warning: {filename} is empty. Deleting.")
                os.remove(filepath)
        else:
            print(f"Failed to fetch {url} - Status: {response.status_code}")
            
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def run():
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # List of targets based on your previous logs
    targets = [
        "https://igceng.com/academics/Academic-Calendar.pdf",
        "https://igceng.com/RTI/RTI.pdf",
        "https://web.archive.org/web/20240519150610if_/https://igceng.com/academics/Academic-Calendar.pdf"
    ]

    for target in targets:
        download_file(target, output_dir)
        time.sleep(2) # Prevent being blocked

if __name__ == "__main__":
    run()
