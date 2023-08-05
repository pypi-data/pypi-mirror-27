.. vim: set fileencoding=utf-8 :
.. Hannah Muckenhirn <hannah.muckenhirn@idiap.ch>
.. Mon 19 Sep 11:35:15 CEST 2016

=========================================================================================================
Reproducing results of paper published in IEEE/ACM Transactions on Audio, Speech and Language Processing
=========================================================================================================
        
This package is part of the Bob_ toolkit and it allows to reproduce the following paper::

    @inproceedings{Muckenhirntaslp2017,
        author = {Muckenhirn, Hannah and Korshunov, Pavel and Magimai.-Doss, Mathew and Marcel, S{\'{e}}bastien},
        title = {Long Term Spectral Statistics for Voice Presentation Attack Detection,
        booktitle = {to appear in IEEE/ACM Transactions on Audio, Speech and Language Processing},
        year = {2017},
    }



I- Installation
--------------------
To install this package -- alone or together with other `Packages of Bob <https://gitlab.idiap.ch/bob/bob/wikis/Packages>`_ -- please read the `Installation Instructions <https://gitlab.idiap.ch/bob/bob/wikis/Installation>`_.
For Bob_ to be able to work properly, some dependent packages are required to be installed.
Please make sure that you have read the `Dependencies <https://gitlab.idiap.ch/bob/bob/wikis/Dependencies>`_ for your operating system.

.. _bob: https://www.idiap.ch/software/bob
.. _AVspoof: https://www.idiap.ch/dataset/avspoof
.. _ASVspoof: http://datashare.is.ed.ac.uk/handle/10283/853


To run all the experiments, two databases need to be downloaded: AVspoof_ and ASVspoof_. The paths to folders with the corresponding data need to be updated in the following files inside the ``bob.paper.taslp_2017/bob/paper/taslp_2017/config/database`` directory:

* asvspoof_cm.py
* avspoof_physical.py
* avspoof_logical.py

Once the databases are downloaded, the corresponding Bob's interfaces need to be updated too. Please run the following commands::

    For AVspoof database: $ ./bin/bob_dbmanage.py avspoof download 
    For ASVspoof database: $ ./bin/bob_dbmanage.py asvspoof download


II- Training systems
-----------------------
In this section, we only explain how to train the system based on Long-Term Spectral Statistics (LTSS) using a Linear Discriminant Analysis as the classifier, referred to as "LTSS, LDA" in the tables.  The system based on LTSS using a Multi-Layer Perceptron (MLP), referred to as "LTSS, MLP" in the tables, is trained with the software Quicknet_, we thus provide directly the scores obtained on the development and evaluation sets in the folder ``quicknet_mlp_scores``. All the score files for the baseline systems can be obtained by running the following commands::

$ wget http://www.idiap.ch/resource/biometric/data/interspeech_2016.tar.gz #Download the scores
$ tar -xzvf interspeech_2016.tar.gz


Training a Presentation Attack Detection (PAD) classifier is done with the script ``./bin/spoof.py`` from Bob's package ``bob.pad.base``, which takes several parameters, including:

* A database and its evaluation protocol
* A data preprocessing algorithm
* A feature extraction algorithm
* A PAD algorithm

All these steps of the PAD system are given as configuration files.

1. Experiments on one database
```````````````````````````````

To train and evaluate the aforementioned system on the same database, you need to run the following command::

$ ./bin/spoof.py -d <Database_Name> -p energy-2gauss-remove-head-tail -e <Feature_Extractor> -a lda -s <Folder_Name> --groups dev eval -vv

`<Folder_Name>` is the folder in which the results of all the subtasks and the final score files are stored. 
`<Database_Name>` can be one of the following:

* ``asvspoof-cm``
* ``avspoof-physical``
* ``avspoof-logical``


`<Feature_Extractor>` corresponds to the features to extract, which can be one of the following:

* ``mean-std-spectrum-16ms-shift-10ms``
*  ``mean-std-spectrum-32ms-shift-10ms``
*  ``mean-std-spectrum-64ms-shift-10ms`` 
*  ``mean-std-spectrum-128ms-shift-10ms``
*  ``mean-std-spectrum-256ms-shift-10ms``
*  ``mean-std-spectrum-512ms-shift-10ms``


In the paper, the feature option ``mean-std-spectrum-256ms-shift-10ms`` was used with the database options ``asvspoof-cm`` and ``avspoof-logical`` while the feature option ``mean-std-spectrum-32ms-shift-10ms`` was used with the database option ``avspoof-physical``. The other options were used to generate Figure 6.


2. Cross-database experiments
`````````````````````````````
To train the aforementioned system on one database, and evaluate it on another database, you need to run two commands::

$ ./bin/spoof.py -d <Database_Training> -p energy-2gauss-remove-head-tail -e <Feature_Extraction> -a lda -s <Folder_Name> --groups dev -vv
$ ./bin/spoof.py -d <Database_Evaluation> -p energy-2gauss-remove-head-tail -e <Feature_Extraction> -a lda -s <Folder_Name> --groups eval -vv --skip-projector-training



III- Evaluating the systems based on the score files
----------------------------------------------------

1. EER on development set, HTER on evaluation set
``````````````````````````````````````````````````

To evaluate any system, you need to run the following command::

  $ ./bin/evaluate_pad.py -d <Folder_Name_Scores>

This script will output the Equal Error Rate (EER) computed on the development set and the Half Total Error Rate (HTER) computed on the evaluation set. `<Folder_Name_Scores>` should contain exactly four score files: ``scores-dev-real``, ``scores-dev-attack``, ``scores-eval-real`` and ``scores-eval-attack``.



2. EER on evaluation set
````````````````````````````

To evaluate the systems on the ASVspoof database following the protocol used for the  "Automatic Speaker Verification Spoofing and Countermeasures Challenge" [1]_, you need to run the following command::

  $ ./bin/compute_EER_perattack_eval.py -d <Name_Scores_Eval_Real> -t <Name_Scores_Eval_Attack> -o <Output_File>

This script output the EER computed on each type of attack of the evaluation set, the average of these EERs over the known attacks, the unknown attacks and all the attacks. This script will print its output in the terminal and in the file specified by `<Output_File>`. `<Name_Scores_Eval_Real>` and `<Name_Scores_Eval_Attack>` correspond respectively to the file containing the scores of the real accesses and of the attacks of the evaluation set. 

.. _bob: https://www.idiap.ch/software/bob
.. _quicknet: http://www1.icsi.berkeley.edu/Speech/qn.html
.. [1] Z. Wu, T. Kinnunen, N. W. D. Evans, J. Yamagishi, C. Hanilci, M. Sahidullah, and A. Sizov, “ASVspoof 2015: the first automatic speaker verification spoofing and countermeasures challenge,” in Proc. of Interspeech, 2015, pp. 2037–2041.
