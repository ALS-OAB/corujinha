import json
import glob
import os
import subprocess

def classify_fil(q):
    t = (q.get('enunciado', '') + ' ' + str(q.get('tema', ''))).lower()
    
    # 02. Teoria Pura do Direito (Kelsen)
    if any(k in t for k in ['kelsen', 'teoria pura', 'norma fundamental', 'imputação', 'dever-ser', 'normativismo']):
        return '02_teoria_pura_kelsen', 'Teoria Pura do Direito de Hans Kelsen'
    # 03. Pós-Positivismo e Princípios (Dworkin/Alexy)
    elif any(k in t for k in ['dworkin', 'alexy', 'pós-positivismo', 'integridade', 'romance em cadeia', 'ponderação', 'colisão de princípios', 'regras e princípios']):
        return '03_pospositivismo_dworkin', 'Pós-Positivismo e Princípios (Dworkin/Alexy)'
    # 06. Conceito de Direito e Moral (Hart)
    elif any(k in t for k in ['hart', 'regra de reconhecimento', 'regras primárias', 'regras secundárias', 'textura aberta']):
        return '06_conceito_direito_hart', 'Conceito de Direito e Moral (Hart)'
    # 05. Teorias da Justiça e Equidade (Rawls)
    elif any(k in t for k in ['rawls', 'posição original', 'véu da ignorância', 'justiça como equidade', 'teoria da justiça', 'bobbio']):
        return '05_teorias_justica', 'Teorias da Justiça e Equidade (Rawls)'
    # 08. Ética, Política e Utilitarismo
    elif any(k in t for k in ['kant', 'imperativo categórico', 'utilitarismo', 'bentham', 'stuart mill', 'deontologia', 'ética', 'virtude']):
        return '08_etica_utilitarismo', 'Ética, Política e Utilitarismo'
    # 04. Hermenêutica Jurídica e Argumentação
    elif any(k in t for k in ['hermenêutica', 'interpretação', 'argumentação', 'tópica', 'gadamer', 'perelman', 'teleológic', 'compreensão']):
        return '04_hermeneutica_argumentacao', 'Hermenêutica Jurídica e Argumentação'
    # 07. Sociologia Jurídica e Efetividade da Norma
    elif any(k in t for k in ['sociologia', 'efetividade', 'max weber', 'durkheim', 'ehrlich', 'pluralismo', 'sociedade']):
        return '07_sociologia_efetividade', 'Sociologia Jurídica e Efetividade da Norma'
    # Fallback
    else:
        return '01_jusnaturalismo_positivismo', 'Jusnaturalismo vs. Juspositivismo'

def main():
    simulados_files = sorted(glob.glob('/home/sfy/Jurimetria_OAB/JUR_Jurimetria/simulados/e*_tipo1_branca.json'))
    print(f"📁 Encontrados {len(simulados_files)} arquivos de simulados dos exames.")

    fil_questions = []
    seen_enunciados = set()

    for f in simulados_files:
        filename = os.path.basename(f)
        exame_num = filename.split('e')[1].split('_')[0]
        with open(f, 'r', encoding='utf-8') as fp:
            items = json.load(fp)
            for item in items:
                num = item.get('num', 0)
                disc = item.get('disciplina', '')
                is_fil = ('filosofia' in disc.lower()) or (disc == '' and 9 <= num <= 10)
                if is_fil:
                    enum = item.get('enunciado', '')[:80]
                    if enum not in seen_enunciados:
                        seen_enunciados.add(enum)
                        item['exame_num'] = int(exame_num)
                        item['exame_label'] = f'{exame_num}º Exame OAB'
                        fil_questions.append(item)

    print(f"✅ Total de questões de Filosofia do Direito extraídas (deduplicadas): {len(fil_questions)}")

    modules = {
        '01_jusnaturalismo_positivismo': {'title': 'Jusnaturalismo vs. Juspositivismo', 'questions': []},
        '02_teoria_pura_kelsen': {'title': 'Teoria Pura do Direito de Hans Kelsen', 'questions': []},
        '03_pospositivismo_dworkin': {'title': 'Pós-Positivismo e Princípios (Dworkin/Alexy)', 'questions': []},
        '04_hermeneutica_argumentacao': {'title': 'Hermenêutica Jurídica e Argumentação', 'questions': []},
        '05_teorias_justica': {'title': 'Teorias da Justiça e Equidade (Rawls)', 'questions': []},
        '06_conceito_direito_hart': {'title': 'Conceito de Direito e Moral (Hart)', 'questions': []},
        '07_sociologia_efetividade': {'title': 'Sociologia Jurídica e Efetividade da Norma', 'questions': []},
        '08_etica_utilitarismo': {'title': 'Ética, Política e Utilitarismo', 'questions': []}
    }

    for idx, q in enumerate(fil_questions, start=1):
        mod_key, mod_title = classify_fil(q)
        
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
            "fundamentacao": "<p>Filosofia do Direito: Teoria Geral do Direito, Hermenêutica Jurídica e Filosofia Política.</p>",
            "dica": "<p>Identifique o autor de referência (Kelsen, Dworkin, Hart, Kant, Rawls) e seus conceitos fundamentais.</p>",
            "aula_comentario": f"<p>Comentário em vídeo referente ao {q.get('exame_label')}.</p>",
            "analise": f"<p>Análise detalhada das alternativas A, B, C e D em desenvolvimento.</p>"
        }

        modules[mod_key]['questions'].append(card_q)

    base_dir = '/home/sfy/Corujinha/FILOSOFIA'
    for mod_key, data in modules.items():
        json_path = os.path.join(base_dir, f"{mod_key}_questoes.json")
        with open(json_path, 'w', encoding='utf-8') as fp:
            json.dump(data['questions'], fp, ensure_ascii=False, indent=2)
        print(f"📦 {mod_key}_questoes.json populado com {len(data['questions'])} questões.")

    print("\n🔨 Executando compilação do ecossistema Filosofia do Direito via build_fil_modules.py...")
    subprocess.run(["python3", os.path.join(base_dir, "build_fil_modules.py")], check=True)
    print("✨ Processo concluído com sucesso!")

if __name__ == '__main__':
    main()
