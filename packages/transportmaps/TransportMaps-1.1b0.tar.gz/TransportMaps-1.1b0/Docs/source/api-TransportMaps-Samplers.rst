TransportMaps.Samplers
======================

**Classes**


.. inheritance-diagram:: TransportMaps.Samplers.Sampler TransportMaps.Samplers.ImportanceSampler TransportMaps.Samplers.RejectionSampler TransportMaps.Samplers.MetropolisHastingsIndependentProposalsSampler TransportMaps.Samplers.MetropolisHastingsSampler TransportMaps.Samplers.MetropolisHastingsWithinGibbsSampler TransportMaps.Samplers.HamiltonianMonteCarloSampler
   :parts: 1


========================================================================================================================================================  ============================================================================================================================
Class                                                                                                                                                     Description
========================================================================================================================================================  ============================================================================================================================
`Sampler <api-TransportMaps-Samplers.html\#TransportMaps.Samplers.Sampler>`_                                                                              Generic sampler of distribution ``d``
`ImportanceSampler <api-TransportMaps-Samplers.html\#TransportMaps.Samplers.ImportanceSampler>`_                                                          Importance sampler of distribution ``d``, with biasing distribution ``d_bias``
`RejectionSampler <api-TransportMaps-Samplers.html\#TransportMaps.Samplers.RejectionSampler>`_                                                            Rejection sampler of distribution ``d``, with biasing distribution ``d_bias``
`MetropolisHastingsIndependentProposalsSampler <api-TransportMaps-Samplers.html\#TransportMaps.Samplers.MetropolisHastingsIndependentProposalsSampler>`_  Metropolis-Hastings with independent proposal sampler of distribution ``d``, with proposal distribution ``d_prop``
`MetropolisHastingsSampler <api-TransportMaps-Samplers.html\#TransportMaps.Samplers.MetropolisHastingsSampler>`_                                          Metropolis-Hastings sampler of distribution ``d``, with proposal ``d_prop``
`MetropolisHastingsWithinGibbsSampler <api-TransportMaps-Samplers.html\#TransportMaps.Samplers.MetropolisHastingsWithinGibbsSampler>`_                    Metropolis-Hastings within Gibbs sampler of distribution ``d``, with proposal ``d_prop`` and Gibbs block sampling ``blocks``
`HamiltonianMonteCarloSampler <api-TransportMaps-Samplers.html\#TransportMaps.Samplers.HamiltonianMonteCarloSampler>`_                                    Hamiltonian Monte Carlo sampler of distribution ``d``, with proposal distribution ``d_prop``
========================================================================================================================================================  ============================================================================================================================


**Functions**

====================================================================  ===================================================
Function                                                              Description
====================================================================  ===================================================
`ess <api-TransportMaps-Samplers.html\#TransportMaps.Samplers.ess>`_  Compute the Effective Sample Size (ESS) of a sample
====================================================================  ===================================================

**Documentation**

.. automodule:: TransportMaps.Samplers
   :members:

