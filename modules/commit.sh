#!/bin/bash
git ls-remote https://github.com/pcm-dpc/COVID-19.git HEAD | awk '{ print $1}' > files/commit_covid.txt