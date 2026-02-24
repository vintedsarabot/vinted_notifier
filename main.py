import os
import requests
from vinted_scraper import VintedScraper

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# 🛒 LISTA DE BÚSQUEDAS: Añade todas las que quieras separadas por comas
URLS_VINTED =  [
  "https://www.vinted.es/catalog?catalog[]=19&brand_ids[]=38777&page=1&time=1771691054&order=newest_first&currency=EUR&price_from=0&price_to=150.00",
  "https://www.vinted.es/catalog?catalog[]=19&page=1&time=1771691110&order=newest_first&currency=EUR&price_from=0&price_to=150.00&search_text=chloe%20paddington%20style%20bag&search_by_image_uuid=",
  "https://www.vinted.es/catalog?catalog[]=19&page=1&time=1771691176&order=newest_first&currency=EUR&price_from=0&search_text=chloe%20paddington&search_by_image_uuid=&brand_ids[]=2113&price_to=300"
]

def send_telegram_msg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def check_vinted():
    scraper = VintedScraper("https://www.vinted.es")
    
    # El bot revisará cada link de la lista uno por uno
    for i, url in enumerate(URLS_VINTED):
        items = scraper.search(url)
        if not items:
            continue

        latest_item = items[0]
        # Creamos un archivo de memoria distinto para cada búsqueda (last_id_0.txt, last_id_1.txt...)
        last_id_file = f"last_id_{i}.txt"

        if os.path.exists(last_id_file):
            with open(last_id_file, "r") as f:
                last_id = f.read().strip()
        else:
            last_id = ""

        if str(latest_item.id) != last_id:
            mensaje = (
                f"🌟 *¡NUEVO ENCONTRADO!* 🌟\n\n"
                f"🛍️ {latest_item.title}\n"
                f"💰 {latest_item.price} {latest_item.currency}\n"
                f"🔗 [COMPRAR YA]({latest_item.url})"
            )
            send_telegram_msg(mensaje)
            
            with open(last_id_file, "w") as f:
                f.write(str(latest_item.id))
# Línea de prueba temporal
send_telegram_msg("🚀 ¡Hola! Si lees esto, la conexión es CORRECTA.")
if __name__ == "__main__":
    check_vinted()


