# DEVELOPMENT WORKFLOW
Welcome to the development workflow

### Basic workflow
In short:
1. Start a new feature branch for each set of edits that you do.
   First, fetch new commits from the upstream repository:
   ```
   git fetch upstream
   ```
   Then, create a new branch based on the main branch of the upstream repository:
   ```
   git checkout -b my-new-feature upstream/main
   ```
2. The Editing Workflow
   #### Overview
   ```
   # hack hack
   git status # Optional
   git diff # Optional
   git add modified_file
   git commit
   # push the branch to your own Github repo
   git push origin my-new-feature
   ```

   #### In More Detail
   1. Make some changes. When you feel that you’ve made a complete, working set of related changes, move on to the next steps.
   2. Optional: Check which files have changed with git status (see git status). You’ll see a listing like this one:
   ```
   - # On branch my-new-feature
   - # Changed but not updated:
   - #   (use "git add <file>..." to update what will be committed)
   - #   (use "git checkout -- <file>..." to discard changes in working directory)
   - #
   - #  modified:   README
   - #
   - # Untracked files:
   - #   (use "git add <file>..." to include in what will be committed)
   - #
   - #  INSTALL
   - no changes added to commit (use "git add" and/or "git commit -a")
   ```
   3. Optional: Compare the changes with the previous version using with git diff (git diff). This brings up a simple text browser interface that highlights the difference between your files and the previous version.
   4. Add any relevant modified or new files using git add modified_file (see git add). This puts the files into a staging area, which is a queue of files that will be added to your next commit. Only add files that have related, complete changes. Leave files with unfinished changes for later commits.
   5. To commit the staged files into the local copy of your repo, do git commit. At this point, a text editor will open up to allow you to write a commit message. Read the commit message section to be sure that you are writing a properly formatted and sufficiently detailed commit message. After saving your message and closing the editor, your commit will be saved. For trivial commits, a short commit message can be passed in through the command line using the -m flag. For example, git commit -am "ENH: Some message".

   In some cases, you will see this form of the commit command: git commit -a. The extra -a flag automatically commits all modified files and removes all deleted files. This can save you some typing of numerous git add commands; however, it can add unwanted changes to a commit if you’re not careful. For more information, see [why the -a flag?](http://www.gitready.com/beginner/2009/01/18/the-staging-area.html) - and the helpful use-case description in the [tangled working copy problem.](https://tomayko.com/writings/the-thing-about-git)
   6. Push the changes to your forked repo on github:
      ```
      git push origin my-new-feature
      ```
   For more information, see [git push](https://www.kernel.org/pub/software/scm/git/docs/git-push.html).
   
   ---
   ##### NOTE:
   Assuming you have followed the instructions in these pages, git will create a default link to your github repo called origin. In git >= 1.7 you can ensure that the link to origin is permanently set by using the --set-upstream option:
   ```
   git push --set-upstream origin my-new-feature
   ```
   From now on git will know that my-new-feature is related to the my-new-feature branch in your own github repo. Subsequent push calls are then simplified to the following:
   ```
   git push
   ```
   You have to use --set-upstream for each new branch that you create.

   ---

   It may be the case that while you were working on your edits, new commits have been added to upstream that affect your work. In this case, follow the Rebasing on main section of this document to apply those changes to your branch.


   ##### Writing the commit message
   Commit messages should be clear and follow a few basic rules. Example:
   ```
   ENH: add functionality X to numpy.<submodule>.

   The first line of the commit message starts with a capitalized acronym
   (options listed below) indicating what type of commit this is.  Then a blank
   line, then more text if needed.  Lines shouldn't be longer than 72
   characters.  If the commit is related to a ticket, indicate that with
   "See #3456", "See ticket 3456", "Closes #3456" or similar.
   ```
   Describing the motivation for a change, the nature of a bug for bug fixes or some details on what an enhancement does are also good to include in a commit message. Messages should be understandable without looking at the code changes. A commit message like `MAINT: fixed another one` is an example of what not to do; the reader has to go look for context elsewhere.

   Please stick to this commit message convention
   Standard acronyms to start the commit message with are:
   | Acronym | Usage |
   | ------- | ----- |
   | BLD | change related to building the project |
   | BUG | bug fix |
   | DEP | deprecate something, or remove a deprecated object |
   | DEV | development tool or utility |
   | DOC | documentation |
   | ENH | enhancement |
   | MAINT | maintenance commit (refactoring, typos, etc.) |
   | REV | revert an earlier commit |
   | STY | style fix (whitespace, PEP8) |
   | REL | related to releases |

3. When finished:
   Contributors: push your feature branch to your own Github repo, and create a pull request.