import os

CORUJINHA_DIR = '/home/sfy/Corujinha'

disciplines_data = [
    {
        "code": "ETICA",
        "name": "Ética Profissional e Estatuto da OAB",
        "desc": "Estatuto da OAB, Código de Ética e Regulamento Geral. Módulos 01 a 08.",
        "badge": "12 Questões na Prova OAB",
        "color": "#d97706",
        "dashboard": "ETICA/Dashboard_Etica_Premium.html",
        "modules": [
            ("Órgãos da OAB", "ETICA/Etica_01_Orgaos_da_OAB_Premium.html"),
            ("Direitos e Prerrogativas", "ETICA/Etica_02_Direitos_e_Prerrogativas_Premium.html"),
            ("Incompatibilidade e Impedimento", "ETICA/Etica_03_Incompatibilidade_e_Impedimento_Premium.html"),
            ("Infrações e Sanções", "ETICA/Etica_04_Infracoes_e_Sancoes_Premium.html"),
            ("Honorários Advocatícios", "ETICA/Etica_05_Publicidade_e_Honorarios_Premium.html"),
            ("Publicidade e Marketing", "ETICA/Etica_06_Publicidade_e_Marketing_Premium.html"),
            ("Advogados e Estagiários", "ETICA/Etica_07_Advogados_e_Estagiarios_Premium.html"),
            ("Processo Disciplinar", "ETICA/Etica_08_Processo_Administrativo_e_Eleitoral_Premium.html")
        ]
    },
    {
        "code": "CIVIL",
        "name": "Direito Civil",
        "desc": "Código Civil (Lei nº 10.406/2002) e LINDB. Módulos 01 a 08.",
        "badge": "6 Questões na Prova OAB",
        "color": "#2563eb",
        "dashboard": "CIVIL/Dashboard_Civil_Premium.html",
        "modules": [
            ("Parte Geral e LINDB", "CIVIL/Civil_01_ParteGeral_Premium.html"),
            ("Negócio Jurídico e Prescrição", "CIVIL/Civil_02_NegocioJuridico_Premium.html"),
            ("Teoria Geral das Obrigações", "CIVIL/Civil_03_Obrigacoes_Premium.html"),
            ("Contratos em Geral e Espécie", "CIVIL/Civil_04_Contratos_Premium.html"),
            ("Responsabilidade Civil", "CIVIL/Civil_05_ResponsabilidadeCivil_Premium.html"),
            ("Direitos Reais e Posse", "CIVIL/Civil_06_DireitosReais_Premium.html"),
            ("Direito de Família", "CIVIL/Civil_07_DireitoDeFamilia_Premium.html"),
            ("Direito das Sucessões", "CIVIL/Civil_08_DireitoDasSucessoes_Premium.html")
        ]
    },
    {
        "code": "CPC",
        "name": "Direito Processual Civil",
        "desc": "Código de Processo Civil (Lei nº 13.105/2015). Módulos 01 a 08.",
        "badge": "6 Questões na Prova OAB",
        "color": "#4f46e5",
        "dashboard": "CPC/Dashboard_CPC_Premium.html",
        "modules": [
            ("Normas Fundamentais", "CPC/CPC_01_NormasFundamentais_Premium.html"),
            ("Partes e Litisconsórcio", "CPC/CPC_02_PartesLitisconsorcio_Premium.html"),
            ("Competência e Atos Processuais", "CPC/CPC_03_CompetenciaAtos_Premium.html"),
            ("Tutela Provisória", "CPC/CPC_04_TutelaProvisoria_Premium.html"),
            ("Procedimento Comum", "CPC/CPC_05_ProcedimentoComum_Premium.html"),
            ("Execução e Cumprimento", "CPC/CPC_06_ExecucaoCumprimento_Premium.html"),
            ("Recursos e Tribunais", "CPC/CPC_07_RecursosTribunais_Premium.html"),
            ("Procedimentos Especiais", "CPC/CPC_08_ProcedimentosEspeciais_Premium.html")
        ]
    },
    {
        "code": "PENAL",
        "name": "Direito Penal",
        "desc": "Código Penal (Decreto-Lei nº 2.848/1940) e Legislação Especial. Módulos 01 a 08.",
        "badge": "6 Questões na Prova OAB",
        "color": "#dc2626",
        "dashboard": "PENAL/Dashboard_Penal_Premium.html",
        "modules": [
            ("Princípios e Aplicação CP", "PENAL/Penal_01_PrincipiosAplicacaoCP_Premium.html"),
            ("Teoria Geral do Crime", "PENAL/Penal_02_TeoriaGeralCrime_Premium.html"),
            ("Ilicitude e Culpabilidade", "PENAL/Penal_03_IlicitudeCulpabilidade_Premium.html"),
            ("Concurso e Penas", "PENAL/Penal_04_ConcursoPenas_Premium.html"),
            ("Crimes Pessoa e Patrimônio", "PENAL/Penal_05_CrimesPessoaPatrimonio_Premium.html"),
            ("Crimes Dignidade e ADM", "PENAL/Penal_06_CrimesDignidadeADM_Premium.html"),
            ("Leis Penais Especiais", "PENAL/Penal_07_LeisPenaisEspeciais_Premium.html"),
            ("Extinção da Punibilidade", "PENAL/Penal_08_ExtincaoPunibilidade_Premium.html")
        ]
    },
    {
        "code": "PROCESSUAL_PENAL",
        "name": "Direito Processual Penal",
        "desc": "Código de Processo Penal (Decreto-Lei nº 3.689/1941). Módulos 01 a 08.",
        "badge": "6 Questões na Prova OAB",
        "color": "#b91c1c",
        "dashboard": "PROCESSUAL_PENAL/Dashboard_ProcessualPenal_Premium.html",
        "modules": [
            ("Inquérito e Ação Penal", "PROCESSUAL_PENAL/PP_01_InqueritoAcaoPenal_Premium.html"),
            ("Jurisdição e Competência", "PROCESSUAL_PENAL/PP_02_JurisdicaoCompetencia_Premium.html"),
            ("Provas e Medidas Cautelares", "PROCESSUAL_PENAL/PP_03_ProvasMedidasCautelares_Premium.html"),
            ("Prisão e Liberdade Provisória", "PROCESSUAL_PENAL/PP_04_PrisaoLiberdadeProvisoria_Premium.html"),
            ("Procedimentos e Júri", "PROCESSUAL_PENAL/PP_05_ProcedimentosJuri_Premium.html"),
            ("Nulidades e Recursos", "PROCESSUAL_PENAL/PP_06_NulidadesRecursos_Premium.html"),
            ("Ações Autônomas e HC", "PROCESSUAL_PENAL/PP_07_AcoesAutonomasHC_Premium.html"),
            ("Execução Penal (LEP)", "PROCESSUAL_PENAL/PP_08_ExecucaoPenalLEP_Premium.html")
        ]
    },
    {
        "code": "CONSTITUCIONAL",
        "name": "Direito Constitucional",
        "desc": "Constituição da República Federativa do Brasil de 1988. Módulos 01 a 08.",
        "badge": "6 Questões na Prova OAB",
        "color": "#059669",
        "dashboard": "CONSTITUCIONAL/Dashboard_Constitucional_Premium.html",
        "modules": [
            ("Teoria da Constituição", "CONSTITUCIONAL/Const_01_TeoriaConstituicao_Premium.html"),
            ("Direitos Fundamentais", "CONSTITUCIONAL/Const_02_DireitosFundamentais_Premium.html"),
            ("Remédios Constitucionais", "CONSTITUCIONAL/Const_03_RemediosConstitucionais_Premium.html"),
            ("Organização do Estado", "CONSTITUCIONAL/Const_04_OrganizacaoEstado_Premium.html"),
            ("Organização dos Poderes", "CONSTITUCIONAL/Const_05_OrganizacaoPoderes_Premium.html"),
            ("Controle de Constitucionalidade", "CONSTITUCIONAL/Const_06_ControleConstitucionalidade_Premium.html"),
            ("Defesa do Estado e Instituições", "CONSTITUCIONAL/Const_07_DefesaEstado_Premium.html"),
            ("Ordem Econômica e Social", "CONSTITUCIONAL/Const_08_OrdemEconomicaSocial_Premium.html")
        ]
    },
    {
        "code": "ADMINISTRATIVO",
        "name": "Direito Administrativo",
        "desc": "Regime Jurídico Administrativo, Licitações e Serviços Públicos. Módulos 01 a 08.",
        "badge": "5 Questões na Prova OAB",
        "color": "#0d9488",
        "dashboard": "ADMINISTRATIVO/Dashboard_Administrativo_Premium.html",
        "modules": [
            ("Organização Administrativa", "ADMINISTRATIVO/Admin_01_OrganizacaoAdministrativa_Premium.html"),
            ("Princípios e Poderes", "ADMINISTRATIVO/Admin_02_PrincipiosPoderes_Premium.html"),
            ("Atos Administrativos", "ADMINISTRATIVO/Admin_03_AtosAdministrativos_Premium.html"),
            ("Licitações e Contratos", "ADMINISTRATIVO/Admin_04_LicitacoesContratos_Premium.html"),
            ("Serviços Públicos e Intervenção", "ADMINISTRATIVO/Admin_05_ServicosIntervencao_Premium.html"),
            ("Agentes e Improbidade", "ADMINISTRATIVO/Admin_06_AgentesImprobidade_Premium.html"),
            ("Responsabilidade do Estado", "ADMINISTRATIVO/Admin_07_ResponsabilidadeEstado_Premium.html"),
            ("Processo e Bens Públicos", "ADMINISTRATIVO/Admin_08_ProcessoBensPublicos_Premium.html")
        ]
    },
    {
        "code": "TRIBUTARIO",
        "name": "Direito Tributário",
        "desc": "Sistema Tributário Nacional e Código Tributário Nacional (CTN). Módulos 01 a 08.",
        "badge": "5 Questões na Prova OAB",
        "color": "#7c3aed",
        "dashboard": "TRIBUTARIO/Dashboard_Tributario_Premium.html",
        "modules": [
            ("Sistema Tributário e Conceito", "TRIBUTARIO/Trib_01_SistemaTributarioConceito_Premium.html"),
            ("Limitações ao Poder de Tributar", "TRIBUTARIO/Trib_02_LimitacoesPoderTributar_Premium.html"),
            ("Competência e Espécies", "TRIBUTARIO/Trib_03_CompetenciaEspecies_Premium.html"),
            ("Obrigação e Lançamento", "TRIBUTARIO/Trib_04_ObrigacaoLancamento_Premium.html"),
            ("Suspensão e Extinção", "TRIBUTARIO/Trib_05_SuspensaoExtincao_Premium.html"),
            ("Exclusão e Garantias", "TRIBUTARIO/Trib_06_ExclusaoGarantias_Premium.html"),
            ("Impostos Federais e Estaduais", "TRIBUTARIO/Trib_07_ImpostosFederaisEstaduais_Premium.html"),
            ("Impostos Municipais e Processo", "TRIBUTARIO/Trib_08_ImpostosMunicipaisProcesso_Premium.html")
        ]
    },
    {
        "code": "TRABALHISTA",
        "name": "Direito do Trabalho",
        "desc": "Consolidação das Leis do Trabalho (CLT) e Direito Material. Módulos 01 a 08.",
        "badge": "5 Questões na Prova OAB",
        "color": "#db2777",
        "dashboard": "TRABALHISTA/Dashboard_Trabalhista_Premium.html",
        "modules": [
            ("Contrato de Trabalho", "TRABALHISTA/Trab_01_ContratodeTrabalho_Premium.html"),
            ("Jornada e Remuneração", "TRABALHISTA/Trab_02_JornadaRemuneracao_Premium.html"),
            ("Férias e Salário", "TRABALHISTA/Trab_03_FeriasESalario_Premium.html"),
            ("Rescisão do Contrato", "TRABALHISTA/Trab_04_RescisaoContrato_Premium.html"),
            ("Estabilidades e Garantias", "TRABALHISTA/Trab_05_StabilidadesGarantias_Premium.html"),
            ("Organização Sindical", "TRABALHISTA/Trab_06_OrganizacaoSindical_Premium.html"),
            ("Equipamentos de Proteção", "TRABALHISTA/Trab_07_EquipamentosProtecao_Premium.html"),
            ("Previdência e Benefícios", "TRABALHISTA/Trab_08_PrevidenciaEBeneficios_Premium.html")
        ]
    },
    {
        "code": "PROCESSUAL_TRABALHISTA",
        "name": "Direito Processual do Trabalho",
        "desc": "Processo do Trabalho na CLT e Instruções Normativas do TST. Módulos 01 a 08.",
        "badge": "5 Questões na Prova OAB",
        "color": "#e11d48",
        "dashboard": "PROCESSUAL_TRABALHISTA/Dashboard_ProcessualTrabalhista_Premium.html",
        "modules": [
            ("Organização Justiça Trabalho", "PROCESSUAL_TRABALHISTA/PT_01_OrganizacaoJusticaTrabalho_Premium.html"),
            ("Reclamação Trabalhista", "PROCESSUAL_TRABALHISTA/PT_02_ReclamacaoTrabalhistaCLT_Premium.html"),
            ("Prova e Perícia", "PROCESSUAL_TRABALHISTA/PT_03_ProvaPericia_Premium.html"),
            ("Recursos Trabalhistas", "PROCESSUAL_TRABALHISTA/PT_04_RecursosTrabalhistas_Premium.html"),
            ("Execução Trabalhista", "PROCESSUAL_TRABALHISTA/PT_05_ExecucaoTrabalhistaCLT_Premium.html"),
            ("Ações Especiais", "PROCESSUAL_TRABALHISTA/PT_06_AcoesEspeciaisTrabalho_Premium.html"),
            ("Cautelar e Inquérito", "PROCESSUAL_TRABALHISTA/PT_07_CautelalInquerito_Premium.html"),
            ("Rito Sumaríssimo", "PROCESSUAL_TRABALHISTA/PT_08_RitoSumarissimo_Premium.html")
        ]
    },
    {
        "code": "EMPRESARIAL",
        "name": "Direito Empresarial",
        "desc": "Código Civil (Livro II), Lei de Sociedades Anônimas e Falências. Módulos 01 a 08.",
        "badge": "4 Questões na Prova OAB",
        "color": "#0284c7",
        "dashboard": "EMPRESARIAL/Dashboard_Empresarial_Premium.html",
        "modules": [
            ("Empresário e Sociedades", "EMPRESARIAL/Emp_01_EmpresarioSociedades_Premium.html"),
            ("Estabelecimento e Nome", "EMPRESARIAL/Emp_02_EstabelecimentoNomeEmpresarial_Premium.html"),
            ("Títulos de Crédito", "EMPRESARIAL/Emp_03_TitulosCredito_Premium.html"),
            ("Contratos Empresariais", "EMPRESARIAL/Emp_04_ContratosEmpresariais_Premium.html"),
            ("Sociedade Anônima (S/A)", "EMPRESARIAL/Emp_05_SociedadeAnonima_Premium.html"),
            ("Falência e Recuperação", "EMPRESARIAL/Emp_06_FalenciaRecuperacao_Premium.html"),
            ("Direito do Consumidor", "EMPRESARIAL/Emp_07_DireitoConsumidor_Premium.html"),
            ("Propriedade Intelectual", "EMPRESARIAL/Emp_08_PropriedadeIntelectual_Premium.html")
        ]
    },
    {
        "code": "FILOSOFIA",
        "name": "Filosofia do Direito",
        "desc": "Pensadores Clássicos e Contemporâneos da Filosofia Jurídica. Módulos 01 a 08.",
        "badge": "2 Questões na Prova OAB",
        "color": "#9333ea",
        "dashboard": "FILOSOFIA/Dashboard_Filosofia_Premium.html",
        "modules": [
            ("Jusnaturalismo e Juspositivismo", "FILOSOFIA/Fil_01_JusnaturalismoJuspositivismo_Premium.html"),
            ("Teoria Pura de Kelsen", "FILOSOFIA/Fil_02_TeoriaPuraKelsen_Premium.html"),
            ("Pós-positivismo (Dworkin/Alexy)", "FILOSOFIA/Fil_03_PospositivismoDworkinAlexy_Premium.html"),
            ("Hermenêutica e Argumentação", "FILOSOFIA/Fil_04_HermeneuticaArgumentacao_Premium.html"),
            ("Teorias da Justiça (Rawls)", "FILOSOFIA/Fil_05_TeoriasJusticaRawls_Premium.html"),
            ("Conceito de Direito (Hart)", "FILOSOFIA/Fil_06_ConceitoDireitoHart_Premium.html"),
            ("Sociologia e Efetividade", "FILOSOFIA/Fil_07_SociologiaEfetividade_Premium.html"),
            ("Ética Política e Utilitarismo", "FILOSOFIA/Fil_08_EticaPoliticaUtilitarismo_Premium.html")
        ]
    },
    {
        "code": "AMBIENTAL",
        "name": "Direito Ambiental",
        "desc": "Lei de Política Nacional do Meio Ambiente e Código Florestal. Módulos 01 a 08.",
        "badge": "2 Questões na Prova OAB",
        "color": "#16a34a",
        "dashboard": "AMBIENTAL/Dashboard_Ambiental_Premium.html",
        "modules": [
            ("Princípios Ambientais", "AMBIENTAL/Amb_01_PrincipiosAmbientais_Premium.html"),
            ("Competências Ambientais", "AMBIENTAL/Amb_02_CompetenciasAmbientais_Premium.html"),
            ("Licenciamento e EIA/RIMA", "AMBIENTAL/Amb_03_LicenciamentoEIA_Premium.html"),
            ("Responsabilidade Civil Ambiental", "AMBIENTAL/Amb_04_ResponsabilidadeCivil_Premium.html"),
            ("Crimes Ambientais (Lei 9.605)", "AMBIENTAL/Amb_05_CrimesAmbientais_Premium.html"),
            ("Código Florestal (Lei 12.651)", "AMBIENTAL/Amb_06_CodigoFlorestal_Premium.html"),
            ("SNUC e Unidades de Conservação", "AMBIENTAL/Amb_07_SNUCUnidadesConservacao_Premium.html"),
            ("Recursos Hídricos e Resíduos", "AMBIENTAL/Amb_08_RecursosHidricosResiduos_Premium.html")
        ]
    },
    {
        "code": "DIREITOS_HUMANOS",
        "name": "Direitos Humanos",
        "desc": "Sistemas Internacional e Interamericano de Proteção aos Direitos Humanos. Módulos 01 a 08.",
        "badge": "2 Questões na Prova OAB",
        "color": "#0891b2",
        "dashboard": "DIREITOS_HUMANOS/Dashboard_DireitosHumanos_Premium.html",
        "modules": [
            ("Conceitos Fundamentais", "DIREITOS_HUMANOS/DH_01_ConceitosFundamentais_Premium.html"),
            ("Sistema Interamericano", "DIREITOS_HUMANOS/DH_02_SistemaInteramericano_Premium.html"),
            ("Incorporação de Tratados", "DIREITOS_HUMANOS/DH_03_IncorporacaoTratados_Premium.html"),
            ("Proteção de Vulneráveis", "DIREITOS_HUMANOS/DH_04_ProtecaoVulneraveis_Premium.html"),
            ("Combate à Tortura", "DIREITOS_HUMANOS/DH_05_CombateTortura_Premium.html"),
            ("Pacto de San José da Costa Rica", "DIREITOS_HUMANOS/DH_06_PactoSanJose_Premium.html"),
            ("Cortes Internacionais", "DIREITOS_HUMANOS/DH_07_CortesInternacionais_Premium.html"),
            ("Direitos Humanos no Brasil", "DIREITOS_HUMANOS/DH_08_DHNoBrasil_Premium.html")
        ]
    },
    {
        "code": "INTERNACIONAL",
        "name": "Direito Internacional",
        "desc": "Direito Internacional Público e Privado (LINDB / Lei de Migração). Módulos 01 a 08.",
        "badge": "2 Questões na Prova OAB",
        "color": "#0284c7",
        "dashboard": "INTERNACIONAL/Dashboard_Internacional_Premium.html",
        "modules": [
            ("Fontes e Tratados", "INTERNACIONAL/Int_01_FontesTratados_Premium.html"),
            ("Sujeitos de Direito Internacional", "INTERNACIONAL/Int_02_SujeitosDireitoInternacional_Premium.html"),
            ("Domínio Público e Espaço", "INTERNACIONAL/Int_03_DominioPublicoEspaco_Premium.html"),
            ("Solução Pacífica de Controvérsias", "INTERNACIONAL/Int_04_SolucaoPacificasControversias_Premium.html"),
            ("Nacionalidade e Condição Jurídica", "INTERNACIONAL/Int_05_NacionalidadeCondicaoJuridica_Premium.html"),
            ("Lei de Migração e Extradição", "INTERNACIONAL/Int_06_LeiMigracaoExtradicao_Premium.html"),
            ("Direito Internacional Privado", "INTERNACIONAL/Int_07_DireitoInternacionalPrivado_Premium.html"),
            ("Cooperação Jurídica Internacional", "INTERNACIONAL/Int_08_CooperacaoJuridicaInternacional_Premium.html")
        ]
    },
    {
        "code": "ECA",
        "name": "Estatuto da Criança e do Adolescente (ECA)",
        "desc": "Lei nº 8.069/1990 e Direitos Fundamentais do Infante. Módulos 01 a 08.",
        "badge": "2 Questões na Prova OAB",
        "color": "#d97706",
        "dashboard": "ECA/Dashboard_ECA_Premium.html",
        "modules": [
            ("Princípios e Direitos Fundamentais", "ECA/ECA_01_PrincipiosDireitosFundamentais_Premium.html"),
            ("Direito à Convivência Familiar", "ECA/ECA_02_DireitoConvivenciaFamiliar_Premium.html"),
            ("Adoção e Guarda", "ECA/ECA_03_AdocaoGuarda_Premium.html"),
            ("Medidas de Proteção", "ECA/ECA_04_MedidasProtecao_Premium.html"),
            ("Ato Infracional e Apreensão", "ECA/ECA_05_AtoInfracionalApreensao_Premium.html"),
            ("Medidas Socioeducativas (SINASE)", "ECA/ECA_06_MedidasSocioeducativasSINASE_Premium.html"),
            ("Conselho Tutelar e Justiça", "ECA/ECA_07_ConselhoTutelarJustica_Premium.html"),
            ("Crimes e Infrações no ECA", "ECA/ECA_08_CrimesInfracoesECA_Premium.html")
        ]
    },
    {
        "code": "CONSUMIDOR",
        "name": "Direito do Consumidor",
        "desc": "Código de Defesa do Consumidor (Lei nº 8.078/1990). Módulos 01 a 08.",
        "badge": "2 Questões na Prova OAB",
        "color": "#ea580c",
        "dashboard": "CONSUMIDOR/Dashboard_Consumidor_Premium.html",
        "modules": [
            ("Relação de Consumo e Princípios", "CONSUMIDOR/Cons_01_RelacaoConsumoPrincipios_Premium.html"),
            ("Direitos Básicos do Consumidor", "CONSUMIDOR/Cons_02_DireitosBasicosConsumidor_Premium.html"),
            ("Responsabilidade pelo Fato", "CONSUMIDOR/Cons_03_ResponsabilidadeFato_Premium.html"),
            ("Responsabilidade pelo Vício", "CONSUMIDOR/Cons_04_ResponsabilidadeVicio_Premium.html"),
            ("Práticas Comerciais e Oferta", "CONSUMIDOR/Cons_05_PraticasComerciaisOferta_Premium.html"),
            ("Proteção Contratual e Cláusulas", "CONSUMIDOR/Cons_06_ProtecaoContratualClausulas_Premium.html"),
            ("Cobrança de Dívidas e Bancos", "CONSUMIDOR/Cons_07_CobrancaDividasBancos_Premium.html"),
            ("Defesa do Consumidor em Juízo", "CONSUMIDOR/Cons_08_DefesaConsumidorJuizo_Premium.html")
        ]
    },
    {
        "code": "ELEITORAL",
        "name": "Direito Eleitoral",
        "desc": "Código Eleitoral (Lei nº 4.737/1965) e Lei das Eleições. Módulos 01 a 08.",
        "badge": "2 Questões na Prova OAB",
        "color": "#65a30d",
        "dashboard": "ELEITORAL/Dashboard_Eleitoral_Premium.html",
        "modules": [
            ("Princípios e Justiça Eleitoral", "ELEITORAL/Eleit_01_PrincipiosJusticaEleitoral_Premium.html"),
            ("Direitos Políticos e Elegibilidade", "ELEITORAL/Eleit_02_DireitosPoliticosElegibilidade_Premium.html"),
            ("Inelegibilidades (LC 64/90)", "ELEITORAL/Eleit_03_InelegibilidadesLC64_Premium.html"),
            ("Partidos Políticos e Convenções", "ELEITORAL/Eleit_04_PartidosPoliticosConvencoes_Premium.html"),
            ("Registro de Candidatura", "ELEITORAL/Eleit_05_RegistroCandidatura_Premium.html"),
            ("Propaganda Eleitoral e Financiamento", "ELEITORAL/Eleit_06_PropagandaFinanciamento_Premium.html"),
            ("Ações Eleitorais (AIJE/AIME)", "ELEITORAL/Eleit_07_AcoesEleitoraisAIJE_AIME_Premium.html"),
            ("Crimes Eleitorais e Processo", "ELEITORAL/Eleit_08_CrimesEleitoraisProcesso_Premium.html")
        ]
    },
    {
        "code": "PREVIDENCIARIO",
        "name": "Direito Previdenciário",
        "desc": "Seguridade Social (Lei 8.212/91) e Planos de Benefícios (Lei 8.213/91). Módulos 01 a 08.",
        "badge": "2 Questões na Prova OAB",
        "color": "#ca8a04",
        "dashboard": "PREVIDENCIARIO/Dashboard_Previdenciario_Premium.html",
        "modules": [
            ("Seguridade Social e Princípios", "PREVIDENCIARIO/Prev_01_SeguridadeSocialPrincipios_Premium.html"),
            ("Segurados e Dependentes RGPS", "PREVIDENCIARIO/Prev_02_SeguradosDependentesRGPS_Premium.html"),
            ("Financiamento e Contribuições", "PREVIDENCIARIO/Prev_03_FinanciamentoContribuicoes_Premium.html"),
            ("Carência e Qualidade de Segurado", "PREVIDENCIARIO/Prev_04_CarenciaQualidadeSegurado_Premium.html"),
            ("Aposentadorias e Incapacidade", "PREVIDENCIARIO/Prev_05_AposentadoriasIncapacidade_Premium.html"),
            ("Pensão por Morte e Auxílios", "PREVIDENCIARIO/Prev_06_PensaoMorteAuxilios_Premium.html"),
            ("Reforma EC 103 e Transição", "PREVIDENCIARIO/Prev_07_ReformaEC103RegrasTransicao_Premium.html"),
            ("Processo Previdenciário", "PREVIDENCIARIO/Prev_08_ProcessoPrevidenciario_Premium.html")
        ]
    },
    {
        "code": "FINANCEIRO",
        "name": "Direito Financeiro",
        "desc": "Orçamento Público, Lei 4.320/64 e Lei de Responsabilidade Fiscal. Módulos 01 a 08.",
        "badge": "2 Questões na Prova OAB",
        "color": "#475569",
        "dashboard": "FINANCEIRO/Dashboard_Financeiro_Premium.html",
        "modules": [
            ("PPA, LDO e LOA", "FINANCEIRO/Fin_01_PPA_LDO_LOA_Premium.html"),
            ("Princípios Orçamentários", "FINANCEIRO/Fin_02_PrincipiosOrcamentarios_Premium.html"),
            ("Receita Pública", "FINANCEIRO/Fin_03_ReceitaPublica_Premium.html"),
            ("Despesa Pública", "FINANCEIRO/Fin_04_DespesaPublica_Premium.html"),
            ("Créditos Adicionais", "FINANCEIRO/Fin_05_CreditosAdicionais_Premium.html"),
            ("Lei de Responsabilidade Fiscal", "FINANCEIRO/Fin_06_LeiResponsabilidadeFiscal_Premium.html"),
            ("Precatórios e Dívida Ativa", "FINANCEIRO/Fin_07_PrecatoriosDividaAtiva_Premium.html"),
            ("Fiscalização e Tribunal de Contas", "FINANCEIRO/Fin_08_FiscalizacaoTribunalContas_Premium.html")
        ]
    }
]

html_str = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>Plataforma Corujinha OAB · Portal Central de Disciplinas</title>

  <!-- Google Fonts: Inter -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

  <style>
    :root {
      --bg: #f8fafc;
      --surface: #ffffff;
      --surface-border: #e2e8f0;
      --text-main: #0f172a;
      --text-muted: #64748b;
      --text-light: #94a3b8;
      --primary: #0f172a;
      --primary-hover: #1e293b;
      --accent-color: #2563eb;
      --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.04), 0 1px 2px rgba(0, 0, 0, 0.02);
      --shadow-float: 0 10px 30px -5px rgba(0, 0, 0, 0.04), 0 4px 12px -2px rgba(0, 0, 0, 0.02);
      --shadow-hover: 0 20px 35px -10px rgba(0, 0, 0, 0.07), 0 8px 16px -4px rgba(0, 0, 0, 0.02);
    }

    * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', system-ui, -apple-system, sans-serif; -webkit-tap-highlight-color: transparent; }

    body {
      background-color: var(--bg);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      -webkit-font-smoothing: antialiased;
    }

    /* Header sobrio */
    header {
      background: var(--surface);
      border-bottom: 1px solid var(--surface-border);
      padding: 18px 40px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: sticky;
      top: 0;
      z-index: 100;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 14px;
    }

    .brand-text h1 {
      font-size: 16px;
      font-weight: 700;
      color: var(--text-main);
      letter-spacing: -0.3px;
    }

    .brand-text p {
      font-size: 12px;
      color: var(--text-muted);
      font-weight: 400;
    }

    .header-info {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .info-pill {
      font-size: 12px;
      font-weight: 600;
      padding: 6px 14px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .info-pill.success {
      background: #eff6ff;
      color: #1d4ed8;
      border: 1px solid #bfdbfe;
    }

    .info-pill.neutral {
      background: #f1f5f9;
      color: #475569;
      border: 1px solid #e2e8f0;
    }

    /* Container Principal */
    main {
      max-width: 1280px;
      width: 100%;
      margin: 0 auto;
      padding: 40px 24px;
      flex: 1;
    }

    /* Hero Card */
    .hero-banner {
      background: var(--surface);
      border: 1px solid var(--surface-border);
      border-left: 4px solid #2563eb;
      border-radius: 12px;
      padding: 28px 32px;
      margin-bottom: 36px;
      box-shadow: var(--shadow-sm);
    }

    .hero-pretitle {
      font-size: 11px;
      font-weight: 800;
      color: #2563eb;
      letter-spacing: 0.8px;
      text-transform: uppercase;
      margin-bottom: 6px;
    }

    .hero-title {
      font-size: 22px;
      font-weight: 800;
      color: var(--text-main);
      margin-bottom: 8px;
      letter-spacing: -0.4px;
    }

    .hero-subtitle {
      font-size: 14px;
      color: var(--text-muted);
      line-height: 1.5;
    }

    /* Grid de Disciplinas */
    .section-title {
      font-size: 18px;
      font-weight: 700;
      color: var(--text-main);
      margin-bottom: 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .search-filter {
      width: 320px;
      padding: 8px 14px;
      border-radius: 8px;
      border: 1px solid var(--surface-border);
      font-size: 13px;
      outline: none;
    }

    .search-filter:focus {
      border-color: #2563eb;
    }

    .disciplines-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
      gap: 24px;
    }

    .disc-card {
      background: var(--surface);
      border: 1px solid var(--surface-border);
      border-radius: 12px;
      padding: 24px;
      box-shadow: var(--shadow-sm);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.2s ease;
    }

    .disc-card:hover {
      box-shadow: var(--shadow-hover);
      border-color: #cbd5e1;
    }

    .disc-top {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 12px;
    }

    .disc-code {
      font-size: 11px;
      font-weight: 800;
      color: var(--text-light);
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .disc-badge {
      font-size: 11px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 6px;
      background: #f1f5f9;
      color: #334155;
    }

    .disc-name {
      font-size: 18px;
      font-weight: 700;
      color: var(--text-main);
      margin-bottom: 6px;
    }

    .disc-desc {
      font-size: 13px;
      color: var(--text-muted);
      line-height: 1.5;
      margin-bottom: 18px;
    }

    .modules-list {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 8px;
      margin-bottom: 20px;
      padding-top: 14px;
      border-top: 1px solid #f1f5f9;
    }

    .module-item {
      font-size: 12px;
      color: #475569;
      text-decoration: none;
      padding: 6px 10px;
      background: #f8fafc;
      border-radius: 6px;
      border: 1px solid #e2e8f0;
      font-weight: 500;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      transition: all 0.15s ease;
    }

    .module-item:hover {
      background: #eff6ff;
      color: #1d4ed8;
      border-color: #bfdbfe;
    }

    .btn-dashboard {
      width: 100%;
      padding: 10px;
      border-radius: 8px;
      background: #0f172a;
      color: #ffffff;
      font-weight: 700;
      font-size: 13px;
      text-align: center;
      text-decoration: none;
      display: block;
      transition: background 0.2s ease;
    }

    .btn-dashboard:hover {
      background: #1e293b;
    }

    footer {
      background: var(--surface);
      border-top: 1px solid var(--surface-border);
      padding: 24px 40px;
      text-align: center;
      font-size: 13px;
      color: var(--text-muted);
    }
  </style>
</head>
<body>
  <!-- Header sobrio original -->
  <header>
    <div class="brand">
      <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="32" height="32" rx="8" fill="#0F172A"/>
        <path d="M8 12C8 9.79086 9.79086 8 12 8H20C22.2091 8 24 9.79086 24 12V20C24 22.2091 22.2091 24 20 24H12C9.79086 24 8 22.2091 8 20V12Z" fill="#2563EB"/>
        <path d="M12 14H20M12 18H17" stroke="white" stroke-width="2" stroke-linecap="round"/>
      </svg>
      <div class="brand-text">
        <h1>Plataforma Corujinha OAB · Portal de Disciplinas</h1>
        <p>Exame de Ordem Unificado (Exames 37 ao 46)</p>
      </div>
    </div>

    <div class="header-info">
      <div class="info-pill success">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
        20 Disciplinas Auditadas
      </div>
      <div class="info-pill neutral">824 Questões Oficiais</div>
    </div>
  </header>

  <main>
    <!-- Hero Banner original -->
    <div class="hero-banner">
      <div class="hero-pretitle">Portal Oficial de Estudos</div>
      <div class="hero-title">Matriz de Disciplinas e Módulos do Exame de Ordem</div>
      <div class="hero-subtitle">
        Estudo sistematizado embasado nas normas formais e materiais aplicadas pela FGV. Selecione a disciplina abaixo para abrir seu Dashboard ou acesse diretamente os Módulos do Curso.
      </div>
    </div>

    <!-- Título da Seção -->
    <div class="section-title">
      <span>Todas as 20 Disciplinas da 1ª Fase OAB</span>
      <input type="text" class="search-filter" id="searchInput" placeholder="Filtrar disciplina (ex: Civil, Penal, Ética...)" onkeyup="filterDisciplines()">
    </div>

    <!-- Grid de Disciplinas -->
    <div class="disciplines-grid" id="discGrid">
"""

for d in disciplines_data:
    html_str += f"""
      <div class="disc-card" data-name="{d['name'].lower()}">
        <div>
          <div class="disc-top">
            <span class="disc-code">{d['code']}</span>
            <span class="disc-badge" style="color: {d['color']};">{d['badge']}</span>
          </div>
          <div class="disc-name">{d['name']}</div>
          <div class="disc-desc">{d['desc']}</div>

          <div class="modules-list">
"""
    for idx, (m_title, m_link) in enumerate(d['modules'], 1):
        html_str += f'            <a class="module-item" href="{m_link}" title="{m_title}">M0{idx}. {m_title}</a>\n'

    html_str += f"""          </div>
        </div>
        <div>
          <a class="btn-dashboard" href="{d['dashboard']}">Abrir Dashboard da Disciplina →</a>
        </div>
      </div>
"""

html_str += """
    </div>
  </main>

  <footer>
    Plataforma Corujinha OAB · Todos os direitos reservados aos materiais didáticos oficiais do Exame de Ordem.
  </footer>

  <script>
    function filterDisciplines() {
      const q = document.getElementById('searchInput').value.toLowerCase();
      const cards = document.querySelectorAll('.disc-card');
      cards.forEach(c => {
        const name = c.getAttribute('data-name');
        if (name.includes(q)) {
          c.style.display = 'flex';
        } else {
          c.style.display = 'none';
        }
      });
    }
  </script>
</body>
</html>
"""

with open(os.path.join(CORUJINHA_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(html_str)

print("✅ Portal Central index.html gerado com SUCESSO utilizando o Design System Oficial (Light/Inter)!")
