# THIS FILE IS PROVIDED AS IS UNDER THE CONDITIONS DETAILED IN LICENSE
# COPYRIGHT ANDREW JOHNSON, 2017
import operator

from drewtils import parsers

__versions__ = '0.1.9'


def dfSubset(data, where):
    """
    Return a subset of the data given a series of conditions

    .. versionadded:: 0.1.9

    Parameters
    ----------
    data: :py:class:`pandas.DataFrame`:
        DataFrame to view
    where: str or list or tuple
        Conditions to apply.

    Notes
    -----

    If the argument is a string, it will be converted
    to a tuple for iteration. Items in iterable can be either a string
    or three-valued iterable of the following form::

        string: 'column operand target'
        iterable: ('column', 'operand', 'target')

    If the first-level item is a string, it will be split at spaces.
    Operands are string-representations of operators from the operator module,
    e.g.::

        'eq', 'ge', 'le', 'ne', 'gt', 'lt', 'contains'

    Returns
    -------
    view: :py:class:`pandas.DataFrame`:
        View into the data frame after successive slices

    See Also
    --------
    :py:mod:`operator`

    """
    view = data
    if isinstance(where, str):
        where = where,
    for item in where:
        if isinstance(item, str):
            cond = item.split()
        else:
            cond = item
        assert len(cond) == 3, ('Conditions should have three arguments, '
                                'not like {}'.format(item))
        evalFunc = getattr(operator, cond[1])
        view = view[evalFunc(view[cond[0]], cond[2])]
    return view
