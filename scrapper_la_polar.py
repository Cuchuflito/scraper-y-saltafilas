from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tkinter as tk
from tkinter import font
import os

# Configuración de Selenium para usar Chrome
driver_path = os.path.join(os.getcwd(), 'chromedriver.exe')
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service)

def get_prices():
    url = "https://www.lapolar.cl"
    driver.get(url)

    try:
        wait = WebDriverWait(driver, 60)  # Aumentar tiempo de espera
        print("Waiting for product prices to be located...")

        # Obtener todos los productos
        product_elements = wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".lp-product-tile, .pdp-link[itemprop='name']")))

        if not product_elements:
            print("No products found on the page.")
            return

        print(f"Found {len(product_elements)} products.")

        products = []
        for product in product_elements:
            try:
                name_element = product.find_element(By.CSS_SELECTOR, ".pdp-link[itemprop='name'] a")
                price_promotion_element = product.find_element(By.CSS_SELECTOR, ".la-polar.price .price-value")
                price_internet_element = product.find_element(By.CSS_SELECTOR, ".internet .price-value")
                link_element = product.find_element(By.CSS_SELECTOR, ".pdp-link[itemprop='name'] a")

                name = name_element.text.strip()
                price_promotion = float(price_promotion_element.get_attribute('data-value').strip().replace(',', ''))
                price_internet = float(price_internet_element.get_attribute('data-value').strip().replace(',', ''))
                link = link_element.get_attribute('href').strip()

                products.append((price_promotion, price_internet, name, link))
            except Exception as e:
                print(f"Error processing product: {e}")

        print("Products captured successfully.")
        # Ordenar por precio de oferta
        products.sort(key=lambda x: x[0])
        print("Sorted products:")
        for price_promotion, price_internet, name, link in products:
            text_box.insert(tk.END, f"Oferta: ${price_promotion:,.2f}, Internet: ${price_internet:,.2f} - {name} - ", "bold")
            text_box.insert(tk.END, link + "\n", "link")

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
        driver.save_screenshot('error_screenshot.png')  # Capturar la pantalla cuando ocurra el error

# Configuración de la GUI
root = tk.Tk()
root.title("Web Scraper de Precios con Selenium")

text_box = tk.Text(root, height=20, width=80)
text_box.pack()

# Configuración de las fuentes para los estilos
bold_font = font.Font(text_box, text_box.cget("font"))
bold_font.configure(weight="bold")

link_font = font.Font(text_box, text_box.cget("font"))
link_font.configure(underline=True)

text_box.tag_configure("bold", font=bold_font)
text_box.tag_configure("link", font=link_font, foreground="blue")

button = tk.Button(root, text="Obtener Precios", command=get_prices)
button.pack()

root.mainloop()

# Cerrar el driver
driver.quit()
