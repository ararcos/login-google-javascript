#!/usr/bin/env python
import sys
import subprocess
import re


def main():

    branch_name = str(
        subprocess.run(
            "git rev-parse --abbrev-ref HEAD", shell=True, check=True, stdout=subprocess.PIPE
        ).stdout
    )[2:-3]
    regular_exp = "^([A-Z]+)\/(OFI+)-([0-9]+)-([a-z]+(?:-[a-z]+)*)"
    is_valid_branch_name = re.match(regular_exp, branch_name)

    if is_valid_branch_name:
        sys.exit(0)
    else:
        print(f'''\n
        Error message:

            The following name is illegal: {branch_name}
            Please rename your branch with using the following regex: 
            {regular_exp} or CR/OFI-<number_ticket>-<title_ticket> 
            (If your name were Carlos Rodriguez - CR).
            Edit regexp if you think something wrong.
            You won't be able to push or commit your changes until the issue is solved.
            Skip hooks with --no-verify (not recommended).
            ''')
        sys.exit(1)


if __name__ == "__main__":
    main()
