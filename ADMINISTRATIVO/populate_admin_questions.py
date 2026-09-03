import json
import glob
import os
import subprocess

def classify_admin(q):
    t = (q.get('enunciado', '') + ' ' + str(q.get('tema', ''))).lower()
    
    # 04. Licitações e Contratos
    if any(k in t for k in ['licitaç', 'licitante', 'edital', 'pregão', 'concorrência', 'dispensa de licitaç', 'inexigibil', 'contrato administrativ', '14.133', '8.666']):
        return '04_licitacoes_contratos', 'Licitações e Contratos (Nova Lei 14.133)'
    # 06. Agentes Públicos e Improbidade
    elif any(k in t for k in ['improbidade', 'servidor público', 'cargo público', 'concurso público', 'estabilidade', 'cumulação', 'acumulação', 'pad ', 'processo disciplinar', 'demissão', 'teto remuneratório', 'nepotismo', 'enriquecimento ilícito', 'prejuízo ao erário', 'agente público']):
        return '06_agentes_improbidade', 'Agentes Públicos e Improbidade'
    # 07. Intervenção do Estado na Propriedade
    elif any(k in t for k in ['desapropriaç', 'tombamento', 'servidão administrativ', 'limitação administrativ', 'ocupação provisória', 'utilidade pública', 'interesse social', 'requisição administrativ', 'expropriatório']):
        return '07_intervencao_propriedade', 'Intervenção do Estado na Propriedade'
    # 05. Serviços Públicos e Concessões
    elif any(k in t for k in ['serviço público', 'concessão', 'permissão', 'autorização de serviço', 'tarifa', 'encampação', 'caducidade da concessão', 'reversão', 'parceria público-privada', 'ppp']):
        return '05_servicos_publicos', 'Serviços Públicos e Concessões'
    # 08. Responsabilidade Civil e Processo Administrativo
    elif any(k in t for k in ['responsabilidade civil', 'responsabilidade objetiva', 'risco administrativo', 'ação indenizatória', 'processo administrativo', '9.784', 'prescrição quinquenal', 'dano moral', 'dano material', 'nexo causal', 'presos em decorrência de sentença', 'agrediu fisicamente']):
        return '08_responsabilidade_processo', 'Responsabilidade Civil e Processo Administrativo'
    # 03. Atos Administrativos
    elif any(k in t for k in ['ato administrativo', 'anulação', 'revogação', 'cassação', 'motivo', 'objeto', 'finalidade', 'vício de legalidade', 'convalidação', 'autoexecutoriedade', 'editou lei, aplicável após sua entrada em vigor', 'licença']):
        return '03_atos_administrativos', 'Atos Administrativos'
    # 02. Princípios e Poderes Administrativos
    elif any(k in t for k in ['poder de polícia', 'poder hierárquico', 'poder disciplinar', 'poder regulamentar', 'autoexecutariedade', 'imperatividade', 'proporcionalidade', 'razoabilidade', 'moralidade', 'impessoalidade', 'adquirir novos computadores', 'transparência', 'agência reguladora', 'fiscaliza']):
        return '02_principios_poderes', 'Princípios e Poderes Administrativos'
    # 01. Organização Administrativa (Fallback / Estrutura)
    else:
        return '01_organizacao_administrativa', 'Organização Administrativa'

def main():
    simulados_files = sorted(glob.glob('/home/sfy/Jurimetria_OAB/JUR_Jurimetria/simulados/e*_tipo1_branca.json'))
    print(f"📁 Encontrados {len(simulados_files)} arquivos de simulados dos exames.")

    admin_questions = []
    for f in simulados_files:
        filename = os.path.basename(f)
        exame_num = filename.split('e')[1].split('_')[0]
        with open(f, 'r', encoding='utf-8') as fp:
            items = json.load(fp)
            for item in items:
                disc = item.get('disciplina', '')
                num = item.get('num', 0)
                
                if 'administrativo' in disc.lower() or (disc == '' and ((exame_num == '37' and 26 <= num <= 31) or (exame_num != '37' and 30 <= num <= 34))):
                    item['exame_num'] = int(exame_num)
                    item['exame_label'] = f'{exame_num}º Exame OAB'
                    admin_questions.append(item)

    print(f"✅ Total de questões de Direito Administrativo extraídas: {len(admin_questions)}")

    modules = {
        '01_organizacao_administrativa': {'title': 'Organização Administrativa', 'questions': []},
        '02_principios_poderes': {'title': 'Princípios e Poderes Administrativos', 'questions': []},
        '03_atos_administrativos': {'title': 'Atos Administrativos', 'questions': []},
        '04_licitacoes_contratos': {'title': 'Licitações e Contratos (Nova Lei 14.133)', 'questions': []},
        '05_servicos_publicos': {'title': 'Serviços Públicos e Concessões', 'questions': []},
        '06_agentes_improbidade': {'title': 'Agentes Públicos e Improbidade', 'questions': []},
        '07_intervencao_propriedade': {'title': 'Intervenção do Estado na Propriedade', 'questions': []},
        '08_responsabilidade_processo': {'title': 'Responsabilidade Civil e Processo Administrativo', 'questions': []}
    }

    for idx, q in enumerate(admin_questions, start=1):
        mod_key, mod_title = classify_admin(q)
        
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
            "fundamentacao": "<p>Legislação de Direito Administrativo (Lei nº 14.133/2021, Lei nº 8.429/92, Lei nº 9.784/99, CF/88).</p>",
            "dica": "<p>Observe os princípios da Administração Pública e o regramento legal e doutrinário aplicável.</p>",
            "aula_comentario": f"<p>Comentário em vídeo referente ao {q.get('exame_label')}.</p>",
            "analise": f"<p>Análise detalhada das alternativas A, B, C e D em desenvolvimento.</p>"
        }

        modules[mod_key]['questions'].append(card_q)

    base_dir = '/home/sfy/Corujinha/ADMINISTRATIVO'
    for mod_key, data in modules.items():
        json_path = os.path.join(base_dir, f"{mod_key}_questoes.json")
        with open(json_path, 'w', encoding='utf-8') as fp:
            json.dump(data['questions'], fp, ensure_ascii=False, indent=2)
        print(f"📦 {mod_key}_questoes.json populado com {len(data['questions'])} questões.")

    print("\n🔨 Executando compilação do ecossistema Administrativo via build_admin_modules.py...")
    subprocess.run(["python3", os.path.join(base_dir, "build_admin_modules.py")], check=True)
    print("✨ Processo concluído com sucesso!")

if __name__ == '__main__':
    main()
