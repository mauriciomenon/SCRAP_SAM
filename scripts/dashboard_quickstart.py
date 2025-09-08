#!/usr/bin/env python3
"""
Quickstart runner: spins up the SSADashboard with a minimal in-memory DataFrame.

Use this to verify the dashboard boots and listens on http://127.0.0.1:8050
without depending on any external Excel input files.

Non-destructive: doesn't modify project code or data.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from datetime import datetime

import pandas as pd


BASE = Path(__file__).resolve().parents[1]
SRC = BASE / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def build_minimal_df() -> pd.DataFrame:
    """Create a minimal DataFrame matching expected SSAColumns index layout.

    Columns by position (0..21):
    0 NUMERO_SSA, 1 SITUACAO, 2 DERIVADA, 3 LOCALIZACAO, 4 DESC_LOCALIZACAO,
    5 EQUIPAMENTO, 6 SEMANA_CADASTRO, 7 EMITIDA_EM, 8 DESC_SSA,
    9 SETOR_EMISSOR, 10 SETOR_EXECUTOR, 11 SOLICITANTE, 12 SERVICO_ORIGEM,
    13 GRAU_PRIORIDADE_EMISSAO, 14 GRAU_PRIORIDADE_PLANEJAMENTO,
    15 EXECUCAO_SIMPLES, 16 RESPONSAVEL_PROGRAMACAO, 17 SEMANA_PROGRAMADA,
    18 RESPONSAVEL_EXECUCAO, 19 DESCRICAO_EXECUCAO, 20 SISTEMA_ORIGEM,
    21 ANOMALIA
    """
    row1 = [
        "SSA-0001",  # 0
        "Aberta",  # 1
        "",  # 2
        "LOC-01",  # 3
        "Área A",  # 4
        "EQ-100",  # 5
        "2024-W45",  # 6
        datetime(2024, 11, 1, 12, 0, 0),  # 7
        "Troca de componente",  # 8
        "ENG",  # 9
        "MANUT",  # 10
        "João",  # 11
        "Sistema",  # 12
        "S3.7",  # 13
        "S2",  # 14
        "Sim",  # 15
        "Alice",  # 16
        "2024-W46",  # 17
        "Bob",  # 18
        "Execução prevista",  # 19
        "SAM",  # 20
        "",  # 21
    ]
    row2 = [
        "SSA-0002",
        "Em Execução",
        "SSA-0001",
        "LOC-02",
        "Área B",
        "EQ-200",
        "2024-W46",
        datetime(2024, 11, 5, 9, 30, 0),
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
    ]

    # Build DataFrame with numeric positions 0..21 (names optional)
    df = pd.DataFrame([row1, row2])
    return df


def main() -> int:
    try:
        from dashboard.Dashboard_SM import SSADashboard  # type: ignore
    except Exception:
        # Fallback absolute import
        from src.dashboard.Dashboard_SM import SSADashboard  # type: ignore

    df = build_minimal_df()
    app = SSADashboard(df)
    print("Starting dashboard on http://127.0.0.1:8050 ...")
    # Dash>=3 uses app.run(); the project wrapper calls run_server()
    # To avoid modifying project code, call the underlying Dash app directly.
    dash_app = getattr(app, "app", None)
    if dash_app is None:
        raise RuntimeError("SSADashboard missing 'app' attribute")
    # Run with debug=False to reduce console noise
    dash_app.run(debug=False, port=8050)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
