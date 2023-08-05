TransportMaps.Likelihoods
=========================

**Classes**


.. inheritance-diagram:: TransportMaps.Likelihoods.LogLikelihood TransportMaps.Likelihoods.AdditiveLogLikelihood TransportMaps.Likelihoods.AdditiveLinearGaussianLogLikelihood TransportMaps.Likelihoods.AdditiveConditionallyLinearGaussianLogLikelihood TransportMaps.Likelihoods.IndependentLogLikelihood
   :parts: 1


====================================================================================================================================================================  =================================================================================================================
Class                                                                                                                                                                 Description
====================================================================================================================================================================  =================================================================================================================
`LogLikelihood <api-TransportMaps-Likelihoods.html\#TransportMaps.Likelihoods.LogLikelihood>`_                                                                        Abstract class for log-likelihood :math:`\log \pi({\bf y} \vert {\bf x})`
`AdditiveLogLikelihood <api-TransportMaps-Likelihoods.html\#TransportMaps.Likelihoods.AdditiveLogLikelihood>`_                                                        Log-likelihood :math:`\log \pi({\bf y} \vert {\bf x})=\log\pi({\bf y} - T({\bf x}))`
`AdditiveLinearGaussianLogLikelihood <api-TransportMaps-Likelihoods.html\#TransportMaps.Likelihoods.AdditiveLinearGaussianLogLikelihood>`_                            Define the log-likelihood for the additive linear Gaussian model
`AdditiveConditionallyLinearGaussianLogLikelihood <api-TransportMaps-Likelihoods.html\#TransportMaps.Likelihoods.AdditiveConditionallyLinearGaussianLogLikelihood>`_  Define the log-likelihood for the additive linear Gaussian model
`IndependentLogLikelihood <api-TransportMaps-Likelihoods.html\#TransportMaps.Likelihoods.IndependentLogLikelihood>`_                                                  Handling likelihoods in the form :math:`\pi({\bf y}\vert{\bf x}) = \prod_{i=1}^{n}\pi_i({\bf y}_i\vert{\bf x}_i)`
====================================================================================================================================================================  =================================================================================================================



**Documentation**

.. automodule:: TransportMaps.Likelihoods
   :members:

