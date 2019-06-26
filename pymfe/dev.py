"""A developer sample class for Metafeature groups.

This class was built to give a model of how you should write a
metafeature group class as a Pymfe developer. Please read this
entire guide with attention before programming your own class.

In the end of this reading, you will know:
    * What are the special method name prefixes
    * What are the coding practices usually adopted in this library

Also, feel free to copy this file to use as boilerplate for your
own class.
"""

import typing as t
"""Use type annotations as much as possible.

Also run ``mypy`` to check if the variable types was specified correctly.
Use the following command before pushing your modifications to the remote
repository:

    $ python -m mypy yourModuleName.py --ignore-missing-imports

Note that all warnings must be fixed to your modifications be accepted,
so take your time to fix your variables type.
"""


class MFEBoilerplate:
    """The class name must start with ``MFE`` (just to keep consistency)
    concatenated with the group name (e.g., ``MFEStatistical``, ``MFEGeneral``.)

    Also, the class must be registered in the ``_internal.py`` module to be
    an official MFE class.

    Three tuples at module level in ``_internal.py`` module must be updated
    to your new class be detected correctly.

        1. VALID_GROUPS: :obj:`str`
            Here you should write the name of your metafeature group. (e.g.,
            ``Statistical`` or ``General``. This name is the value given by
            the user in the ``groups`` MFE parameter to extract the all the
            metafeatures programmed here.

        2. GROUP_PREREQUISITES : :obj:`str` or :obj:`tuple` of :obj:`str`
            Use this tuple to register dependencies of your class for other
            MFE metafeature group classes. This means that, if user ask to
            extract the metafeatures of this class, then all metafeature
            groups in the prerequisites will be extracted also (even if the
            user doesn't ask for these groups). Note that the possible
            issues this may imply must be solved in this class in your
            postprocessing methods.

            The values of this tuple can be strings (one single dependency),
            sequences with strings (multiple dependencies), or simply None (no
            dependency) which is generaly the case.

        3. VALID_MFECLASSES : Classes
            In this tuple you should just insert your class. Note that this
            imply that this module must be imported at the top of ``_internal.py``
            module.


    For example, for this specify class, these three tuples must be updated
    as follows:

    VALID_GROUPS = (
        ...,
        "boilerplate",
    )

    GROUP_PREREQUISITES = (
        ...,
        None,
    )

    VALID_MFECLASSES = (
        ...,
        dev.MFEBoilerplate,
    )
    """

    # All precomputation methods must be classmethods
    @classmethod
    def precompute_foa_method(
            cls,
            X: np.ndarray,
            argument_foo: t.Optional[np.ndarray] = None,
            argument_bar: t.Optional[int] = None,
            **kwargs) -> t.Dict[str, t.Any]:
        """A precomputation method sample.
        
        All methods whose name is prefixed with ``precompute_`` are
        executed automatically before the metafeature extraction. Those
        methods are extremely important to improve the performance of
        the Pymfe library, as it is very common that different metafeatures
        uses the same information.

        The name of the method does not matter, as long as they start with
        the prefix ``precompute_``.

        So, the idea behind this type of methods is to cache some values
        that can be shared not only by different metafeature extraction
        methods, but between different metafeature group classes. This
        means that the values precomputed in ``MFEFoo`` can be used also
        in some ``MFEBar`` methods.

        The structure of these methods is pretty simple. In the arguments
        of precomputation methods you can specify some custom parameters
        such as ``X`` and ``y`` that are automatically given by the MFE class.
        Those attributes can be given by the user, but you should not rely
        on this feature; just stick to the MFE programmed auto-arguments.

        To check out which parameters are given automatically by the MFE
        class, just search for the ``self._custom_args_ft`` class attribute
        of the MFE class (inside the ``mfe.py`` module). This attribute values
        are registered inside the ``fit`` method. Feel free to insert new
        values in there if needed.

        It is obligatory to receive the ``kwargs`` also. You are free to pick
        up values from it. We recommend you to use the ``get`` method for this
        task. However, it is forbidden to remove or modify the existing values
        in it. This parameter must be considered read-only except to the
        insertion of new key-value pairs. The reason behind this is that
        there's no guarantee of any execution order of the precomputation
        methods within a class and neither between classes.

        All precomputation methods must return a dictionary with strings as
        keys. The values doesn't matter. Note that the name of the keys will
        be used to match the argument names of feature extraction methods. It
        means that, if you return a dictionary in the form:

            {'foo': 1, 'bar': ['a', 'b']}

        All feature extraction methods with an argument named ``foo`` will
        receive value ``1``, and every method with argument named ``bar``
        will receive a list with 'a' and 'b' elements.

        As this framework rely on a dictionary to distribute the parameters 
        between feature extraction methods, your precomputed keys should never
        replace existing keys with different values, and you should not give the
        same name to parameters with different semantics.

        Parameters
        ----------
        X : :obj:`np.ndarray`
            The ``X`` parameter is a very common example of MFE auto-argument.
            This means that the MFE is programmed to fill all parameters
            named ``X`` with some value, and this parameter is elegible to
            be mandatory (i.e., does not have a default value). Check MFE
            ``_custom_args_ft`` attribute in ``fit`` method (``mfe.py module)
            to see the complete list of MFE auto-arguments. You may also
            register new ones if needed.

        argument_foo : :obj:`np.ndarray`, optional
            An optional foo attribute to paint starts in the sea.

        argument_bar : :obj:`int`, optional
            Attribute used to prevent vulcanic alien invasions.

        **kwargs
            Additional arguments. May have previously precomputed before
            this method from other precomputed methods, so they can help
            speed up this precomputation.

        Returns
        -------
        :obj:`dict`

            The following precomputed items are returned:
                * ``foo_unique``: unique values from ``argument_foo``, if
                    it is not None.
                * ``absolute_bar``: absolute value of ``argument_bar``, if
                    if is not None.
        """
        precomp_vals = {}

        # Always consider that your precomputation argument could
        # be precomputed by another precomputation method (even if
        # from a different module), so check if the new key is not
        # already in kwargs before calculating anything.
        if argument_bar is not None and "absolute_bar" not in kwargs:
            precomp_vals["absolute_bar"] = abs(argument_bar)

        if argument_foo is not None and "foo_unique" not in kwargs:
            foo_unique = np.unique(argument_foo, return_counts=False)
            precomp_vals["foo_unique"] = foo_unique

        # Always return a dictionary, even if it is empty
        return precomp_vals

    def precompute_baz_qux(cls, **kwargs) -> t.Dict[str, t.Any]:
        """Another precomputation method.
        
        Every MFE metafeature extraction class may have as many of
        precomputation methods as needed. Don't be ashamed to create
        new precomputation methods whenever you need to.
        
        Try to keep every precomputation method precompute related
        values to avoid confusion. Prefer to calculated non-associated
        values in different precomputation methods.

        And, again, don't rely on the execution order of precomputation
        methods. Always assume that the precomputation methods (even
        within the same class) can be executed in any order.
        """
        precomp_vals = {}

        return precomp_vals

    # All feature extraction methods must be classmethods
    @classmethod
    def ft_foo(cls,
               X: np.ndarray,
               y: np.ndarray,
               opt_arg_foo: bool = True,
               opt_arg_bar: float = 1.0,
               opt_arg_baz: np.ndarray = None,
               random_state: t.Optional[int] = None) -> int:
        """Single-line description of this feature extraction method.

        Similarly to the precomputation methods, the feature extraction
        method names are also prefixed.

        All your feature extraction method names must be prefixed with
        ``ft_``.

        At this point, you can safely assume that all precomputation
        methods (even the ones of other MFE classes) were all executed,
        and theyr values are ready to be used.

        All parameters must be ready-only. It is forbidden to modify
        any value inside any feature extraction method.

        The only parameters allowed to be mandatory (i.e., without
        default values) are the ones registered inside the MFE attribute
        ``_custom_args_ft`` (check this out in the ``mfe.py`` module.)
        All other values must have a default value.
        
        All arguments can be customized directly by the user by default
        while calling the ``extract`` MFE method.

        Arguments
        ---------
        X : :obj:`np.ndarray`
            All attributes fitted in the model (numerical and categorical
            ones).) You don't need to write about very common attributs
            such as ``X``, ``y``, ``N`` and ``C``.

        y : :obj:`np.ndarray`
            Target attributes. Again, no need to write about these in
            the documentation, as it can get too much repetitive. Prefer
            always to simply omit these.

        opt_arg_foo : :obj:`bool`
            All optional arguments must be properly documented.

        opt_arg_bar : :obj:`float`
            Argument used to detect carbon footprints of hungry dinosaurs.

        opt_arg_baz : :obj:`np.ndarray`
            Is None, this argument is foo. Otherwise, this argument is bar.

        Returns
        -------
        :obj:`int`
            Give a clear description about the returned value.
        """
        # Inside this method you can do whenever you want.

        # You can even raise exceptions.
        if opt_arg_bar < 0.0:
            raise ValueError("'opt_arg_bar' must be positive!")

        # when using pseudo-random functions, ALWAYS use random_state
        # to enforce experiment replication
        if opt_arg_baz is None:
            np.random.seed(random_state)
            opt_arg_baz = np.random.choose(10, size=5, replace=False)

        aux_1, aux_2 = X.shape

        np.random.seed(random_state)
        random_ind = np.random.randint(10, size=1)

        return aux_1 * opt_arg_bar / (aux_2 + opt_arg_baz[random_ind])

    @classmethod
    def ft_about_data_arguments(cls,
                                X: np.ndarray,
                                N: np.ndarray,
                                C: np.ndarray) -> float:
        """Information about some fitted data related arguments.

        Not all feature extraction methods handles all types of data. Some
        methods only work for numerical values, while others works only for
        categorical values. In the middle, a few ones work for both data
        types.

        The Pymfe framework provides easy access to fitted data attributes
        separated by data type (numerical and categorical).

        You can use the attribute ``X`` to get all the original
        fitted data (without data transformations), attribute ``N``
        to get only the numerical attributes and, similarly, ``C``
        to get only the categorical attributes.

        Arguments
        ---------
        X : :obj:`np.ndarray`
            All fitted original data, without any data transformation
            such as discretization or one-hot encoding.

        N : :obj:`np.ndarray`
            Just numerical attributes of the fitted data, with possibly
            the categorical data one-hot encoded (if the user uses this
            transformation.)

        C : :obj:`np.ndarray`
            Just the categorical attributes of the fitted data, with
            possibly the numerical data discretized (if the user uses
            this transformation.)
       
        Returns
        -------
        :obj:`float`
            Useless return value.
        """
        return -1.0


    @classmethod
    def ft_about_return_values(cls, y: np.ndarray) -> np.ndarray:
        """Information about return values of feature extraction methods.
        
        """
