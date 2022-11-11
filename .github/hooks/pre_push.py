#!/usr/bin/env python
import re
import subprocess
import sys


def main():

    print("python-githooks > pre-push")
    print('Running tests and lint')
    return_code = subprocess.call("make lint && make test",  shell=True)
    if return_code == 0:
        print("Successful pre-push hook")
    else:
        print("Pre-push has fail. Please solve errors and try again")
        sys.exit(return_code)


    branch_name = str(subprocess.run("git rev-parse --abbrev-ref HEAD",
                      shell=True, check=True, stdout=subprocess.PIPE).stdout)[2:-3]
    regular_exp = "^([A-Z]+)\/(OFI+)-([0-9]+)-([a-z]+(?:-[a-z]+)*)"
    is_valid_branch_name = re.match(regular_exp, branch_name)

    if is_valid_branch_name:
        print("Successful branch name")
        sys.exit(return_code)
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
