#! /bin/bash

find inputfiles -name "*.gz" | xargs gunzip -c
