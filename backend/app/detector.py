"""Detección de desinformación basada en reglas (sin IA).

Combina señales lingüísticas de riesgo con la base de verificaciones.
No emite juicios: solo señala riesgo y remite a fuentes verificadas.
"""

# Palabras/patrones que suelen acompañar desinformación electoral
HIGH_RISK_SIGNALS = [
    "candidato va a", "eliminó las elecciones", "se anularon", "voto será nulo",
    "fraude electoral", "cambio de fecha", "elecciones suspendidas", "gana por decreto",
    "se robó", "denuncia penal", "detenido por", "renunció", "dimitió",
    "bono de", "pagarán", "regalan", "gratis", "confirmado", "no es cierto",
    "falso", "en cadena", "reenvía", "esto es real", "urgente",
]

# Temas comunes en el ciclo electoral ecuatoriano
THEMES = [
    "elecciones", "cne", "consejo nacional electoral", "voto", "sufragio",
    "candidato", "candidata", "plan de gobierno", "debate", "padrón",
    "bono", "fraude", "fecha", "junta", "recinto", "delegado",
]


def classify(message: str) -> dict:
    text = message.lower()
    signals = [s for s in HIGH_RISK_SIGNALS if s in text]
    themes = [t for t in THEMES if t in text]

    if len(signals) >= 2:
        risk = "high"
    elif signals:
        risk = "medium"
    else:
        risk = "low"

    return {
        "risk": risk,
        "signals": signals,
        "themes": themes,
        "risk_label": {
            "high": "Alto riesgo de desinformación",
            "medium": "Riesgo moderado",
            "low": "Sin señales claras",
        }[risk],
    }
