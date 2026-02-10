import json
import argparse
from pathlib import Path

def convert_item(item, args):
    # Combine instruction + input + options
    options_joined = args.options_separator.join(item["options"]) if isinstance(item["options"], list) else item["options"]
    full_instruction = item["instruction"] + item["input"] + options_joined + """
Please respond with the following requirements:
1. **The response must be in JSON format**
2. **The JSON must contain all the options and corresponding proabilities**
Example format:
{
    "A": "prob_A",
    "B": "prob_B",
    ...
}
    """

    # Extract thinking processes
    thinking_texts = [
        tp["thinking_process"]
        for tp in item["thinking"]["thinking_processes"]
    ]
    thinking_content = "\n\n".join(thinking_texts)

    # Build thinking part with configurable tags
    thinking_part = f"{args.thinking_start}\n{thinking_content}\n{args.thinking_end}"

    output_parts = [thinking_part]

    # Optionally add distribution
    if args.include_distribution:
        if args.sort_distribution:
            sorted_items = sorted(item["options_dist"].items())
        else:
            sorted_items = item["options_dist"].items()

        if args.dist_percentage:
            dist_items = [
                f'"{k}": "{v:.{args.dist_precision}f}%"'
                for k, v in sorted_items
            ]
        else:
            dist_items = [
                f'"{k}": "{v:.{args.dist_precision}f}"'
                for k, v in sorted_items
            ]

        dist_str = args.dist_brackets[0] + ", ".join(dist_items) + args.dist_brackets[1]
        output_parts.append(dist_str)

    full_output = args.output_separator.join(output_parts)

    return {
        "instruction": full_instruction.rstrip(),
        "output": full_output
    }

def main():
    parser = argparse.ArgumentParser(
        description="Convert national pride survey JSON to instruction-tuning format with configurable thinking tags and output style."
    )

    # Input / Output
    parser.add_argument("-i", "--input", type=str, required=True, help="Path to input JSON file")
    parser.add_argument("-o", "--output", type=str, required=True, help="Path to output JSON file")

    # Thinking tags
    parser.add_argument("--thinking-start", type=str, default="<thinking>",
                        help="Start tag for thinking section (default: '<thinking>')")
    parser.add_argument("--thinking-end", type=str, default="</thinking>",
                        help="End tag for thinking section (default: '</thinking>')")

    # Distribution options
    parser.add_argument("--no-distribution", action="store_true",
                        help="Exclude the options distribution from output")
    parser.add_argument("--dist-percentage", action="store_true", default=True,
                        help="Format distribution as percentages (add '%%')")
    parser.add_argument("--no-dist-percentage", dest="dist_percentage", action="store_false",
                        help="Format distribution as raw numbers")
    parser.add_argument("--dist-precision", type=int, default=2,
                        help="Decimal places for distribution values (default: 2)")
    parser.add_argument("--no-sort-distribution", dest="sort_distribution", action="store_false", default=True,
                        help="Do not sort distribution keys (preserve original order)")
    parser.add_argument("--dist-brackets", type=str, default="{}", nargs=2, metavar=('OPEN', 'CLOSE'),
                        help="Brackets around distribution, e.g. --dist-brackets '[' ']' (default) or '(' ')'")

    # Formatting
    parser.add_argument("--options-separator", type=str, default=", ",
                        help="Separator between options in instruction (default: ', ')")
    parser.add_argument("--output-separator", type=str, default="",
                        help="Separator between thinking and distribution in output (default: newline)")

    args = parser.parse_args()
    args.include_distribution = not args.no_distribution
    if len(args.dist_brackets) != 2:
        parser.error("--dist-brackets requires exactly two arguments: open and close")

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        return

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    converted = [convert_item(item, args) for item in data]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(converted, f, indent=2, ensure_ascii=False)

    print(f"Conversion complete! {len(converted)} items saved to {output_path}")

if __name__ == "__main__":
    main()