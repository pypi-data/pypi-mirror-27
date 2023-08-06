# -*- coding: utf-8 -*-
r"""
.. _SoftiMAX:

SoftiMAX at MAX IV
------------------

The images below are produced by scripts in
``\examples\withRaycing\14_SoftiMAX``.

The beamline will have two branches:
- STXM (Scanning Transmission X-ray Microscopy) and
- CXI (Coherent X-ray Imaging),

see the scheme provided by K. Thånell.

.. imagezoom:: _images/softiMAX_layout.*


STXM branch
~~~~~~~~~~~

.. rubric:: Rays vs. hybrid

The propagation through the first optical elements – from undulator to front
end (FE) slit, to M1, to M2 and to plane grating (PG) – is done with rays:

+------------+------------+------------+------------+
|     FE     |     M1     |     M2     |     PG     |
+============+============+============+============+
|  |st_rFE|  |  |st_rM1|  |  |st_rM2|  |  |st_rPG|  |
+------------+------------+------------+------------+

.. |st_rFE| imagezoom:: _images/stxm-2D-1-rays-0emit-0enSpread-monoE-00-FE.*
.. |st_rM1| imagezoom:: _images/stxm-2D-1-rays-0emit-0enSpread-monoE-01-M1local.*
.. |st_rM2| imagezoom:: _images/stxm-2D-1-rays-0emit-0enSpread-monoE-02-M2local.*
.. |st_rPG| imagezoom:: _images/stxm-2D-1-rays-0emit-0enSpread-monoE-02a-PGlocal.*
   :loc: upper-right-corner

Starting from PG – to M3, to exit slit, to Fresnel zone plate (FZP) and to
variously positioned sample screen – the propagation is done by rays or waves,
compared below. Despite the M3 footprint looks not perfect (not black at
periphery), the field at normal surfaces (exit slit, FZP (not shown) and sample
screen) is of perfect quality. At the best focus, rays and waves result in a
similar image. Notice a micron-sized depth of focus.

+-----------+---------------------+---------------------+
|           |         rays        |         wave        |
+===========+=====================+=====================+
|    M3     |       |st_rM3|      |      |st_hM3|       |
+-----------+---------------------+---------------------+
| exit slit |       |st_rES|      |      |st_hES|       |
+-----------+---------------------+---------------------+
|  sample   |       |st_rS|       |      |st_hS|        |
+-----------+---------------------+---------------------+

.. |st_rM3| imagezoom:: _images/stxm-2D-1-rays-0emit-0enSpread-monoE-03-M3local.*
.. |st_hM3| imagezoom:: _images/stxm-2D-2-hybr-0emit-0enSpread-monoE-03-M3local.*
   :loc: upper-right-corner
.. |st_rES| imagezoom:: _images/stxm-2D-1-rays-0emit-0enSpread-monoE-04-ExitSlit.*
.. |st_hES| imagezoom:: _images/stxm-2D-2-hybr-0emit-0enSpread-monoE-04-ExitSlit.*
   :loc: upper-right-corner
.. |st_rS| animation:: _images/stxm-2D-1-rays-0emit-0enSpread-monoE-06i-ExpFocus-Is
.. |st_hS| imagezoom:: _images/stxm-2D-2-hybr-0emit-0enSpread-monoE-06i-ExpFocus-Is
   :loc: upper-right-corner


.. rubric:: Influence of emittance

Non-zero emittance radiation is treated in xrt not by convolution, as in other
wave propagation programs, but by incoherent addition of single-electron
intensities. The filament trajectory of every electron (one per repeat) attains
a positional and angular shift within the given emittance distribution, and the
resulted single-electron field is considered as fully coherent. The following
images are calculated for the exit slit and the focus screen for zero and
non-zero emittance (for MAX IV 3 GeV ring: ε\ :sub:`x`\ =263 pm·rad,
β\ :sub:`x`\ =9 m, ε\ :sub:`z`\ =8 pm·rad, β\ :sub:`z`\ =2 m). At the real
emittance, the horizontal focal size increases by ~75%. A finite energy band,
as determined by vertical size of the exit slit, results in somewhat bigger
broadening due to a chromatic dependence of the focal length.

+-----------+------------------+--------------------+--------------------+
|           |   0 emittance    |   real emittance   |      |refeb|       |
+===========+==================+====================+====================+
| exit slit |     |st_hESb|    |      |st_hES2|     |      |st_hES3|     |
+-----------+------------------+--------------------+--------------------+
|  sample   |     |st_hSb|     |      |st_hS2|      |      |st_hS3|      |
+-----------+------------------+--------------------+--------------------+

.. |refeb| replace:: real emittance, finite energy band
.. |st_hESb| imagezoom:: _images/stxm-2D-2-hybr-0emit-0enSpread-monoE-04-ExitSlit.*
.. |st_hES2| imagezoom:: _images/stxm-2D-2-hybr-non0e-0enSpread-monoE-04-ExitSlit.*
.. |st_hS2| animation:: _images/stxm-2D-2-hybr-non0e-0enSpread-monoE-06i-ExpFocus-Is
.. |st_hES3| imagezoom:: _images/stxm-2D-2-hybr-non0e-0enSpread-wideE-04-ExitSlit.*
   :loc: upper-right-corner
.. |st_hSb| imagezoom:: _images/stxm-2D-2-hybr-0emit-0enSpread-monoE-06i-ExpFocus-Is
.. |st_hS3| animation:: _images/stxm-2D-2-hybr-non0e-0enSpread-wideE-06i-ExpFocus-Is
   :loc: upper-right-corner

.. rubric:: Correction of emittance effects

The increased focal size can be amended by closing the exit slit. With flux
loss of about 2/3 the focal size is almost restored.

+-----------+--------------------+--------------------+
|           |  80 µm exit slit   |  20 µm exit slit   |
+===========+====================+====================+
| exit slit |     |st_hES2b|     |      |st_hES4|     |
+-----------+--------------------+--------------------+
|  sample   |     |st_hS2b|      |      |st_hS4|      |
+-----------+--------------------+--------------------+

.. |st_hES2b| imagezoom:: _images/stxm-2D-2-hybr-non0e-0enSpread-monoE-04-ExitSlit.*
.. |st_hES4| imagezoom:: _images/stxm-2D-2-hybr-non0e-0enSpread-monoE-025H-04-ExitSlit.*
   :loc: upper-right-corner
.. |st_hS2b| animation:: _images/stxm-2D-2-hybr-non0e-0enSpread-monoE-06i-ExpFocus-Is
.. |st_hS4| animation:: _images/stxm-2D-2-hybr-non0e-0enSpread-monoE-025H-06i-ExpFocus-Is
   :loc: upper-right-corner

.. rubric:: Coherence signatures

The beam improvement can also be viewed via the coherence properties by four
available methods (see :ref:`coh_signs`). As the horizontal exit slit becomes
smaller, one can observe the increase in the degree of coherence (DOC) and the
increase of the primary (coherent) mode weight. The width of DOC relative to
that of the intensity distribution determines the coherent beam fraction. Both
widths vary with varying the screen position around the focal point, so that
the coherent fraction also varies, and sometimes it is even not easy to define
the width of DOC in view of its complex shape. An important advantage of the
eigen-mode or PCA methods is a simple definition of the coherent fraction as
the eigenvalue of the zeroth mode (component); this eigenvalue appears to be
invariant around the focal point, see below. Note that the methods 3 and 4 give
mathematically equal results; the calculated figures differ by
~10\ :sup:`-13`\ .

+-----------+--------------------------+--------------------------+
|           |     80 µm exit slit      |     20 µm exit slit      |
+===========+==========================+==========================+
| method 1  |        |st_hS80m1|       |       |st_hS20m1|        |
+-----------+--------------------------+--------------------------+
| method 3  |        |st_hS80m3|       |       |st_hS20m3|        |
+-----------+--------------------------+--------------------------+
| method 4  |        |st_hS80m4|       |       |st_hS20m4|        |
+-----------+--------------------------+--------------------------+

.. |st_hS80m1| animation:: _images/stxm-IDOC-2D-2-hybr-non0e-0enSpread-monoE
.. |st_hS20m1| animation:: _images/stxm-IDOC-2D-2-hybr-non0e-0enSpread-monoE-025H
   :loc: upper-right-corner
.. |st_hS80m3| animation:: _images/stxm-Modes-eigen_modes_of_mutual_intensity-2D-2-hybr-non0e-0enSpread-monoE
.. |st_hS20m3| animation:: _images/stxm-Modes-eigen_modes_of_mutual_intensity-2D-2-hybr-non0e-0enSpread-monoE-025%H
   :loc: upper-right-corner
.. |st_hS80m4| animation:: _images/stxm-Modes-principal_components_of_one-electron_images-2D-2-hybr-non0e-0enSpread-monoE
.. |st_hS20m4| animation:: _images/stxm-Modes-principal_components_of_one-electron_images-2D-2-hybr-non0e-0enSpread-monoE-025%H
   :loc: upper-right-corner

CXI branch
~~~~~~~~~~

.. rubric:: 2D vs 1D

Although the sample screen images are of good quality (the dark field is almost
black), the mirror footprints may be noisy and not well convergent in the
periphery. Compare the M3 footprint with that in the previous section (STXM
branch) where the difference is in the mirror area and thus in the sample
density. The used 10\ :sup:`6` wave samples (i.e. 10\ :sup:`12` possible paths)
are not enough for the slightly enlarged area in the present example. The
propagation is therefore performed in separated horizontal and vertical
directions, which dramatically improves the quality of the footprints.
Disadvantages of the cuts are losses in visual representation and incorrect
evaluation of the flux.

+---------------+-------------------+--------------------+--------------------+
|               |         2D        |     1D hor cut     |     1D ver cut     |
+===============+===================+====================+====================+
| M3 footprint  |     |cxiM32D|     |     |cxiM31Dh|     |     |cxiM31Dv|     |
+---------------+-------------------+--------------------+--------------------+
| sample screen |     |cxiS2D|      |     |cxiS1Dh|      |     |cxiS1Dv|      |
+---------------+-------------------+--------------------+--------------------+

.. |cxiM32D| imagezoom:: _images/cxi_2D-2-hybr-0emit-0enSpread-monoE-03-M3local.*
.. |cxiM31Dh| imagezoom:: _images/cxi_1D-2-hybr-1e6hor-0emit-0enSpread-monoE-03-M3local.*
.. |cxiM31Dv| imagezoom:: _images/cxi_1D-2-hybr-1e6ver-0emit-0enSpread-monoE-03-M3local.*
   :loc: upper-right-corner
.. |cxiS2D| animation:: _images/cxi_S2D
.. |cxiS1Dh| animation:: _images/cxi_S1Dh
.. |cxiS1Dv| animation:: _images/cxi_S1Dv
   :loc: upper-right-corner

.. _wavefronts:

.. rubric:: Flat screen vs normal-surface screen (wave front)

The following images demonstrate the correctness of the directional
Kirchhoff-like integral. Five diffraction integrals are calculated on flat
screens around the focus position: for two polarizations and for three
directional components. The latter ones define the wave fronts at every flat
screen position; these wave fronts are further used as new curved screens. The
calculated diffraction fields at these curved screens indeed have narrow phase
distributions, as shown by the color histograms, which is indeed expected for a
wave front. The flat screens at the same positions have rapid phase variation
(several Fresnel zones).

    .. note::

        In the process of wave propagation,  wave fronts -- surfaces of
        constant phase -- are not used in any way. We therefore call it “wave
        propagation”, not “wave *front* propagation” as frequently called by
        others. The wave fronts in this example were calculated to solely
        demonstrate the correctness of the local propagation directions after
        having calculated the diffracted field.

+------------------------------+------------------------------+
|         flat screen          |  curved screen (wave front)  |
+==============================+==============================+
|          |cxiFlat|           |          |cxiFront|          |
+------------------------------+------------------------------+

.. |cxiFlat| animation:: _images/cxi-S1DhFlat
.. |cxiFront| animation:: _images/cxi-S1DhFront
   :loc: upper-right-corner

The curvature of the calculated wave fronts varies across the focus position.
The wave fronts become more flat as one approaches the focus, see the figure
below. This is in contrast to *ray* propagation, where the angular ray
distribution is invariant at any position between two optical elements.

.. imagezoom:: _images/cxi-waveFronts.*

.. rubric:: Rays, waves and hybrid

The following images are horizontal cuts at the footprints and sample screens
calculated by

- rays,
- rays + wave hybrid (rays up to PG and wave from PG) and
- purely by wave.

+-----------------+-------------+--------------+-------------+
|                 |    rays     |   hybrid     |    wave     |
+=================+=============+==============+=============+
| front end slit  |  |cxi-hFE|  | same as rays |  |cxi-wFE|  |
+-----------------+-------------+--------------+-------------+
| footprint on M1 |  |cxi-hM1|  | same as rays |  |cxi-wM1|  |
+-----------------+-------------+--------------+-------------+
| footprint on M2 |  |cxi-hM2|  | same as rays |  |cxi-wM2|  |
+-----------------+-------------+--------------+-------------+
| footprint on PG |  |cxi-hPG|  | same as rays |  |cxi-wPG|  |
+-----------------+-------------+--------------+-------------+
| footprint on M3 |  |cxi-rM3|  |  |cxi-hM3|   |  |cxi-wM3|  |
+-----------------+-------------+--------------+-------------+
| exit slit       |  |cxi-rES|  |  |cxi-hES|   |  |cxi-wES|  |
+-----------------+-------------+--------------+-------------+
| footprint on M4 |  |cxi-rM4|  |  |cxi-hM4|   |  |cxi-wM4|  |
+-----------------+-------------+--------------+-------------+
| footprint on M5 |  |cxi-rM5|  |  |cxi-hM5|   |  |cxi-wM5|  |
+-----------------+-------------+--------------+-------------+
|  sample screen  |  |cxi-rS|   |  |cxi-hS|    |  |cxi-wS|   |
+-----------------+-------------+--------------+-------------+

.. |cxi-hFE| imagezoom:: _images/cxi_1D-2-hybr-hor-0emit-0enSpread-monoE-00-FE.*
.. |cxi-wFE| imagezoom:: _images/cxi_1D-3-wave-hor-0emit-0enSpread-monoE-00-FE.*
   :loc: upper-right-corner
.. |cxi-hM1| imagezoom:: _images/cxi_1D-2-hybr-hor-0emit-0enSpread-monoE-01-M1local.*
.. |cxi-wM1| imagezoom:: _images/cxi_1D-3-wave-hor-0emit-0enSpread-monoE-01-M1local.*
   :loc: upper-right-corner
.. |cxi-hM2| imagezoom:: _images/cxi_1D-2-hybr-hor-0emit-0enSpread-monoE-02-M2local.*
.. |cxi-wM2| imagezoom:: _images/cxi_1D-3-wave-hor-0emit-0enSpread-monoE-02-M2local.*
   :loc: upper-right-corner
.. |cxi-hPG| imagezoom:: _images/cxi_1D-2-hybr-hor-0emit-0enSpread-monoE-02-PGlocal.*
.. |cxi-wPG| imagezoom:: _images/cxi_1D-3-wave-hor-0emit-0enSpread-monoE-02-PGlocal.*
   :loc: upper-right-corner
.. |cxi-rM3| imagezoom:: _images/cxi_1D-1-rays-hor-0emit-0enSpread-monoE-03-M3local.*
.. |cxi-hM3| imagezoom:: _images/cxi_1D-2-hybr-hor-0emit-0enSpread-monoE-03-M3local.*
.. |cxi-wM3| imagezoom:: _images/cxi_1D-3-wave-hor-0emit-0enSpread-monoE-03-M3local.*
   :loc: upper-right-corner
.. |cxi-rES| imagezoom:: _images/cxi_1D-1-rays-hor-0emit-0enSpread-monoE-04-ExitSlit.*
.. |cxi-hES| imagezoom:: _images/cxi_1D-2-hybr-hor-0emit-0enSpread-monoE-04-ExitSlit.*
.. |cxi-wES| imagezoom:: _images/cxi_1D-3-wave-hor-0emit-0enSpread-monoE-04-ExitSlit.*
   :loc: upper-right-corner
.. |cxi-rM4| imagezoom:: _images/cxi_1D-1-rays-hor-0emit-0enSpread-monoE-05-M4local.*
.. |cxi-hM4| imagezoom:: _images/cxi_1D-2-hybr-hor-0emit-0enSpread-monoE-05-M4local.*
.. |cxi-wM4| imagezoom:: _images/cxi_1D-3-wave-hor-0emit-0enSpread-monoE-05-M4local.*
   :loc: upper-right-corner
.. |cxi-rM5| imagezoom:: _images/cxi_1D-1-rays-hor-0emit-0enSpread-monoE-06-M5local.*
.. |cxi-hM5| imagezoom:: _images/cxi_1D-2-hybr-hor-0emit-0enSpread-monoE-06-M5local.*
.. |cxi-wM5| imagezoom:: _images/cxi_1D-3-wave-hor-0emit-0enSpread-monoE-06-M5local.*
   :loc: upper-right-corner
.. |cxi-rS| animation:: _images/cxi-rS
.. |cxi-hS| animation:: _images/cxi-hS
.. |cxi-wS| animation:: _images/cxi-wS
   :loc: upper-right-corner

.. rubric:: Coherence signatures

This section demonstrates the 2nd method out of the three available (see
:ref:`coh_signs`), the methods 1 and 3 being considered above for the STXM
branch. The diagonal cut of the absolute value of the mutual intensity gives
the usual 1D intensity distribution. The antidiagonal cut represents the
correlation between two symmetric points relative 0. Normalized by intensity,
it gives the absolute value of the degree of coherence.

+--------------------------------------+--------------------------------------+
|             0 emittance              |            real emittance            |
+======================================+======================================+
|           |cxi-coh2-0emit|           |           |cxi-coh2-non0e|           |
+--------------------------------------+--------------------------------------+

.. |cxi-coh2-0emit| animation:: _images/cxi-coh2-0emit
.. |cxi-coh2-non0e| animation:: _images/cxi-coh2-non0e
   :loc: upper-right-corner

"""
pass
