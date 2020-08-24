# Git Cheat Sheet
### GIT BASICS
|                             |                                                                 |
| --------------------------- | :-------------------------------------------------------------: |
| `git init <directory>`      |          Create empty Git repo in specified directory.          |
| `git clone <repo>`          |        Clone repo located at <repo> onto local machine.         |
| `git add <directory>`       |      Stage all changes in <directory> for the next commit.      |
| `git commit -m "<message>"` |                   Commit the staged snapshot.                   |
| `git status`                |      List which files are staged, unstaged, and untracked.      |
| `git log`                   |   Display the entire commit history using the default format.   |
| `git diff`                  | Show unstaged changes between your index and working directory. |


### GIT BRANCHES
|                            |                                                    |
| -------------------------- | :------------------------------------------------: |
| `git branch`               |       List all of the branches in your repo.       |
| `git checkout -b <branch>` | Create and check out a new branch named. <branch>. |
| `git merge <branch>`       |      Merge <branch> into the current branch.       |


### REMOTE REPOSITORIES
|                               |                                                                        |
| ----------------------------- | :--------------------------------------------------------------------: |
| `git fetch <remote> <branch>` |              Fetches a specific <branch>, from the repo.               |
| `git pull <remote>`           |          Fetch the specified remote’s copy of current branch.          |
| `git push <remote> <branch>`  | Push the branch to <remote>, along with necessary commits and objects. |
