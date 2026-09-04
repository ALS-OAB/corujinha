import os
import json
import glob
from collections import defaultdict

SIMULADOS_DIR = '/home/sfy/Jurimetria_OAB/JUR_Jurimetria/simulados'
CORUJINHA_DIR = '/home/sfy/Corujinha'

print("=== RECONSTRUTOR FORENSE MESTRE DE TODAS AS 20 DISCIPLINAS ===")

# 1. Map official exam discipline names to Corujinha folder names
DISCIPLINE_FOLDER_MAP = {
    "Ética Profissional": "ETICA",
    "Direito Constitucional": "CONSTITUCIONAL",
    "Direito Penal": "PENAL",
    "Processo Penal": "PROCESSUAL_PENAL",
    "Direito Administrativo": "ADMINISTRATIVO",
    "Direito Tributário": "TRIBUTARIO",
    "Direito do Trabalho": "TRABALHISTA",
    "Processo do Trabalho": "PROCESSUAL_TRABALHISTA",
    "Direito Empresarial": "EMPRESARIAL",
    "Processo Civil": "CPC",
    "Direito Civil": "CIVIL",
    "Filosofia do Direito": "FILOSOFIA",
    "Direito Internacional": "INTERNACIONAL",
    "Direitos Humanos": "DIREITOS_HUMANOS",
    "Direito Ambiental": "AMBIENTAL",
    "Estatuto da Criança e do Adolescente (ECA)": "ECA",
    "Direito do Consumidor": "CONSUMIDOR",
    "Direito Eleitoral": "ELEITORAL",
    "Direito Financeiro": "FINANCEIRO",
    "Direito Previdenciário": "PREVIDENCIARIO",
}

# Sub-module definition rules per discipline
# Each discipline has 8 canonical modules
MODULE_SCHEMAS = {
    "ETICA": [
        ("01_orgaos_da_oab", "Órgãos da OAB"),
        ("02_direitos_e_prerrogativas", "Direitos e Prerrogativas"),
        ("03_incompatibilidade_e_impedimento", "Incompatibilidades e Impedimentos"),
        ("04_infracoes_e_sancoes", "Infrações e Sanções Disciplinares"),
        ("05_publicidade_e_honorarios", "Honorários Advocatícios"),
        ("06_publicidade_e_marketing", "Publicidade e Marketing"),
        ("07_advogados_e_estagiarios", "Atividades de Advocacia e Estágio"),
        ("08_processo_administrativo_e_eleitoral", "Processo Disciplinar e Eleitoral"),
    ],
    "CONSTITUCIONAL": [
        ("01_direitos_fundamentais", "Direitos e Garantias Fundamentais"),
        ("02_organizacao_estado", "Organização do Estado e Repartição de Competências"),
        ("03_poder_legislativo", "Poder Legislativo e Processo Legislativo"),
        ("04_poder_executivo", "Poder Executivo e Presidência da República"),
        ("05_poder_judiciario", "Poder Judiciário e Súmulas Vinculantes"),
        ("06_controle_constitucionalidade", "Controle de Constitucionalidade (ADI, ADC, ADPF)"),
        ("07_defesa_estado", "Defesa do Estado e das Instituições Democráticas"),
        ("08_ordem_social_economica", "Ordem Social e Econômica"),
    ],
    "ADMINISTRATIVO": [
        ("01_organizacao_administrativa", "Organização Administrativa e Administração Indireta"),
        ("02_principios_poderes", "Princípios e Poderes da Administração Pública"),
        ("03_atos_administrativos", "Atos Administrativos"),
        ("04_licitacoes_contratos", "Licitações e Contratos Administrativos (Lei nº 14.133/21)"),
        ("05_servicos_publicos", "Serviços Públicos e Concessões"),
        ("06_agentes_improbidade", "Agentes Públicos e Improbidade Administrativa"),
        ("07_intervencao_propriedade", "Intervenção do Estado na Propriedade e Desapropriação"),
        ("08_responsabilidade_processo", "Responsabilidade Civil do Estado e Processo Administrativo"),
    ],
    "PENAL": [
        ("01_teoria_geral_crime", "Teoria Geral do Crime e Aplicação da Lei Penal"),
        ("02_ilicitude_culpabilidade", "Ilicitude, Culpabilidade e Erro"),
        ("03_punibilidade_penas", "Teoria das Penas e Extinção da Punibilidade"),
        ("04_crimes_contra_vida", "Crimes contra a Pessoa e contra a Vida"),
        ("05_crimes_contra_patrimonio", "Crimes contra o Patrimônio"),
        ("06_crimes_dignidade_sexual", "Crimes contra a Dignidade Sexual"),
        ("07_crimes_administracao", "Crimes contra a Administração Pública"),
        ("08_concurso_agentes", "Concurso de Pessoas e Concurso de Crimes"),
    ],
    "PROCESSUAL_PENAL": [
        ("01_inquerito_acao_penal", "Inquérito Policial e Ação Penal"),
        ("02_competencia_jurisdicao", "Jurisdição e Competência Processual Penal"),
        ("03_prisao_cautelares", "Prisão, Liberdade Provisória e Medidas Cautelares"),
        ("04_provas_processo_penal", "Provas e Cadeia de Custódia"),
        ("05_procedimentos_penais", "Procedimento Comum e Tribunal do Júri"),
        ("06_nulidades_decisoes", "Nulidades e Sentença Penal"),
        ("07_recursos_penais", "Recursos em Espécie e Ações Autônomas de Impugnação"),
        ("08_juizado_especial", "Juizados Especiais Criminais e Execução Penal"),
    ],
    "TRABALHISTA": [
        ("01_contrato_trabalho", "Contrato Individual de Trabalho e Alterações"),
        ("02_jornada_remuneracao", "Jornada de Trabalho e Duração do Trabalho"),
        ("03_ferias_salario", "Remuneração, Salário e Férias"),
        ("04_rescisao_contrato", "Cessação do Contrato de Trabalho e Verbas Rescisórias"),
        ("05_estabilidades_garantias", "Estabilidades Provisórias e Garantias no Emprego"),
        ("06_organizacao_sindical", "Direito Coletivo do Trabalho e Organização Sindical"),
        ("07_saude_seguranca", "Segurança, Saúde no Trabalho e Insalubridade/Periculosidade"),
        ("08_previdencia_beneficios", "FGTS e Benefícios Trabalhistas"),
    ],
    "PROCESSUAL_TRABALHISTA": [
        ("01_organizacao_justica", "Organização da Justiça do Trabalho e Competência"),
        ("02_reclamacao_trabalhista", "Petições, Atos e Resposta do Reclamado"),
        ("03_provas_pericia", "Provas, Audiência e Perícia Trabalhista"),
        ("04_recursos_trabalhistas", "Recursos Trabalhistas (RO, RR, Agravo)"),
        ("05_execucao_trabalhista", "Execução Trabalhista e Embargos"),
        ("06_acoes_especiais", "Procedimento Sumaríssimo e Ações Especiais"),
        ("07_cautela_inquerito", "Procedimentos Especiais e Inquérito"),
        ("08_rito_sumarissimo", "Custas, Sucumbência e Justiça Gratuita"),
    ],
    "TRIBUTARIO": [
        ("01_sistema_tributario", "Sistema Tributário Nacional e Princípios Constitutional-Tributários"),
        ("02_obrigacao_tributaria", "Obrigação Tributária e Fato Gerador"),
        ("03_credito_tributario", "Lançamento, Crédito Tributário, Suspensão e Extinção"),
        ("04_impostos_uniao", "Impostos da União (IR, IPI, II, IE, ITR)"),
        ("05_impostos_estados", "Impostos dos Estados e Municípios (ICMS, IPVA, ITCMD, IPTU, ISS)"),
        ("06_responsabilidade_tributaria", "Responsabilidade Tributária e Substituição"),
        ("07_administracao_tributaria", "Fiscalização, Certidões e Dívida Ativa"),
        ("08_execucao_fiscal", "Processo Judicial Tributário e Execução Fiscal"),
    ],
    "EMPRESARIAL": [
        ("01_empresario_sociedades", "Teoria Geral da Empresa e Sociedades Personificadas"),
        ("02_estabelecimento_nome", "Estabelecimento Empresarial e Nome Empresarial"),
        ("03_titulos_credito", "Títulos de Crédito (Cheque, Duplicata, Nota Promissória)"),
        ("04_contratos_empresariais", "Contratos Empresariais e Bancários"),
        ("05_sociedade_anonima", "Sociedades por Ações (S/A)"),
        ("06_falencia_recuperacao", "Recuperação Judicial e Falência (Lei nº 11.101/05)"),
        ("07_direito_consumidor", "Concorrência e Propriedade Industrial"),
        ("08_propriedade_intelectual", "Propriedade Intelectual e Marcas"),
    ],
    "CPC": [
        ("01_principios_normas", "Princípios Processuais e Normas Fundamentais do CPC"),
        ("02_jurisdicao_competencia", "Jurisdição, Competência e Sujeitos do Processo"),
        ("03_peticao_inicial_tutelas", "Petição Inicial e Tutelas Provisórias"),
        ("04_contestacao_resposta", "Resposta do Réu, Contestação e Reconvenção"),
        ("05_provas_sentenca", "Instrução Probatória e Sentença"),
        ("06_recursos_civeis", "Recursos Cíveis (Apelação, Agravo, Embargos)"),
        ("07_execucao_cumprimento", "Cumprimento de Sentença e Processo de Execução"),
        ("08_procedimentos_especiais", "Procedimentos Especiais e Juizados Especiais Cíveis"),
    ],
    "CIVIL": [
        ("01_parte_geral", "Parte Geral e LINDB"),
        ("02_negocio_juridico", "Fatos e Negócios Jurídicos"),
        ("03_obrigacoes", "Teoria Geral das Obrigações"),
        ("04_contratos", "Contratos em Geral e Espécies"),
        ("05_responsabilidade_civil", "Responsabilidade Civil"),
        ("06_direitos_reais", "Direitos Reais e Posse"),
        ("07_direito_de_familia", "Direito de Família"),
        ("08_direito_das_sucessoes", "Direito das Sucessões"),
    ],
    "AMBIENTAL": [
        ("01_principios_constitucional", "Princípios de Direito Ambiental e Proteção Constitucional"),
        ("02_pnma_sisnama", "Política Nacional do Meio Ambiente e SISNAMA"),
        ("03_licenciamento_eia", "Licenciamento Ambiental e Estudo de Impacto (EIA/RIMA)"),
        ("04_responsabilidade_dano", "Responsabilidade por Danos Ambientais (Civil, Adm e Penal)"),
        ("05_codigo_florestal_app", "Código Florestal, APP e Reserva Legal"),
        ("06_unidades_conservacao", "Unidades de Conservação (SNUC)"),
        ("07_recursos_hidricos_residuos", "Recursos Hídricos e Resíduos Sólidos"),
        ("08_crimes_ambientais", "Crimes Ambientais (Lei nº 9.605/98)"),
    ],
    "CONSUMIDOR": [
        ("01_relacao_consumo", "Conceito de Consumidor, Fornecedor e Relação de Consumo"),
        ("02_direitos_basicos", "Direitos Básicos do Consumidor"),
        ("03_fato_vicio_produto", "Responsabilidade pelo Fato e Vício do Produto/Serviço"),
        ("04_praticas_comerciais", "Práticas Comerciais, Oferta e Publicidade"),
        ("05_protecao_contratual", "Proteção Contratual e Cláusulas Abusivas"),
        ("06_superendividamento", "Prevenção ao Superendividamento"),
        ("07_bancos_dados_cadastros", "Bancos de Dados, Cadastros de Consumidores e SPC/Serasa"),
        ("08_defesa_coletiva", "Defesa do Consumidor em Juízo e Ações Coletivas"),
    ],
    "ECA": [
        ("01_doutrina_protecao", "Doutrina da Proteção Integral e Direitos Fundamentais da Criança"),
        ("02_direito_convivencia", "Direito à Convivência Familiar e Comunitária (Guarda, Tutela, Adoção)"),
        ("03_autorizacao_viagem", "Autorização para Viajar e Prevenção"),
        ("04_atos_infracionais", "Atos Infracionais e Responsabilidade do Adolescente"),
        ("05_medidas_socioeducativas", "Medidas Socioeducativas e Internação"),
        ("06_medidas_protecao", "Medidas de Proteção e Conselhos Tutelares"),
        ("07_crimes_infracoes_adm", "Crimes e Infrações Administrativas contra a Criança"),
        ("08_justica_infancia", "Justiça da Infância e da Juventude e Procedimentos"),
    ],
    "DIREITOS_HUMANOS": [
        ("01_teoria_geral_dh", "Teoria Geral dos Direitos Humanos e Afirmação Histórica"),
        ("02_sistema_interamericano", "Sistema Interamericano de Direitos Humanos (CADH / Pacto de San José)"),
        ("03_corte_interamericana", "Corte Interamericana e Comissão Interamericana"),
        ("04_declaracao_universal", "Declaração Universal dos Direitos Humanos (DUDH)"),
        ("05_protecao_minorias", "Proteção aos Grupos Vulneráveis e Minorias"),
        ("06_mecanismos_nacionais", "Mecanismos Nacionais de Proteção aos Direitos Humanos"),
        ("07_tratados_internacionais", "Tratados Internacionais na Constituição Federal (Art. 5º, §3º)"),
        ("08_combate_discriminacao", "Combate ao Preconceito, Discriminação e Violência"),
    ],
    "INTERNACIONAL": [
        ("01_lindb_conflito_leis", "LINDB e Conflito de Leis no Espaço"),
        ("02_nacionalidade_estrangeiro", "Nacionalidade, Condição Jurídica do Estrangeiro e Lei de Migração"),
        ("03_extradicao_expulsao", "Extradição, Expulsão e Deportação"),
        ("04_cooperacao_juridica", "Cooperação Jurídica Internacional e Cartas Rogatórias"),
        ("05_homologacao_sentenca", "Homologação de Decisões Estrangeiras pelo STJ"),
        ("06_contratos_internacionais", "Contratos Internacionais e Comércio Exterior"),
        ("07_sujeitos_dip", "Sujeitos de Direito Internacional Público e Organizações"),
        ("08_tratados_imunidades", "Tratados Internacionais e Imunidade de Jurisdição"),
    ],
    "FILOSOFIA": [
        ("01_jusnaturalismo_positivismo", "Jusnaturalismo vs. Positivismo Jurídico"),
        ("02_teoria_pura_kelsen", "Teoria Pura do Direito (Hans Kelsen)"),
        ("03_pospositivismo_dworkin", "Pós-Positivismo, Princípios e Regras (Ronald Dworkin)"),
        ("04_hermeneutica_argumentacao", "Hermenêutica Jurídica e Teoria da Argumentação"),
        ("05_teorias_justica", "Teorias da Justiça (John Rawls, Aristóteles)"),
        ("06_conceito_direito_hart", "O Conceito de Direito (H.L.A. Hart)"),
        ("07_sociologia_efetividade", "Sociologia do Direito e Efetividade das Normas"),
        ("08_etica_utilitarismo", "Ética Jurídica, Moral e Utilitarismo"),
    ],
    "FINANCEIRO": [
        ("01_ppa_ldo_loa", "Planejamento Orçamentário: PPA, LDO e LOA"),
        ("02_principios_orcamentarios", "Princípios Orçamentários"),
        ("03_receita_publica", "Receita Pública e Estágios da Receita"),
        ("04_despesa_publica", "Despesa Pública e Empenho"),
        ("05_creditos_adicionais", "Créditos Adicionais (Suplementares, Especiais, Extraordinários)"),
        ("06_lrf_responsabilidade", "Lei de Responsabilidade Fiscal (LRF - LC nº 101/00)"),
        ("07_precatorios_divida", "Precatórios Judiciais e Dívida Pública"),
        ("08_fiscalizacao_tribunal", "Fiscalização Financeira e Tribunal de Contas"),
    ],
    "ELEITORAL": [
        ("01_principios_justica", "Princípios de Direito Eleitoral e Justiça Eleitoral"),
        ("02_direitos_politicos", "Direitos Políticos (Alistamento e Votação)"),
        ("03_elegibilidade_inelegibilidades", "Elegibilidade e Inelegibilidades (LC nº 64/90)"),
        ("04_partidos_federacoes", "Partidos Políticos e Federações Partidárias"),
        ("05_propaganda_eleitoral", "Propaganda Eleitoral e Direito de Resposta"),
        ("06_financiamento_contas", "Financiamento de Campanha e Prestação de Contas"),
        ("07_acoes_eleitorais", "Ações Eleitorais (AIJE, AIME, Representações)"),
        ("08_crimes_eleitorais", "Crimes Eleitorais e Processo Penal Eleitoral"),
    ],
    "PREVIDENCIARIO": [
        ("01_seguridade_social", "Seguridade Social: Saúde, Assistência e Previdência"),
        ("02_segurados_rgps", "Segurados do RGPS (Obrigatórios e Facultativos)"),
        ("03_financiamento_contribuicoes", "Financiamento da Seguridade Social e Contribuições"),
        ("04_carencia_qualidade", "Carência e Manutenção/Perda da Qualidade de Segurado"),
        ("05_aposentadorias_incapacidade", "Aposentadorias e Benefícios por Incapacidade"),
        ("06_pensao_morte_auxilios", "Pensão por Morte, Auxílio-Reclusão e Salário-Família"),
        ("07_reforma_ec103", "Regras de Transição da Reforma Previdenciária (EC nº 103/19)"),
        ("08_processo_previdenciario", "Processo Administrativo e Judicial Previdenciário"),
    ]
}

# Load official exam master questions
master_questions_by_folder = defaultdict(list)

for sf in sorted(glob.glob(os.path.join(SIMULADOS_DIR, 'e*_tipo1_branca.json'))):
    exame_num = int(os.path.basename(sf).split('e')[1].split('_')[0])
    exame_label = f"{exame_num}º Exame OAB"
    with open(sf, 'r', encoding='utf-8') as f:
        items = json.load(f)
    for item in items:
        disc = item.get('disciplina', '')
        # Handle exceptions / non-civil purges that were corrected
        # If question is environmental (logistica reversa/APP), force AMBIENTAL
        txt = (item.get('enunciado', '') + ' ' + item.get('tema', '')).lower()
        if 'resíduos sólidos' in txt or 'logística reversa' in txt or 'lei nº 12.305' in txt or 'supressão de vegetação nativa em área de preservação permanente' in txt:
            disc = "Direito Ambiental"
            
        folder_target = DISCIPLINE_FOLDER_MAP.get(disc)
        if folder_target:
            item['exame_num'] = exame_num
            item['exame_label'] = exame_label
            item['exame'] = exame_label
            item['disciplina'] = disc
            master_questions_by_folder[folder_target].append(item)

print("\n--- RESUMO DE RECOLHIMENTO DAS QUESTÕES OFICIAIS ---")
total_rebuilt = 0
for folder_name, qlist in master_questions_by_folder.items():
    print(f"📦 Disciplina: {folder_name:<22} | Questões oficiais: {len(qlist):3d}")
    total_rebuilt += len(qlist)

print(f"\nTotal Geral de Questões Oficiais Agrupadas: {total_rebuilt}\n")

# Now re-build the sub-module JSON files for each discipline folder
for folder_name, qlist in master_questions_by_folder.items():
    folder_path = os.path.join(CORUJINHA_DIR, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    
    # Get module definitions for this discipline
    schema_modules = MODULE_SCHEMAS.get(folder_name, [("01_geral", "Geral")])
    num_modules = len(schema_modules)
    
    # Clean up any misplaced/extraneous json files in the folder (like administrative files in Penal)
    allowed_filenames = [f"{prefix}_questoes.json" for prefix, _ in schema_modules]
    for existing_file in glob.glob(os.path.join(folder_path, '*_questoes.json')):
        if os.path.basename(existing_file) not in allowed_filenames:
            os.remove(existing_file)
            print(f"  🗑️ Removido arquivo incorreto/excedente: {folder_name}/{os.path.basename(existing_file)}")
            
    # Partition questions fairly across the 8 modules based on exam sequence and count
    qlist.sort(key=lambda x: (x.get('exame_num', 0), x.get('num', 0)))
    
    # Group questions into modules
    module_buckets = defaultdict(list)
    for idx, q in enumerate(qlist):
        mod_idx = idx % num_modules
        mod_prefix, mod_title = schema_modules[mod_idx]
        q['modulo_codigo'] = mod_prefix
        q['modulo_nome'] = mod_title
        module_buckets[mod_prefix].append(q)
        
    # Write each module JSON file
    for mod_prefix, mod_title in schema_modules:
        bucket_qs = module_buckets[mod_prefix]
        bucket_qs.sort(key=lambda x: (x.get('exame_num', 0), x.get('num', 0)))
        
        # Renumber sequence in file
        for i, item in enumerate(bucket_qs, 1):
            item['id'] = i
            
        out_file = os.path.join(folder_path, f"{mod_prefix}_questoes.json")
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(bucket_qs, f, ensure_ascii=False, indent=2)

print("🎉 RECONSTRUÇÃO FORENSE DE TODAS AS 20 DISCIPLINAS FINALIZADA COM SUCESSO!")
