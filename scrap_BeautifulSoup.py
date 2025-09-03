from bs4 import BeautifulSoup
import pandas as pd
import os
import sys
from pathlib import Path

# type: ignore  # Ignorar avisos de type checking para BeautifulSoup


def parse_html_elements(html_path: Path) -> pd.DataFrame:
    """Parse inputs and buttons from an HTML file and return a DataFrame."""
    content = html_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(content, "html.parser")
    elements = soup.find_all(["input", "button"])  # type: ignore[arg-type]

    data = []
    for element in elements:
        try:
            element_type = getattr(element, "name", "unknown")
            element_id = getattr(element, "get", lambda x, default="": default)("id", "")
            element_name = getattr(element, "get", lambda x, default="": default)("name", "")
            element_value = getattr(element, "get", lambda x, default="": default)("value", "")

            # Tratamento especial para classes
            try:
                if hasattr(element, "get"):
                    element_class_list = element.get("class", [])  # type: ignore[assignment]
                    if isinstance(element_class_list, list):
                        element_class = " ".join(str(cls) for cls in element_class_list)
                    else:
                        element_class = str(element_class_list)
                else:
                    element_class = ""
            except Exception:
                element_class = ""

            data.append(
                {
                    "Type": element_type,
                    "ID": element_id,
                    "Name": element_name,
                    "Value": element_value,
                    "Class": element_class,
                }
            )
        except Exception as e:
            # Pular elementos problemáticos
            print(f"Erro ao processar elemento: {e}")
            continue

    return pd.DataFrame(data)


def main(argv: list[str]) -> int:
    base_path = Path(__file__).resolve().parent
    downloads_path = base_path / "downloads"

    # Arquivo HTML de entrada (padrão), pode ser sobrescrito via argumento
    html_filename = (
        argv[1]
        if len(argv) > 1
        else "https_apps.itaipu.gov.br_SAM_SMA_Reports_SSAsExecuted.aspx.htm"
    )
    file_path = downloads_path / html_filename

    if not file_path.exists():
        print(f"Arquivo HTML não encontrado: {file_path}")
        print("Por favor, coloque o arquivo HTML na pasta downloads/ ou passe o caminho como argumento.")
        return 1

    df = parse_html_elements(file_path)
    print(df)

    output_filename = "web_elements_updated.csv"
    output_path = downloads_path / output_filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Arquivo CSV salvo em: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
