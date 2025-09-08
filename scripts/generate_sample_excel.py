#!/usr/bin/env python3
"""
Generate a minimal Excel compatible with the project's DataLoader
(expects header=2, i.e., data starts after two header rows).

Writes to: ~/git/scrap_sam_rework/downloads/Report.xlsx

Safe and non-destructive.
"""
from __future__ import annotations

from pathlib import Path
from datetime import datetime
import pandas as pd


REWORK = Path.home() / "git" / "scrap_sam_rework"
OUT = REWORK / "downloads" / "Report.xlsx"


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)

    # Build data rows matching positional indices used by SSAColumns (0..21)
    rows = [
        [
            "SSA-1001",
            "Aberta",
            "",
            "LOC-01",
            "Área A",
            "EQ-10",
            "2024-W45",
            datetime(2024, 11, 1, 8, 0, 0),
            "Troca de componente",
            "ENG",
            "MANUT",
            "João",
            "Sistema",
            "S3.7",
            "S2",
            "Sim",
            "Alice",
            "2024-W46",
            "Bob",
            "Execução planejada",
            "SAM",
            "",
        ],
        [
            "SSA-1002",
            "Em Execução",
            "SSA-1001",
            "LOC-02",
            "Área B",
            "EQ-20",
            "2024-W46",
            datetime(2024, 11, 5, 10, 30, 0),
            "Inspeção",
            "ENG",
            "ELETR",
            "Maria",
            "Sistema",
            "S2",
            "S2",
            "Não",
            "Carlos",
            "2024-W47",
            "Daniel",
            "Aguardando material",
            "SAM",
            "",
        ],
    ]

    # A minimal header row (names not used by code that relies on positions)
    header = [
        "Numero","Situacao","Derivada","Localizacao","Desc_Localizacao","Equipamento",
        "Semana_Cadastro","Emitida_Em","Desc_SSA","Setor_Emissor","Setor_Executor","Solicitante",
        "Servico_Origem","Prioridade_Emissao","Prioridade_Planejamento","Execucao_Simples",
        "Resp_Programacao","Semana_Programada","Resp_Execucao","Descricao_Execucao","Sistema_Origem","Anomalia"
    ]

    # Writer: DataLoader uses header=2 -> put two header rows, then header labels, then data
    df = pd.DataFrame(rows, columns=header)
    with pd.ExcelWriter(OUT, engine="xlsxwriter") as writer:
        # Write two dummy header rows first
        pd.DataFrame([header]).to_excel(writer, sheet_name="Sheet1", header=False, index=False, startrow=0)
        pd.DataFrame([header]).to_excel(writer, sheet_name="Sheet1", header=False, index=False, startrow=1)
        # Now write the real header+data starting at row 2 (zero-based)
        df.to_excel(writer, sheet_name="Sheet1", index=False, startrow=2)

    print(f"Sample Excel written to: {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
