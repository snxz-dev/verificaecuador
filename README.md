<p align="center">
  <img src="https://img.shields.io/badge/elecciones-29%20nov%202026-ffd60a?style=for-the-badge&labelColor=0b1220&color=ffd60a" alt="Elecciones Ecuador 2026">
  <img src="https://img.shields.io/badge/MediaHack%20II-Openlab%20%2B%20KAS-e5484d?style=for-the-badge&labelColor=0b1220&color=e5484d" alt="MediaHack II">
  <img src="https://img.shields.io/badge/⚡%20100%25%20gratis-30a46c?style=for-the-badge&labelColor=0b1220&color=30a46c" alt="Free">
</p>

<h1 align="center">🇪🇨 VerificaEcuador</h1>

<p align="center">
  <strong>Verifica antes de compartir</strong><br>
  Herramienta contra la <em>desinformación electoral</em> en Ecuador.<br>
  Ingresa texto o imagen → detecta riesgo → remite a fuentes verificadas.
</p>

<p align="center">
  <a href="https://verificaecuador.vercel.app">
    <img src="https://img.shields.io/badge/🌐_Demo_en_vivo-verificaecuador.vercel.app-3d6bff?style=for-the-badge&labelColor=0b1220" alt="Demo en vivo">
  </a>
  <a href="https://verificaecuador.onrender.com/docs">
    <img src="https://img.shields.io/badge/⚙️_API_docs-Render-f5a524?style=for-the-badge&labelColor=0b1220" alt="API Docs">
  </a>
  <a href="https://github.com/snxz-dev/verificaecuador">
    <img src="https://img.shields.io/badge/📦_Código_fuente-GitHub-ffffff?style=for-the-badge&labelColor=0b1220" alt="GitHub">
  </a>
</p>

---

## 📖 ¿Qué es?

**VerificaEcuador** es una plataforma web que permite a los ciudadanos contrastar noticias y afirmaciones sobre las **elecciones del 29 de noviembre de 2026** con fuentes verificadas.

> En Ecuador, la desinformación circula como cadenas de WhatsApp, capturas de pantalla y memes. VerificaEcuador pone en las manos de la gente una herramienta simple: **pega un texto o una imagen**, y en segundos obtienes el nivel de riesgo junto con verificaciones de fuentes confiables.

### ✨ Características principales

| Feature | Descripción |
|---|---|
| 📝 **Verificación por texto** | Escribe o pega una afirmación y obtén el nivel de riesgo + fuentes |
| 🖼️ **Verificación por imagen** | Sube, arrastra o **pega con Ctrl+V** una captura — el OCR extrae el texto automáticamente |
| 🎨 **Detección de riesgo** | Alto 🚨 / Moderado ⚠️ / Sin señales ✅ con señales específicas detectadas |
| 📡 **Fuentes en vivo** | Si la BD no tiene respuesta, busca en **Ecuador Chequea**, **Google Fact Check**, **Primera Plana** y **RSS** en tiempo real |
| 🖼️ **Imágenes oficiales** | Cada verificación muestra la imagen oficial del artículo de verificación |
| 🤖 **Bot de Telegram** | Mismo análisis disponible como bot (ejecución local) |
| 🔒 **Marco ético** | No emite juicios — siempre remite a la fuente original |

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                     USUARIO                              │
│              (navegador o Telegram)                      │
└──────────────┬──────────────────────┬────────────────────┘
               │ POST /verify         │ POST /verify-image
               │ o POST /verify-image │
               ▼                      ▼
┌──────────────────────────────────────────────────────────┐
│  🌐 FRONTEND (Vercel)                                    │
│  Astro · Página de verificación con pestaña Texto|Imagen │
│  verificaecuador.vercel.app                              │
└──────────────────────┬───────────────────────────────────┘
                       │ HTTP
                       ▼
┌──────────────────────────────────────────────────────────┐
│  ⚙️ API (Render · FastAPI)                                │
│  verificaecuador.onrender.com                             │
│                                                          │
│  ┌─────────────┐  ┌──────────┐  ┌─────────────────────┐ │
│  │ /verify     │  │ /image   │  │ /verify-image       │ │
│  │ (texto)     │  │ (proxy)  │  │ (OCR + verificación)│ │
│  └──────┬──────┘  └──────────┘  └─────────┬───────────┘ │
│         │                                  │              │
│  ┌──────▼──────────────────────────────────▼───────────┐ │
│  │                Motor de detección                    │ │
│  │  Señales de riesgo · Temas electorales · Clasificador│ │
│  └──────┬──────────────────────────────────┬───────────┘ │
│         │                                  │              │
└─────────┼──────────────────────────────────┼──────────────┘
          │                                  │
          ▼                                  ▼
┌──────────────────┐           ┌──────────────────────────┐
│ 🗄️ NEON           │           │ 📡 FUENTES EN VIVO       │
│ PostgreSQL        │           │ Ecuador Chequea (API)    │
│ fact_checks       │           │ Google Fact Check (API)  │
│ (verificaciones   │           │ Primera Plana (API)      │
│  pre-cargadas)    │           │ RSS feeds                │
└──────────────────┘           └──────────────────────────┘
```

### Stack tecnológico

| Capa | Tecnología | Hosting |
|---|---|---|
| 🌐 Frontend | **Astro** (estático) | [Vercel](https://vercel.com) (free) |
| ⚙️ API | **FastAPI** + Python 3.12 | [Render](https://render.com) (free) |
| 🗄️ Base de datos | **PostgreSQL** serverless | [Neon](https://neon.tech) (free) |
| 📡 Fuentes en vivo | httpx + APIs públicas | Costo: $0 |
| 🖼️ OCR | RapidOCR (onnxruntime) | Local en Render (sin API externa) |
| 🤖 Bot | python-telegram-bot | Local (Docker) |

> **Costo total: $0** · Sin tarjeta de crédito en ningún servicio.

---

## 🚀 Demo en vivo

**🔗 [verificaecuador.vercel.app](https://verificaecuador.vercel.app)**

### Ejemplo 1: Texto
1. Escribe: *"se anularon las elecciones de noviembre, es urgente reenviar"*
2. Resultado: 🔴 **Alto riesgo** → verificaciones del CNE con veredicto FALSO

### Ejemplo 2: Imagen
1. Cambia a la pestaña **🖼️ Imagen**
2. Pega con **Ctrl+V** un pantallazo de una cadena de WhatsApp
3. Resultado: el OCR lee el texto → mismo análisis de riesgo + verificaciones

### Ejemplo 3: Fuentes en vivo
1. Escribe: *"la vacuna contra el covid causa esclerosis múltiple según la OMS"*
2. Resultado: la BD no tiene respuesta → **busca en vivo** → encuentra verificación de **Newtral/Ecuador Chequea**

---

## 🛠️ Ejecución local

### Requisitos
- [Docker](https://docs.docker.com/get-docker/) + Docker Compose

### Pasos

```bash
# 1. Clonar el repo
git clone https://github.com/snxz-dev/verificaecuador.git
cd verificaecuador

# 2. Configurar variables de entorno
cp .env.example .env
# Edita .env con tu TELEGRAM_TOKEN y DATABASE_URL (Neon)
# Si no tienes Neon, puedes apuntar a un Postgres local (ver más abajo)

# 3. Levantar todo
docker compose up -d

# 4. Sembrar la BD (solo la primera vez)
docker compose exec backend python -c "
import os, psycopg2
conn = psycopg2.connect(os.environ['DATABASE_URL'])
conn.autocommit = True
with open('db/seed.sql') as f: conn.cursor().execute(f.read())
conn.close(); print('✅ Base de datos sembrada')
"
```

### URLs locales

| Servicio | URL |
|---|---|
| 🌐 Web | [http://localhost:4321](http://localhost:4321) |
| ⚙️ API | [http://localhost:8000](http://localhost:8000) |
| 📚 Docs API | [http://localhost:8000/docs](http://localhost:8000/docs) |
| 🤖 Bot | Habla con tu bot en Telegram |

### Solo la API (sin Docker)

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## 📡 Probar la API

### Verificar texto
```bash
curl -X POST https://verificaecuador.onrender.com/verify \
  -H "Content-Type: application/json" \
  -d '{"text":"se anularon las elecciones de noviembre urgente"}'
```

### Verificar imagen
```bash
curl -X POST https://verificaecuador.onrender.com/verify-image \
  -F "image=@captura.png"
```

### Respuesta ejemplo
```json
{
  "classification": {
    "risk": "high",
    "signals": ["urgente", "se anularon", "reenviar"],
    "themes": ["elecciones", "CNE"]
  },
  "matches": [
    {
      "claim": "Se anularon las elecciones",
      "verdict": "FALSO",
      "source": "CNE Ecuador",
      "url": "https://cnegob.ec/...",
      "explanation": "El CNE negó la anulación..."
    }
  ],
  "live_sources": true
}
```

---

## 🧠 Cómo funciona la detección

El motor de detección (`backend/app/detector.py`) analiza el texto sin inteligencia artificial — usa reglas lingüísticas y patrones conocidos:

1. **Señales de riesgo**: busca palabras típicas de desinformación:
   - Urgencia: *"urgente"*, *"reenviar"*, *"no te lo van a decir"*
   - Manipulación: *"confirmado"*, *"se anularon"*, *"en cadena"*
   - Emocional: *"comparte masivamente"*, *"esta vez sí es verdad"*

2. **Temas electorales**: detecta contexto político:
   - *"elecciones"*, *"CNE"*, *"padrón"*, *"fraude"*, *"candidato"*

3. **Búsqueda en fuentes**:
   - Primero consulta la **base de datos** (verificaciones pre-cargadas del CNE, Ecuador Chequea, Primera Plana)
   - Si no hay coincidencia, busca en **fuentes en vivo** (APIs públicas en tiempo real)

4. **Clasificación**:
   - 🔴 **Alto riesgo**: múltiples señales + tema electoral + sin verificación de fuentes confiables
   - 🟡 **Riesgo moderado**: algunas señales detectadas
   - 🟢 **Sin señales claras**: texto no presenta patrones típicos de desinformación

> ⚠️ **No emite juicios editoriales**: solo clasifica el nivel de riesgo y remite a la fuente original para que el usuario decida.

---

## 📁 Estructura del proyecto

```
verificaecuador/
├── backend/
│   ├── app/
│   │   ├── main.py          # API FastAPI (endpoints /verify, /verify-image, /image)
│   │   ├── bot.py           # Bot de Telegram
│   │   ├── config.py        # Variables de entorno
│   │   ├── db.py            # Conexión a PostgreSQL (Neon)
│   │   ├── detector.py      # Motor de detección de riesgo
│   │   ├── ocr.py           # OCR con RapidOCR (onnxruntime)
│   │   └── sources.py       # Fuentes en vivo (Ecuador Chequea, Google, etc.)
│   ├── Dockerfile
│   ├── requirements.txt
│   └── install.sh           # Script de instalación para Render
├── frontend/
│   ├── src/pages/index.astro  # Página principal (Texto | Imagen)
│   ├── Dockerfile
│   └── package.json
├── db/
│   └── seed.sql             # Datos de verificaciones (CNE, Ecuador Chequea, etc.)
├── docs/
│   └── guion-demo.md        # Guion de presentación para el demo
├── docker-compose.yml       # Orquestación local
├── render.yaml              # Blueprint para despliegue en Render
└── .env.example             # Plantilla de variables de entorno
```

---

## 🌍 Despliegue en producción

| Pieza | Servicio | URL |
|---|---|---|
| 🌐 Web | Vercel | [verificaecuador.vercel.app](https://verificaecuador.vercel.app) |
| ⚙️ API | Render | [verificaecuador.onrender.com](https://verificaecuador.onrender.com) |
| 🗄️ BD | Neon | PostgreSQL serverless |

### Variables de entorno

| Variable | Dónde | Descripción |
|---|---|---|
| `DATABASE_URL` | Render | URL de conexión a Neon (PostgreSQL) |
| `PYTHON_VERSION` | Render | `3.12.3` |
| `PUBLIC_API_URL` | Vercel | `https://verificaecuador.onrender.com` |

> Nota: la API de Render en plan gratis se duerme tras 15 min sin visitas. La primera petición tarda ~1 min en despertar (normal).

---

## 🎤 Demo (MediaHack II)

Ver [docs/guion-demo.md](docs/guion-demo.md) para el guion completo de la presentación (~3-4 minutos).

### Tips para el día del demo
- ⏰ **5 min antes**: abre la web y haz una verificación de prueba para despertar la API
- 📋 **Ten listo** un pantallazo de cadena falsa en el portapapeles (para Ctrl+V)
- 🎯 **Frase clave**: *"La desinformación circula como imagen. Aquí la pegamos y el sistema la lee y la verifica."*

---

## 🔐 Marco ético

VerificaEcuador se rige por estos principios:

- **Supervisión humana**: no hay veredictos automáticos, siempre se remite a fuentes
- **Neutralidad política**: no favorece ni perjudica candidaturas
- **Protección de datos**: no se almacenan mensajes de usuarios
- **Código abierto**: el código fuente es público y auditable
- **Transparencia**: el usuario decide — solo ofrecemos contexto y fuentes

---

## 👥 Equipo

Desarrollado para **MediaHack II** (Openlab Ecuador + KAS · 14-15 agosto 2026).

---

## 📄 Licencia

Proyecto educativo para MediaHack II. El código fuente es público para fines de transparencia y auditoría.

---

<p align="center">
  <sub>
    🇪🇨 Ecuador elige el 29 de noviembre de 2026 ·
    <strong>Verifica antes de compartir</strong>
  </sub>
</p>
