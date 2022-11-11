#!/usr/bin/env bash
set -e

# Colors
BLUE='\033[1;34m'
NOCOLOR='\033[0m'

# Running terraform fmt before all commits
files=$(find . -iname '*.tf' -type f | sed 's/^\.\///')
for f in $files
do
  if [ -e "$f" ] && [[ $f == *.tf ]]; then
    terraform fmt -check=true "$f" > /dev/null || {
        printf "%s ${BLUE}%s${NOCOLOR}. %s: \n\n" "Incorrectly formatted files found, running" "terraform fmt"
        printf "%s\n\n" "$(terraform fmt "$f")"
    }
  fi
done
