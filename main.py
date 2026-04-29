from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os, pickle, time, base64
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_service():
    creds = None

    if os.path.exists('token.pkl'):
        with open('token.pkl', 'rb') as token:
            creds = pickle.load(token)

    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

        with open('token.pkl', 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)


def get_html(payload):
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/html':
                data = part['body']['data']
                return base64.urlsafe_b64decode(data).decode('utf-8')
            elif 'parts' in part:
                result = get_html(part)
                if result:
                    return result
    else:
        if payload['mimeType'] == 'text/html':
            data = payload['body']['data']
            return base64.urlsafe_b64decode(data).decode('utf-8')
    return None


def abrir_link_oculto(url):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    wait = WebDriverWait(driver, 15)

    driver.get(url)

    try:
        botao = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(., 'Confirmar atualização')] | //a[contains(., 'Confirmar atualização')]")
            )
        )

        botao.click()
        print("Botão 'Confirmar atualização' clicado")

    except Exception as e:
        print("Não achou botão exato, tentando fallback...", e)

        try:
            botoes = driver.find_elements(By.XPATH, "//button | //a")

            for b in botoes:
                texto = b.text.lower()
                if "confirmar" in texto or "continuar" in texto:
                    b.click()
                    print("Botão alternativo clicado:", texto)
                    break

        except Exception as e2:
            print("Falha no fallback:", e2)

    import time
    time.sleep(5)

    driver.quit()


def check_email(service, seen_ids):
    results = service.users().messages().list(
        userId='me',
        q='from:netflix subject:"Importante: Como atualizar sua residência Netflix"',
        maxResults=5
    ).execute()

    messages = results.get('messages', [])

    for msg in messages:
        if msg['id'] in seen_ids:
            continue

        msg_data = service.users().messages().get(
            userId='me',
            id=msg['id'],
            format='full'
        ).execute()

        payload = msg_data['payload']
        headers = payload['headers']

        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), '')
        date_str = next((h['value'] for h in headers if h['name'] == 'Date'), '')

        if subject != "Importante: Como atualizar sua residência Netflix":
            continue

        try:
            email_time = parsedate_to_datetime(date_str)
        except:
            continue

        now = datetime.now(timezone.utc)

        if now - email_time > timedelta(minutes=15):
            continue

        html = get_html(payload)
        if not html:
            continue

        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a')

        for link in links:
            href = link.get('href')
            text = link.get_text(strip=True).lower()

            if href and "UPDATE_HOUSEHOLD_REQUESTED_OTP_CTA" in href:
                print("\nEMAIL DETECTADO")
                print("Link:", href)
                abrir_link_oculto(href)
                seen_ids.add(msg['id'])
                return


def main():
    service = get_service()
    seen_ids = set()

    print("Monitorando emails da Netflix...")

    while True:
        check_email(service, seen_ids)
        time.sleep(30)


if __name__ == '__main__':
    main()