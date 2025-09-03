#!/usr/bin/env python3
"""
Create a focused Flake8 fix plan using the latest reports/rework_sanity.txt output.
Groups by error code and lists top offenders first.

Output: reports/rework_flake8_plan.md
"""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import re


LINE_RE = re.compile(r"^(?P<file>[^:]+):(?P<line>\d+):(?P<col>\d+): (?P<code>[A-Z]\d{3}) (?P<msg>.*)$")


def main() -> int:
    ws = Path(__file__).resolve().parents[1]
    report = ws / "reports" / "rework_sanity.txt"
    out = ws / "reports" / "rework_flake8_plan.md"

    if not report.exists():
        out.write_text("Sem rework_sanity.txt para analisar.\n", encoding="utf-8")
        print(out)
        return 1

    by_code: dict[str, list[tuple[str, int, int, str]]] = defaultdict(list)
    lines = report.read_text(encoding="utf-8", errors="replace").splitlines()
    for line in lines:
        m = LINE_RE.match(line)
        if not m:
            continue
        d = m.groupdict()
        by_code[d["code"]].append(
            (d["file"], int(d["line"]), int(d["col"]), d["msg"]) 
        )

    order = sorted(by_code.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    buf: list[str] = ["# Flake8 Fix Plan (foco por código)", ""]
    for code, items in order:
        buf.append(f"## {code} ({len(items)} ocorrências)")
        if code == "F811":
            buf.append("- Atenção: redefinição de nomes; revisar imports e ordem de código.")
        if code == "E402":
            buf.append("- Mover imports para o topo do arquivo.")
        if code == "F401":
            buf.append("- Remover imports não utilizados.")
        if code == "E501":
            buf.append("- Ajustar linhas > 88 colunas (ou quebrar em múltiplas linhas).")
        if code == "E722":
            buf.append("- Evitar 'except:' genérico; especificar exceções.")
        buf.append("")
        # top 10 examples
        for f, ln, col, msg in items[:10]:
            buf.append(f"- {f}:{ln}:{col} {msg}")
        buf.append("")

    out.write_text("\n".join(buf) + "\n", encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
