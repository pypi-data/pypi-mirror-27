[![Build Status](https://travis-ci.org/hammerlab/mhcflurry.svg?branch=master)](https://travis-ci.org/hammerlab/mhcflurry) [![Coverage Status](https://coveralls.io/repos/github/hammerlab/mhcflurry/badge.svg?branch=master)](https://coveralls.io/github/hammerlab/mhcflurry?branch=master)

# mhcflurry
[MHC I](https://en.wikipedia.org/wiki/MHC_class_I) ligand
prediction package with competitive accuracy and a fast and 
[documented](http://www.hammerlab.org/mhcflurry/) implementation.

MHCflurry supports Class I peptide/MHC binding affinity prediction using
ensembles of allele-specific models. It runs on Python 2.7 and 3.4+ using
the [keras](https://keras.io) neural network library. It exposes [command-line](http://www.hammerlab.org/mhcflurry/commandline_tutorial.html)
and [Python library](http://www.hammerlab.org/mhcflurry/python_tutorial.html) interfaces.

If you find MHCflurry useful in your research please cite:

> O'Donnell, T. et al., 2017. MHCflurry: open-source class I MHC binding affinity prediction. bioRxiv. Available at: http://www.biorxiv.org/content/early/2017/08/09/174243.

## Installation (pip)

Install the package:

```
$ pip install mhcflurry
```

Then download our datasets and trained models:

```
$ mhcflurry-downloads fetch
```

You can now generate predictions:

```
$ mhcflurry-predict \
       --alleles HLA-A0201 HLA-A0301 \
       --peptides SIINFEKL SIINFEKD SIINFEKQ \
       --out /tmp/predictions.csv \
       
Wrote: /tmp/predictions.csv
```

See the [documentation](http://www.hammerlab.org/mhcflurry/) for more details.
