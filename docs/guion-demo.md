# 🎤 Guion de demo — VerificaEcuador (MediaHack II)

Presentación de ~3-4 minutos.

## 1. El problema (30 s)

> Ecuador elige el **29 de noviembre de 2026**, y con eso llega la desinformación:
> cadenas de WhatsApp, capturas manipuladas, rumores sobre el CNE y el voto.
> La gente no sabe a quién creer. Nosotros construimos **VerificaEcuador**:
> pegas una afirmación —o una imagen— y te decimos el nivel de riesgo,
> remitiéndote siempre a fuentes verificadas.

## 2. Demo en vivo — Texto (60 s)

1. Abrir `https://verificaecuador.vercel.app`
2. Escribir: **"se anularon las elecciones de noviembre, es urgente reenviar"**
3. Señalar: badge rojo **"Alto riesgo"** → señales detectadas → tarjetas del
   **CNE con veredicto FALSO** e imagen oficial.

> *"En 2 segundos: riesgo alto y la verificación oficial del CNE."*

## 3. Demo en vivo — Imagen (60 s)

1. Cambiar a la pestaña **🖼️ Imagen**
2. Pegar con **Ctrl+V** un pantallazo de una cadena falsa (ej: texto sobre la vacuna)
3. Señalar: **"Texto detectado"** (el OCR lo leyó solo) → mismo flujo →
   verificación en vivo.

> *"La desinformación circula como imagen. Aquí la pegamos y el sistema
> la lee y la verifica."*

## 4. El truco que sorprende (30 s)

> *"¿Y si la afirmación no está en nuestra base? No pasa nada: buscamos en
> vivo en 4 fuentes — Ecuador Chequea, Google Fact Check, Primera Plana y su
> RSS. Todo gratis, sin API keys."*

Probar: **"la vacuna contra el covid causa esclerosis múltiple según la OMS"**
→ mostrar que la verificación viene de **Newtral** (no está en la BD).

## 5. Cómo está hecho (30 s)

> *"Web en **Astro** (Vercel), API en **FastAPI** (Render), base de datos
> **Postgres serverless en Neon**, OCR local sin servicios externos, y
> **$0 de costo** — todo en planes gratuitos."*

## 6. Marco ético + cierre (30 s)

> *"VerificaEcuador **no emite juicios**: solo marca riesgo y te manda a la
> fuente original. Sin sesgo político, sin guardar mensajes de usuarios,
> código abierto. **Verifica antes de compartir.**"*

## Tips de la demo

- **Despierta la API ~1 min antes**: si la API de Render durmió (15 min sin
  uso), la primera petición tarda ~1 min. Haz una verificación de prueba antes.
- Ten el pantallazo **listo en el portapapeles** para el Ctrl+V.
- Los colores de la bandera en la web 🇪🇨 son un buen detalle visual.
