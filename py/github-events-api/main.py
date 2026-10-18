
import sys
import requests
from collections import defaultdict

BASE_URL = "https://api.github.com"


def get_commit_count(repo, before, head):
    if not before or not head or set(before) == {"0"}:
        return None

    url = f"{BASE_URL}/repos/{repo}/compare/{before}...{head}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json().get("total_commits")
    except (requests.RequestException, ValueError):
        return None


def get_event_info(event):
    event_type = event.get("type")
    repo = event.get("repo", {}).get("name", "unknown repository")
    payload = event.get("payload") or {}

    if event_type == "PushEvent":
        commits = payload.get("commits")
        count = (
            len(commits)
            if commits is not None
            else get_commit_count(
                repo, payload.get("before"), payload.get("head")
            )
        )
        return (repo, "push", count)

    if event_type == "WatchEvent":
        return (repo, "star", None)

    if event_type == "PublicEvent":
        return (repo, "public", None)

    if event_type == "IssuesEvent":
        action = payload.get("action", "updated")
        return (repo, f"issue:{action}", None)

    if event_type == "PullRequestEvent":
        action = payload.get("action", "updated")
        return (repo, f"pr:{action}", None)

    if event_type == "ForkEvent":
        return (repo, "fork", None)

    if event_type == "CreateEvent":
        return (repo, "create", None)

    if event_type == "ReleaseEvent":
        return (repo, "release", None)

    return None


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <github_username>")
        return

    username = sys.argv[1]

    try:
        response = requests.get(
            f"{BASE_URL}/users/{username}/events",
            timeout=10,
        )
        response.raise_for_status()
        events = response.json()

        groups = defaultdict(int)
        unknown_counts = defaultdict(int)

        for event in events:
            info = get_event_info(event)

            if info is None:
                continue

            repo, action, count = info
            key = (repo, action)

            if action == "push":
                if count is not None:
                    groups[key] += count
                else:
                    unknown_counts[key] += 1
            else:
                groups[key] += 1

        if not groups:
            print("No supported recent activity found.")
            return

        for (repo, action), count in groups.items():
            if action == "push":
                if unknown_counts[(repo, action)]:
                    print(f"- Pushed {count} known commits to {repo}"
                          if count else f"- Pushed commits to {repo}")
                else:
                    word = "commit" if count == 1 else "commits"
                    print(f"- Pushed {count} {word} to {repo}")

            elif action == "star":
                print(f"- Starred {repo}")

            elif action == "public":
                print(f"- Made {repo} public")

            elif action.startswith("issue:"):
                status = action.split(":", 1)[1]
                print(f"- {status.capitalize()} an issue in {repo}")

            elif action.startswith("pr:"):
                status = action.split(":", 1)[1]
                print(f"- {status.capitalize()} a pull request in {repo}")

            elif action == "fork":
                print(f"- Forked {repo}")

            elif action == "create":
                print(f"- Created something in {repo}")

            elif action == "release":
                print(f"- Published a release in {repo}")

    except requests.HTTPError as error:
        if error.response is not None and error.response.status_code == 404:
            print("GitHub user not found.")
        else:
            print(f"GitHub API error: {error}")

    except (requests.RequestException, ValueError) as error:
        print(f"Request failed: {error}")


if __name__ == "__main__":
    main()
