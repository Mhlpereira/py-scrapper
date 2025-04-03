import requests
import os
import zipfile
from bs4 import BeautifulSoup

def download_files():
    url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
    
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    pdf_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if 'Anexo' in link.text and href.endswith('.pdf'):
            if 'Anexo I' in link.text or 'Anexo II' in link.text:
                pdf_links.append(href)
    
    downloaded_files = []
    for pdf_url in pdf_links:
        filename = os.path.join("downloads", pdf_url.split('/')[-1])
        
        pdf_response = requests.get(pdf_url)
        with open(filename, 'wb') as f:
            f.write(pdf_response.content)
        
        downloaded_files.append(filename)
        print(f"Downloaded: {filename}")
    
    zip_filename = "anexos.zip"
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for file in downloaded_files:
            zipf.write(file, arcname=os.path.basename(file))
    
    print(f"Files compressed into: {zip_filename}")
    return downloaded_files

if __name__ == "__main__":
    download_files()