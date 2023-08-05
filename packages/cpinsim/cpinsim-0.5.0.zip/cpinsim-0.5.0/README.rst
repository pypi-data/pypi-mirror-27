README
======

CPINSim - Constrained Protein Interaction Networks Simulator
-------------------------------------------------------------

CPINSim is a package for the simulation of constrained protein interaction networks. Beside simulation of complex formation in a cell there are methods for data preprocessing provided:  Annotation of interactions and constraints with domains; A parser to provide the needed protein input format.


Features
~~~~~~~~

-  Annotate interactions and constraints with domains: Infer domains from known ones where possible, set unique artificial domains otherwise.
- Parse the interaction and constraints files into a protein-wise text representation as input for the simulation.
- Simulate the complex formation in a cell for the given input proteins with regard to the interaction dependencies which are encoded as constraints. Further, the simulation of perturbation effects like knockout or overexpression of one or multiple proteins is possible.


System requirements
~~~~~~~~~~~~~~~~~~~

-  `python3 <http://www.python.org/>`__
-  `networkx <http://networkx.github.io/>`__
-  `scipy <http://www.scipy.org/>`__
-  `bitarray <http://pypi.python.org/pypi/bitarray>`__


Installation
~~~~~~~~~~~~

We recommend the installation using conda:

.. code-block:: shell

    $ conda create -n cpinsim -c bioconda cpinsim
    $ source activate cpinsim

    # You now have a 'cpinsim' script; try it:
    $ cpinsim --help

    # To switch back to your normal environment, use
    $ source deactivate

Alternatively, you can download the source code from `github <http://github.com/BiancaStoecker/cpinsim>`_ and install it using the setup script:

.. code-block:: shell

   $ git clone http://github.com/BiancaStoecker/cpinsim.git cpinsim
   $ cd cpinsim
   /cpinsim python setup.py install

In this case you have to install the requirements listed above.


Platform support
~~~~~~~~~~~~~~~~

CPINSim is a pure Python program. This means that it runs on any operating system (OS) for which Python 3 and the other packages are available.


Example usage
~~~~~~~~~~~~~

The needed input file ``proteins_extended_adhesome.csv`` can be downloaded from the git repository via

.. code-block:: shell

    wget https://raw.githubusercontent.com/BiancaStoecker/cpinsim/master/example_files/proteins_extended_adhesome.csv


**Example 1:** Simulate the complex formation for proteins ``proteins_extended_adhesome.csv`` with 100 copies per protein (``-n``). Save the simulated graph at ``simulated_graph.gz`` and some logging information about the simulation steps at ``simulation.log``.

For further parameters the default values are used.


.. code-block:: shell

    $ cpinsim simulate example_files/proteins_extended_adhesome.csv -n 100 -og simulated_graph.gz -ol simlation.log

    
**Example 2:** Simulate the complex formation as in example 1, but now knock out the protein *FYN* and overexpress the protein *ABL1* by factor 5.


.. code-block:: shell

    $ cpinsim simulate example_files/proteins_extended_adhesome.csv -n 100 -og simulated_graph_ko_FYN_oexp_ABL1.gz -ol simlation_ko_FYN_oexp_ABL1.log -p FYN 0 -p ABL1 5


To investigate the simulation results one can extract the simulation graph in a python shell and for example look at the node lists of the resulting complexes:

.. code-block:: python

    import pickle, gzip
    import networkx as nx
    
    f = gzip.open("simulated_graph.gz", "rb")
    graph = pickle.load(f)
    
    # get list of complexes sorted descendingly by their number of nodes
    complexes = sorted(list(nx.connected_component_subgraphs(graph)), key=len, reverse=True)
    for c in complexes[0:5]:
        # nodes have unique integer ids, for protein name the "name" attribut is needed
        print([c.node[node]["name"] for node in c])
    
    f.close()

With the steps above, ``complexes`` contains each protein complex as full networkx graph datastructure for further analysis. 

Additional example files for the data preprocessing steps and a full workflow including the evaluation of the simulation results will we uploaded in the near future.
 
