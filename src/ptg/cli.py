import argparse
import sys
from pathlib import Path

from ptg.converter import convert_html_to_tikz


def main():
    parser = argparse.ArgumentParser(
        description="Konvertiert Plotly HTML-Dateien in TikZ (.tex) Grafiken."
    )
    parser.add_argument(
        "files",
        nargs="*",
        type=Path,
        help="Pfad(e) zu Plotly HTML-Datei(en). Wenn leer, wird die GUI gestartet."
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Zielpfad für die .tex-Datei (nur relevant bei einer einzelner Eingabedatei)."
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Grafische Benutzeroberfläche (PyQt6 GUI) starten."
    )

    args = parser.parse_args()

    if args.gui or not args.files:
        from ptg.gui import main as gui_main
        gui_main()
        return

    if args.output and len(args.files) > 1:
        print("❌ Fehler: --output kann nur mit genau einer Eingabedatei verwendet werden.", file=sys.stderr)
        sys.exit(1)

    for file_path in args.files:
        try:
            print(f"⏳ Verarbeite {file_path}...")
            out_path = args.output if (args.output and len(args.files) == 1) else None
            tex_file = convert_html_to_tikz(file_path, output_path=out_path)
            print(f"✅ Erfolgreich: {tex_file}")
        except Exception as e:
            print(f"❌ Fehler bei {file_path}: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
