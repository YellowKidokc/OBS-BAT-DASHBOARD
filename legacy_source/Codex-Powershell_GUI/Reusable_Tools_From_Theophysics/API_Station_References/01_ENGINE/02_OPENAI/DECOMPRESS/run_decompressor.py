#!/usr/bin/env python3
"""
LOSSLESS DECOMPRESSION - COMPANION PAPER GENERATOR

Expands compressed Theophysics notation into full academic prose.
Takes dense symbolic format (t:k|v:) and generates publication-ready text.

Usage:
    python run_decompressor.py input.md
    python run_decompressor.py input.md -o output.md

Output: Full markdown companion paper with expanded prose
"""

import sys
from pathlib import Path
from datetime import datetime

def main():
    # Check if OpenAI is installed
    try:
        from openai import OpenAI
    except ImportError:
        print("[ERROR] openai library not installed")
        print("   Install with: pip install openai")
        sys.exit(1)

    # Parse arguments
    if len(sys.argv) < 2:
        print("Usage: python run_decompressor.py <input_file> [-o output_file]")
        print("\nExample:")
        print("  python run_decompressor.py LOSSLESS_188.md")
        print("  python run_decompressor.py compressed.md -o expanded.md")
        sys.exit(1)

    input_file = Path(sys.argv[1])

    # Create OpenAI_DATA folder in the same directory as input
    data_folder = input_file.parent / "OpenAI_DATA"
    data_folder.mkdir(exist_ok=True)

    # Check for output flag
    output_file = None
    if "-o" in sys.argv and len(sys.argv) > sys.argv.index("-o") + 1:
        output_file = Path(sys.argv[sys.argv.index("-o") + 1])
    else:
        # Default output: OpenAI_DATA/input_filename_EXPANDED_YYYYMMDD_HHMMSS.md
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = data_folder / f"{input_file.stem}_EXPANDED_{timestamp}.md"

    # Validate input
    if not input_file.exists():
        print(f"[ERROR] Input file not found: {input_file}")
        sys.exit(1)

    # Get script directory
    script_dir = Path(__file__).parent

    # Load config
    config_file = script_dir / "config.txt"
    if not config_file.exists():
        print(f"[ERROR] config.txt not found in {script_dir}")
        print("   Create config.txt with:")
        print("   OPENAI_API_KEY=your_key_here")
        print("   MODEL=gpt-4o")
        sys.exit(1)

    config = {}
    for line in config_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            config[key.strip()] = value.strip()

    api_key = config.get("OPENAI_API_KEY")
    model = config.get("MODEL", "gpt-4o")

    if not api_key:
        print("[ERROR] OPENAI_API_KEY not found in config.txt")
        sys.exit(1)

    # Load prompt
    prompt_file = script_dir / "prompt.txt"
    if not prompt_file.exists():
        print(f"[ERROR] prompt.txt not found in {script_dir}")
        sys.exit(1)

    system_prompt = prompt_file.read_text(encoding='utf-8')

    # Read input
    print(f"📄 Reading: {input_file.name}")
    input_text = input_file.read_text(encoding='utf-8')
    input_size = len(input_text)

    # Estimate tokens (rough: 4 chars = 1 token)
    estimated_tokens = input_size // 4
    print(f"   Input size: {input_size:,} chars (~{estimated_tokens:,} tokens)")

    if estimated_tokens > 100000:
        print("[WARNING] Large input. May require multiple API calls.")

    # Call OpenAI
    print(f"\n[AI] Calling OpenAI ({model})...")
    print(f"   Decompressing into full prose...")
    print(f"   This may take 1-2 minutes for large documents...")

    try:
        client = OpenAI(api_key=api_key)

        # Reasoning models (gpt-5-*) use max_completion_tokens, others use max_tokens
        token_param = {}
        if model.startswith("gpt-5"):
            token_param["max_completion_tokens"] = int(config.get("MAX_TOKENS", 16000))
        else:
            token_param["max_tokens"] = int(config.get("MAX_TOKENS", 16000))

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": input_text}
            ],
            temperature=int(config.get("TEMPERATURE", 0)),
            **token_param
        )

        result_text = response.choices[0].message.content

        # Add header
        header = f"""# Companion Paper - Lossless Decompression

**Source:** {input_file.name}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Model:** {model}
**Decompressor Version:** v1.0

---

"""

        full_output = header + result_text

        # Check for continuation marker
        if "CONTINUATION NEEDED" in result_text:
            print("\n[WARNING] Note: Document requires continuation")
            print("   OpenAI hit token limit. Run again on remaining elements.")

        # Save output
        output_file.write_text(full_output, encoding='utf-8')
        output_size = len(full_output)

        # Display summary
        print(f"\n[OK] Decompression complete!")
        print(f"[OUTPUT] Saved: {output_file.name}")
        print(f"   Output size: {output_size:,} chars (~{output_size // 4:,} tokens)")
        print(f"   Expansion ratio: {output_size / input_size:.1f}x")

    except Exception as e:
        print(f"\n[ERROR] calling OpenAI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
