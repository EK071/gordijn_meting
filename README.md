# Gordijn Meting Tool

Een web-based tool voor het inmeten en verwerken van gordijnen binnen de Google Workspace-omgeving.

## Functionaliteiten

- Mobielvriendelijke interface voor het inmeten van gordijnen
- Digitale vastlegging van alle relevante metingen en specificaties
- Foto-upload mogelijkheid per raam
- Automatische verwerking tot werkbon
- Integratie met Google Workspace (Google Sheets)
- Kostenberekening per raam (fase 2)

## Installatie

1. Clone de repository:
```bash
git clone [repository-url]
cd gordijn_meting
```

2. Maak een virtuele omgeving aan en activeer deze:
```bash
python -m venv venv
source venv/bin/activate  # Op Windows: venv\Scripts\activate
```

3. Installeer de benodigde packages:
```bash
pip install -r requirements.txt
```

4. Stel de Google Workspace credentials in:
- Maak een project aan in de Google Cloud Console
- Activeer de Google Sheets API
- Maak een service account aan en download de credentials
- Plaats het credentials bestand in de root van het project

5. Start de applicatie:
```bash
python app.py
```

De applicatie is nu beschikbaar op `http://localhost:5000`

## Gebruik

1. Open de applicatie in een webbrowser op je mobiele apparaat
2. Vul alle gevraagde gegevens in:
   - Project informatie
   - Raam afmetingen
   - Ophangsysteem specificaties
   - Gordijn specificaties
3. Upload eventueel foto's van het raam
4. Klik op "Opslaan" om de meting vast te leggen
5. De gegevens worden automatisch opgeslagen in Google Sheets
6. Een PDF werkbon wordt gegenereerd en kan worden gedeeld met het atelier

## Ontwikkeling

### Structuur
```
gordijn_meting/
├── app.py              # Flask applicatie
├── requirements.txt    # Python dependencies
├── static/            # Statische bestanden (CSS, JS, afbeeldingen)
├── templates/         # HTML templates
└── uploads/           # Uploaded bestanden
```

### Toevoegen van nieuwe functionaliteit

1. Voeg nieuwe velden toe aan het formulier in `app.py`
2. Update de HTML template in `templates/index.html`
3. Voeg de verwerking toe in de submit route
4. Update de Google Sheets integratie indien nodig

## Licentie

Dit project is eigendom van [Bedrijfsnaam] en is niet openbaar beschikbaar. 