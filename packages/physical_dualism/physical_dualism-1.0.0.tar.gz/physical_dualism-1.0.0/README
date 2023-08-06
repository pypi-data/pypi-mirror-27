About
=====

Python library that approximates the natural frequency from stress via physical
dualism, and vice versa.

This work is a part of the investigation within the research project
[ON174027]_, supported by the Ministry for Science and Technology, Republic of
Serbia. This support is gratefully acknowledged.

References
----------

.. [ON174027]
   "Computational Mechanics in Structural Engineering"

Installation
============

To install physical_dualism run::

    $ pip install physical_dualism

Usage examples
==============

Quick start::

    >>> from physical_dualism import approximate_natural_frequency_from_stress

    >>> mode = 1
    >>> a = 2310.0 # [mm] strip length
    >>> sigma_cr = 19.4754 # [MPa] critical buckling stress
    >>> ro = 10000.0 / 10**9 # [kg/mm**3] mass density

    # Mass matrix expects mass density normalized to 1 [m] of length, even if everything is done in [mm]
    >>> ro /= 10**3

    # [rad/s] natural frequency approximated from critical buckling stress
    >>> print "%.4f" % approximate_natural_frequency_from_stress(mode, a, sigma_cr, ro)
    60.0179

Please see the `fsm_eigenvalue`_ source code for more examples.

.. _`fsm_eigenvalue`: https://bitbucket.org/petar/fsm_eigenvalue/src/

Contribute
==========

If you find any bugs, or wish to propose new features `please let us know`_.

If you'd like to contribute, simply fork `the repository`_, commit your changes
and send a pull request. Make sure you add yourself to `AUTHORS`_.

.. _`please let us know`: https://bitbucket.org/petar/physical_dualism/issues/new
.. _`the repository`: http://bitbucket.org/petar/physical_dualism
.. _`AUTHORS`: https://bitbucket.org/petar/physical_dualism/src/default/AUTHORS
