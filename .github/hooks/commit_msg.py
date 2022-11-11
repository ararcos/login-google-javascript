#!/usr/bin/env python
import sys


def main():
    with open(sys.argv[1], "r", encoding="utf-8") as f_p:
        lines = f_p.readlines()

        for commit_msg in lines:

            if commit_msg.strip() == "# ------------------------ >8 ------------------------":
                break

            if commit_msg[0] == "#":
                continue
            if (
                commit_msg.startswith("fix:")
                or commit_msg.startswith("feat:")
                or commit_msg.startswith("refactor:")
                or commit_msg.startswith("test:")
            ):
                return sys.exit(0)
                # you can return true let commit go
            else:
                print(
                    """Commit error: The commit message should start with 'fix:', 'feat:',
                'refactor:', 'test:'"""
                )

                return sys.exit(1)



if __name__ == "__main__":
    main()
