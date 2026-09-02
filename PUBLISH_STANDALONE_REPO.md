# Publishing this prepared repository

The chat environment cannot operate an already-open Chrome tab or inherit its login session. The connected GitHub tool available during packaging did not expose repository-creation actions.

## GitHub web route

1. Create a new public repository named `proper-hat-guessing-k5-minus-e`.
2. Do not initialize it with a README, license, or gitignore.
3. From a terminal in this extracted directory, run the commands below.

```bash
git init
git branch -M main
git add .
git commit -m "Public research disclosure v0.1: HG_P(K5-e)=8"
git remote add origin https://github.com/matthewprotti/proper-hat-guessing-k5-minus-e.git
git push -u origin main
```

If GitHub CLI is installed and authenticated, one command replaces steps 1 and 3:

```bash
gh repo create matthewprotti/proper-hat-guessing-k5-minus-e --public --source=. --remote=origin --push
```

After the push, run `python3 VERIFY_PACKAGE.py` from a fresh clone, create a `v0.1` tag/release, and attach the repository ZIP and manuscript PDF. The prior public timestamp commit `cc9f874ce1f5fa91db42c84bf3e38e8170309a8d` should remain in the README and release notes.
