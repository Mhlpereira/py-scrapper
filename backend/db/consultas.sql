SELECT o.razao_social, SUM(d.valor) AS total_despesas
FROM demonstracoes d
JOIN operadoras o ON d.operadora_id = o.id
WHERE d.descricao_conta LIKE '%EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS%'
  AND d.data >= DATE_TRUNC('quarter', CURRENT_DATE) - INTERVAL '3 months'
GROUP BY o.razao_social
ORDER BY total_despesas DESC
LIMIT 10;

SELECT o.razao_social, SUM(d.valor) AS total_despesas
FROM demonstracoes d
JOIN operadoras o ON d.operadora_id = o.id
WHERE d.descricao_conta LIKE '%EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS%'
  AND d.data >= CURRENT_DATE - INTERVAL '1 year'
GROUP BY o.razao_social
ORDER BY total_despesas DESC
LIMIT 10;