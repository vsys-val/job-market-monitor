DROP VIEW IF EXISTS jobs_clean;

CREATE VIEW jobs_clean AS
SELECT
    id,
    TRIM(titulo) AS titulo,
    TRIM(empresa) AS empresa,
    TRIM(localizacao) AS localizacao,
    LOWER(TRIM(url)) AS url,
    COALESCE(NULLIF(TRIM(categoria), ''), 'Não informado') AS categoria,
    COALESCE(NULLIF(TRIM(tipo_contrato), ''), 'Não informado') AS tipo_contrato,
    data_publicacao,
    COALESCE(NULLIF(TRIM(salario), ''), 'Não informado') AS salario,
    LOWER(TRIM(fonte)) AS fonte
FROM jobs
WHERE
    titulo IS NOT NULL
    AND TRIM(titulo) <> ''
    AND empresa IS NOT NULL
    AND TRIM(empresa) <> ''
    AND url IS NOT NULL
    AND TRIM(url) <> '';