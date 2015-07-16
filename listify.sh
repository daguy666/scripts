#!/bin/bash

file_to_list=$1

if [ -z $file_to_list ];
    then
    echo "Usage $0 <file to listify>"
    exit 2
fi

sed -e 's/\(.*\)/"\1"/g' -e "s/$/,/g" $file_to_list
