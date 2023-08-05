# qstest
Python codes for the (q,s)-test, a generalised significance test for individual communities in networks. 

Please cite:

    Kojaku, S. and Masuda, N. "A generalised significance test for individual communities in networks". Preprint arXiv:???? (2017).

# Installation
  You can install this python package with pip, a package management system for the software written in Python.
  
  To install qstest, type

```bash 
    pip install qstest
```

  If you failed to install, then type the following command: 
	
  
```bash 
  sudo python setup.py install
```
  

## USAGE
 
 ```python
    sg, pvals = qstest(network, communities, qfunc, sfunc, cdalgorithm, num_of_rand_net = 500, alpha = 0.05, num_of_thread = 2)
 ```
 
#### Input 
* `network` - Networkx Graph class instance.
* `communities` - C-dimensional list of lists. communities[c] is a list containing the IDs of nodes belonging to community c.
* `qfunc` - Quality function of individual communities. Following quality functions are available:
    * qmod - Modularity-based quality function of individual communities, 
    * qint - Internal average degree, 
    * qexp - Expansion,　　
    * qcnd - Conductance.　

  You can use your quality function of individual communities. See ["How to pass my quality function to qstest"](#how-to-pass-my-quality-function-to-qstest).

 * `sfunc`  - Size function that computes the size of individual communities. Following size functions are available:
    * n - Number of nodes in a community, 
    * vol - Sum of degrees of nodes in a community.
    
    You can use your definition of the size of a community. See ["How to pass my size function to qstest"](#how-to-pass-my-size-function-to-qstest).
   
 * `cdalgorithm` - Community detection algorithm. Following algorithms are available:
    * louvain_algorithm - [Louvain algorithm](http://perso.crans.org/aynaud/communities/index.html),
    * label_propagation - [Label propagation algorithm](https://networkx.github.io/documentation/stable/reference/algorithms/generated/networkx.algorithms.community.asyn_lpa.asyn_lpa_communities.html#networkx.algorithms.community.asyn_lpa.asyn_lpa_communities).

    You can use your algorithm for finding communities. See ["How to pass my community detection algorithm to qstest"](#how-to-pass-my-community-detection-algorithm-to-qstest).
 
 * `num_of_rand_net` (optional)  - Number of randomised networks. (Default: 500)
 * `alpha` (optional)  - Statistical significance level before the Šidák correction. (Default: 0.05)
 * `num_of_thread` (optional) - Maximum number of threads running in a CPU. (Default: 4)
  
#### Output
 * `sg` - C-dimensional list. sg[c] = True if community c is significant, and sg[c] = False if it is insignificant. 
 * `pvals` - C-dimensional list. pvals[c] is the p-value for community c. 

#### Example
```python
import networkx as nx
import qstest as qs

network = nx.karate_club_graph()
communities = qs.louvain_algorithm(network)
sg, pvals = qs.qstest(network, communities, qs.qmod, qs.vol, qs.louvain_algorithm)
```

## How to pass my quality function to qstest
Write a function that outputs the quality of a community (a large quality value indicates a good community) as follows:

 ```python
    q = my_qfunc(network, community)
```

#### Input
 * `network` - Networkx Graph class instance, 
 * `community` - List of nodes belonging to a community.

#### Output
  * `q` - Quality of the community.

Then, pass the implemented **my_qfunc** to **qstest**:
```python
sg, pvals = qs.qstest(network, communities, my_qfunc, sfunc, cdalgorithm)
```

#### Example
```python
import networkx as nx
import qstest as qs

# Number of intra-community edges
def my_qfunc(network, nodes):
        return network.subgraph(nodes).size()

network = nx.karate_club_graph()
communities = qs.louvain_algorithm(network)
sg, pvals = qs.qstest(network, communities, my_qfunc, qs.vol, qs.louvain_algorithm)
```

## How to pass my size function to qstest 
Write a function that outputs the size of a community as follows:

```python
    sz = my_sfunc(network, community)
```

#### Input
 * `network` - Networkx Graph class instance, 
 * `community` - List of the IDs of nodes belonging to a community.

#### Output
  * `sz` - Size of the community.

Then, provide the implemented **my_sfunc** to **qstest**:
```python
sg, pvals = qs.qstest(network, communities, qfunc, my_sfunc, cdalgorithm)
```  

#### Example
```python
import networkx as nx
import qstest as qs

def my_sfunc(network, nodes):
        return len(nodes) * len(nodes)

network = nx.karate_club_graph()
communities = qs.louvain_algorithm(network)
sg, pvals = qs.qstest(network, communities, qs.qmod, my_sfunc, qs.louvain_algorithm)
```

## How to pass my community detection algorithm to qstest
To pass the community detection algorithm to qstest, write the following wrapper function:
 
 ```python
    communities = my_cdalgorithm(network)
 ```
    
#### Input 
 * `network` - Networkx Graph class instance. 

#### Output
 * `community` - List of nodes belonging to a community.

Then, provide the implemented **my_cdalgorithm** to **qstest**:
```python
sg, pvals = qs.qstest(network, communities, qfunc, sfunc, my_cdalgorithm)
```  

If the community-detection algorithm requires parameters such as the number of communities, then pass the parameters through global variables: define, for example, a global variable C, then access to C from the cdalgorithm.
  
#### Example:
```python
import networkx as nx
import qstest as qs
from networkx.algorithms import community as nxcdalgorithm

# Wrapper function for an algorithm, async_fluidc, implemented in Networkx 2.0
def my_cdalgorithm(network):
        communities = []
        subnets = nx.connected_component_subgraphs(network)
        for subnet in subnets:
                coms_iter = nxcdalgorithm.asyn_fluidc(subnet, min([C, subnet.order()]), maxiter)
                for nodes in iter(coms_iter):
                       communities.append(list(nodes))
        return communities

# Pareameters of the community-detection algorithm called from my_cdalgorithm
C = 3
maxiter = 10

network = nx.karate_club_graph()
communities = my_cdalgorithm(network)
sg, pvals = qs.qstest(network, communities, qs.qmod, qs.vol, my_cdalgorithm)
```

## REQUIREMENT: 
* Python 2.7 or later
* Networkx 2.0 or later
--- 
Last updated: 25 December 2017


