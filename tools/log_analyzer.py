#!/usr/bin/env python3
"""
Analisador de datalogs ME7Logger para AMK 1.8T.

Uso:
    python log_analyzer.py datalog.csv
    python log_analyzer.py datalog.csv --plot
    python log_analyzer.py datalog.csv --check-knock
"""

import argparse
import csv
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


@dataclass
class LogEntry:
    time_s: float
    rpm: float
    load_g_rev: float
    boost_bar: float
    iat_c: float
    coolant_c: float
    lambda_val: float
    ignition_deg: float
    knock_cyl1: float = 0.0
    knock_cyl2: float = 0.0
    knock_cyl3: float = 0.0
    knock_cyl4: float = 0.0
    throttle_pct: float = 0.0
    n75_duty: float = 0.0


@dataclass
class LogSummary:
    max_rpm: float = 0.0
    max_boost: float = 0.0
    max_load: float = 0.0
    max_iat: float = 0.0
    min_lambda: float = 9.9
    max_lambda: float = 0.0
    total_knock_events: int = 0
    knock_events_by_cyl: dict = field(default_factory=lambda: {1: 0, 2: 0, 3: 0, 4: 0})
    pull_segments: list = field(default_factory=list)


# Limites de alerta para AMK 1.8T com etanol
ALERT_THRESHOLDS = {
    "lambda_lean":   0.95,   # acima disto em carga total = magro demais
    "lambda_rich":   0.78,   # abaixo disto = desperdiçando combustível
    "boost_max":     1.15,   # K03s: não passar disto por muito tempo
    "iat_max":       55.0,   # temperatura de admissão alta demais
    "coolant_max":   105.0,  # temperatura de arrefecimento alta demais
    "knock_limit":   0,      # qualquer knock é problema
}


def parse_csv(filepath: Path) -> list[LogEntry]:
    """
    Parseia CSV exportado pelo ME7Logger.
    Formato esperado: time,rpm,load,boost,iat,coolant,lambda,ign,k1,k2,k3,k4,tps,n75
    """
    entries = []
    with open(filepath, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            try:
                entries.append(LogEntry(
                    time_s=float(row.get("time", row.get("Time", i * 0.1))),
                    rpm=float(row.get("rpm", row.get("RPM", 0))),
                    load_g_rev=float(row.get("load", row.get("Load", 0))),
                    boost_bar=float(row.get("boost", row.get("Boost", 0))),
                    iat_c=float(row.get("iat", row.get("IAT", 25))),
                    coolant_c=float(row.get("coolant", row.get("Coolant", 90))),
                    lambda_val=float(row.get("lambda", row.get("Lambda", 1.0))),
                    ignition_deg=float(row.get("ign", row.get("Ignition", 15))),
                    knock_cyl1=float(row.get("k1", row.get("Knock1", 0))),
                    knock_cyl2=float(row.get("k2", row.get("Knock2", 0))),
                    knock_cyl3=float(row.get("k3", row.get("Knock3", 0))),
                    knock_cyl4=float(row.get("k4", row.get("Knock4", 0))),
                    throttle_pct=float(row.get("tps", row.get("TPS", 0))),
                    n75_duty=float(row.get("n75", row.get("N75", 0))),
                ))
            except (ValueError, KeyError):
                continue
    return entries


def detect_pulls(entries: list[LogEntry], min_rpm: float = 3000,
                 min_duration_s: float = 2.0) -> list[list[LogEntry]]:
    """Detecta segmentos de aceleração a fundo (WOT pulls)."""
    pulls = []
    current_pull: list[LogEntry] = []

    for entry in entries:
        in_pull = entry.throttle_pct >= 85.0 and entry.rpm >= min_rpm
        if in_pull:
            current_pull.append(entry)
        elif current_pull:
            duration = current_pull[-1].time_s - current_pull[0].time_s
            if duration >= min_duration_s:
                pulls.append(current_pull)
            current_pull = []

    return pulls


def analyze(entries: list[LogEntry]) -> LogSummary:
    summary = LogSummary()

    for e in entries:
        summary.max_rpm = max(summary.max_rpm, e.rpm)
        summary.max_boost = max(summary.max_boost, e.boost_bar)
        summary.max_load = max(summary.max_load, e.load_g_rev)
        summary.max_iat = max(summary.max_iat, e.iat_c)

        if e.load_g_rev > 100:  # só conta lambda em carga alta
            summary.min_lambda = min(summary.min_lambda, e.lambda_val)
            summary.max_lambda = max(summary.max_lambda, e.lambda_val)

        for cyl, knock in enumerate([e.knock_cyl1, e.knock_cyl2,
                                     e.knock_cyl3, e.knock_cyl4], start=1):
            if knock > 0:
                summary.total_knock_events += 1
                summary.knock_events_by_cyl[cyl] += 1

    summary.pull_segments = detect_pulls(entries)
    return summary


def print_report(summary: LogSummary, entries: list[LogEntry]) -> None:
    print("\n" + "=" * 60)
    print("  RELATÓRIO DE DATALOG — AMK 1.8T")
    print("=" * 60)
    print(f"  Pontos registrados: {len(entries)}")
    print(f"  Duração total:      {entries[-1].time_s:.1f}s" if entries else "")
    print()
    print("  PICOS REGISTRADOS:")
    print(f"    RPM máx:          {summary.max_rpm:.0f} rpm")
    print(f"    Boost máx:        {summary.max_boost:.2f} bar")
    print(f"    Carga máx:        {summary.max_load:.1f} g/rev")
    print(f"    Temp. admissão:   {summary.max_iat:.1f} °C")
    print(f"    Lambda (carga):   {summary.min_lambda:.3f} – {summary.max_lambda:.3f}")
    print()
    print("  KNOCK:")
    if summary.total_knock_events == 0:
        print("    ✓ Nenhum evento de knock detectado")
    else:
        print(f"    ⚠ TOTAL: {summary.total_knock_events} eventos")
        for cyl, count in summary.knock_events_by_cyl.items():
            if count > 0:
                print(f"      Cilindro {cyl}: {count} eventos")
    print()
    print(f"  PULLS DETECTADOS: {len(summary.pull_segments)}")
    for i, pull in enumerate(summary.pull_segments, start=1):
        rpm_start = pull[0].rpm
        rpm_end = pull[-1].rpm
        duration = pull[-1].time_s - pull[0].time_s
        max_boost = max(e.boost_bar for e in pull)
        print(f"    Pull {i}: {rpm_start:.0f}→{rpm_end:.0f} rpm, "
              f"{duration:.1f}s, boost_max={max_boost:.2f} bar")
    print()
    print("  ALERTAS:")
    alerts = _check_alerts(summary, entries)
    if not alerts:
        print("    ✓ Nenhum alerta")
    for alert in alerts:
        print(f"    ⚠ {alert}")
    print("=" * 60 + "\n")


def _check_alerts(summary: LogSummary, entries: list[LogEntry]) -> list[str]:
    alerts = []

    if summary.max_boost > ALERT_THRESHOLDS["boost_max"]:
        alerts.append(f"Boost acima do limite K03s: {summary.max_boost:.2f} bar "
                       f"(máx recomendado: {ALERT_THRESHOLDS['boost_max']} bar)")

    if summary.max_iat > ALERT_THRESHOLDS["iat_max"]:
        alerts.append(f"IAT alta: {summary.max_iat:.1f}°C — verificar intercooler")

    if summary.min_lambda < ALERT_THRESHOLDS["lambda_rich"] and summary.min_lambda > 0:
        alerts.append(f"Mistura muito rica: lambda {summary.min_lambda:.3f} — "
                       "verificar injetores/mapa de injeção")

    if summary.max_lambda > ALERT_THRESHOLDS["lambda_lean"]:
        alerts.append(f"Mistura magra em carga: lambda {summary.max_lambda:.3f} — "
                       "PERIGO: aumentar injeção imediatamente")

    if summary.total_knock_events > 0:
        most_affected = max(summary.knock_events_by_cyl,
                            key=lambda c: summary.knock_events_by_cyl[c])
        alerts.append(f"Knock detectado — cilindro mais afetado: {most_affected}. "
                       "Reduzir avanço de ignição ou boost")

    return alerts


def plot_pull(pull: list[LogEntry], pull_num: int) -> None:
    if not MATPLOTLIB_AVAILABLE:
        print("matplotlib não instalado — instale com: pip install matplotlib")
        return

    times = [e.time_s - pull[0].time_s for e in pull]
    fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True)
    fig.suptitle(f"Pull {pull_num} — AMK 1.8T Datalog", fontsize=12)

    axes[0].plot(times, [e.boost_bar for e in pull], "b-", label="Boost (bar)")
    axes[0].plot(times, [e.lambda_val for e in pull], "r-", label="Lambda")
    axes[0].axhline(y=0.88, color="r", linestyle="--", alpha=0.4, label="λ target E100")
    axes[0].legend(loc="upper left")
    axes[0].set_ylabel("Boost / Lambda")
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(times, [e.ignition_deg for e in pull], "g-", label="Avanço (°)")
    axes[1].set_ylabel("Avanço ignição (°)")
    axes[1].legend(loc="upper left")
    axes[1].grid(True, alpha=0.3)

    axes[2].plot(times, [e.rpm for e in pull], "k-", label="RPM")
    axes[2].set_ylabel("RPM")
    axes[2].set_xlabel("Tempo (s)")
    axes[2].legend(loc="upper left")
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    output = f"pull_{pull_num}.png"
    plt.savefig(output, dpi=150)
    print(f"Gráfico salvo: {output}")
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Análise de datalog ME7Logger — AMK 1.8T")
    parser.add_argument("logfile", type=Path, help="Arquivo CSV do ME7Logger")
    parser.add_argument("--plot", action="store_true", help="Gerar gráficos dos pulls")
    parser.add_argument("--check-knock", action="store_true",
                        help="Mostrar apenas entradas com knock")
    args = parser.parse_args()

    if not args.logfile.exists():
        print(f"Erro: arquivo não encontrado: {args.logfile}")
        sys.exit(1)

    entries = parse_csv(args.logfile)
    if not entries:
        print("Nenhum dado encontrado no arquivo. Verificar formato do CSV.")
        sys.exit(1)

    summary = analyze(entries)
    print_report(summary, entries)

    if args.check_knock:
        knock_entries = [e for e in entries if
                         e.knock_cyl1 > 0 or e.knock_cyl2 > 0 or
                         e.knock_cyl3 > 0 or e.knock_cyl4 > 0]
        print(f"\nEntradas com knock ({len(knock_entries)}):")
        for e in knock_entries:
            print(f"  t={e.time_s:.1f}s  rpm={e.rpm:.0f}  "
                  f"boost={e.boost_bar:.2f}  ign={e.ignition_deg:.1f}°  "
                  f"knock=[{e.knock_cyl1:.0f},{e.knock_cyl2:.0f},"
                  f"{e.knock_cyl3:.0f},{e.knock_cyl4:.0f}]")

    if args.plot:
        for i, pull in enumerate(summary.pull_segments, start=1):
            plot_pull(pull, i)


if __name__ == "__main__":
    main()
