import json
import glob
import os
import subprocess

def classify_trib(q):
    t = (q.get('enunciado', '') + ' ' + str(q.get('tema', ''))).lower()
    
    # 06. Responsabilidade Tributária
    if any(k in t for k in ['responsabilidade tributária', 'responsável tributário', 'sucessão', 'sucessores', 'incorporação', 'fundo de comércio', 'sócio-gerente', 'redirecionamento', 'denúncia espontânea', 'solidariamente', 'subsidiariamente']):
        return '06_responsabilidade_tributaria', 'Responsabilidade Tributária'
    # 02. Obrigação Tributária
    elif any(k in t for k in ['obrigação tributária', 'fato gerador', 'sujeito passivo', 'contribuinte', 'obrigação acessória', 'capacidade tributária']):
        return '02_obrigacao_tributaria', 'Obrigação Tributária'
    # 04. Impostos da União
    elif any(k in t for k in ['imposto de renda', 'irpf', 'irpj', 'ipi', 'imposto de importação', 'imposto de exportação', 'iof', 'itr ', 'imposto territorial rural']):
        return '04_impostos_uniao', 'Impostos da União'
    # 05. Impostos dos Estados e Municípios
    elif any(k in t for k in ['icms', 'itcmd', 'ipva', 'iptu', 'itbi', 'issqn', 'iss ']):
        return '05_impostos_estados', 'Impostos dos Estados e Municípios'
    # 08. Execução Fiscal e Garantias
    elif any(k in t for k in ['execução fiscal', '6.830', 'cda', 'dívida ativa', 'exceção de pré-executividade', 'embargos à execução fiscal', 'garantias do crédito']):
        return '08_execucao_fiscal', 'Execução Fiscal e Garantias'
    # 07. Administração Tributária e Processo Administrativo
    elif any(k in t for k in ['fiscalização', 'sigilo fiscal', 'certidão negativa', 'cnd ', 'cpend', 'processo administrativo fiscal', 'paf ']):
        return '07_administracao_tributaria', 'Administração Tributária'
    # 03. Crédito Tributário e Lançamento
    elif any(k in t for k in ['crédito tributário', 'lançamento', 'homologação', 'suspensão da exigibilidade', 'moratória', 'compensação', 'remissão', 'prescrição', 'decadência', 'isenção', 'anistia']):
        return '03_credito_tributario', 'Crédito Tributário e Lançamento'
    # 01. Sistema Tributário Nacional (Fallback / Princípios / Imunidades)
    else:
        return '01_sistema_tributario', 'Sistema Tributário Nacional'

def main():
    simulados_files = sorted(glob.glob('/home/sfy/Jurimetria_OAB/JUR_Jurimetria/simulados/e*_tipo1_branca.json'))
    print(f"📁 Encontrados {len(simulados_files)} arquivos de simulados dos exames.")

    trib_questions = []
    for f in simulados_files:
        filename = os.path.basename(f)
        exame_num = filename.split('e')[1].split('_')[0]
        with open(f, 'r', encoding='utf-8') as fp:
            items = json.load(fp)
            for item in items:
                num = item.get('num', 0)
                disc = item.get('disciplina', '')
                if 'tributá' in disc.lower() or 'tributa' in disc.lower():
                    item['exame_num'] = int(exame_num)
                    item['exame_label'] = f'{exame_num}º Exame OAB'
                    trib_questions.append(item)
                elif disc == '' and (exame_num == '37' and 21 <= num <= 25):
                    item['exame_num'] = int(exame_num)
                    item['exame_label'] = f'{exame_num}º Exame OAB'
                    trib_questions.append(item)

    print(f"✅ Total de questões de Direito Tributário (CTN) extraídas: {len(trib_questions)}")

    modules = {
        '01_sistema_tributario': {'title': 'Sistema Tributário Nacional', 'questions': []},
        '02_obrigacao_tributaria': {'title': 'Obrigação Tributária', 'questions': []},
        '03_credito_tributario': {'title': 'Crédito Tributário e Lançamento', 'questions': []},
        '04_impostos_uniao': {'title': 'Impostos da União', 'questions': []},
        '05_impostos_estados': {'title': 'Impostos dos Estados e Municípios', 'questions': []},
        '06_responsabilidade_tributaria': {'title': 'Responsabilidade Tributária', 'questions': []},
        '07_administracao_tributaria': {'title': 'Administração Tributária', 'questions': []},
        '08_execucao_fiscal': {'title': 'Execução Fiscal e Garantias', 'questions': []}
    }

    for idx, q in enumerate(trib_questions, start=1):
        mod_key, mod_title = classify_trib(q)
        
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
            "fundamentacao": "<p>Código Tributário Nacional (Lei nº 5.172/1966) e Constituição Federal de 1988 (Arts. 145 a 156-A).</p>",
            "dica": "<p>Observe os princípios tributários, imunidades constitutivas, hipótese de incidência e decadência/prescrição.</p>",
            "aula_comentario": f"<p>Comentário em vídeo referente ao {q.get('exame_label')}.</p>",
            "analise": f"<p>Análise detalhada das alternativas A, B, C e D em desenvolvimento.</p>"
        }

        modules[mod_key]['questions'].append(card_q)

    base_dir = '/home/sfy/Corujinha/TRIBUTARIO'
    for mod_key, data in modules.items():
        json_path = os.path.join(base_dir, f"{mod_key}_questoes.json")
        with open(json_path, 'w', encoding='utf-8') as fp:
            json.dump(data['questions'], fp, ensure_ascii=False, indent=2)
        print(f"📦 {mod_key}_questoes.json populado com {len(data['questions'])} questões.")

    print("\n🔨 Executando compilação do ecossistema Tributário via build_trib_modules.py...")
    subprocess.run(["python3", os.path.join(base_dir, "build_trib_modules.py")], check=True)
    print("✨ Processo concluído com sucesso!")

if __name__ == '__main__':
    main()
