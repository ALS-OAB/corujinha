import json
import glob
import os
import subprocess

def classify_penal(q):
    t = (q.get('enunciado', '') + ' ' + str(q.get('tema', ''))).lower()
    
    # 07. Crimes contra a Administração Pública
    if any(k in t for k in ['peculato', 'concussão', 'corrupção', 'prevaricação', 'condescendência', 'advocacia administrativa', 'desacato', 'desobediência', 'denunciação caluniosa', 'falso testemunho', 'fraude em certame', 'crimes contra a administração', 'funcionário público']):
        return '07_crimes_administracao', 'Crimes Contra a Administração Pública'
    # 06. Crimes contra a Dignidade Sexual
    elif any(k in t for k in ['estupro', 'vulnerável', 'importunação sexual', 'assédio sexual', 'satisfação de lascívia', 'dignidade sexual', 'pornográfic', 'relações sexuais']):
        return '06_crimes_dignidade_sexual', 'Crimes Contra a Dignidade Sexual e Família'
    # 05. Crimes contra o Patrimônio
    elif any(k in t for k in ['furto', 'roubo', 'latrocínio', 'extorsão', 'estelionato', 'receptação', 'dano', 'apropriação', 'gerente bancário']):
        return '05_crimes_contra_patrimonio', 'Crimes Contra o Patrimônio'
    # 04. Crimes contra a Vida e Pessoa
    elif any(k in t for k in ['homicídio', 'infanticídio', 'aborto', 'suicídio', 'lesão corporal', 'rixa', 'ameaça', 'sequestro', 'cárcere privado', 'omissão de socorro', 'matar', 'agred', 'tapa no rosto', 'injúria', 'calúnia', 'difamação', 'burro', 'idiota', 'repórter', 'coveiro', 'feminicídio', 'veneno']):
        return '04_crimes_contra_vida', 'Crimes Contra a Vida e Pessoa'
    # 08. Concurso de Agentes e Lei de Drogas
    elif any(k in t for k in ['tráfico', 'drogas', 'entorpecente', 'coautoria', 'participação', 'cooperação dolosamente distinta', 'concurso de pessoas', 'concurso de agentes', 'associação para o tráfico', 'auxílio no furto', 'planejaram matar']):
        return '08_concurso_agentes', 'Concurso de Agentes e Lei de Drogas'
    # 03. Punibilidade e Penas
    elif any(k in t for k in ['prescrição', 'dosimetria', 'reincidência', 'antecedentes', 'sursis', 'livramento condicional', 'extinção da punibilidade', 'multa', 'restritiva de direitos', 'privativa de liberdade', 'indulto', 'anistia', 'graça', 'detração', 'remição', 'pena de oito meses', 'regime fechado']):
        return '03_punibilidade_penas', 'Punibilidade e Penas'
    # 02. Ilicitude e Culpabilidade
    elif any(k in t for k in ['legítima defesa', 'estado de necessidade', 'estrito cumprimento', 'exercício regular', 'excludente de ilicitude', 'imputabilidade', 'embriaguez', 'erro de proibição', 'coação moral irresistível', 'obediência hierárquica', 'culpabilidade', 'lutador de mma', 'agredida por um terceiro']):
        return '02_ilicitude_culpabilidade', 'Ilicitude e Culpabilidade'
    # 01. Teoria Geral do Crime (Fallback)
    else:
        return '01_teoria_geral_crime', 'Teoria Geral do Crime e Tipicidade'

def main():
    simulados_files = sorted(glob.glob('/home/sfy/Jurimetria_OAB/JUR_Jurimetria/simulados/e*_tipo1_branca.json'))
    print(f"📁 Encontrados {len(simulados_files)} arquivos de simulados dos exames.")

    penal_questions = []
    for f in simulados_files:
        filename = os.path.basename(f)
        exame_num = filename.split('e')[1].split('_')[0]
        with open(f, 'r', encoding='utf-8') as fp:
            items = json.load(fp)
            for item in items:
                num = item.get('num', 0)
                if (exame_num == '37' and 56 <= num <= 61) or (exame_num != '37' and 57 <= num <= 62):
                    item['exame_num'] = int(exame_num)
                    item['exame_label'] = f'{exame_num}º Exame OAB'
                    penal_questions.append(item)

    print(f"✅ Total de questões de Direito Penal (CP) extraídas: {len(penal_questions)}")

    modules = {
        '01_teoria_geral_crime': {'title': 'Teoria Geral do Crime e Tipicidade', 'questions': []},
        '02_ilicitude_culpabilidade': {'title': 'Ilicitude e Culpabilidade', 'questions': []},
        '03_punibilidade_penas': {'title': 'Punibilidade e Penas', 'questions': []},
        '04_crimes_contra_vida': {'title': 'Crimes Contra a Vida e Pessoa', 'questions': []},
        '05_crimes_contra_patrimonio': {'title': 'Crimes Contra o Patrimônio', 'questions': []},
        '06_crimes_dignidade_sexual': {'title': 'Crimes Contra a Dignidade Sexual e Família', 'questions': []},
        '07_crimes_administracao': {'title': 'Crimes Contra a Administração Pública', 'questions': []},
        '08_concurso_agentes': {'title': 'Concurso de Agentes e Lei de Drogas', 'questions': []}
    }

    for idx, q in enumerate(penal_questions, start=1):
        mod_key, mod_title = classify_penal(q)
        
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
            "fundamentacao": "<p>Código Penal Brasileiro (Decreto-Lei nº 2.848/1940).</p>",
            "dica": "<p>Analise os elementos do fato típico, ilicitude, culpabilidade e a tipificação penal abstrata.</p>",
            "aula_comentario": f"<p>Comentário em vídeo referente ao {q.get('exame_label')}.</p>",
            "analise": f"<p>Análise detalhada das alternativas A, B, C e D em desenvolvimento.</p>"
        }

        modules[mod_key]['questions'].append(card_q)

    base_dir = '/home/sfy/Corujinha/PENAL'
    for mod_key, data in modules.items():
        json_path = os.path.join(base_dir, f"{mod_key}_questoes.json")
        with open(json_path, 'w', encoding='utf-8') as fp:
            json.dump(data['questions'], fp, ensure_ascii=False, indent=2)
        print(f"📦 {mod_key}_questoes.json populado com {len(data['questions'])} questões.")

    print("\n🔨 Executando compilação do ecossistema Penal via build_penal_modules.py...")
    subprocess.run(["python3", os.path.join(base_dir, "build_penal_modules.py")], check=True)
    print("✨ Processo concluído com sucesso!")

if __name__ == '__main__':
    main()
