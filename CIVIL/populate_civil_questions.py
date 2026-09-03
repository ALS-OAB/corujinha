import os
import json
import glob
import re

# Paths
SIMULADOS_DIR = '/home/sfy/Jurimetria_OAB/JUR_Jurimetria/simulados'
CIVIL_DIR = '/home/sfy/Corujinha/CIVIL'

files = sorted(glob.glob(os.path.join(SIMULADOS_DIR, 'e*_tipo1_branca.json')))

print(f"Encontrados {len(files)} arquivos de simulados dos exames.")

civil_questions = []
for fpath in files:
    filename = os.path.basename(fpath)
    exame_num = filename.split('e')[1].split('_')[0]
    exame_label = f"{exame_num}º Exame OAB"
    
    with open(fpath, 'r', encoding='utf-8') as fp:
        items = json.load(fp)
        for item in items:
            disc = item.get('disciplina', '')
            num = item.get('num', 0)
            # Identify Civil questions
            if disc == 'Direito Civil' or (disc == '' and 35 <= num <= 42):
                item['exame_label'] = exame_label
                item['exame_num'] = int(exame_num)
                civil_questions.append(item)

print(f"Total de questões de Direito Civil extraídas: {len(civil_questions)}")

# Categorization mapping based on legal themes
def classify_question(q):
    text = (q.get('enunciado', '') + ' ' + q.get('tema', '')).lower()
    
    # 08. Sucessões
    if any(k in text for k in ['herança', 'testamento', 'sucess', 'herdeir', 'legado', 'indign', 'deserda', 'inventári', 'partilha', 'faleceram', 'falecido', 'falecimento', 'deixando filhos', 'morte de']):
        return '08_direito_das_sucessoes', 'Direito das Sucessões'
    # 07. Família
    elif any(k in text for k in ['casad', 'casam', 'divórci', 'cônjuge', 'união estável', 'alimentos', 'pátrio poder', 'poder familiar', 'regime de bens', 'comunhão de bens', 'divórcio']):
        return '07_direito_de_familia', 'Direito de Família'
    # 06. Direitos Reais
    elif any(k in text for k in ['posse', 'usucapi', 'propriedade', 'hipoteca', 'penhor', 'servidão', 'usufruto', 'laje', 'vizinhança', 'direitos reais', 'imóvel sem acesso', 'terreno']):
        return '06_direitos_reais', 'Direitos Reais'
    # 05. Responsabilidade Civil
    elif any(k in text for k in ['dano', 'indeniz', 'responsab', 'imprudênc', 'negligênc', 'colidiu', 'acidente', 'causou prejuízo', 'nexo de causalidade', 'atropelamento']):
        return '05_responsabilidade_civil', 'Responsabilidade Civil'
    # 04. Contratos
    elif any(k in text for k in ['contrato', 'locaç', 'alug', 'fiança', 'compra e venda', 'comprou de', 'vender para', 'doaç', 'empréstimo', 'comodato', 'mútuo', 'arrendamento']):
        return '04_contratos', 'Direito dos Contratos'
    # 03. Obrigações
    elif any(k in text for k in ['obrigaç', 'devedor', 'credor', 'solidári', 'pagamento', 'inadimpl', 'mora', 'cláusula penal', 'prestação']):
        return '03_obrigacoes', 'Teoria Geral das Obrigações'
    # 02. Negócio Jurídico / Defeitos / Prescrição
    elif any(k in text for k in ['negócio jurídico', 'anula', 'nulidade', 'erro', 'dolo', 'coaç', 'lesão', 'estado de perigo', 'simulaç', 'fraude contra credores', 'prescriç', 'decadênc', 'procuração']):
        return '02_negocio_juridico', 'Fatos e Negócios Jurídicos'
    # 01. Parte Geral / Pessoas
    else:
        return '01_parte_geral', 'Parte Geral e Pessoa Civil'

modules_data = {
    '01_parte_geral': [],
    '02_negocio_juridico': [],
    '03_obrigacoes': [],
    '04_contratos': [],
    '05_responsabilidade_civil': [],
    '06_direitos_reais': [],
    '07_direito_de_familia': [],
    '08_direito_das_sucessoes': []
}

for q in civil_questions:
    mod_prefix, default_theme = classify_question(q)
    
    # Format options dictionary
    opts = q.get('alternativas', q.get('opcoes', {}))
    if isinstance(opts, list):
        # Array of strings
        opts_dict = {}
        for idx, opt_str in enumerate(opts):
            letter = chr(65 + idx)
            opts_dict[letter] = opt_str
        opts = opts_dict
    
    # Clean up option prefixes if A), B), etc are inside text
    cleaned_opts = {}
    for letter, opt_text in opts.items():
        opt_clean = re.sub(r'^[A-D][\)\.\:\-]\s*', '', opt_text.strip())
        cleaned_opts[letter] = opt_clean
        
    enunciado = q.get('enunciado', '').strip()
    if not enunciado.startswith('<p>'):
        enunciado = f"<p>{enunciado}</p>"

    tema = q.get('tema', default_theme)
    if not tema or tema == 'Direito Civil':
        tema = f"{default_theme} - {q['exame_label']}"

    formatted_q = {
        "num": len(modules_data[mod_prefix]) + 1,
        "id": len(modules_data[mod_prefix]) + 1,
        "exame": q['exame_label'],
        "tema": tema,
        "enunciado": enunciado,
        "opcoes": cleaned_opts,
        "gabarito": q.get('gabarito', 'A').strip().upper(),
        "core": True,
        # Neutral placeholders for back of card (as requested)
        "sintese": f"<p><i>Aguardando síntese didática ({default_theme}).</i></p>",
        "logica_conceito": "<p><i>Aguardando povoamento da lógica do conceito em momento oportuno.</i></p>",
        "fundamentacao": "<p>Código Civil (Lei nº 10.406/2002)</p>",
        "dica": "<p><i>Aguardando dica didática.</i></p>",
        "aula_comentario": "<p><i>Aguardando transcrição da videoaula.</i></p>",
        "analise": "<p><i>Aguardando análise detalhada das alternativas.</i></p>"
    }
    
    modules_data[mod_prefix].append(formatted_q)

# Write JSON files for each module
for mod_prefix, q_list in modules_data.items():
    out_json_path = os.path.join(CIVIL_DIR, f"{mod_prefix}_questoes.json")
    with open(out_json_path, 'w', encoding='utf-8') as out_f:
        json.dump(q_list, out_f, ensure_ascii=False, indent=2)
    print(f"Atualizado {mod_prefix}_questoes.json com {len(q_list)} questões reais.")

print("\nTodos os arquivos JSON de questões foram populados com sucesso!")
