import json
import glob
import os
import subprocess

def classify_int(q):
    t = (q.get('enunciado', '') + ' ' + str(q.get('tema', ''))).lower()
    
    # 03. Extradição, Expulsão e Deportação
    if any(k in t for k in ['extradição', 'extraditado', 'expulsão', 'deportação', 'repatriamento', 'repatriado']):
        return '03_extradicao_expulsao', 'Extradição, Expulsão e Deportação'
    # 05. Homologação de Sentença Estrangeira
    elif any(k in t for k in ['homologação', 'homologar', 'sentença estrangeira', 'laudo arbitral estrangeiro', 'stj ']):
        return '05_homologacao_sentenca', 'Homologação de Sentença Estrangeira'
    # 04. Cooperação Jurídica Internacional
    elif any(k in t for k in ['cooperação jurídica', 'auxílio direto', 'carta rogatória', 'exequatur']):
        return '04_cooperacao_juridica', 'Cooperação Jurídica Internacional'
    # 08. Tratados e Imunidades Diplomáticas
    elif any(k in t for k in ['tratado', 'convenção de viena', 'cvdt', 'denúncia', 'reserva', 'imunidade diplomática', 'agente diplomático', 'consular']):
        return '08_tratados_imunidades', 'Tratados e Imunidades Diplomáticas'
    # 07. Sujeitos de DIP e Imunidades
    elif any(k in t for k in ['imunidade de jurisdição', 'imunidade de execução', 'embaixada', 'organização internacional', 'estado estrangeiro']):
        return '07_sujeitos_dip', 'Sujeitos de DIP e Imunidades'
    # 06. Contratos Internacionais e Comércio Exterior
    elif any(k in t for k in ['contrato internacional', 'incoterms', 'cisg', 'compra e venda internacional', 'arbitragem internacional']):
        return '06_contratos_internacionais', 'Contratos Internacionais'
    # 02. Nacionalidade e Condição do Estrangeiro
    elif any(k in t for k in ['nacionalidade', 'brasileiro nato', 'naturalizado', 'estrangeiro', 'visto', 'asilo', 'refúgio', 'lei de migração', '13.445']):
        return '02_nacionalidade_estrangeiro', 'Nacionalidade e Condição do Estrangeiro'
    # Fallback
    else:
        return '01_lindb_conflito_leis', 'LINDB e Conflito de Leis no Espaço'

def main():
    simulados_files = sorted(glob.glob('/home/sfy/Jurimetria_OAB/JUR_Jurimetria/simulados/e*_tipo1_branca.json'))
    print(f"📁 Encontrados {len(simulados_files)} arquivos de simulados dos exames.")

    int_questions = []
    for f in simulados_files:
        filename = os.path.basename(f)
        exame_num = filename.split('e')[1].split('_')[0]
        with open(f, 'r', encoding='utf-8') as fp:
            items = json.load(fp)
            for item in items:
                num = item.get('num', 0)
                disc = item.get('disciplina', '')
                if 'internacional' in disc.lower():
                    item['exame_num'] = int(exame_num)
                    item['exame_label'] = f'{exame_num}º Exame OAB'
                    int_questions.append(item)
                elif disc == '' and (exame_num == '37' and 19 <= num <= 20):
                    item['exame_num'] = int(exame_num)
                    item['exame_label'] = f'{exame_num}º Exame OAB'
                    int_questions.append(item)

    print(f"✅ Total de questões de Direito Internacional extraídas: {len(int_questions)}")

    modules = {
        '01_lindb_conflito_leis': {'title': 'LINDB e Conflito de Leis no Espaço', 'questions': []},
        '02_nacionalidade_estrangeiro': {'title': 'Nacionalidade e Condição do Estrangeiro', 'questions': []},
        '03_extradicao_expulsao': {'title': 'Extradição, Expulsão e Deportação', 'questions': []},
        '04_cooperacao_juridica': {'title': 'Cooperação Jurídica Internacional', 'questions': []},
        '05_homologacao_sentenca': {'title': 'Homologação de Sentença Estrangeira', 'questions': []},
        '06_contratos_internacionais': {'title': 'Contratos Internacionais', 'questions': []},
        '07_sujeitos_dip': {'title': 'Sujeitos de DIP e Imunidades', 'questions': []},
        '08_tratados_imunidades': {'title': 'Tratados e Imunidades Diplomáticas', 'questions': []}
    }

    for idx, q in enumerate(int_questions, start=1):
        mod_key, mod_title = classify_int(q)
        
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
            "fundamentacao": "<p>LINDB (Decreto-Lei nº 4.657/1942), Lei de Migração (Lei nº 13.445/2017) e Convenção de Viena sobre Direito dos Tratados.</p>",
            "dica": "<p>Verifique o elemento de conexão aplicável (domicílio/local do ato), hipóteses de extradição e a competência do STJ.</p>",
            "aula_comentario": f"<p>Comentário em vídeo referente ao {q.get('exame_label')}.</p>",
            "analise": f"<p>Análise detalhada das alternativas A, B, C e D em desenvolvimento.</p>"
        }

        modules[mod_key]['questions'].append(card_q)

    base_dir = '/home/sfy/Corujinha/INTERNACIONAL'
    for mod_key, data in modules.items():
        json_path = os.path.join(base_dir, f"{mod_key}_questoes.json")
        with open(json_path, 'w', encoding='utf-8') as fp:
            json.dump(data['questions'], fp, ensure_ascii=False, indent=2)
        print(f"📦 {mod_key}_questoes.json populado com {len(data['questions'])} questões.")

    print("\n🔨 Executando compilação do ecossistema Direito Internacional via build_int_modules.py...")
    subprocess.run(["python3", os.path.join(base_dir, "build_int_modules.py")], check=True)
    print("✨ Processo concluído com sucesso!")

if __name__ == '__main__':
    main()
