import os
import json
import glob

CIVIL_DIR = '/home/sfy/Corujinha/CIVIL'

# 1. Load all current questions across the 8 JSON files
files = sorted(glob.glob(os.path.join(CIVIL_DIR, '*_questoes.json')))
all_questions = []

for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        items = json.load(f)
        all_questions.extend(items)

print(f"Total de questões lidas: {len(all_questions)}")

# 2. Strict taxonomy mapping based on exact scenario analysis
# We map each question by identifying key terms in its text/ID/exame

def classify_question_exact(q):
    txt = (q.get('enunciado', '') + ' ' + q.get('tema', '')).lower()
    exame = q.get('exame', '')
    
    # --- PURGE NON-CIVIL ---
    # Q1 de E37 (Empresa Alfa - resíduos sólidos / logística reversa / Lei 12.305/2010 -> DIREITO AMBIENTAL)
    if 'resíduos sólidos' in txt or 'logística reversa' in txt or 'lei nº 12.305' in txt or 'pilhas e baterias' in txt:
        return None, 'Direito Ambiental'

    # --- DIREITO DAS SUCESSÕES (Apenas herança, testamento, cota hereditária, inventário e indignidade sucessória) ---
    # Maria Cristina (38º) - Direito Real de Habitação
    if 'maria cristina era casada com roberto' in txt:
        return '08_direito_das_sucessoes', 'Direito das Sucessões'
    # Os irmãos Eduardo e Letícia herdaram um apartamento (38º)
    if 'eduardo e letícia herdaram um apartamento' in txt:
        return '08_direito_das_sucessoes', 'Direito das Sucessões'
    # João viúvo pai de Marcela e Tatiana (41º) - Renúncia de herança e credores
    if 'marcela e tatiana' in txt:
        return '08_direito_das_sucessoes', 'Direito das Sucessões'
    # Testamento deixado por Natália (44º) - Substituição testamentária
    if 'lego o apartamento x para meus filhos' in txt:
        return '08_direito_das_sucessoes', 'Direito das Sucessões'
    # Mateus e Pedro adquiriram um veículo (45º) - Devedores solidários / herdeiros
    if 'mateus e pedro adquiriram um veículo de joana' in txt:
        return '08_direito_das_sucessoes', 'Direito das Sucessões'
    # Gustavo viúvo pai de Heitor e Gabriela (45º) - Doação / dispensa de colação
    if 'gustavo, viúvo, é pai de heitor e gabriela' in txt:
        return '08_direito_das_sucessoes', 'Direito das Sucessões'
    # Lucas desferiu golpes fatais em seus pais (46º) - Exclusão por Indignidade / MP
    if 'lucas desferiu golpes fatais em seus pais' in txt:
        return '08_direito_das_sucessoes', 'Direito das Sucessões'

    # --- DIREITO DE FAMÍLIA ---
    # Pedro e Joana casados comunhão parcial herdou ações (37º)
    if 'pedro e joana casaram-se pelo regime da comunhão parcial' in txt:
        return '07_direito_de_familia', 'Direito de Família'
    # Mariana e Lucas casados comunhão parcial (40º)
    if 'mariana e lucas estão casados há mais de 10 anos' in txt:
        return '07_direito_de_familia', 'Direito de Família'
    # Vitória e Rodrigo casados (40º) - Alimentos / Guarda
    if 'vitória e rodrigo foram casados' in txt:
        return '07_direito_de_familia', 'Direito de Família'
    # Natália ajuizou ação declaratória de filiação (41º)
    if 'ajuizou ação declaratória de filiação' in txt:
        return '07_direito_de_familia', 'Direito de Família'
    # Júlio Cesar e Thayane casados (39º) - Guarda compartilhada e Alimentos
    if 'júlio cesar e thayane' in txt:
        return '07_direito_de_familia', 'Direito de Família'
    # Priscila e Lucas (42º) - Maioridade e Alimentos
    if 'priscila e lucas tiveram filhos muito cedo' in txt:
        return '07_direito_de_familia', 'Direito de Família'
    # Paulo e Glória união estável (43º) - Regime de bens / Concorrência
    if 'paulo e glória mantiveram união estável' in txt:
        return '07_direito_de_familia', 'Direito de Família'
    # Fabiano e Vitória comunhão parcial (43º)
    if 'fabiano e vitória, casados pelo regime de comunhão parcial' in txt:
        return '07_direito_de_familia', 'Direito de Família'
    # Beatriz nasceu 250 dias após morte (44º) - Presunção de Paternidade
    if 'beatriz nasceu duzentos e cinquenta dias' in txt:
        return '07_direito_de_familia', 'Direito de Família'
    # Gabriel e Vitória faleceu acidente aéreo (44º) - Tutela dos menores
    if 'gabriel e vitória, pais de ana e de clara' in txt:
        return '07_direito_de_familia', 'Direito de Família'
    # Joaquim 71 anos viúvo sem partilha (46º) - Regime Obrigatorio
    if 'joaquim, de 71 anos de idade, é viúvo' in txt:
        return '07_direito_de_familia', 'Direito de Família'

    # --- DIREITOS REAIS ---
    # Waldo e Tadeu (37º) - Usufruto / Posse
    if 'waldo é titular de vultoso patrimônio' in txt:
        return '06_direitos_reais', 'Direitos Reais'
    # Antônio prédio encravado (38º) - Passagem Forçada / Servidão
    if 'antônio é proprietário de um prédio que não tem acesso' in txt:
        return '06_direitos_reais', 'Direitos Reais'
    # Vítor empréstimo hipoteca (39º) - Hipoteca / Garantia Real
    if 'vítor contraiu empréstimo perante uma instituição bancária' in txt:
        return '06_direitos_reais', 'Direitos Reais'
    # Joana doméstica usucapião (40º) - Usucapião Urbana
    if 'joana trabalhou por 15 anos como empregada doméstica' in txt:
        return '06_direitos_reais', 'Direitos Reais'
    # João concessão de direito de superfície a Paula (41º) - Superfície
    if 'concedeu a paula o direito de' in txt or 'joão é proprietário de um terreno' in txt:
        return '06_direitos_reais', 'Direitos Reais'
    # Bruno APP vegetação (42º) - Propriedade / Função Social
    if 'bruno pretende realizar supressão de vegetação' in txt:
        return '06_direitos_reais', 'Direitos Reais'
    # Mariana e Manuela locação imóvel (42º) - Posse / Usufruto
    if 'mariana e manuela celebraram contrato escrito' in txt:
        return '06_direitos_reais', 'Direitos Reais'
    # Brás Cubas possuidor (42º) - Usucapião / Posse
    if 'brás cubas procurou você' in txt:
        return '06_direitos_reais', 'Direitos Reais'
    # Cláudia devedora penhora carro (44º) - Penhor / Comodato
    if 'cláudia é devedora de valores elevados' in txt:
        return '06_direitos_reais', 'Direitos Reais'
    # Carlos direito real de laje (44º) - Direito Real de Laje
    if 'carlos é titular de direito real de uma laje' in txt:
        return '06_direitos_reais', 'Direitos Reais'
    # Ruth Sítio Felicidade canos (45º) - Servidão / Vizinhança
    if 'ruth é proprietária do sítio felicidade' in txt:
        return '06_direitos_reais', 'Direitos Reais'

    # --- RESPONSABILIDADE CIVIL ---
    # Henrique médico Nicola cirurgia (37º)
    if 'henrique, 50 anos, médico dermatologista' in txt:
        return '05_responsabilidade_civil', 'Responsabilidade Civil'
    # Luan colidiu veículo (39º) - Acidente / Danos
    if 'luan, conduzindo seu automóvel em velocidade' in txt:
        return '05_responsabilidade_civil', 'Responsabilidade Civil'
    # Mário desvio poste (43º) - Estado de Necessidade e Regresso
    if 'mário conduzia imprudentemente seu veículo' in txt:
        return '05_responsabilidade_civil', 'Responsabilidade Civil'
    # Ariano carona João (45º) - Carona simples / Transporte benévolo
    if 'ariano ofereceu carona' in txt:
        return '05_responsabilidade_civil', 'Responsabilidade Civil'
    # Farmácia Vida+ vazamento de dados (45º) - Danos morais / LGPD
    if 'farmácia vida+' in txt:
        return '05_responsabilidade_civil', 'Responsabilidade Civil'

    # --- CONTRATOS EM GERAL E ESPÉCIES ---
    # Nicolas servidor TJSP doação bisneto (39º)
    if 'nicolas, servidor do tribunal de justiça' in txt:
        return '04_contratos', 'Contratos em Geral e Espécies'
    # Renata Tadeu Luzia fiadora (38º) - Fiança
    if 'renata exigiu a indicação de um fiador' in txt or 'luzia, fiadora' in txt:
        return '04_contratos', 'Contratos em Geral e Espécies'
    # Ana comprou carro Miguel sinal/arras (38º)
    if 'ana comprou de miguel' in txt or 'sinal equivalente' in txt:
        return '04_contratos', 'Contratos em Geral e Espécies'
    # Lúcia Cristina inadimplemento sinal (39º)
    if 'lúcia vendeu' in txt or 'cristina comprou' in txt:
        return '04_contratos', 'Contratos em Geral e Espécies'
    # Aluísio Fábio Letícia hipoteca bem de terceiro (41º)
    if 'letícia ofereceu em garantia' in txt or 'aluísio emprestou a fábio' in txt:
        return '04_contratos', 'Contratos em Geral e Espécies'
    # Cláudia arquiteto Lúcio prestação serviços (41º)
    if 'cláudia contratou o arquiteto lúcio' in txt:
        return '04_contratos', 'Contratos em Geral e Espécies'
    # Dagoberto compromisso compra e venda (43º)
    if 'dagoberto celebrou contrato' in txt:
        return '04_contratos', 'Contratos em Geral e Espécies'
    # Lorena Marta comissão corretagem (46º)
    if 'lorena alienou imóvel' in txt or 'comissão de corretagem' in txt:
        return '04_contratos', 'Contratos em Geral e Espécies'
    # Eduardo Clara escritura pública RI (46º)
    if 'eduardo vendeu imóvel a clara' in txt:
        return '04_contratos', 'Contratos em Geral e Espécies'
    # Marcelo alugou cavalo haras (39º)
    if 'marcelo alugou um cavalo' in txt:
        return '04_contratos', 'Contratos em Geral e Espécies'
    # André comprou carro vício redibitório (40º)
    if 'andré, mediante contrato escrito, comprou o carro' in txt:
        return '04_contratos', 'Contratos em Geral e Espécies'
    # Antônio locatário infiltração (40º)
    if 'antônio, locatário de um imóvel residencial' in txt:
        return '04_contratos', 'Contratos em Geral e Espécies'
    # Joana contratou Maria fotógrafa (37º)
    if 'joana contratou maria para fotografar' in txt:
        return '04_contratos', 'Contratos em Geral e Espécies'

    # --- TEORIA GERAL DAS OBRIGAÇÕES ---
    # Joaquim restaurante engasga (40º) - Gestão de negócios / Obrigações
    if 'joaquim' in txt and 'restaurante' in txt:
        return '03_obrigacoes', 'Teoria Geral das Obrigações'
    # Adriana fisioterapeuta (41º) - Prescrição
    if 'adriana' in txt and 'fisioterapeuta' in txt:
        return '03_obrigacoes', 'Teoria Geral das Obrigações'

    # --- FATOS E NEGÓCIOS JURÍDICOS (02) / PARTE GERAL (01) ---
    # Robson advogado preso incapaz (38º)
    if 'robson, advogado de sucesso' in txt:
        return '01_parte_geral', 'Parte Geral e LINDB'
    if 'capacidade' in txt or 'emancip' in txt or 'personalidade' in txt:
        return '01_parte_geral', 'Parte Geral e LINDB'
    if 'erro' in txt or 'dolo' in txt or 'coação' in txt or 'simulação' in txt or 'lesão' in txt:
        return '02_negocio_juridico', 'Fatos e Negócios Jurídicos'

    return '01_parte_geral', 'Parte Geral e LINDB'


# Categorize into lists
categorized = {
    '01_parte_geral': [],
    '02_negocio_juridico': [],
    '03_obrigacoes': [],
    '04_contratos': [],
    '05_responsabilidade_civil': [],
    '06_direitos_reais': [],
    '07_direito_de_familia': [],
    '08_direito_das_sucessoes': []
}

purged_count = 0
seen_ids = set()

for q in all_questions:
    # Deduplicate by unique key (exame + num + enunciado snippet)
    unique_key = f"{q.get('exame')}_{q.get('num')}_{q.get('enunciado')[:30]}"
    if unique_key in seen_ids:
        continue
    seen_ids.add(unique_key)
    
    mod_code, mod_name = classify_question_exact(q)
    if mod_code is None:
        print(f"🗑️ EXPURGADA (NÃO-CIVIL): Exame {q.get('exame')} Q{q.get('num')} - Enunciado: {q.get('enunciado')[:80]}...")
        purged_count += 1
    else:
        q['disciplina'] = 'Direito Civil'
        q['modulo_codigo'] = mod_code
        q['modulo_nome'] = mod_name
        categorized[mod_code].append(q)

print(f"\nExpurgadas {purged_count} questões não-cíveis do acervo.")

# Save updated JSONs
for mod_code, qlist in categorized.items():
    # Sort by exame number and question number
    qlist.sort(key=lambda x: (x.get('exame_num', 0), x.get('num', 0)))
    
    # Re-number sequence in file
    for idx, q in enumerate(qlist, 1):
        q['id'] = idx
        
    out_path = os.path.join(CIVIL_DIR, f"{mod_code}_questoes.json")
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(qlist, f, ensure_ascii=False, indent=2)
    print(f"💾 {mod_code}_questoes.json: {len(qlist)} questões cíveis gravadas.")

print("\nReorganização forense completa com sucesso!")
