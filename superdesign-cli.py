#!/usr/bin/env python3
"""
Superdesign CLI - Claude Code ile UI tasarımı üret
Kullanım: python3 superdesign-cli.py "Design a login page"
"""

import subprocess
import sys
import os
import re

SYSTEM_PROMPT = """You are a senior front-end designer. Create a COMPLETE HTML file.

RULES:
1. Output ONLY the HTML code - no explanations before or after
2. Use Tailwind CSS: <script src="https://cdn.tailwindcss.com"></script>
3. Use Lucide icons: <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>
4. Use Google Fonts (Inter, Poppins, DM Sans)
5. NO images - use CSS placeholders only
6. Avoid blue/indigo colors unless specified
7. Use 4pt/8pt spacing system
8. Make it responsive (mobile, tablet, desktop)
9. Use modern dark or light theme
10. Add subtle shadows, rounded corners, smooth transitions

Output the complete HTML starting with <!DOCTYPE html> and ending with </html>.
DO NOT include any text before or after the HTML code."""

def get_next_filename(base_name: str, output_dir: str) -> str:
    """Get next available filename with incrementing number."""
    os.makedirs(output_dir, exist_ok=True)

    n = 1
    while True:
        filename = f"{base_name}_{n}.html"
        filepath = os.path.join(output_dir, filename)
        if not os.path.exists(filepath):
            return filename
        n += 1

def extract_html(text: str) -> str:
    """Extract HTML from Claude's response."""
    # Try to find HTML between DOCTYPE and </html>
    match = re.search(r'(<!DOCTYPE html>.*?</html>)', text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1)

    # Try to find HTML starting with <html>
    match = re.search(r'(<html.*?</html>)', text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1)

    # If text starts with <!DOCTYPE or <html, return as is
    text = text.strip()
    if text.lower().startswith('<!doctype') or text.lower().startswith('<html'):
        return text

    return None

def run_superdesign(prompt: str, output_dir: str = ".superdesign/design_iterations"):
    """Run Claude Code with Superdesign system prompt."""

    # Extract design name from prompt
    words = prompt.lower().replace("design", "").replace("create", "").replace("make", "")
    words = words.replace("a ", "").replace("an ", "").replace("the ", "")
    words = words.replace("modern ", "").replace("simple ", "").replace("beautiful ", "")
    base_name = "_".join(words.split()[:2]) or "design"
    base_name = "".join(c for c in base_name if c.isalnum() or c == "_")
    base_name = base_name.strip("_") or "design"

    filename = get_next_filename(base_name, output_dir)
    filepath = os.path.join(output_dir, filename)

    full_prompt = f"{SYSTEM_PROMPT}\n\nCreate: {prompt}"

    print(f"\n🎨 Superdesign CLI")
    print(f"📝 Prompt: {prompt}")
    print(f"📁 Output: {filepath}")
    print(f"\n⏳ Claude Code çalışıyor...\n")

    try:
        # Run Claude Code and capture output
        result = subprocess.run(
            ["claude", "-p", full_prompt],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__)) or ".",
            timeout=120
        )

        output = result.stdout.strip()

        # Extract HTML from response
        html = extract_html(output)

        if html:
            # Ensure output directory exists
            os.makedirs(output_dir, exist_ok=True)

            # Write HTML to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)

            print(f"✅ Tasarım oluşturuldu: {filepath}")
            print(f"\n🌐 Tarayıcıda açmak için:")
            print(f"   xdg-open {filepath}")
            return filepath
        else:
            print("⚠️  HTML çıktısı alınamadı.")
            print("\nClaude Code çıktısı:")
            print("-" * 40)
            print(output[:1000] if len(output) > 1000 else output)
            print("-" * 40)
            return None

    except subprocess.TimeoutExpired:
        print("❌ Zaman aşımı (120s)")
        return None
    except FileNotFoundError:
        print("❌ Claude Code CLI bulunamadı!")
        print("   Yüklemek için: npm install -g @anthropic-ai/claude")
        return None
    except Exception as e:
        print(f"❌ Hata: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("🎨 Superdesign CLI - Claude Code ile UI tasarımı üret")
        print("\nKullanım:")
        print("  python3 superdesign-cli.py \"Design a modern login page\"")
        print("\nÖrnekler:")
        print("  - \"Design a calculator UI\"")
        print("  - \"Create a chat interface\"")
        print("  - \"Design a music player with dark theme\"")
        print("  - \"Create a pricing table\"")
        print("  - \"Design a dashboard with stats cards\"")
        sys.exit(1)

    prompt = " ".join(sys.argv[1:])
    run_superdesign(prompt)

if __name__ == "__main__":
    main()
