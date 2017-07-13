#!/bin/bash
for i in "ssqq"$(;seq -w 21 24); do
    echo $i
    printf $i.format"already exists\n"
done

