# Live CSV Dashboard

Een simpele basis om een **live dashboard** te bouwen op basis van een CSV-bestand.

## 1) Installeren

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2) Starten

```bash
streamlit run app.py
```

Open daarna de URL die Streamlit toont (meestal `http://localhost:8501`).

## 3) CSV koppelen

- Standaard leest de app `data/metrics.csv`.
- In de sidebar kun je een ander pad invullen.
- De app refresht automatisch (standaard elke 5 seconden).

## 4) CSV-formaat

- Voeg bij voorkeur een tijdkolom toe, bijvoorbeeld `datum` of `timestamp`.
- Voeg één of meer numerieke kolommen toe (`omzet`, `orders`, etc.).

Voorbeeld:

```csv
datum,omzet,orders,bezoekers
2026-02-10 09:00:00,1200,42,300
2026-02-10 10:00:00,1350,47,340
```

## 5) Live updates

Als je CSV continu wordt aangevuld (bijv. door een script), zie je nieuwe waarden na de volgende refresh automatisch terug in de grafiek en KPI's.
