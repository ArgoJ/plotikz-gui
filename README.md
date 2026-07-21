# pt-gui (`ptg`)

Ein Python-Package zum Konvertieren von interaktiven Plotly HTML-Dateien in TikZ-Grafiken (`.tex`) für LaTeX.

## Installation

Installiere das Paket im Entwicklungsmodus oder regulär:

```bash
pip install -e .
```

## Benutzung

### 1. Grafische Benutzeroberfläche (GUI)
Starte die Drag & Drop Benutzeroberfläche:

```bash
ptg
# oder
ptg-gui
# oder
python -m ptg
```

### 2. Command Line Interface (CLI)
Konvertiere HTML-Dateien direkt im Terminal:

```bash
ptg datei1.html datei2.html
```

Mit benutzerdefiniertem Ausgabepfad:

```bash
ptg datei.html -o ziel.tex
```

### 3. Verwendung als Python-Bibliothek

```python
from ptg import convert_html_to_tikz, extract_plotly_fig

# Direkte Konvertierung in .tex
tex_path = convert_html_to_tikz("plot.html")

# Oder Plotly Figure-Objekt extrahieren
fig = extract_plotly_fig("plot.html")
fig.show()
```
