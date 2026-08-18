CREATE TABLE IF NOT EXISTS fact_checks (
    id SERIAL PRIMARY KEY,
    claim TEXT NOT NULL,
    verdict TEXT NOT NULL,
    source TEXT NOT NULL,
    url TEXT NOT NULL,
    explanation TEXT,
    theme TEXT,
    keywords TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

INSERT INTO fact_checks (claim, verdict, source, url, explanation, theme, keywords) VALUES
(
    'Se anularon las elecciones generales de noviembre',
    'FALSO',
    'Consejo Nacional Electoral (CNE)',
    'https://www.cne.gob.ec',
    'El CNE confirmó que las elecciones se mantienen para el 29 de noviembre de 2026. Ninguna autoridad electoral ha anunciado su anulación.',
    'elecciones',
    'elecciones anularon noviembre suspendidas'
),
(
    'El voto será nulo si no se marca la papeleta completa',
    'FALSO',
    'CNE / Ecuador Chequea',
    'https://www.ecuadorchequea.com',
    'El voto es válido si la intención del elector es clara, aunque no esté completa la papeleta. La validez la determina la junta receptora del voto.',
    'voto',
    'voto nulo papeleta marca junta'
),
(
    'Se cambió la fecha de las elecciones a diciembre',
    'FALSO',
    'CNE',
    'https://www.cne.gob.ec',
    'El calendario electoral oficial fija las elecciones para el 29 de noviembre de 2026. No existe resolución que las cambie.',
    'elecciones',
    'fecha diciembre cambio elecciones'
),
(
    'Hay un fraude electoral planeado con las máquinas de votación',
    'SIN EVIDENCIA',
    'Ecuador Chequea',
    'https://www.ecuadorchequea.com',
    'No se ha presentado evidencia pública verificable de un plan de fraude. Las auditorías del sistema de votación son públicas y observables.',
    'fraude',
    'fraude maquinas votacion auditoria'
),
(
    'Un candidato repartirá un bono de 500 dólares si gana',
    'FALSO',
    'Primera Plana / Fact-check',
    'https://primeraplana.com.ec',
    'No existe una propuesta oficial registrada en el plan de gobierno del candidato que ofrezca ese bono. La cadena circula sin fuente oficial.',
    'bono',
    'bono candidato regalan pagaran'
),
(
    'Los padrones electorales fueron manipulados en favor de un candidato',
    'SIN EVIDENCIA',
    'CNE',
    'https://www.cne.gob.ec',
    'El CNE publica el padrón actualizado y la ciudadanía puede verificar su inscripción. No hay evidencia verificable de manipulación.',
    'padrón',
    'padron manipulado inscripcion'
),
(
    'El debate presidencial fue cancelado',
    'FALSO',
    'CNE / Ecuador Chequea',
    'https://www.ecuadorchequea.com',
    'El calendario oficial mantiene el debate presidencial programado. La cancelación no consta en ninguna resolución del CNE.',
    'debate',
    'debate cancelado presidencial'
);
