from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

class AdNabuFixedTask:
    def __init__(self):
        options = Options()
        # Adding arguments to ignore the "DEPRECATED_ENDPOINT" console noise
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.wait = WebDriverWait(self.driver, 20)
        self.url = "https://adnabu-store-assignment1.myshopify.com/"

    def run(self):
        try:
            print("→ Navigating to store...")
            self.driver.get(self.url)
            self.driver.maximize_window()

            # 1. Login
            pwd_input = self.wait.until(EC.element_to_be_clickable((By.NAME, "password")))
            pwd_input.send_keys("AdNabuQA")
            self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
            print("→ Login successful.")

            # 2. Select Product (Using partial text to avoid exact match errors)
            print("→ Searching for product link...")
            # We use a broad XPath to find the snowboard link regardless of exact ID
            product_xpath = "//a[contains(text(), 'Liquid') or contains(@href, 'liquid')]"
            product = self.wait.until(EC.presence_of_element_located((By.XPATH, product_xpath)))
            
            # Use JavaScript to scroll and click (Avoids "Element Click Intercepted" errors)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", product)
            time.sleep(1) # Brief pause for scroll to settle
            self.driver.execute_script("arguments[0].click();", product)
            print("→ Product page opened.")

            # 3. Add to Cart
            print("→ Clicking Add to Cart...")
            add_to_cart = self.wait.until(EC.element_to_be_clickable((By.NAME, "add")))
            self.driver.execute_script("arguments[0].click();", add_to_cart)

            # 4. Handle Cart Drawer and Checkout
            print("→ Waiting for Cart Drawer...")
            # Shopify drawers can take a second to animate
            checkout_btn = self.wait.until(EC.element_to_be_clickable((By.NAME, "checkout")))
            self.driver.execute_script("arguments[0].click();", checkout_btn)

            # 5. Final Verification
            self.wait.until(EC.url_contains("checkouts"))
            print("\n✅ SUCCESS: Task completed. Item is in the checkout flow.")

        except Exception as e:
            print(f"\n❌ FAILED AT STEP: {self.driver.current_url}")
            print(f"Error details: {str(e)}")
        finally:
            time.sleep(5)
            self.driver.quit()

if __name__ == "__main__":
    AdNabuFixedTask().run()
