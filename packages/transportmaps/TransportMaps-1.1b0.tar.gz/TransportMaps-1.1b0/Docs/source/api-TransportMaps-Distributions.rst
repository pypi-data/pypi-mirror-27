TransportMaps.Distributions
===========================

**Sub-modules**

.. toctree::
   :maxdepth: 1

   api-TransportMaps-Distributions-Inference
   api-TransportMaps-Distributions-Decomposable
   api-TransportMaps-Distributions-Examples


**Classes**


.. inheritance-diagram:: TransportMaps.Distributions.Distribution TransportMaps.Distributions.ProductDistribution TransportMaps.Distributions.ConditionalDistribution TransportMaps.Distributions.FactorizedDistribution TransportMaps.Distributions.FrozenDistribution_1d TransportMaps.Distributions.GaussianDistribution TransportMaps.Distributions.StandardNormalDistribution TransportMaps.Distributions.LogNormalDistribution TransportMaps.Distributions.LogisticDistribution TransportMaps.Distributions.GammaDistribution TransportMaps.Distributions.BetaDistribution TransportMaps.Distributions.WeibullDistribution TransportMaps.Distributions.GumbelDistribution TransportMaps.Distributions.BananaDistribution TransportMaps.Distributions.ConditionallyGaussianDistribution TransportMaps.Distributions.MeanConditionallyGaussianDistribution TransportMaps.Distributions.ParametricDistribution TransportMaps.Distributions.TransportMapDistribution TransportMaps.Distributions.PushForwardTransportMapDistribution TransportMaps.Distributions.PullBackTransportMapDistribution
   :parts: 1


==================================================================================================================================================  ===================================================================================================================
Class                                                                                                                                               Description
==================================================================================================================================================  ===================================================================================================================
`Distribution <api-TransportMaps-Distributions.html\#TransportMaps.Distributions.Distribution>`_                                                    Abstract distribution :math:`\nu_\pi`.
`ProductDistribution <api-TransportMaps-Distributions.html\#TransportMaps.Distributions.ProductDistribution>`_                                      Abstract distribution :math:`\nu(A_1\times\cdots\times A_n) = \nu_1(A_1)\cdots\nu_n(A_n)`
`ConditionalDistribution <api-TransportMaps-Distributions.html\#TransportMaps.Distributions.ConditionalDistribution>`_                              Abstract distribution :math:`\pi_{{\bf X}\vert{\bf Y}}`.
`FactorizedDistribution <api-TransportMaps-Distributions.html\#TransportMaps.Distributions.FactorizedDistribution>`_                                Distribution :math:`\nu_\pi` defiened by its conditional factors.
`FrozenDistribution_1d <api-TransportMaps-Distributions.html\#TransportMaps.Distributions.FrozenDistribution_1d>`_                                  [Abstract] Generic frozen distribution 1d
`GaussianDistribution <api-TransportMaps-Distributions.html\#TransportMaps.Distributions.GaussianDistribution>`_                                    Multivariate Gaussian distribution :math:`\pi`
`StandardNormalDistribution <api-TransportMaps-Distributions.html\#TransportMaps.Distributions.StandardNormalDistribution>`_                        Multivariate Standard Normal distribution :math:`\pi`.
`LogNormalDistribution <api-TransportMaps-Distributions.html\#TransportMaps.Distributions.LogNormalDistribution>`_
`LogisticDistribution <api-TransportMaps-Distributions.html\#TransportMaps.Distributions.LogisticDistribution>`_
`GammaDistribution <api-TransportMaps-Distributions.html\#TransportMaps.Distributions.GammaDistribution>`_
`BetaDistribution <api-TransportMaps-Distributions.html\#TransportMaps.Distributions.BetaDistribution>`_
`WeibullDistribution <api-TransportMaps-Distributions.html\#TransportMaps.Distributions.WeibullDistribution>`_
`GumbelDistribution <api-TransportMaps-Distributions.html\#TransportMaps.Distributions.GumbelDistribution>`_
`BananaDistribution <api-TransportMaps-Distributions.html\#TransportMaps.Distributions.BananaDistribution>`_
`ConditionallyGaussianDistribution <api-TransportMaps-Distributions.html\#TransportMaps.Distributions.ConditionallyGaussianDistribution>`_          Multivariate Gaussian distribution :math:`\pi({\bf x}\vert{\bf y}) \sim \mathcal{N}(\mu({\bf y}), \Sigma({\bf y}))`
`MeanConditionallyGaussianDistribution <api-TransportMaps-Distributions.html\#TransportMaps.Distributions.MeanConditionallyGaussianDistribution>`_  Multivariate Gaussian distribution :math:`\pi({\bf x}\vert{\bf y}) \sim \mathcal{N}(\mu({\bf y}), \Sigma)`
`ParametricDistribution <api-TransportMaps-Distributions.html\#TransportMaps.Distributions.ParametricDistribution>`_                                Parametric distribution :math:`\pi_{\bf a}`.
`TransportMapDistribution <api-TransportMaps-Distributions.html\#TransportMaps.Distributions.TransportMapDistribution>`_                            Abstract class for densities of the transport map type (:math:`T^\sharp \pi` or :math:`T_\sharp \pi`)
`PushForwardTransportMapDistribution <api-TransportMaps-Distributions.html\#TransportMaps.Distributions.PushForwardTransportMapDistribution>`_      Class for densities of the transport map type :math:`T_\sharp \pi`
`PullBackTransportMapDistribution <api-TransportMaps-Distributions.html\#TransportMaps.Distributions.PullBackTransportMapDistribution>`_            Class for densities of the transport map type :math:`T^\sharp \pi`
==================================================================================================================================================  ===================================================================================================================



**Documentation**

.. automodule:: TransportMaps.Distributions
   :members:

