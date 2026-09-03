import json
import glob
import os
import subprocess

def classify_const(q):
    t = (q.get('enunciado', '') + ' ' + str(q.get('tema', ''))).lower()
    
    # 03. Remédios Constitucionais
    if any(k in t for k in ['habeas corpus', 'mandado de segurança', 'mandado de injunção', 'habeas data', 'ação popular', 'direito de petição', 'obtenção de certidão']):
        return '03_remedios_constitucionais', 'Remédios Constitucionais'
    # 06. Controle de Constitucionalidade
    elif any(k in t for k in ['ação direta', 'ação declaratória', 'arguição de descumprimento', 'controle concentrado', 'controle difuso', 'súmula vinculante', 'legitimado', 'representação de inconstitucionalidade', 'controvérsias entre órgãos judiciários']):
        return '06_controle_constitucionalidade', 'Controle de Constitucionalidade'
    # 07. Defesa do Estado e das Instituições
    elif any(k in t for k in ['estado de defesa', 'estado de sítio', 'forças armadas', 'segurança pública', 'polícia', 'intervenção federal', 'intervenção estadual', 'deixasse de realizar os depósitos', 'deixasse de pagar']):
        return '07_defesa_estado', 'Defesa do Estado e das Instituições'
    # 04. Organização do Estado e Competências
    elif any(k in t for k in ['competência', 'privativa', 'concorrente', 'bens da união', 'jazida', 'repartição', 'criação de município', 'incorporação de município', 'autonomia dos estados']):
        return '04_organizacao_estado', 'Organização do Estado e Competências'
    # 08. Ordem Econômica, Financeira e Social
    elif any(k in t for k in ['ordem econômica', 'ordem social', 'saúde', 'educação', 'meio ambiente', 'indígena', 'índios', 'família', 'previdência', 'orçamento', 'usucapião urbano', 'reforma agrária']):
        return '08_ordem_economica_social', 'Ordem Econômica, Financeira e Social'
    # 02. Direitos e Garantias Fundamentais
    elif any(k in t for k in ['direitos fundamentais', 'direitos individuais', 'nacionalidade', 'brasileiro nato', 'naturalizado', 'direitos políticos', 'partidos políticos', 'inelegibil', 'sufrágio', 'inviolab', 'religião', 'pianista', 'exercício da profissão', 'violento temporal', 'domicílio', 'requisição administrativa', 'liberdade de expressão', 'associação']):
        return '02_direitos_fundamentais', 'Direitos e Garantias Fundamentais'
    # 05. Organização dos Poderes / Processo Legislativo
    elif any(k in t for k in ['poder legislativo', 'poder executivo', 'poder judiciário', 'processo legislativo', 'medida provisória', 'lei complementar', 'lei ordinária', 'emenda à constituição', 'pec ', 'câmara', 'senado', 'congresso', 'presidente da república', 'deputado', 'senador', 'cpi', 'imunidade parlamentar', 'foro por prerrogativa', 'crime de responsabilidade', 'impeachment', 'cnj', 'precatório', 'veto']):
        return '05_organizacao_poderes', 'Organização dos Poderes'
    # 01. Teoria da Constituição e Poder Constitucional (Fallback)
    else:
        return '01_teoria_constituicao', 'Teoria da Constituição e Poder Constitucional'

def main():
    simulados_files = sorted(glob.glob('/home/sfy/Jurimetria_OAB/JUR_Jurimetria/simulados/e*_tipo1_branca.json'))
    print(f"📁 Encontrados {len(simulados_files)} arquivos de simulados dos exames.")

    const_questions = []
    for f in simulados_files:
        filename = os.path.basename(f)
        exame_num = filename.split('e')[1].split('_')[0]
        with open(f, 'r', encoding='utf-8') as fp:
            items = json.load(fp)
            for item in items:
                disc = item.get('disciplina', '')
                num = item.get('num', 0)
                
                if 'constitucional' in disc.lower() or (disc == '' and 11 <= num <= 16):
                    item['exame_num'] = int(exame_num)
                    item['exame_label'] = f'{exame_num}º Exame OAB'
                    const_questions.append(item)

    print(f"✅ Total de questões de Direito Constitucional extraídas: {len(const_questions)}")

    modules = {
        '01_teoria_constituicao': {'title': 'Teoria da Constituição e Poder Constitucional', 'questions': []},
        '02_direitos_fundamentais': {'title': 'Direitos e Garantias Fundamentais', 'questions': []},
        '03_remedios_constitucionais': {'title': 'Remédios Constitucionais', 'questions': []},
        '04_organizacao_estado': {'title': 'Organização do Estado e Competências', 'questions': []},
        '05_organizacao_poderes': {'title': 'Organização dos Poderes', 'questions': []},
        '06_controle_constitucionalidade': {'title': 'Controle de Constitucionalidade', 'questions': []},
        '07_defesa_estado': {'title': 'Defesa do Estado e das Instituições', 'questions': []},
        '08_ordem_economica_social': {'title': 'Ordem Econômica, Financeira e Social', 'questions': []}
    }

    for idx, q in enumerate(const_questions, start=1):
        mod_key, mod_title = classify_const(q)
        
        # Build options dictionary
        opcoes = {}
        for opt in ['A', 'B', 'C', 'D']:
            val = q.get(f'opcao_{opt.lower()}') or q.get('opcoes', {}).get(opt, f'Opção {opt}')
            opcoes[opt] = val

        gabarito = q.get('gabarito', 'A').upper()
        if gabarito not in ['A', 'B', 'C', 'D']:
            gabarito = 'A'

        card_q = {
            "num": len(modules[mod_key]['questions']) + 1,
            "id": idx,
            "exame": q.get('exame_label', f"{q.get('exame_num')}º Exame OAB"),
            "tema": f"{q.get('tema') or mod_title} ({q.get('exame_label')})",
            "enunciado": q.get('enunciado', ''),
            "opcoes": opcoes,
            "gabarito": gabarito,
            "core": True,
            "sintese": f"<p><strong>Aguardando síntese didática / lógica do conceito.</strong><br>Questão oficial extraída do {q.get('exame_label')}. Gabarito definitivo: <strong>Alternativa {gabarito}</strong>.</p>",
            "logica_conceito": f"<p>Fundamentação teórica do tema <em>{q.get('tema') or mod_title}</em> pendente de elaboração pedagógica.</p>",
            "fundamentacao": "<p>Constituição da República Federativa do Brasil de 1988 (CF/88).</p>",
            "dica": "<p>Analise a jurisprudência consolidada do Supremo Tribunal Federal (STF) e a norma constitucional aplicável.</p>",
            "aula_comentario": f"<p>Comentário em vídeo referente ao {q.get('exame_label')}.</p>",
            "analise": f"<p>Análise detalhada das alternativas A, B, C e D em desenvolvimento.</p>"
        }

        modules[mod_key]['questions'].append(card_q)

    base_dir = '/home/sfy/Corujinha/CONSTITUCIONAL'
    for mod_key, data in modules.items():
        json_path = os.path.join(base_dir, f"{mod_key}_questoes.json")
        with open(json_path, 'w', encoding='utf-8') as fp:
            json.dump(data['questions'], fp, ensure_ascii=False, indent=2)
        print(f"📦 {mod_key}_questoes.json populado com {len(data['questions'])} questões.")

    print("\n🔨 Executando compilação do ecossistema Constitucional via build_const_modules.py...")
    subprocess.run(["python3", os.path.join(base_dir, "build_const_modules.py")], check=True)
    print("✨ Processo concluído com sucesso!")

if __name__ == '__main__':
    main()
