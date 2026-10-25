import argparse
import subprocess
import sys
from datetime import datetime
from gitdata import get_git_log
from llm import generate_standup

def copy_to_clipboard(text):
    try:
        if sys.platform == "darwin":
            subprocess.run("pbcopy", input=text, text=True, check=True)
        elif sys.platform.startswith("linux"):
            subprocess.run(["xclip", "-selection", "clipboard"],
                           input=text, text=True, check=True)
        elif sys.platform == "win32":
            subprocess.run("clip", input=text, text=True, check=True, shell=True)
        print("Copied to clipboard")
    except Exception:
        pass

def main():
    parser = argparse.ArgumentParser(description="Git Standup Sloth")
    parser.add_argument("--repo", default=".", help="Path to git repo")
    parser.add_argument("--since", default="24 hours ago", help="Time window")
    parser.add_argument("--output", default=None, help="Save to markdown file")
    args = parser.parse_args()

    print("Reading git log...")
    log = get_git_log(args.repo, args.since)

    print("Asking the sloth...")
    standup = generate_standup(log)

    print("\n" + "=" * 40)
    print(standup)
    print("=" * 40)

    copy_to_clipboard(standup)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(f"# Standup - {datetime.now().strftime('%Y-%m-%d')}\n\n")
            f.write(standup)
        print(f"\nSaved to {args.output}")

if __name__ == "__main__":
    main()