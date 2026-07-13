-- Quantidade total de registros
SELECT COUNT(*) AS total_registros
FROM jobs;


-- Campos ausentes
SELECT
    SUM(CASE WHEN titulo IS NULL OR TRIM(titulo) = '' THEN 1 ELSE 0 END) AS titulo_ausente,
    SUM(CASE WHEN empresa IS NULL OR TRIM(empresa) = '' THEN 1 ELSE 0 END) AS empresa_ausente,
    SUM(CASE WHEN localizacao IS NULL OR TRIM(localizacao) = '' THEN 1 ELSE 0 END) AS localizacao_ausente,
    SUM(CASE WHEN categoria IS NULL OR TRIM(categoria) = '' THEN 1 ELSE 0 END) AS categoria_ausente,
    SUM(CASE WHEN salario IS NULL OR TRIM(salario) = '' THEN 1 ELSE 0 END) AS salario_ausente
FROM jobs;


-- Possíveis URLs duplicadas
SELECT
    url,
    COUNT(*) AS quantidade
FROM jobs
GROUP BY url
HAVING COUNT(*) > 1;


-- Valores distintos de tipo de contrato
SELECT
    tipo_contrato,
    COUNT(*) AS quantidade
FROM jobs
GROUP BY tipo_contrato
ORDER BY quantidade DESC;


-- Valores distintos de localização
SELECT
    localizacao,
    COUNT(*) AS quantidade
FROM jobs
GROUP BY localizacao
ORDER BY quantidade DESC;


-- Títulos possivelmente duplicados
SELECT
    titulo,
    empresa,
    COUNT(*) AS quantidade
FROM jobs
GROUP BY titulo, empresa
HAVING COUNT(*) > 1
ORDER BY quantidade DESC;