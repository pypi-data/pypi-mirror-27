Building Transport Maps
=======================

Before exploring the capabilities of the software we need to set some notation and definitions.

**Notation and definitions**

Let :math:`\nu_\rho` and :math:`\nu_\pi` be two distributions which are absolutely 
continuos with respect to the Lebesgue measure, 
with densities :math:`\rho:\mathbb{R}^d \rightarrow \mathbb{R}_+` and 
:math:`\pi:\mathbb{R}^d \rightarrow \mathbb{R}_+` respectively.

A **transport map** is a map :math:`T:\mathbb{R}^d \rightarrow \mathbb{R}^d` such that 
:math:`\nu_\rho(A) = \nu_\pi(T(A))` for every measurable :math:`A` :cite:`Villani2009`.   
For this transport we will say that :math:`T` *pushes forward* :math:`\nu_\rho` to :math:`\nu_\pi`
and write :math:`T_\sharp \nu_\rho = \nu_\pi`.  
Equivalently we will say that :math:`T` *pulls back* :math:`\nu_\pi` to :math:`\nu_\rho`
and write :math:`T^\sharp \nu_\pi = \nu_\rho`.

Under the assumed conditions the distribution :math:`T_\sharp \nu_\rho` is 
absolutely continuous with respect to the Lebesgue measure and its density is defined by 
:cite:`Bogachev2005`

.. math::

   T_\sharp \rho({\bf x}) := \rho \circ T^{-1}({\bf x}) \; \left\vert \nabla T^{-1} \right\vert = \pi({\bf x})

In the same way :math:`T^\sharp \nu_\pi = \nu_\rho` has the density

.. math::

   T^\sharp \pi({\bf x}) := \pi \circ T({\bf x}) \; \left\vert \nabla T \right\vert = \rho({\bf x})

We focus here exclusively on invertible transports (set :math:`\mathcal{T}`) and mainly (but not only) on Knothe-Rosenblatt rearrangements :cite:`Knothe1957`, :cite:`Rosenblatt1952`, i.e lower triangular ones:

.. math::

   T({\bf x}) = \left[
   \begin{array}{l}
   T_1(x_1) \\
   T_2(x_1, x_2) \\
   \;\;\;\vdots\\
   T_d(x_1,\ldots,x_d)
   \end{array}
   \right] \;.

We denote the set of Knothe-Rosenblatt rearrangements by :math:`\mathcal{T}_\triangle \subset \mathcal{T}`. Under the assumed contions, there always exist :math:`T\in\mathcal{T}_\triangle` such that :math:`T_\sharp \pi_1 = \pi_2` (and :math:`T^\sharp \pi_2 = \pi_1`).

**Contents**

The following examples are designed to drive you through the capabilities of the software. We start with some simple ones and we build up on them when we move toward more complex problems. The user is thus suggested to go through each of the examples in an ordered way.

.. toctree::
   :maxdepth: 2

   examples-direct-transport.rst
   examples-transport-from-samples.rst
