TransportMaps.Algorithms.Adaptivity
===================================

**Classes**


.. inheritance-diagram:: TransportMaps.Algorithms.Adaptivity.Builder TransportMaps.Algorithms.Adaptivity.KullbackLeiblerBuilder TransportMaps.Algorithms.Adaptivity.SequentialKullbackLeiblerBuilder TransportMaps.Algorithms.Adaptivity.ToleranceSequentialKullbackLeiblerBuilder TransportMaps.Algorithms.Adaptivity.L2RegressionBuilder TransportMaps.Algorithms.Adaptivity.ToleranceSequentialL2RegressionBuilder
   :parts: 1


==========================================================================================================================================================================  =======================================================================================================
Class                                                                                                                                                                       Description
==========================================================================================================================================================================  =======================================================================================================
`Builder <api-TransportMaps-Algorithms-Adaptivity.html\#TransportMaps.Algorithms.Adaptivity.Builder>`_                                                                      [Abstract] Basis builder class.
`KullbackLeiblerBuilder <api-TransportMaps-Algorithms-Adaptivity.html\#TransportMaps.Algorithms.Adaptivity.KullbackLeiblerBuilder>`_                                        Basis builder through minimization of kl divergence
`SequentialKullbackLeiblerBuilder <api-TransportMaps-Algorithms-Adaptivity.html\#TransportMaps.Algorithms.Adaptivity.SequentialKullbackLeiblerBuilder>`_                    Solve over a list of maps, using the former to warm start the next one
`ToleranceSequentialKullbackLeiblerBuilder <api-TransportMaps-Algorithms-Adaptivity.html\#TransportMaps.Algorithms.Adaptivity.ToleranceSequentialKullbackLeiblerBuilder>`_  Solve over a list of maps, using the former to warm start the next one, until a target tolerance is met
`L2RegressionBuilder <api-TransportMaps-Algorithms-Adaptivity.html\#TransportMaps.Algorithms.Adaptivity.L2RegressionBuilder>`_                                              Basis builder through :math:`\mathcal{L}^2` regression
`ToleranceSequentialL2RegressionBuilder <api-TransportMaps-Algorithms-Adaptivity.html\#TransportMaps.Algorithms.Adaptivity.ToleranceSequentialL2RegressionBuilder>`_
==========================================================================================================================================================================  =======================================================================================================



**Documentation**

.. automodule:: TransportMaps.Algorithms.Adaptivity
   :members:

