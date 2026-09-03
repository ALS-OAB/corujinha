import re
import sys

def clean_vtt(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    clean_lines = []
    seen = set()

    for line in lines:
        # Ignore VTT headers, timestamps, positioning metadata
        line_s = line.strip()
        if not line_s or line_s.startswith('WEBVTT') or '-->' in line_s or line_s.startswith('Kind:') or line_s.startswith('Language:'):
            continue
        
        # Remove HTML/formatting tags
        line_clean = re.sub(r'<[^>]+>', '', line_s).strip()
        
        if line_clean and line_clean not in seen:
            clean_lines.append(line_clean)
            seen.add(line_clean)

    # Group into readable paragraphs
    text = " ".join(clean_lines)
    
    # Write cleanly to transcript markdown
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Transcrição Integral: Módulo 03 - Incompatibilidades e Impedimentos\n\n")
        f.write(f"**Fonte:** Gran OAB - Prof.ª Maria Christina\n\n")
        f.write("---\n\n")
        
        # Split text into chunks of ~500 chars for readability
        words = text.split()
        chunk = []
        for word in words:
            chunk.append(word)
            if len(chunk) > 60 and word.endswith(('.', '!', '?', ';')):
                f.write(" ".join(chunk) + "\n\n")
                chunk = []
        if chunk:
            f.write(" ".join(chunk) + "\n\n")

if __name__ == '__main__':
    vtt_in = sys.argv[1]
    md_out = sys.argv[2]
    clean_vtt(vtt_in, md_out)
    print(f"Transcrição gerada em: {md_out}")
