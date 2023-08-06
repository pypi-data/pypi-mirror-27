# BgReference #

bgreference is a library to fast retrive Genome Reference partial sequences.

## Install using CONDA
```
conda install -c bbglab bgreference
```

## or install using PIP
```
pip install bgreference
```

## Usage example

```
#!python
from bgreference import hg19, hg38

# Get 10 bases from chromosome one build hg19
tenbases_hg19 = hg19('1', 12345, size=10)

# Get 10 bases from chromosome one builg hg38
tenbases_hg38 = hg38('1', 12345, size=10)

# Use synonymous sequence names

hg19(2, 23456)
hg19('2', 23456)
hg19('chr2', 23456)

hg19('MT', 234, size=3)
hg19('chrM', 234, size=3)
hg19('chrMT', 234, size=3)
hg19('M', 234, size=3)

```