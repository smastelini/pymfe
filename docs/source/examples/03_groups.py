"""
03 - Extracting meta-features by group
======================================

In this example, we will show you how to select different meta-features groups.
"""

# Load a dataset
from sklearn.datasets import load_iris
from pymfe.mfe import MFE

data = load_iris()
y = data.target
X = data.data

###############################################################################
# General
# -------
#
# These are the most simple measures for extracting general properties of the
# datasets. For instance, ``nr_attr`` and ``nr_class`` are the total number of
# attributes in the dataset and the number of output values (classes) in the
# dataset, respectively. The following examples illustrate these measures:

# Extract all general measures
mfe = MFE(groups=["general"])
mfe.fit(X, y)
ft = mfe.extract()
print(ft)

# Extract only two general measures
mfe = MFE(features=["nr_attr", "nr_class"])
mfe.fit(X, y)
ft = mfe.extract()
print(ft)

###############################################################################
# Statistical
# -----------
#
# Statistical meta-features are the standard statistical measures to describe
# the numerical properties of a distribution of data. As it requires only
# numerical attributes, the categorical data are transformed to numerical. For
# instance, ``cor_cor`` and ``skewness`` are the absolute correlation between
# of each pair of attributes and the skewness of the numeric attributes in the
# dataset, respectively. The following examples illustrate these measures:

# Extract all statistical measures
mfe = MFE(groups=["statistical"])
mfe.fit(X, y)
ft = mfe.extract()
print(ft)

# Extract only two statistical measures
mfe = MFE(features=["can_cor", "cor", "iq_range"])
mfe.fit(X, y)
ft = mfe.extract()
print(ft)

###############################################################################
# Information theory
# ------------------
#
# Information theory meta-features are particularly appropriate to
# describe discrete (categorical) attributes, but they also fit continuous ones
# using a discretization process. These measures are based on information
# theory. For instance, ``class_ent`` and ``mut_inf`` are the entropy of the
# class and the common information shared between each attribute and the
# class in the dataset, respectively. The following examples illustrate these
# measures:

# Extract all info-theo measures
mfe = MFE(groups=["info-theory"])
mfe.fit(X, y)
ft = mfe.extract()
print(ft)

# Extract only two info-theo measures
mfe = MFE(features=["class_ent", "mut_inf"])
mfe.fit(X, y)
ft = mfe.extract()
print(ft)

###############################################################################
# Model based
# -----------
#
# These measures describe characteristics of the investigated models. These
# meta-features can include, for example, the description of the Decision Tree
# induced for a dataset, like its number of leaves (``leaves``) and the number
# of nodes (``nodes``) of the tree. The following examples illustrate these
# measures:

# Extract all model-based measures
mfe = MFE(groups=["model-based"])
mfe.fit(X, y)
ft = mfe.extract()
print(ft)

# Extract only two model-based measures
mfe = MFE(features=["leaves", "nodel"])
mfe.fit(X, y)
ft = mfe.extract()
print(ft)


###############################################################################
# Landmarking
# -----------
#
# Landmarking measures are simple and fast algorithms, from which performance
# characteristics can be extracted. These measures include the performance of
# simple and efficient learning algorithms like Naive Bayes (``naive_bayes``)
# and 1-Nearest Neighbor (``one_nn``). The following examples illustrate these
# measures:

# Extract all landmarking measures
mfe = MFE(groups=["landmarking"])
mfe.fit(X, y)
ft = mfe.extract()
print(ft)

# Extract only two landmarking measures
mfe = MFE(features=["one_nn", "naive_bayes"])
mfe.fit(X, y)
ft = mfe.extract()
print(ft)
