import json
import glob
import os
import subprocess

def classify_fin(q):
    t = (q.get('enunciado', '') + ' ' + str(q.get('tema', ''))).lower()
    
    # 06. LRF (LC 101/00)
    if any(k in t for k in ['lrf', 'lei de responsabilidade fiscal', 'lc 101', 'relatório de gestão', 'despesa total com pessoal', 'limite prudencial', 'margem de expansão']):
        return '06_lrf_responsabilidade', 'Lei de Responsabilidade Fiscal (LC 101/00)'
    # 05. Créditos Adicionais
    elif any(k in t for k in ['crédito adicional', 'créditos adicionais', 'crédito suplementar', 'crédito especial', 'crédito extraordinário', 'suplementação orçamentária', 'superávit financeiro']):
        return '05_creditos_adicionais', 'Créditos Adicionais'
    # 07. Precatórios e Dívida Ativa
    elif any(k in t for k in ['precatório', 'precatórios', 'dívida ativa', 'dívida fundada', 'dívida consolidada', 'operação de crédito', 'empréstimo público']):
        return '07_precatorios_divida', 'Precatórios e Dívida Ativa'
    # 01. Orçamento Público (PPA, LDO, LOA)
    elif any(k in t for k in ['ppa', 'ldo', 'loa', 'plano plurianual', 'diretrizes orçamentárias', 'orçamento anual', 'emenda parlamentar', 'impositivo', 'proposta orçamentária']):
        return '01_ppa_ldo_loa', 'Orçamento Público: PPA, LDO e LOA'
    # 08. Fiscalização e Tribunais de Contas
    elif any(k in t for k in ['tribunal de contas', 'tcu', 'tce', 'controle externo', 'parecer prévio', 'tomada de contas']):
        return '08_fiscalizacao_tribunal', 'Fiscalização Financeira e Tribunais de Contas'
    # 04. Despesa Pública
    elif any(k in t for k in ['despesa pública', 'empenho', 'liquidação', 'restos a pagar', 'estágio da despesa', 'despesa de pessoal']):
        return '04_despesa_publica', 'Despesa Pública: Empenho e Liquidação'
    # 03. Receita Pública
    elif any(k in t for k in ['receita pública', 'arrecadação', 'recolhimento', 'estágio da receita', 'renúncia de receita', 'receita corrente', 'imposto', 'taxa']):
        return '03_receita_publica', 'Receita Pública e Estágios'
    # Fallback
    else:
        return '02_principios_orcamentarios', 'Princípios Orçamentários Constitucionais'

def main():
    simulados_files = sorted(glob.glob('/home/sfy/Jurimetria_OAB/JUR_Jurimetria/simulados/e*_tipo1_branca.json'))
    print(f"📁 Encontrados {len(simulados_files)} arquivos de simulados dos exames.")

    fin_questions = []

    for f in simulados_files:
        filename = os.path.basename(f)
        exame_num = filename.split('e')[1].split('_')[0]
        with open(f, 'r', encoding='utf-8') as fp:
            items = json.load(fp)
            for item in items:
                disc = item.get('disciplina', '')
                if 'financeiro' in disc.lower():
                    item['exame_num'] = int(exame_num)
                    item['exame_label'] = f'{exame_num}º Exame OAB'
                    fin_questions.append(item)

    print(f"✅ Total de questões de Direito Financeiro extraídas: {len(fin_questions)}")

    modules = {
        '01_ppa_ldo_loa': {'title': 'Orçamento Público: PPA, LDO e LOA', 'questions': []},
        '02_principios_orcamentarios': {'title': 'Princípios Orçamentários Constitucionais', 'questions': []},
        '03_receita_publica': {'title': 'Receita Pública e Estágios', 'questions': []},
        '04_despesa_publica': {'title': 'Despesa Pública: Empenho e Liquidação', 'questions': []},
        '05_creditos_adicionais': {'title': 'Créditos Adicionais', 'questions': []},
        '06_lrf_responsabilidade': {'title': 'Lei de Responsabilidade Fiscal (LC 101/00)', 'questions': []},
        '07_precatorios_divida': {'title': 'Precatórios e Dívida Ativa', 'questions': []},
        '08_fiscalizacao_tribunal': {'title': 'Fiscalização Financeira e Tribunais de Contas', 'questions': []}
    }

    for idx, q in enumerate(fin_questions, start=1):
        mod_key, mod_title = classify_fin(q)
        
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
            "fundamentacao": "<p>Constituição Federal (Arts. 165 a 169), Lei de Responsabilidade Fiscal (LC nº 101/2000) e Lei nº 4.320/1964.</p>",
            "dica": "<p>Diferencie PPA (planejamento de 4 anos), LDO (metas e prioridades) e LOA (fixação de despesas e estimativa de receitas).</p>",
            "aula_comentario": f"<p>Comentário em vídeo referente ao {q.get('exame_label')}.</p>",
            "analise": f"<p>Análise detalhada das alternativas A, B, C e D em desenvolvimento.</p>"
        }

        modules[mod_key]['questions'].append(card_q)

    base_dir = '/home/sfy/Corujinha/FINANCEIRO'
    for mod_key, data in modules.items():
        json_path = os.path.join(base_dir, f"{mod_key}_questoes.json")
        with open(json_path, 'w', encoding='utf-8') as fp:
            json.dump(data['questions'], fp, ensure_ascii=False, indent=2)
        print(f"📦 {mod_key}_questoes.json populado com {len(data['questions'])} questões.")

    print("\n🔨 Executando compilação do ecossistema Direito Financeiro via build_fin_modules.py...")
    subprocess.run(["python3", os.path.join(base_dir, "build_fin_modules.py")], check=True)
    print("✨ Processo concluído com sucesso!")

if __name__ == '__main__':
    main()
