"""Module dedicated to extraction of Model-Based Metafeatures.
"""

from collections import Counter
import typing as t
import numpy as np
from sklearn.tree import DecisionTreeClassifier


class MFEModelBased:
    """Keep methods for metafeatures of ``model-based`` group.

    The convention adopted for metafeature extraction related methods is to
    always start with ``ft_`` prefix to allow automatic method detection. This
    prefix is predefined within ``_internal`` module.

    All method signature follows the conventions and restrictions listed below:

    1. For independent attribute data, ``X`` means ``every type of attribute``,
       ``N`` means ``Numeric attributes only`` and ``C`` stands for
       ``Categorical attributes only``. It is important to note that the
       categorical attribute sets between ``X`` and ``C`` and the numerical
       attribute sets between ``X`` and ``N`` may differ due to data
       transformations, performed while fitting data into MFE model,
       enabled by, respectively, ``transform_num`` and ``transform_cat``
       arguments from ``fit`` (MFE method).

    2. Only arguments in MFE ``_custom_args_ft`` attribute (set up inside
       ``fit`` method) are allowed to be required method arguments. All other
       arguments must be strictly optional (i.e., has a predefined
       default value).

    3. The initial assumption is that the user can change any optional
       argument, without any previous verification of argument value or its
       type, via kwargs argument of ``extract`` method of MFE class.

     4. The return value of all feature extraction methods should be a single
        value or a generic Sequence (preferably a :obj:`np.ndarray`)
        type with numeric values.

    There is another type of method adopted for automatic detection. It is
    adopted the prefix ``precompute_`` for automatic detection of these
    methods. These methods run while fitting some data into an MFE model
    automatically, and their objective is to precompute some common value
    shared between more than one feature extraction method. This strategy is a
    trade-off between more system memory consumption and speeds up of feature
    extraction. Their return value must always be a dictionary whose keys are
    possible extra arguments for both feature extraction methods and other
    precomputation methods. Note that there is a share of precomputed values
    between all valid feature-extraction modules (e.g., ``class_freqs``
    computed in module ``statistical`` can freely be used for any
    precomputation or feature extraction method of module ``landmarking``).
    """

    @classmethod
    def precompute_model_based_class(cls, N: np.ndarray, y: np.ndarray,
                                     random_state: t.Optional[int],
                                     **kwargs) -> t.Dict[str, t.Any]:
        """Precompute ``model``, ``table`` and ``tree_depth``.

        Parameters
        ----------
        N : :obj:`np.ndarray`
            Attributes from fitted data.

        y : :obj:`np.ndarray`
            Target attribute from fitted data.

        random_state : :obj:`int`, optional
            If int, random_state is the seed used by the random number
            generator; If RandomState instance, random_state is the random
            number generator; If None, the random number generator is the
            RandomState instance used by np.random.

        kwargs:
            Additional arguments. May have previously precomputed before this
            method from other precomputed methods, so they can help speed up
            this precomputation.

        Returns
        -------
        dict
            With following precomputed items:
                - ``model`` (:obj:`DecisionTreeClassifier`): decision tree
                  classifier.
                - ``table`` (:obj:`np.ndarray`): tree property table.
                - ``tree_depth`` (:obj: `np.ndarray`): the depth of each tree
                  node ordered by node (e.g., index one contain the node one
                  depth, the index two the node two depth and so on).
        """
        prepcomp_vals = {}  # type: t.Dict[str, t.Any]

        if N is not None and y is not None\
           and not {"model", "table", "tree_depth"}.issubset(kwargs):
            model = DecisionTreeClassifier(random_state=random_state)
            model.fit(N, y)
            table = MFEModelBased.extract_table(N, y, model)
            tree_depth = MFEModelBased.tree_depth(model)
            prepcomp_vals["model"] = model
            prepcomp_vals["table"] = table
            prepcomp_vals["tree_depth"] = tree_depth

        return prepcomp_vals

    @classmethod
    def extract_table(cls, N: np.ndarray, y: np.ndarray,
                      model: DecisionTreeClassifier) -> np.ndarray:
        """Precompute ``model``, ``table`` and ``tree_depth``.

        Parameters
        ----------
        N : :obj:`np.ndarray`
            Attributes from fitted data.

        y : :obj:`np.ndarray`
            Target attribute from fitted data.

        random_state : :obj:`int`, optional
            If int, random_state is the seed used by the random number
            generator; If RandomState instance, random_state is the random
            number generator; If None, the random number generator is the
            RandomState instance used by np.random.

        kwargs:
            Additional arguments. May have previously precomputed before this
            method from other precomputed methods, so they can help speed up
            this precomputation.

        Returns
        -------
        :obj:`np.ndarray`
            Tree property table.
                - Each line represents a node.
                - Column 0: It is the id of the attributed splited in that
                  node.
                - Column 1: It is 1 if the node is a leaf node, otherwise 0.
                - Columns 2: It is the number of examples that fall on that
                  node.
                - Columns 3: It is 0 if the node is not a leaf, otherwise is
                  the class number represented by that leaf node.
        """
        table = np.zeros((model.tree_.node_count, 4))  # type: np.ndarray
        table[:, 0] = model.tree_.feature
        table[:, 2] = model.tree_.n_node_samples

        leaves = model.apply(N)  # type: DecisionTreeClassifier
        if not isinstance(y, np.number):
            _, y = np.unique(y, return_inverse=True)
        tmp = np.array([leaves, y + 1])  # type: np.ndarray

        x = 0  # type: int
        for x in set(leaves):
            table[x, 3] = list(Counter(tmp[1, tmp[0, :] == x]).keys())[0] + 1
            table[x, 1] = 1

        return table

    @classmethod
    def ft_leaves(cls, table: np.ndarray) -> int:
        """Number of leaves of the DT model.

        Parameters
        ----------
        table : :obj:`np.ndarray`
            Tree property table.

        Returns
        -------
        :obj:`np.ndarray`
            Number of leaves.
        """

        return np.sum(table[:, 1], dtype=int)

    @classmethod
    def ft_tree_depth(cls, tree_depth: np.ndarray) -> np.ndarray:
        """Tree depth, which is the level of all tree nodes and leaves of the
        DT model.

        Parameters
        ----------
        tree_depth : :obj:`np.ndarray`
            Tree depth from ``tree_depth`` method.

        Returns
        -------
        :obj:`np.ndarray`
            Tree depth.
        """

        return tree_depth

    @classmethod
    def tree_depth(cls, model: DecisionTreeClassifier) -> np.ndarray:
        """Compute the depth of each node.

        Parameters
        ----------
        model : :obj:`DecisionTreeClassifier`
            The DT model.

        Returns
        -------
        :obj:`np.ndarray`
            The depth of each node.
        """

        def node_depth(node: int, depth: int, l, r, depths: t.List[int]):
            depths += [depth]
            if l[node] != -1 and r[node] != -1:
                node_depth(l[node], depth + 1, l, r, depths)
                node_depth(r[node], depth + 1, l, r, depths)

        depths = []  # type: t.List[int]
        node_depth(0, 0, model.tree_.children_left, model.tree_.children_right,
                   depths)
        return np.array(depths)

    @classmethod
    def ft_leaves_branch(cls, table: np.ndarray,
                         tree_depth: np.ndarray) -> np.ndarray:
        """Size of branches, which consists in the level of all leaves of the
        DT model.

        Parameters
        ----------
        table : :obj:`np.ndarray`
            Tree property table.

        tree_depth : :obj:`np.ndarray`
            Tree depth from ``tree_depth`` method.

        Returns
        -------
        :obj:`np.ndarray`
            Size of branches.
        """

        return tree_depth[table[:, 1] == 1]

    @classmethod
    def ft_leaves_corrob(cls, N: np.ndarray, table: np.ndarray) -> np.ndarray:
        """Leaves corroboration, which is the proportion of examples that
        belong to each leaf of the DT model.

        Parameters
        ----------
        N : :obj:`np.ndarray`
            Attributes from fitted data.

        table : :obj:`np.ndarray`
            Tree property table.

        Returns
        -------
        :obj:`np.ndarray`
            Leaves corroboration.
        """
        return table[:, 2][table[:, 1] == 1] / N.shape[0]

    @classmethod
    def ft_tree_shape(cls, table: np.ndarray,
                      tree_depth: np.ndarray) -> np.ndarray:
        """Tree shape, which is the probability of arrive in each leaf given a
        random walk. We call this as the structural shape of the DT model.

        Parameters
        ----------
        table : :obj:`np.ndarray`
            Tree property table.

        tree_depth : :obj:`np.ndarray`
            Tree depth from ``tree_depth`` method.

        Returns
        -------
        :obj:`np.ndarray`
            The tree shape.
        """
        aux = tree_depth[table[:, 1] == 1]  # type: np.ndarray
        return -(1.0 / 2**aux) * np.log2(1.0 / 2**aux)

    @classmethod
    def ft_leaves_homo(cls, table: np.ndarray,
                       tree_depth: np.ndarray) -> np.ndarray:
        """Homogeneity, which is the number of leaves divided by the structural
        shape of the DT model.

        Parameters
        ----------
        table : :obj:`np.ndarray`
            Tree property table.

        tree_depth : :obj:`np.ndarray`
            Tree depth from ``tree_depth`` method.

        Returns
        -------
        :obj:`np.ndarray`
            The homogeneity.
        """
        leaves = MFEModelBased.ft_leaves(table)  # type: int
        tree_shape = MFEModelBased.ft_tree_shape(
            table, tree_depth)  # type: np.ndarray
        return leaves / tree_shape

    @classmethod
    def ft_leaves_per_class(cls, table: np.ndarray) -> np.ndarray:
        """Leaves per class, which is the proportion of leaves of the DT model
        associated with each class.

        Parameters
        ----------
        table : :obj:`np.ndarray`
            Tree property table.

        Returns
        -------
        :obj:`np.ndarray`
            Leaves per class.
        """
        aux = np.array(list(Counter(table[:, 3]).values()))  # np.ndarray
        aux = aux[1:] / MFEModelBased.ft_leaves(table)
        return aux

    @classmethod
    def ft_nodes(cls, table: np.ndarray) -> int:
        """Number of nodes of the DT model.

        Parameters
        ----------
        table : :obj:`np.ndarray`
            Tree property table.

        Returns
        -------
        :obj:`np.ndarray`
            Number of nodes.
        """
        return np.sum(table[:, 1] != 1)

    @classmethod
    def ft_nodes_per_attr(cls, N: np.ndarray, table: np.ndarray) -> float:
        """Ratio of the number of nodes of the DT model per the number of
        attributes.

        Parameters
        ----------
        N : :obj:`np.ndarray`
            Attributes from fitted data.

        table : :obj:`np.ndarray`
            Tree property table.

        Returns
        -------
        :obj:`np.ndarray`
            Ratio of the number of nodes.
        """
        nodes = MFEModelBased.ft_nodes(table)  # type: int
        attr = N.shape[1]  # type: float
        return nodes / attr

    @classmethod
    def ft_nodes_per_inst(cls, N: np.ndarray, table: np.ndarray) -> float:
        """Ratio of the number of nodes of the DT model per the number of
        instances.

        Parameters
        ----------
        N : :obj:`np.ndarray`
            Attributes from fitted data.

        table : :obj:`np.ndarray`
            Tree property table.

        Returns
        -------
        :obj:`np.ndarray`
            Ratio of the number of nodes per instances.
        """
        nodes = MFEModelBased.ft_nodes(table)  # type: int
        inst = N.shape[0]  # type: float
        return nodes / inst

    @classmethod
    def ft_nodes_per_level(cls, table: np.ndarray,
                           tree_depth: np.ndarray) -> float:
        """Number of nodes of the DT model per level.

        Parameters
        ----------
        table : :obj:`np.ndarray`
            Tree property table.

        tree_depth : :obj:`np.ndarray`
            Tree depth from ``tree_depth`` method.

        Returns
        -------
        :obj:`np.ndarray`
            Number of nodes per level.
        """
        aux = tree_depth[table[:, 1] == 0]  # type: np.ndarray
        aux = np.array(list(Counter(aux).values()))
        return aux

    @classmethod
    def ft_nodes_repeated(cls, table: np.ndarray) -> np.ndarray:
        """Repeated nodes, which is the number of repeated attributes that
        appear in the DT model.

        Parameters
        ----------
        table : :obj:`np.ndarray`
            Tree property table.

        Returns
        -------
        :obj:`np.ndarray`
            Repeated nodes.
        """
        aux = table[:, 0][table[:, 0] > 0]  # type: np.ndarray
        aux = np.array(list(Counter(aux).values()))
        return aux

    @classmethod
    def ft_var_importance(cls, model: DecisionTreeClassifier) -> np.ndarray:
        """Features importance. It is calculated using the Gini index to
        estimate the amount of information used in the DT model.

        Parameters
        ----------
        model : :obj:`DecisionTreeClassifier`
            The DT model.

        Return:
        :obj:`np.ndarray`
            Features importance.
        """
        importance = model.tree_.compute_feature_importances()  # np.ndarray
        return importance

    @classmethod
    def ft_tree_imbalance(cls, table: np.ndarray,
                          tree_depth: np.ndarray) -> np.ndarray:
        """Tree imbalance.

        Parameters
        ----------
        table : :obj:`np.ndarray`
            Tree property table.

        tree_depth : :obj:`np.ndarray`
            Tree depth from ``tree_depth`` method.

        Returns
        -------
        :obj:`np.ndarray`
            Tree imbalance values.
        """
        aux = 1.0 / 2**tree_depth[table[:, 1] == 1]  # np.ndarray
        tmp = np.unique(aux, return_counts=True)  # np.ndarray
        tmp = tmp[0] * tmp[1]
        return -(1.0 / 2**tmp) * np.log2(1.0 / 2**tmp)
