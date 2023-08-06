integrated Python toolkit for pathway based analysis

[![Build Status](https://travis-ci.org/iseekwonderful/PyPathway.svg?branch=master)](https://travis-ci.org/iseekwonderful/PyPathway)
![](https://img.shields.io/badge/python-3.5-blue.svg)
![](https://img.shields.io/badge/python-3.6-blue.svg)
![](https://img.shields.io/badge/license-MIT-blue.svg)



## Installation

### General requirement
**Python version: >= 3.5**


### Windows

* The [Visual C++ 2015 Build Tools](http://landinghub.visualstudio.com/visual-cpp-build-tools) is required to compile c extensions.

* `numpy`, `scipy` and `staticmodels` (anaconda is recommend)


### Unix / Linux

* gcc or clang compiler


### Sources

* install via pypi
```
pip install pypathway
```
* install from the source
```
git clone https://github.com/iseekwonderful/PyPathway.git
cd PyPathway
python setup.py install
```

## Features
* Public databases APIs: `STRING`, `BioGRID`, `KEGG`, `Reactome` and `WikiPathway`
* Functional set based and network based enrichment analysis algorithms implemented: `ORA`, `GSEA` and `SPIA`
* Performance optimize for denovo enrichment algorithm `MAGI` and `Hotnet2`.
* Network propagation random walk, RWR and heat kernel
* Interactive visualization for pathway, graph and analysis result.
* Web page exportation for results.

## Highlights
* Integrated with pandas, networkx and numpy. Most of the methods accept both text file and data structure from these packages 
* Dynamic visualization for IPython notebook. 
* Most classes implement `__repr__` method for interactive environment.

## Network process

Intuitive APIs for querying and retrieval interaction network from public database. The return object are stored in `networkx.Graph` object.

### Support databases

* `KEGG`
* `Reactome`
* `WikiPathway`
* `STRING`
* `BioGRID`

### Search
```
from pypathway import PublicDatabase
kg = PublicDatabase.search_kegg('CD4')
wp = PublicDatabase.search_wp('CD4')
rt = PublicDatabase.search_reactome('CD4')
```

### Load

```
pathway = r[0].load()
```

### Plot

```
pathway.draw()
```

![](https://github.com/iseekwonderful/PyPathway/blob/master/docs/markdowns/images/network_process/netprocess_KEGG.png)

### IPython notebook examples

* [STRING and BioGRID](https://github.com/iseekwonderful/PyPathway/blob/master/examples/pathviz/STRING%7CBioGID_query.ipynb)
* [Pathway databases](https://github.com/iseekwonderful/PyPathway/blob/master/examples/pathviz/Pathway_Datatbase_APIs.ipynb)

## Enrichment Analysis

### Support methods

* ORA
* GSEA
* Network enrichment (SPIA and Enrichment)
* denovo enrichment (MAGI and Hotnet2)

### Implementation / Interface

* Staticmethod `run()` for the starting of the analysis
 
```python
r = SPIA.run(all=c.background, de=c.deg, organism='hsa')
```

* `table`, `plot()` and `graph()` method for the presentation of the analysis

```python
res.table

```
![](https://github.com/iseekwonderful/PyPathway/blob/master/docs/markdowns/images/enrichment/enrichment_table.png)

```python
res.plot()
```

![](https://github.com/iseekwonderful/PyPathway/blob/master/docs/markdowns/images/enrichment/enrichment_general_ora.png)
```python

res.graph()
```

![](https://github.com/iseekwonderful/PyPathway/blob/master/docs/markdowns/images/enrichment/GO%20graph%20plot.png)

### IPython examples

* [ORA](https://github.com/iseekwonderful/PyPathway/blob/master/examples/analysis/ORA.ipynb)
* [GSEA](https://github.com/iseekwonderful/PyPathway/blob/master/examples/analysis/GSEA.ipynb)
* [Network enrichment](https://github.com/iseekwonderful/PyPathway/blob/master/examples/analysis/network_enrichment.ipynb)
* [MAGI](https://github.com/iseekwonderful/PyPathway/blob/master/examples/analysis/MAGI.ipynb)
* [Hotnet2](https://github.com/iseekwonderful/PyPathway/blob/master/examples/analysis/Hotnet2.ipynb)

## Modeling

* the Python Interface and optimize for `MAGI`
* several c extension for `Hotnet permutation performance 

## Propagation

Implemented algorithms

* Random walk
```python

random_walk(G, h)
```
* Random walk with restart
```python

random_walk_with_restart(G, h, rp=0.7, n=-1)
```
* Heat kernel
```python
diffusion_kernel(G, h, rp=0.8, n=100)

```

### detail

> ![](https://github.com/iseekwonderful/PyPathway/blob/master/docs/markdowns/images/propagation/propagation_overview.png)

image source: [Network propagation: a universal amplifier of genetic associations](http://www.nature.com/nrg/journal/v18/n9/abs/nrg.2017.38.html)

### IPython notebook examples

* [Propagation](https://github.com/iseekwonderful/PyPathway/blob/master/examples/analysis/propagation.ipynb)

## Utility and Performance


* The Id converter
* GMT file manager
* network and expression data sets.
* numpy implementation of SPIA
* node swap c extension for Hotnet2
* multi-threading for MAGI


## Interactive Visualization

The interactive visualization for IPython notebook

### Feature
* `__repr__` Implemented for most classes
* dynamic visualization for networkx.Graph instance
* visualizer for pathway object
* visualizer for Gene ontology DAG.
