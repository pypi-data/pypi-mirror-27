Statistical Models
==================

Probability distributions are the building blocks of statistical models.
Therefore we start showing how to construct *user-defined distributions* for a set of
classical statistical inference problems.

In the following we will work with the random variable 
:math:`{\bf X} \sim \nu_\pi` defined over 
the probability space :math:`(\Omega,\mathcal{F},P)`.
The **distribution** :math:`\nu_\pi` is assumed to be absolutely continuous with 
respect to the Lebesgue measure (:math:`\nu_\pi \ll \lambda`), and thus
adimts the **density** :math:`\pi` such that 

.. math::
   
   \nu_\pi(A) = \int_A \pi({\bf x}) d{\bf x} \;,

for all :math:`\nu_\pi`-measurable sets :math:`A`.

.. toctree::
   :maxdepth: 1
   
   pm-distributions.ipynb
   pm-bayesian-inference.ipynb
   pm-data-assimilation.ipynb
