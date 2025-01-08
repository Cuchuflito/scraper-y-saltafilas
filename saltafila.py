from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def abrir_pagina(url):
    """Abre una página web en una ventana de navegador nueva sin cerrar las anteriores."""
    options = Options()
    options.add_argument("--log-level=3")
    options.add_argument("--new-window")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)

    for i in range(100):  
        time.sleep(0.5)  
        driver.execute_script("window.open('', '_blank', 'width=800,height=600');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(f"https://queue.puntoticket.com/?c=puntoticket&e=lot178&t_cal=1&t_ct=3")  # ACA VA LA URL QUE QUIERAS PONER


    print("Abriendo múltiples ventanas. No se cerrarán.")
    input("Presiona Enter para cerrar el navegador...")

    driver.quit()

def main():
    urls = [
        "https://www.puntoticket.com/system-of-a-down-2025",
    ]

    for url in urls:
        try:
            abrir_pagina(url)
        except Exception as e:
            print(f"Error al abrir {url}: {str(e)}")

if __name__ == "__main__":
    main()
