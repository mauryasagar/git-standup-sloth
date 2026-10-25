import subprocess

def get_git_log(repo_path=".", since="24 hours ago", max_chars=2500):
    cmd = [
        "git", "-C", repo_path, "log",
        f"--since={since}",
        "--pretty=format:%h | %s",
        "--stat",
        "--no-merges"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    log = result.stdout.strip()
    if not log:
        return "No commits found in this period."
    return log[:max_chars]