# Inconsistencies between Verilator and other simulators for register initial values

To reproduce the experiment, run:

```
python3 experiment.py
```

The result will appear in `result.txt` and is as below:

Row ID | Clock polarity | Reset polarity | Data value | Clock value | Reset value | Output bit (Verilator) | Output bit (Icarus) | Output bit (Commercial)
-------|----------------|----------------|------------|-------------|-------------|------------------------|---------------------|----------------------
0      | 0              | 0              | 0          | 0           | 0           | 0                      | 1                   | 1                       
1      | 0              | 0              | 0          | 0           | 1           | 0                      | 0                   | 0                       
2      | 0              | 0              | 0          | 1           | 0           | 0                      | 1                   | 1                       
3      | 0              | 0              | 0          | 1           | 1           | 0                      | x                   | x                       
4      | 0              | 0              | 1          | 0           | 0           | 0                      | 1                   | 1                       
5      | 0              | 0              | 1          | 0           | 1           | 0                      | 1                   | 1                       
6      | 0              | 0              | 1          | 1           | 0           | 0                      | 1                   | 1                       
7      | 0              | 0              | 1          | 1           | 1           | 0                      | x                   | x                       
8      | 0              | 1              | 0          | 0           | 0           | 0                      | 1                   | 1                       
9      | 0              | 1              | 0          | 0           | 1           | 0                      | 0                   | 0                       
10     | 0              | 1              | 0          | 1           | 0           | 0                      | x                   | x                       
11     | 0              | 1              | 0          | 1           | 1           | 0                      | 0                   | 0                       
12     | 0              | 1              | 1          | 0           | 0           | 0                      | 1                   | 1                       
13     | 0              | 1              | 1          | 0           | 1           | 0                      | 1                   | 1                       
14     | 0              | 1              | 1          | 1           | 0           | 0                      | x                   | x                       
15     | 0              | 1              | 1          | 1           | 1           | 0                      | 1                   | 1                       
16     | 1              | 0              | 0          | 0           | 0           | 0                      | 1                   | 1                       
17     | 1              | 0              | 0          | 0           | 1           | 0                      | x                   | x                       
18     | 1              | 0              | 0          | 1           | 0           | 0                      | 1                   | 1                       
19     | 1              | 0              | 0          | 1           | 1           | 0                      | 0                   | 0                       
20     | 1              | 0              | 1          | 0           | 0           | 0                      | 1                   | 1                       
21     | 1              | 0              | 1          | 0           | 1           | 0                      | x                   | x                       
22     | 1              | 0              | 1          | 1           | 0           | 0                      | 1                   | 1                       
23     | 1              | 0              | 1          | 1           | 1           | 0                      | 1                   | 1                       
24     | 1              | 1              | 0          | 0           | 0           | 0                      | x                   | x                       
25     | 1              | 1              | 0          | 0           | 1           | 0                      | 0                   | 0                       
26     | 1              | 1              | 0          | 1           | 0           | 0                      | 1                   | 1                       
27     | 1              | 1              | 0          | 1           | 1           | 0                      | 0                   | 0                       
28     | 1              | 1              | 1          | 0           | 0           | 0                      | x                   | x                       
29     | 1              | 1              | 1          | 0           | 1           | 0                      | 1                   | 1                       
30     | 1              | 1              | 1          | 1           | 0           | 0                      | 1                   | 1                       
31     | 1              | 1              | 1          | 1           | 1           | 0                      | 1                   | 1                       