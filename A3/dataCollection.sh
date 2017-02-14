#!/bin/bash

num_iterations=(100 300 1000 3000 10000 30000 100000 300000 1000000)
# num_iterations=(100 300 1000)

for i in "${num_iterations[@]}"
do
   python3 sample.py stress=high $i
done

echo

for i in "${num_iterations[@]}"
do
   python3 sample.py stress=low $i snow=true
done

echo

for i in "${num_iterations[@]}"
do
   python3 sample.py stress=high $i snow=true day=weekend
done

echo

for i in "${num_iterations[@]}"
do
   python3 sample.py humidity=high $i snow=true day=weekend stress=high
done