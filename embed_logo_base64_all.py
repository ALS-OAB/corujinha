import os
import glob
import base64

def main():
    logo_path = '/home/sfy/Corujinha/assets/oab-nc.png'
    if not os.path.exists(logo_path):
        print(f"Error: {logo_path} not found.")
        return

    with open(logo_path, 'rb') as f:
        logo_bytes = f.read()
        b64_str = base64.b64encode(logo_bytes).decode('utf-8')

    b64_src = f"data:image/png;base64,{b64_str}"
    print(f"Base64 string generated ({len(b64_str)} bytes).")

    # 1. Update all HTML files
    html_files = glob.glob('/home/sfy/Corujinha/**/*.html', recursive=True)
    print(f"Processing {len(html_files)} HTML files...")

    updated_html_count = 0
    for file_path in html_files:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        new_content = content
        
        # Replace header-badge with img tag
        new_content = new_content.replace(
            '<span class="header-badge">OAB</span>',
            f'<img src="{b64_src}" alt="OAB Nacional" style="height: 32px; width: auto; object-fit: contain;">'
        )
        
        # Replace brand-mark with img tag
        new_content = new_content.replace(
            '<div class="brand-mark">OAB</div>',
            f'<img src="{b64_src}" alt="OAB Nacional" style="height: 38px; width: auto; object-fit: contain;">'
        )

        # Replace src="oab-nc.png" with base64 data URI
        new_content = new_content.replace('src="oab-nc.png"', f'src="{b64_src}"')

        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            updated_html_count += 1

    print(f"Successfully updated {updated_html_count} / {len(html_files)} HTML files with embedded Base64 logo.")

    # 2. Update all build scripts
    py_files = glob.glob('/home/sfy/Corujinha/**/build_*.py', recursive=True)
    print(f"Processing {len(py_files)} Python build scripts...")

    updated_py_count = 0
    for file_path in py_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content = content

        # Check if OAB_LOGO_BASE64 constant is in py script
        if 'OAB_LOGO_BASE64 =' not in new_content:
            # Insert OAB_LOGO_BASE64 definition near imports
            lines = new_content.split('\n')
            insert_idx = 0
            for idx, l in enumerate(lines):
                if l.startswith('import ') or l.startswith('from '):
                    insert_idx = idx + 1
            lines.insert(insert_idx, f'OAB_LOGO_BASE64 = "{b64_src}"')
            new_content = '\n'.join(lines)

        # Replace template strings in py script
        new_content = new_content.replace(
            '<span class="header-badge">OAB</span>',
            '<img src="{OAB_LOGO_BASE64}" alt="OAB Nacional" style="height: 32px; width: auto; object-fit: contain;">'
        )
        new_content = new_content.replace('src="oab-nc.png"', 'src="{OAB_LOGO_BASE64}"')
        new_content = new_content.replace("src='oab-nc.png'", "src='{OAB_LOGO_BASE64}'")

        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            updated_py_count += 1

    print(f"Successfully updated {updated_py_count} / {len(py_files)} Python build scripts.")

if __name__ == '__main__':
    main()
