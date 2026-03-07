When reporting an issue and especially submitting a pull request, please
make sure that you are acquainted with Contributor Guidelines:

https://github.com/micropython/micropython/wiki/ContributorGuidelines

as well as the Code Conventions, which includes details of how to commit:

https://github.com/micropython/micropython/blob/master/CODECONVENTIONS.md

## Fixing commit messages

The CI checks every commit message in a pull request against the rules in
`CODECONVENTIONS.md`. If a check fails, follow the steps below to correct
the messages and push the fix.

### Check locally before pushing

Run the checker on the commits in your branch before pushing:

```bash
# Check the last N commits (replace N with the number of commits in your PR)
python tools/verifygitlog.py -N
```

A passing run prints `ok`. Failures are listed as:

```
error: commit <sha>: <description of the problem>
```

### Fix the most recent commit

If only the last commit needs fixing:

```bash
git commit --amend -s
# -s adds or keeps the Signed-off-by line
# Your editor opens — update the message, save and close
```

Then force-push your branch:

```bash
git push --force-with-lease
```

### Fix an older commit with interactive rebase

If a commit further back in history needs fixing:

```bash
# Rebase the last N commits interactively
git rebase -i HEAD~N
```

In the editor that opens, change `pick` to `reword` (or `r`) on each line
whose message needs editing. Save and close. Git will pause at each marked
commit and open your editor — update the message, save and close, and the
rebase continues.

Once all messages are correct, verify locally:

```bash
python tools/verifygitlog.py -N
```

Then force-push:

```bash
git push --force-with-lease
```

### Commit message example

```
path/to/changed/file: Short description ending with a full stop.

Optional longer description that explains the change in detail.
Each line should be 75 characters or fewer.

Signed-off-by: Your Name <you@example.com>
```


### Common mistakes and how to fix them

| Error message | Fix |
|---|---|
| `Subject line is too long (X characters, max 72)` | Shorten the first line to 72 characters or fewer, add additional lines if needed |
| `Subject prefix cannot begin with "." or "/"` | Use the module/directory name only, e.g. `extmod/foo` not `./extmod/foo` |
| `must end with "."` | Add a full stop at the end of the first line |
| `must start with "path: "` | Add a path prefix, e.g. `py/objstr: Fix …` |
| `Message must be signed-off` | Add `-s` to your commit command, or amend with `git commit --amend -s`,. The signature must be on the last line of the commit message.|
| `Unwanted email address` | Configure a real email address: `git config user.email you@example.com` |


