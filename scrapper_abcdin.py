import os
import logging
import warnings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tkinter as tk
from tkinter import font
import time

# Suprimir mensajes de TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Solo mostrar mensajes FATAL
logging.getLogger('tensorflow').setLevel(logging.FATAL)
warnings.filterwarnings("ignore", category=UserWarning, module='tensorflow')

# Configuración de Selenium para usar Chrome
driver_path = os.path.join(os.getcwd(), 'chromedriver.exe')
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service)

def get_prices():
    base_url = "https://www.abcdin.cl/especial/top-venta-cyber/?icn=home--cyber&ici=huincha-vip-1_generico_generico"
    start = 0
    sz = 36
    page_count = 0
    products = []

    while True:
        url = f"{base_url}&start={start}&sz={sz}" if page_count > 0 else base_url
        driver.get(url)

        wait = WebDriverWait(driver, 60)  # Aumentar tiempo de espera
        try:
            print(f"Processing page {page_count + 1}...")

            # Esperar a que los productos estén cargados
            product_elements = wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".lp-product-tile")))

            if not product_elements:
                print("No products found on the page.")
                break

            print(f"Found {len(product_elements)} products on page {page_count + 1}.")

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

            # Incrementar el contador de página y el parámetro `start` para la siguiente página
            page_count += 1
            start += sz

            # Verificar si hay más productos
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-page.rounded-0.mobile-margin-left.page-end")
                if not next_button.is_enabled():
                    print("Next button is disabled. Exiting pagination.")
                    break  # No hay más páginas
            except:
                print("Next button not found. Exiting pagination.")
                break  # No se encontró el botón de siguiente página, salir del bucle

        except Exception as e:
            print(f"An error occurred: {e}")
            import traceback
            traceback.print_exc()
            driver.save_screenshot('error_screenshot.png')  # Capturar la pantalla cuando ocurra el error
            break

    print("Products captured successfully.")
    # Ordenar por precio de oferta
    products.sort(key=lambda x: x[0])
    print("Sorted products:")
    text_box.insert(tk.END, f"Found {len(products)} products across {page_count} pages:\n\n")
    for price_promotion, price_internet, name, link in products:
        text_box.insert(tk.END, f"Oferta: ${price_promotion:,.2f}, Internet: ${price_internet:,.2f} - {name} - ", "bold")
        text_box.insert(tk.END, link + "\n", "link")

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
