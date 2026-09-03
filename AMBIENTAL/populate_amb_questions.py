import json
import glob
import os
import subprocess

def classify_amb(q):
    t = (q.get('enunciado', '') + ' ' + str(q.get('tema', ''))).lower()
    
    # 05. Crimes Ambientais
    if any(k in t for k in ['crimes ambientais', 'crime ambiental', 'lei nº 9.605', 'lei 9.605', 'penalmente', 'sanção penal', 'delito ambiental', 'pena ']):
        return '05_crimes_ambientais', 'Crimes Ambientais'
    # 06. Código Florestal
    elif any(k in t for k in ['código florestal', 'lei nº 12.651', 'lei 12.651', 'área de preservação permanente', ' app ', 'preserva', 'reserva legal', 'cadastro ambiental rural', ' car ']):
        return '06_codigo_florestal', 'Código Florestal'
    # 07. Unidades de Conservação e SNUC
    elif any(k in t for k in ['unidade de conservação', 'snuc', 'lei nº 9.985', 'lei 9.985', 'parque nacional', 'reserva biológica', 'apa ', 'proteção integral']):
        return '07_snuc_unidades', 'Unidades de Conservação e SNUC'
    # 03. Licenciamento Ambiental e EIA/RIMA
    elif any(k in t for k in ['licenciamento ambiental', 'licença ambiental', 'licença prévia', 'licença de instalação', 'licença de operação', 'eia/rima', 'estudo de impacto ambiental', 'estudo prévio']):
        return '03_licenciamento_eia', 'Licenciamento Ambiental e EIA/RIMA'
    # 02. Competências Constitucionais Ambientais
    elif any(k in t for k in ['competência', 'lei complementar nº 140', 'lc 140', 'art. 23', 'art. 24', 'órgão ambiental estadual', 'órgão ambiental municipal']):
        return '02_competencias_ambientais', 'Competências Constitucionais Ambientais'
    # 04. Responsabilidade Civil por Danos Ambientais
    elif any(k in t for k in ['responsabilidade civil', 'dano ambiental', 'risco integral', 'reparação do dano', 'poluidor']):
        return '04_responsabilidade_civil', 'Responsabilidade Civil por Danos Ambientais'
    # 08. Recursos Hídricos e Resíduos Sólidos
    elif any(k in t for k in ['recursos hídricos', 'outorga', 'resíduos sólidos', 'logística reversa']):
        return '08_recursos_hidricos', 'Recursos Hídricos e Resíduos Sólidos'
    # Fallback
    else:
        return '01_principios_ambientais', 'Princípios do Direito Ambiental'

def main():
    simulados_files = sorted(glob.glob('/home/sfy/Jurimetria_OAB/JUR_Jurimetria/simulados/e*_tipo1_branca.json'))
    print(f"📁 Encontrados {len(simulados_files)} arquivos de simulados dos exames.")

    amb_questions = []
    for f in simulados_files:
        filename = os.path.basename(f)
        exame_num = filename.split('e')[1].split('_')[0]
        with open(f, 'r', encoding='utf-8') as fp:
            items = json.load(fp)
            for item in items:
                num = item.get('num', 0)
                disc = item.get('disciplina', '')
                if 'ambiental' in disc.lower():
                    item['exame_num'] = int(exame_num)
                    item['exame_label'] = f'{exame_num}º Exame OAB'
                    amb_questions.append(item)
                elif disc == '' and (exame_num == '37' and 32 <= num <= 33):
                    item['exame_num'] = int(exame_num)
                    item['exame_label'] = f'{exame_num}º Exame OAB'
                    amb_questions.append(item)
                elif exame_num == '42' and num == 37:
                    item['exame_num'] = int(exame_num)
                    item['exame_label'] = f'{exame_num}º Exame OAB'
                    amb_questions.append(item)

    print(f"✅ Total de questões de Direito Ambiental extraídas: {len(amb_questions)}")

    modules = {
        '01_principios_ambientais': {'title': 'Princípios do Direito Ambiental', 'questions': []},
        '02_competencias_ambientais': {'title': 'Competências Constitucionais Ambientais', 'questions': []},
        '03_licenciamento_eia': {'title': 'Licenciamento Ambiental e EIA/RIMA', 'questions': []},
        '04_responsabilidade_civil': {'title': 'Responsabilidade Civil por Danos Ambientais', 'questions': []},
        '05_crimes_ambientais': {'title': 'Crimes Ambientais', 'questions': []},
        '06_codigo_florestal': {'title': 'Código Florestal', 'questions': []},
        '07_snuc_unidades': {'title': 'Unidades de Conservação e SNUC', 'questions': []},
        '08_recursos_hidricos': {'title': 'Recursos Hídricos e Resíduos Sólidos', 'questions': []}
    }

    for idx, q in enumerate(amb_questions, start=1):
        mod_key, mod_title = classify_amb(q)
        
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
            "fundamentacao": "<p>Política Nacional do Meio Ambiente (Lei nº 6.938/1981), Código Florestal (Lei nº 12.651/2012) e CF/1988 (Art. 225).</p>",
            "dica": "<p>Analise a responsabilidade civil objetiva (risco integral), as fases do licenciamento e a proteção às APPs e Reserva Legal.</p>",
            "aula_comentario": f"<p>Comentário em vídeo referente ao {q.get('exame_label')}.</p>",
            "analise": f"<p>Análise detalhada das alternativas A, B, C e D em desenvolvimento.</p>"
        }

        modules[mod_key]['questions'].append(card_q)

    base_dir = '/home/sfy/Corujinha/AMBIENTAL'
    for mod_key, data in modules.items():
        json_path = os.path.join(base_dir, f"{mod_key}_questoes.json")
        with open(json_path, 'w', encoding='utf-8') as fp:
            json.dump(data['questions'], fp, ensure_ascii=False, indent=2)
        print(f"📦 {mod_key}_questoes.json populado com {len(data['questions'])} questões.")

    print("\n🔨 Executando compilação do ecossistema Direito Ambiental via build_amb_modules.py...")
    subprocess.run(["python3", os.path.join(base_dir, "build_amb_modules.py")], check=True)
    print("✨ Processo concluído com sucesso!")

if __name__ == '__main__':
    main()
