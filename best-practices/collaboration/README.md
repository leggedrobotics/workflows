# Software Collaboration Guide

## Beginners
If you have never used git please read the following:

- Beginner Guide Git:
<https://towardsdatascience.com/an-easy-beginners-guide-to-git-2d5a99682a4c>

- Beginner Guide Git in VSCode:
<https://code.visualstudio.com/docs/editor/versioncontrol>

- Beginner Guide GitHub:
<https://medium.com/@jonathanmines/the-ultimate-github-collaboration-guide-df816e98fb67>

- Beginner GitKraken Guide:
<https://support.gitkraken.com/start-here/guide/>

## Conventions:
### Repository Naming:
We recommend lower_case separated by underscores:   

| Good: | `anymal_c_rsl`                                  |
| ----- | ----------------------------------------------- |
| Bad:  | `Anymal_c_rsl` , `anymal-c-rsl`, `ANYmal-C-RSL` |

### Branch Naming

| Branch Name:              | Description:                                                 |
| ------------------------- | ------------------------------------------------------------ |
| `main`                    | Main branch. Don`t push to it directly.                      |
| `dev/name_lower_case`     | Continue development of an existing code within the project. |
| `fix/name_lower_case`     | If you found an error and want to quickly fix it.            |
| `feature/name_lower_case` | Develop something new not part of the code base.             |

### Merging vs Rebasing

| Strategy: | Description:                                                                                           |
| --------- | ------------------------------------------------------------------------------------------------------ |
| `Merge`   | Use if preserving the complete history and chronological order of contributions is important           |
| `Rebase`  | Apply always when the `Merge` Strategy Requirements are not fulfilled to keep the `main` branch clean. |

[Read more here.](https://betterprogramming.pub/differences-between-git-merge-and-rebase-and-why-you-should-care-ae41d96237b6#:~:text=Reading%20the%20official%20Git%20manual,it%20happened%2C%20rebase%20rewrites%20it%20)


## Single Main Developer
Recommended workflows: 
- Always work on `dev` `fix` or `feature`.
- Regularly merge your code into `master`. 
- [Optionally]: Create a `pull request` with yourself as the reviewer and check everything in the `dif`-view before merging.

## Two Main Developers
- Follow Single Main Developer guide.
- Each `pull request` to main has to be approved by the other developer.

## Multiple Developers
- Add CI/CD Integration, GitHub Actions are handy.
- Automated code-formatting and checking. 
- Automated unit testing.

