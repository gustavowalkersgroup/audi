#!/usr/bin/env python3
"""
Visualizador de mapas ECU para ME7.5.20 AMK 1.8T.

Lê valores de mapas em formato texto (exportados pelo RomRaider) e gera
visualizações 3D ou 2D para comparação entre stock e modificado.

Uso:
    python map_visualizer.py kfzw_stock.csv kfzw_modified.csv --map KFZW
    python map_visualizer.py kfmiop_stock.csv --map KFMIOP --3d
"""

import argparse
import csv
import sys
from pathlib import Path

try:
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib import cm
    DEPS_AVAILABLE = True
except ImportError:
    DEPS_AVAILABLE = False

MAP_METADATA = {
    "KFZW": {
        "name": "Avanço de Ignição Principal",
        "x_label": "RPM",
        "y_label": "Carga (mg/Hub)",
        "z_label": "Avanço (°)",
        "unit": "°",
    },
    "KFMIOP": {
        "name": "Mapa de Injeção Base",
        "x_label": "RPM",
        "y_label": "Carga (mg/Hub)",
        "z_label": "Injeção (mg/Hub)",
        "unit": "mg/Hub",
    },
    "KFLDRL": {
        "name": "Duty Cycle N75 (Wastegate)",
        "x_label": "RPM",
        "y_label": "Carga Desejada",
        "z_label": "Duty Cycle (%)",
        "unit": "%",
    },
    "LAMFA": {
        "name": "Target Lambda (Carga Alta)",
        "x_label": "RPM",
        "y_label": "Carga (mg/Hub)",
        "z_label": "Lambda",
        "unit": "λ",
    },
}


def load_map_csv(filepath: Path) -> tuple[list[float], list[float], list[list[float]]]:
    """
    Carrega mapa no formato RomRaider CSV:
    Primeira linha: header com eixo X (RPM)
    Primeira coluna: eixo Y (carga)
    Células: valores Z
    """
    with open(filepath, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        rows = list(reader)

    if not rows:
        raise ValueError(f"Arquivo vazio: {filepath}")

    x_axis = [float(v) for v in rows[0][1:] if v.strip()]
    y_axis = []
    z_data = []

    for row in rows[1:]:
        if not row or not row[0].strip():
            continue
        y_axis.append(float(row[0]))
        z_data.append([float(v) for v in row[1:len(x_axis) + 1]])

    return x_axis, y_axis, z_data


def plot_3d(x_axis: list[float], y_axis: list[float],
            z_data: list[list[float]], meta: dict, title: str) -> None:
    if not DEPS_AVAILABLE:
        print("numpy e matplotlib necessários: pip install numpy matplotlib")
        return

    x = np.array(x_axis)
    y = np.array(y_axis)
    z = np.array(z_data)
    X, Y = np.meshgrid(x, y)

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection="3d")
    surf = ax.plot_surface(X, Y, z, cmap=cm.viridis, alpha=0.9)
    ax.set_xlabel(meta["x_label"])
    ax.set_ylabel(meta["y_label"])
    ax.set_zlabel(meta["z_label"])
    ax.set_title(f"{meta['name']}\n{title}")
    fig.colorbar(surf, ax=ax, shrink=0.5, label=meta["unit"])
    plt.tight_layout()
    output = title.replace(" ", "_").lower() + "_3d.png"
    plt.savefig(output, dpi=150)
    print(f"Mapa 3D salvo: {output}")
    plt.close()


def plot_comparison(x_axis: list[float], y_axis: list[float],
                    z_stock: list[list[float]], z_mod: list[list[float]],
                    meta: dict) -> None:
    if not DEPS_AVAILABLE:
        print("numpy e matplotlib necessários: pip install numpy matplotlib")
        return

    z1 = np.array(z_stock)
    z2 = np.array(z_mod)
    diff = z2 - z1

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle(f"Comparação: {meta['name']}", fontsize=13)

    x_ticks = range(len(x_axis))
    y_ticks = range(len(y_axis))

    for ax, data, title, cmap in [
        (axes[0], z1, "Stock", "Blues"),
        (axes[1], z2, "Modificado", "Oranges"),
        (axes[2], diff, "Diferença (Mod − Stock)", "RdYlGn"),
    ]:
        im = ax.imshow(data, aspect="auto", cmap=cmap, origin="lower")
        ax.set_title(title)
        ax.set_xticks(range(0, len(x_axis), max(1, len(x_axis) // 8)))
        ax.set_xticklabels([f"{x_axis[i]:.0f}" for i in
                            range(0, len(x_axis), max(1, len(x_axis) // 8))],
                           rotation=45, fontsize=7)
        ax.set_yticks(range(0, len(y_axis), max(1, len(y_axis) // 8)))
        ax.set_yticklabels([f"{y_axis[i]:.0f}" for i in
                            range(0, len(y_axis), max(1, len(y_axis) // 8))],
                           fontsize=7)
        ax.set_xlabel(meta["x_label"])
        ax.set_ylabel(meta["y_label"])
        plt.colorbar(im, ax=ax, label=meta["unit"])

    plt.tight_layout()
    output = f"comparison_{meta['name'].split()[0].lower()}.png"
    plt.savefig(output, dpi=150)
    print(f"Comparação salva: {output}")
    plt.close()


def print_map_table(x_axis: list[float], y_axis: list[float],
                    z_data: list[list[float]], meta: dict) -> None:
    col_w = 7
    print(f"\n  {meta['name']} ({meta['unit']})")
    print(f"  {'':>8}", end="")
    for x in x_axis:
        print(f"{x:>{col_w}.0f}", end="")
    print()
    print("  " + "-" * (8 + col_w * len(x_axis)))
    for y_val, row in zip(y_axis, z_data):
        print(f"  {y_val:>7.0f}|", end="")
        for val in row:
            print(f"{val:>{col_w}.2f}", end="")
        print()
    print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Visualizador de mapas ECU ME7.5.20 — AMK 1.8T")
    parser.add_argument("stock", type=Path, help="CSV do mapa stock")
    parser.add_argument("modified", type=Path, nargs="?",
                        help="CSV do mapa modificado (opcional para comparação)")
    parser.add_argument("--map", choices=list(MAP_METADATA.keys()),
                        default="KFZW", help="Tipo de mapa")
    parser.add_argument("--3d", dest="three_d", action="store_true",
                        help="Plotar mapa 3D")
    parser.add_argument("--table", action="store_true",
                        help="Imprimir tabela no terminal")
    args = parser.parse_args()

    meta = MAP_METADATA[args.map]

    if not args.stock.exists():
        print(f"Erro: arquivo não encontrado: {args.stock}")
        sys.exit(1)

    x_axis, y_axis, z_stock = load_map_csv(args.stock)

    if args.table:
        print_map_table(x_axis, y_axis, z_stock, meta)

    if args.three_d:
        plot_3d(x_axis, y_axis, z_stock, meta, f"{args.map} Stock")

    if args.modified:
        if not args.modified.exists():
            print(f"Erro: arquivo modificado não encontrado: {args.modified}")
            sys.exit(1)
        _, _, z_mod = load_map_csv(args.modified)
        plot_comparison(x_axis, y_axis, z_stock, z_mod, meta)
        if args.three_d:
            plot_3d(x_axis, y_axis, z_mod, meta, f"{args.map} Modificado")


if __name__ == "__main__":
    main()
