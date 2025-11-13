# Foundation F2 — Git Basics
*30–60 minutes | You + your repo, no team drama yet*

## Objectives
- Initialize or clone a repo
- Stage, commit, and push
- Create branches and merge safely
- Undo common mistakes

## Prerequisites
Module 3 (GitHub + SSH key).

## 1) Identity
```bash
git config --global user.name  "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
```

## 2) Start or Clone
```bash
mkdir -p ~/projects/f2 && cd ~/projects/f2
git init
echo "# F2 Demo" > README.md
git status
```

Clone instead:
```bash
cd ~/projects
git clone git@github.com:YOUR_USERNAME/REPO.git
cd REPO
```

## 3) Stage & Commit
```bash
git add README.md
git commit -m "chore: initial commit"
git log --oneline --graph --decorate --all | head
```

## 4) Remote Basics
```bash
git remote add origin git@github.com:YOUR_USERNAME/REPO.git
git push -u origin main
git remote -v
```

## 5) Branch Flow
```bash
git checkout -b feature/readme
echo "Learning Git." >> README.md
git add README.md
git commit -m "docs: add learning line"
git push -u origin feature/readme
```

Merge locally (simple fast‑forward case):
```bash
git checkout main
git pull
git merge feature/readme
git push
```

## 6) See What Changed
```bash
git status
git diff               # unstaged
git diff --staged      # staged
git log -p -n 1        # last commit patch
```

## 7) Undo Without Panic
```bash
git restore <file>                 # discard unstaged changes
git restore --staged <file>        # unstage
git commit --amend                 # edit last commit (before push)
git reset --hard HEAD~1            # drop last commit (danger)
```

## 8) Upstream (keep track of original)
```bash
git remote add upstream git@github.com:ORIGINAL/REPO.git
git fetch upstream
git merge upstream/main            # or git rebase upstream/main
```

## 9) Checkpoint
- A new branch exists on GitHub with your commit.
- `git log --oneline` shows a clean history.
- You can undo a staged file and amend a message locally.

## Exercises
1. Create a `feature/hello` branch that adds `hello.txt`; open a PR on GitHub.
2. Use `git revert <commit>` to create a reversal commit.
3. Fork a tiny repo, clone your fork, add `upstream`, and sync.

## Troubleshooting
- **Permission denied (publickey)** — re‑add SSH key (Module 3), `ssh -T git@github.com`.
- **Detached HEAD** — `git switch -c fix/detached` to save work, then merge back.
- **Merge conflicts** — `git status` shows files; edit, `git add`, and `git commit` to finish.
