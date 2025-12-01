USE acompanhamento_pacientes_bd;

-- =========================================================
-- 1. Lista de Pacientes Ativos com Endereço Completo
-- =========================================================
CREATE OR REPLACE VIEW ViewPacientesAtivosEndereco AS
SELECT 
    P.Nome AS Nome_Paciente,
    P.Telefone AS Telefone_Paciente,
    P.Email AS Email_Paciente,
    P.Numero_da_casa AS Numero,
    B.Nome_do_Bairro AS Bairro,
    C.Nome_da_Cidade AS Cidade,
    E.Nome_do_Estado AS Estado,
    PA.Nome_do_País AS Pais
FROM 
    pacientes AS P
INNER JOIN 
    bairros AS B ON P.Bairros_idBairros = B.idBairros
INNER JOIN 
    cidades AS C ON B.Cidades_idCidades = C.idCidades
INNER JOIN 
    estados AS E ON C.Estados_idEstados = E.idEstados
INNER JOIN 
    paises AS PA ON E.Países_idPaises = PA.idPaises
WHERE 
    P.Status = 'A'
ORDER BY 
    P.Nome;

-- =========================================================
-- 2. Contagem de Pacientes por Profissional
-- =========================================================
CREATE OR REPLACE VIEW ViewPacientesPorProfissional AS
SELECT 
    P.Nome AS Nome_Profissional,
    COUNT(PHP.Pacientes_idPacientes) AS Total_de_Pacientes
FROM 
    profissionais AS P
INNER JOIN 
    pacientes_has_profissionais AS PHP ON P.idProfissionais = PHP.Profissionais_idProfissionais
GROUP BY 
    P.idProfissionais, P.Nome
ORDER BY 
    Total_de_Pacientes DESC;


-- =========================================================
-- 3. Profissionais que mais atuaram em alertas (último ano)
-- =========================================================
CREATE OR REPLACE VIEW ViewProfissionaisMaisAtuantesAlertas AS
SELECT 
    PR.Nome AS Nome_Profissional,
    COUNT(A.idAlertas) AS Total_Alertas_Ultimo_Ano
FROM 
    profissionais AS PR
INNER JOIN 
    pacientes_has_profissionais AS PHP ON PR.idProfissionais = PHP.Profissionais_idProfissionais
INNER JOIN 
    pacientes AS P ON PHP.Pacientes_idPacientes = P.idPacientes
INNER JOIN 
    alertas AS A ON P.idPacientes = A.Pacientes_idPacientes
WHERE 
    A.geracao >= DATE_SUB('2025-11-18', INTERVAL 1 YEAR)
GROUP BY 
    PR.idProfissionais, PR.Nome
ORDER BY 
    Total_Alertas_Ultimo_Ano DESC;

-- =========================================================
-- 4. Pacientes mais atendidos no último ano
-- =========================================================
CREATE OR REPLACE VIEW ViewPacientesMaisAtendidos AS
SELECT 
    P.Nome AS Nome_Paciente,
    COUNT(HM.idhistorico_medico) AS Total_Consultas
FROM 
    historico_medico AS HM
INNER JOIN 
    pacientes AS P ON HM.Pacientes_idPacientes = P.idPacientes
WHERE 
    HM.tipo_evento = 'Consulta'
AND 
    HM.data_evento >= DATE_SUB('2025-11-18', INTERVAL 1 YEAR)
GROUP BY 
    P.idPacientes, P.Nome
ORDER BY 
    Total_Consultas DESC;


-- =========================================================
-- 5. Bairro com mais alertas no último semestre
-- =========================================================
CREATE OR REPLACE VIEW ViewBairroComMaisAlertasRecentes AS
SELECT 
    B.Nome_do_Bairro AS Bairro,
    COUNT(A.idAlertas) AS Total_Alertas_6Meses
FROM 
    alertas AS A
INNER JOIN 
    pacientes AS P ON A.Pacientes_idPacientes = P.idPacientes
INNER JOIN 
    bairros AS B ON P.Bairros_idBairros = B.idBairros
WHERE 
    A.geracao >= DATE_SUB('2025-11-18', INTERVAL 6 MONTH)
GROUP BY 
    B.idBairros, B.Nome_do_Bairro
ORDER BY 
    Total_Alertas_6Meses DESC;