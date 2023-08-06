.. vim: set fileencoding=utf-8 :
.. Pavel Korshunov <pavel.korshunov@idiap.ch>
.. Mon 3 Apr 13:43:22 2017

============================================================
 Package for paper published in ISBA 2018 on CNN-based PADs 
============================================================


If you use this package, please cite the following paper::

    @inproceedings{KorshunovISBA2018,
        author = {Pavel Korshunov, Andr\'e Gon\c{c}alves, Ricardo Violato, Fl\'avio Sim\~oes, and S\'ebastien Marcel},
        title = {On the Use of Convolutional Neural Networks for Speech Presentation Attack Detection},
        booktitle = {International Conference on Identity, Security and Behavior Analysis (ISBA 2018)},
        year = {2018},
	month = jan,
	address = {Singapore},
    }

This package contains scripts to reproduce the results from the paper. The package is also provides score files for CNN-based and MFCC-GMM PAD systems reported in the paper.


Downloading score files
-----------------------

We are providing the score files obtained for all the  systems presented in the paper. These score files can be used to compute error rates and DET curves presented in the paper. To download the scores, please follow these steps:

.. code-block:: sh

    $ #You should be inside the package directory bob.paper.isba2018-pad-dnn
    $ wget http://www.idiap.ch/resource/biometric/data/isba2018-pad-dnn.tar.gz #Download the scores
    $ tar -xzvf isba2018-pad-dnn.tar.gz  


Reproducing results of the paper
--------------------------------

We assume that scores of the PAD systems can be found in folder `scores`. 

To compute error rates presented in the main results Table 4 of the paper, the following script should be used:

.. code-block:: sh

    $ ./compute_overall_results.sh

The script will create a folder for each configuration of PAD system and datasets. The folders contain DET curves for each given configuration (subset of these plots are shown in Figure 4 of the paper), histograms of score distributions, and error rates. The script also creates a text file 'latex_table_overall_stats_eer.txt' which contains a LaTeX formatted table with the results from Table 4 of the paper.

To compute error rates for different types of attack as presented in Table 5, please execute the following script:

.. code-block:: sh

    $ ./compute_results_per_attack.sh

The script will compute error rates for each type of attack of voicePA and BioCPqD-PA databases used in the paper and produce 'latex_table__per_attack_stats_eer.txt' file with LaTeX formatted table that has results from Table 5 of the paper.



