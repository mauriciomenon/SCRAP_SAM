from bs4 import BeautifulSoup
import pandas as pd
import os

# type: ignore  # Ignorar avisos de type checking para BeautifulSoup

# Caminhos cross-platform
base_path = os.path.dirname(os.path.abspath(__file__))
downloads_path = os.path.join(base_path, "downloads")

# Arquivo HTML de entrada (ajuste conforme necessário)
html_filename = "https_apps.itaipu.gov.br_SAM_SMA_Reports_SSAsExecuted.aspx.htm"
file_path = os.path.join(downloads_path, html_filename)

# Verificar se o arquivo existe
if not os.path.exists(file_path):
    print(f"Arquivo HTML não encontrado: {file_path}")
    print("Por favor, coloque o arquivo HTML na pasta downloads/")
    exit(1)

# Carregar o conteúdo do arquivo HTML
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# Analisar o conteúdo HTML
soup = BeautifulSoup(content, 'html.parser')

# Encontrar todos os elementos input e button
elements = soup.find_all(['input', 'button'])

# Preparar uma lista para armazenar os dados
data = []

# Extrair informações relevantes de cada elemento
for element in elements:
    try:
        element_type = getattr(element, 'name', 'unknown')
        element_id = getattr(element, 'get', lambda x, default='': default)('id', '')
        element_name = getattr(element, 'get', lambda x, default='': default)('name', '')
        element_value = getattr(element, 'get', lambda x, default='': default)('value', '')

        # Tratamento especial para classes
        try:
            if hasattr(element, 'get'):
                element_class_list = element.get('class', [])
                if isinstance(element_class_list, list):
                    element_class = ' '.join(str(cls) for cls in element_class_list)
                else:
                    element_class = str(element_class_list)
            else:
                element_class = ''
        except:
            element_class = ''

        data.append({
            'Type': element_type,
            'ID': element_id,
            'Name': element_name,
            'Value': element_value,
            'Class': element_class
        })
    except Exception as e:
        # Pular elementos problemáticos
        print(f"Erro ao processar elemento: {e}")
        continue

# Criar um DataFrame com os dados
df = pd.DataFrame(data)

# Exibir o DataFrame
print(df)

# Salvar o DataFrame como uma tabela em um arquivo CSV
output_filename = "web_elements_updated.csv"
output_path = os.path.join(downloads_path, output_filename)
df.to_csv(output_path, index=False)

print(f"Arquivo CSV salvo em: {output_path}")
