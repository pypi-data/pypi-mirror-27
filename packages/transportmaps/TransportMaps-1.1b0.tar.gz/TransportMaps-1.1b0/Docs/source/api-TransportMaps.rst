API - TransportMaps
===================

**Sub-modules**

.. toctree::
   :maxdepth: 1

   api-TransportMaps-FiniteDifference
   api-TransportMaps-Distributions
   api-TransportMaps-Functionals
   api-TransportMaps-Likelihoods
   api-TransportMaps-Maps
   api-TransportMaps-Algorithms
   api-TransportMaps-Diagnostics
   api-TransportMaps-Samplers
   api-TransportMaps-XML
   api-TransportMaps-CLI
   api-TransportMaps-tests
   api-TransportMaps-Densities


**Classes**


.. inheritance-diagram:: TransportMaps.TMO TransportMaps.SumChunkReduce TransportMaps.TupleSumChunkReduce TransportMaps.TensorDotReduce TransportMaps.ExpectationReduce TransportMaps.TupleExpectationReduce
   :parts: 1


========================================================================================  ===============================================================================
Class                                                                                     Description
========================================================================================  ===============================================================================
`TMO <api-TransportMaps.html\#TransportMaps.TMO>`_                                        Base object for every object in the module.
`SumChunkReduce <api-TransportMaps.html\#TransportMaps.SumChunkReduce>`_                  Define the summation of the chunks operation.
`TupleSumChunkReduce <api-TransportMaps.html\#TransportMaps.TupleSumChunkReduce>`_        Define the summation of the chunks operation over list of tuples.
`TensorDotReduce <api-TransportMaps.html\#TransportMaps.TensorDotReduce>`_                Define the reduce tensordot operation carried out through the mpi_eval function
`ExpectationReduce <api-TransportMaps.html\#TransportMaps.ExpectationReduce>`_            Define the expectation operation carried out through the mpi_eval function
`TupleExpectationReduce <api-TransportMaps.html\#TransportMaps.TupleExpectationReduce>`_  Define the expectation operation applied on a tuple
========================================================================================  ===============================================================================


**Functions**

====================================================================================================================================================================  ================================================================================================================================================================================
Function                                                                                                                                                              Description
====================================================================================================================================================================  ================================================================================================================================================================================
`deprecate <api-TransportMaps.html\#TransportMaps.deprecate>`_
`setLogLevel <api-TransportMaps.html\#TransportMaps.setLogLevel>`_                                                                                                    Set the log level for all existing and new objects related to the TransportMaps module
`get_mpi_pool <api-TransportMaps.html\#TransportMaps.get_mpi_pool>`_                                                                                                  Get a pool of ``n`` processors
`mpi_eval <api-TransportMaps.html\#TransportMaps.mpi_eval>`_                                                                                                          Interface for the parallel evaluation of a generic function on points ``x``
`generate_total_order_midxs <api-TransportMaps.html\#TransportMaps.generate_total_order_midxs>`_                                                                      Generate a total order multi-index
`kl_divergence <api-TransportMaps.html\#TransportMaps.kl_divergence>`_                                                                                                Compute :math:`\mathcal{D}_{KL}(\pi_1 | \pi_2)`
`grad_a_kl_divergence <api-TransportMaps.html\#TransportMaps.grad_a_kl_divergence>`_                                                                                  Compute :math:`\nabla_{\bf a}\mathcal{D}_{KL}(\pi_1 | \pi_{2,{\bf a}})`
`hess_a_kl_divergence <api-TransportMaps.html\#TransportMaps.hess_a_kl_divergence>`_                                                                                  Compute :math:`\nabla^2_{\bf a}\mathcal{D}_{KL}(\pi_1 | \pi_{2,{\bf a}})`
`tuple_grad_a_kl_divergence <api-TransportMaps.html\#TransportMaps.tuple_grad_a_kl_divergence>`_                                                                      Compute :math:`\left(\mathcal{D}_{KL}(\pi_1 | \pi_{2,{\bf a}}),\nabla_{\bf a}\mathcal{D}_{KL}(\pi_1 | \pi_{2,{\bf a}})\right)`
`action_hess_a_kl_divergence <api-TransportMaps.html\#TransportMaps.action_hess_a_kl_divergence>`_                                                                    Evaluate action of :math:`\nabla^2_{\bf a}\mathcal{D}_{KL}(\pi_1 | \pi_{2,{\bf a}})` on vector :math:`v`.
`storage_hess_a_kl_divergence <api-TransportMaps.html\#TransportMaps.storage_hess_a_kl_divergence>`_                                                                  Assemble :math:`\nabla^2_{\bf a}\mathcal{D}_{KL}(\pi_1 | \pi_{2,{\bf a}})`.
`kl_divergence_component <api-TransportMaps.html\#TransportMaps.kl_divergence_component>`_                                                                            Compute :math:`-\sum_{i=0}^m f(x_i) = -\sum_{i=0}^m \log\pi\circ T_k(x_i) + \log\partial_{x_k}T_k(x_i)`
`grad_a_kl_divergence_component <api-TransportMaps.html\#TransportMaps.grad_a_kl_divergence_component>`_                                                              Compute :math:`-\sum_{i=0}^m \nabla_{\bf a}f[{\bf a}](x_i) = -\sum_{i=0}^m \nabla_{\bf a} \left(\log\pi\circ T_k[{\bf a}](x_i) + \log\partial_{x_k}T_k[{\bf a}](x_i)\right)`
`hess_a_kl_divergence_component <api-TransportMaps.html\#TransportMaps.hess_a_kl_divergence_component>`_                                                              Compute :math:`-\sum_{i=0}^m \nabla^2_{\bf a}f[{\bf a}](x_i) = -\sum_{i=0}^m \nabla^2_{\bf a} \left(\log\pi\circ T_k[{\bf a}](x_i) + \log\partial_{x_k}T_k[{\bf a}](x_i)\right)`
`misfit_squared <api-TransportMaps.html\#TransportMaps.misfit_squared>`_                                                                                              Compute :math:`\vert f_1 - f_2 \vert^2`
`grad_a_misfit_squared <api-TransportMaps.html\#TransportMaps.grad_a_misfit_squared>`_                                                                                Compute :math:`\nabla_{\bf a}\vert f_{1,{\bf a}} - f_2 \vert^2`
`hess_a_misfit_squared <api-TransportMaps.html\#TransportMaps.hess_a_misfit_squared>`_                                                                                Compute :math:`\nabla^2_{\bf a}\vert f_{1,{\bf a}} - f_2 \vert^2`
`L2_misfit <api-TransportMaps.html\#TransportMaps.L2_misfit>`_                                                                                                        Compute :math:`\Vert f_1 - f_2 \Vert_{L^2_\pi}`
`L2squared_misfit <api-TransportMaps.html\#TransportMaps.L2squared_misfit>`_                                                                                          Compute :math:`\Vert f_1 - f_2 \Vert^2_{L^2_\pi}`
`grad_a_L2squared_misfit <api-TransportMaps.html\#TransportMaps.grad_a_L2squared_misfit>`_                                                                            Compute :math:`\nabla_{\bf a}\Vert f_{1,{\bf a}} - f_2 \Vert^2_{L^2_\pi}`
`hess_a_L2squared_misfit <api-TransportMaps.html\#TransportMaps.hess_a_L2squared_misfit>`_                                                                            Compute :math:`\nabla^2_{\bf a}\Vert f_{1,{\bf a}} - f_2 \Vert^2_{L^2_\pi}`
`storage_hess_a_L2squared_misfit <api-TransportMaps.html\#TransportMaps.storage_hess_a_L2squared_misfit>`_                                                            Assemble :math:`\nabla^2_{\bf a}\Vert f_{1,{\bf a}} - f_2 \Vert^2_{L^2_\pi}`.
`action_hess_a_L2squared_misfit <api-TransportMaps.html\#TransportMaps.action_hess_a_L2squared_misfit>`_                                                              Evaluate the action of :math:`\nabla^2_{\bf a}\Vert f_{1,{\bf a}} - f_2 \Vert^2_{L^2_\pi}` on :math:`v`.
`grad_t_kl_divergence <api-TransportMaps.html\#TransportMaps.grad_t_kl_divergence>`_                                                                                  Compute :math:`\nabla_T \mathcal{D}_{KL}(\pi_1, \pi_2(T))`.
`grad_x_grad_t_kl_divergence <api-TransportMaps.html\#TransportMaps.grad_x_grad_t_kl_divergence>`_                                                                    Compute :math:`\nabla_x \nabla_T \mathcal{D}_{KL}(\pi_1, \pi_2(T))`.
`laplace_approximation <api-TransportMaps.html\#TransportMaps.laplace_approximation>`_                                                                                Compute the Laplace approximation of the distribution :math:`\pi`.
`laplace_approximation_withBounds <api-TransportMaps.html\#TransportMaps.laplace_approximation_withBounds>`_                                                          Compute the Laplace approximation of the distribution :math:`\pi`.
`maximum_likelihood <api-TransportMaps.html\#TransportMaps.maximum_likelihood>`_                                                                                      Compute the maximum likelihood of the log-likelihood :math:`\log\pi({\bf y}\vert{\bf x})`.
`Default_IsotropicIntegratedExponentialTriangularTransportMap <api-TransportMaps.html\#TransportMaps.Default_IsotropicIntegratedExponentialTriangularTransportMap>`_  Generate a triangular transport map with default settings.
`Default_IsotropicIntegratedExponentialDiagonalTransportMap <api-TransportMaps.html\#TransportMaps.Default_IsotropicIntegratedExponentialDiagonalTransportMap>`_      Generate a diagonal transport map with default settings.
`Default_IsotropicIntegratedSquaredTriangularTransportMap <api-TransportMaps.html\#TransportMaps.Default_IsotropicIntegratedSquaredTriangularTransportMap>`_          Generate a triangular transport map with default settings.
`Default_IsotropicIntegratedSquaredDiagonalTransportMap <api-TransportMaps.html\#TransportMaps.Default_IsotropicIntegratedSquaredDiagonalTransportMap>`_              Generate a diagonal transport map with default settings.
`Default_IsotropicMonotonicLinearSpanTriangularTransportMap <api-TransportMaps.html\#TransportMaps.Default_IsotropicMonotonicLinearSpanTriangularTransportMap>`_      Generate a triangular transport map with default settings.
`Default_IsotropicLinearSpanTriangularTransportMap <api-TransportMaps.html\#TransportMaps.Default_IsotropicLinearSpanTriangularTransportMap>`_                        Generate a triangular transport map with default settings.
`Default_LinearSpanTriangularTransportMap <api-TransportMaps.html\#TransportMaps.Default_LinearSpanTriangularTransportMap>`_                                          Generate a linear span triangular transport map with default settings and user defined sparsity and orders.
====================================================================================================================================================================  ================================================================================================================================================================================

**Documentation**

.. automodule:: TransportMaps
   :members:

