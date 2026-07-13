-- Total de vagas coletadas
SELECT COUNT(*) AS total_vagas
FROM jobs;


-- Quantidade de vagas por empresa
SELECT
    empresa,
    COUNT(*) AS quantidade_vagas
FROM jobs
GROUP BY empresa
ORDER BY quantidade_vagas DESC;


-- Quantidade de vagas por localização
SELECT
    localizacao,
    COUNT(*) AS quantidade_vagas
FROM jobs
GROUP BY localizacao
ORDER BY quantidade_vagas DESC;


-- Quantidade de vagas por categoria
SELECT
    categoria,
    COUNT(*) AS quantidade_vagas
FROM jobs
GROUP BY categoria
ORDER BY quantidade_vagas DESC;


-- Vagas que mencionam Analyst no título
SELECT
    titulo,
    empresa,
    localizacao
FROM jobs
WHERE titulo LIKE '%Analyst%'
ORDER BY empresa;