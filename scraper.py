import os
import time
from playwright.sync_api import sync_playwright

def run_scraper():
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Get credentials from environment variables
        target_url = os.getenv("TARGET_URL")
        email = os.getenv("USER_EMAIL")
        password = os.getenv("USER_PASS")

        print(f"Navigating to {target_url}...")
        
        try:
            page.goto(target_url)
            
            # Basic login logic - adjust selectors if they differ
            if email and password:
                print("Attempting login...")
                page.fill('input[name="email"]', email)
                page.fill('input[name="password"]', password)
                page.click('button[type="submit"]')
                page.wait_for_load_state("networkidle")
            
            # Take a screenshot to prove it worked
            page.screenshot(path=f"{output_dir}/evidence.png")
            print("Successfully saved evidence.png")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    run_scraper()
