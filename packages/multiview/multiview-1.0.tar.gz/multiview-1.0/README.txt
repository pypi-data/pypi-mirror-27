Introduction

Given a multiview dataset with ``v`` input data matrices, multiview dimensionality
reduction methods produce a single, low-dimensional projection of the input data 
samples, trying to maintain as much of the original information as possible.

Multiview learning can be thought of as an effort to adapt some of the manifold algorithms
principles to algorithms whose main inputs are multiview data. These data can be understood
as different views of the same data, so it is attempted to use these views to and all their
information for dimensionality reduction and spectral clustering.

Methods developed here are adaptions of single view algorithms to multiview data.
Also, these modules are translation from the multiview package, firstly written in
R.

MVMDS

MVMDS (Multiview Multidimensional Scaling) ia one of the approaches to dimensionality reduction that offers the class 
mvmds to perform multiview dimensionality reduction in a similar way than
the multidimensional scaling method does (similar to ``cmdscale`` in R language).
In general, it is a technique used for analyzing similarity or dissimilarity data.


MvtSNE

Another dimensionality reduction function in this package is the class :doc:`mvtsne`, that
extends the ``tsne`` algorithm (available in ``manifold`` module) to work with multiview data.
It based on the conversion of affinities of data to probabilities. The affinities
in the original space are represented by Gaussian joint probabilities and the affinities
in the embedded space are represented by Student's t-distributions.


MVSC

Given a multiview dataset with ``v`` input data matrices, multiview spectral clustering (MVSC) methods
produce a single clustering assignment, considering the information from all the 
input views.
Package ``multiview`` offers the class :doc:`mvsc` to perform multiview spectral 
clustering. It is an extension to spectral clustering (``kernlab::specc`` in R language) 
to multiview datasets.


Alternative use

Although the methods in this package have been divided in dimensionality reduction
and clustering, there is a close relationship between both tasks. In fact, all three
methods can be used for both tasks.

First, the data projection produced by dimensionality reduction methods can be
fed to a standard clustering algorithm in order to obtain a multiview clustering.
Second, as mvsc also returns the projection resulting from the k first common
eigenvectors in matrix $evectors, this space can also be used as a low-dimensional
embedding of the original multiview data, for visualization or other purposes.

References: 

  * Abbas, Ali E. 2009. "A Kullback-Leibler View of Linear and Log-Linear Pools." *Decision Analysis*
    6 (1): 25-37. doi:`10.1287/deca.1080.0133 <http://pubsonline.informs.org/doi/abs/10.1287/deca.1080.0133>`_.

  * Carvalho, Arthur, and Kate Larson. 2012. "A Consensual Linear Opinion Pool." 
    http://arxiv.org/abs/1204.5399.

  * Kruskal, J B. 1964. "Multidimensional scaling by optimizing goodness of fit to 
    a nonmetric hypothesis." *Psychometrika* 29 (1): 1\-27. doi:`10.1007/BF02289565 <https://link.springer.com/article/10.1007%2FBF02289565>`_.

  * Ng, Andrew Y, Michael I Jordan, and Yair Weiss. 2001. "On spectral clustering: 
    Analysis and an algorithm." *Nips* 14 (14). MIT Press: 849-56.

  * Planck, Max, and Ulrike Von Luxburg. 2006. "A Tutorial on Spectral Clustering." 
    *Statistics and Computing* 17 (March). Springer US: 395-416. doi
    `10.1007/s11222-007-9033-z <https://link.springer.com/article/10.1007%2Fs11222-007-9033-z>`_.

  * Shi, Jianbo, and Jitendra Malik. 2005. "Normalized Cuts and Image Segmentation 
    Normalized Cuts and Image Segmentation." *Pattern Analysis and Machine Intelligence, IEEE Transactions* 
    on 22 (March): 888-905. doi:`10.1109/CVPR.1997.609407 <http://ieeexplore.ieee.org/document/609407/?reload=true>`_.

  * Trendafilov, Nickolay T. 2010. "Stepwise estimation of common principal 
    components." *Computational Statistics and Data Analysis* 54 (12): 3446-57. 
    doi:`10.1016/j.csda.2010.03.010 <http://www.sciencedirect.com/science/article/pii/S016794731000112X?via%3Dihub>`_.

  * Van Der Maaten, Laurens, Geoffrey Hinton, and Geoffrey Hinton van der Maaten. 
    2008. "Visualizing Data using t-SNE." doi:`10.1007/s10479-011-0841-3 <https://link.springer.com/article/10.1007%2Fs10479-011-0841-3>`_.

  * Multiview features dataset. https://archive.ics.uci.edu/ml/datasets/Multiple+Features