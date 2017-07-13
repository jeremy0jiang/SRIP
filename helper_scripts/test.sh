#!/bin/bash
for i in {"01","02","03","04"}; do
    echo $i
    printf $i.format"already exists\n"
done

