# MCP Server Demo

Dieses Projekt demonstriert eine modulare, Multi-Tenant-fähige Architektur für das Model Context Protocol (MCP) mit Plug-and-Play-Mechanismus, Auto-Discovery und einer modernen React-UI. Die Kommunikation erfolgt über einen zentralen Orchestrator, der Anfragen an verschiedene MCP-Module verteilt.

## Features

- **Multi-Tenant**: Jeder Tenant kann eigene API-Keys und Modulzuordnungen haben.
- **Plug-and-Play**: Neue MCP-Module können einfach hinzugefügt und dynamisch genutzt werden.
- **Auto-Discovery**: Der Orchestrator erkennt verfügbare Module automatisch.
- **React-Frontend**: Komfortable Verwaltung und Testen von Tenants und Modulen.
- **Docker-basiert**: Alle Komponenten laufen als Container im selben Netzwerk.

## Projektstruktur

```
mcp-server-demo/
│
├── orchestrator/         # Zentrale API, Discovery, Multi-Tenant-Logik
│   ├── main.py
│   ├── kunden.json       # Tenant-Konfiguration
│   └── ...
│
├── mcp_proalpha/         # Beispiel-MCP-Modul (ProAlpha)
│   └── main.py
├── mcp_hubspot/          # Beispiel-MCP-Modul (HubSpot)
│   └── main.py
├── mcp_docs/             # Beispiel-MCP-Modul (Docs)
│   └── main.py
│
├── frontend-react/       # React-UI für Tenant- und Modulverwaltung
│   └── src/App.tsx
│
├── docker-compose.yml    # Startet alle Services im gemeinsamen Netzwerk
└── README.md
```

## Schnellstart

### Voraussetzungen

- Docker & Docker Compose
- Node.js (nur für lokale Frontend-Entwicklung)

### Starten aller Services

```bash
docker-compose up --build
```

- Orchestrator-API: [http://localhost:8000](http://localhost:8000)
- Frontend: [http://localhost:3033](http://localhost:3033)

### Beispiel: Anfrage an den Orchestrator

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -H "X-API-Key: abc123" \
  -d '{"query": "Was ist der Status?"}'
```

Antwort:
```json
{
  "kunde": "kunde1",
  "antworten": [
    "mcp_proalpha: Antwort von ProAlpha: Was ist der Status?",
    "mcp_hubspot: Antwort von HubSpot: Was ist der Status?"
  ]
}
```

### Frontend-Funktionen

- Tenants anlegen, auswählen und löschen
- API-Key-Verwaltung pro Tenant
- Module pro Tenant zuordnen
- Anfragen an den Orchestrator senden und Antworten anzeigen

## Eigene Module hinzufügen

1. Neuen Ordner nach Vorbild von `mcp_proalpha` anlegen.
2. FastAPI-Service mit `/answer`-Endpoint implementieren.
3. In `docker-compose.yml` als neuen Service eintragen.
4. Im Frontend oder in `kunden.json` dem gewünschten Tenant zuordnen.

## Entwicklung

### Frontend lokal starten

```bash
cd frontend-react
npm install
npm start
```

### Backend-Änderungen

- Änderungen an Python-Code erfordern einen Neustart des jeweiligen Containers:
  ```bash
  docker-compose restart orchestrator mcp_proalpha mcp_hubspot mcp_docs
  ```

## Hinweise

- Die Kommunikation zwischen Orchestrator und Modulen erfolgt über das interne Docker-Netzwerk per Service-Name.
- Die Discovery prüft, ob Module erreichbar sind, bevor Anfragen weitergeleitet werden.
- API-Keys regeln den Zugriff pro Tenant.

---

**Viel Spaß beim Ausprobieren!**  
Bei Fragen oder Problemen: Issues anlegen oder direkt im Code nachschauen.
