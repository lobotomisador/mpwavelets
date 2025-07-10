---
title: "Spectral shape measures for damping modification factors of MP-wavelets"
author:
  - Carlo Ruiz
  - Mario Ordaz
institute: Instituto de Ingeniería, UNAM, Mexico City, México
date: "2024"
documentclass: article
geometry: margin=1in
fontsize: 11pt
linestretch: 1.5
bibliography: references.bib
csl: ieee.csl
link-citations: true
numbersections: true
toc: true
toc-depth: 3
lot: true
lof: true
header-includes:
  - \usepackage{amsmath}
  - \usepackage{amssymb}
  - \usepackage{graphicx}
  - \usepackage{booktabs}
  - \usepackage{longtable}
  - \usepackage{array}
  - \usepackage{multirow}
  - \usepackage{wrapfig}
  - \usepackage{float}
  - \usepackage{colortbl}
  - \usepackage{pdflscape}
  - \usepackage{tabu}
  - \usepackage{threeparttable}
  - \usepackage{threeparttablex}
  - \usepackage{makecell}
  - \usepackage{xcolor}
  - \usepackage{hyperref}
  - \hypersetup{colorlinks=true, linkcolor=blue, citecolor=blue, urlcolor=blue}
abstract: |
  We present a simplified model for estimating damping modification factors for Mavroeidis-Papageorgiou (MP) wavelets, which accurately represent near-fault pulse-like ground motions. The model uses a spectral shape measure ($S_R$) that requires only the 5% damped displacement spectrum as input. The study first shows damping modification factors (DMFs) for a comprehensive sample of representative wavelets and damping ratios. Then, an
  evaluation of the proposed predictor model is conducted, where it is shown that
  most information required to estimate the DMF is contained
  within $S_R$. It is shown that the rules derived here to predict DMFs for MP
  wavelets produce low errors even for damping levels significantly far from 5%,
  and surprisingly, work well for other narrow-band waveforms such as Tarquis'
  pulses. This opens the possibility of accurately predicting the DMF for real
  near-fault pulse-like ground motions.
keywords:
  - damping modification factor
  - wavelet
  - near-fault
  - pulse-like
  - spectral shape
---

# Introduction

Seismic design and assessment of tall and flexible structures or
seismically isolated systems usually require spectra computed with a
critical damping percentage different from the 5% contained in most
building codes[@kawasumi1956]. Even though the exact dynamical response of
a viscously damped elastic structure is obtained by solving the
equations of motion for a given record, rarely does the engineer have
access to the records that generated the design spectrum. Therefore, to
design structures with critical damping different than 5%, the engineer
must either estimate the spectral ordinates directly using analytical
methods, e.g. with random vibration theory, or use an empirical
multiplicative factor. This factor is referenced as a 'damping scaling
factor' or 'damping modification factor' (DMF or B in the literature)
and is defined as the spectral ordinate ratio for an arbitrary damping
with respect to the 5% damped ordinates and will be referenced
henceforth as DMF.

Most authors acknowledge DMF dependence on various physical parameters of both the system and ground motion, including damping, system frequency, magnitude, fault distance, energy dissipation cycles, frequency content, and soil conditions. However, most studies neglect the influence of damping effects in DMF's peaks versus valleys, and statistical regression models average this effect, particularly for high frequencies.

Hudson[@hudson1956] conducted one of the earliest analytical studies on response spectrum techniques in earthquake engineering, deriving a mean velocity spectrum for randomly distributed vibrations (see their Appendix for details).

Empirical DMF computation studies trace back to the pioneering work of Newmark and Hall[@newmark1982], who used a small number of ground motions to find clear dependency on vibration period and proposed equations for all spectral regions.

Arias and Husid[@arias1962] used random vibration theory to show that under certain assumptions, the DMF is proportional to the square root of the damping ratio. However, finite duration and stochasticity of real earthquakes significantly influence system response. This led them to suggest an exponent of 0.4 instead of 0.5, representing one of the earliest analytical treatments of this predictor variable. Rosenblueth[@rosenblueth1964] validated this result and demonstrated strong dependence on motion duration, citing the 1960 Agadir earthquake as an example of a destructive, short-duration earthquake.

Using a different approach, Miranda and Miranda[@miranda2020] found that a
measure of spectral shape called _SaRatio_ ($S_R$ henceforth) is
a better statistical predictor for the DMF than magnitude, distance,
record-duration, and other physical event-specific parameters. This
makes intuitive sense since it is natural to think that all
peculiarities of the motion due to event-specific parameters should
manifest themselves in the shape of the spectrum. This is a notable
example of a study based on analytical methods that does not use random
vibration theory. A study on the effectiveness of this measure for
near-fault pulse-like ground motions, however, has not been performed to
date.

The destructive effects of the 1994 Northridge and 1995 Kobe earthquakes
renewed interest in seismologists and engineers in developing parametric
models that can capture the qualitative nature of the displacement,
velocity, and acceleration pulses that are characteristic of the rupture
processes of motions with forward directivity. These motions contain a
dominant velocity pulse that delivers an energy burst to structures,
which causes significant plastic displacements. Such motions are
referred to as 'near-fault' and 'pulse-like' motions, or shortly as NFPL.

Hubbard and Mavroeidis[@hubbard2011] studied the influence of earthquake
magnitude on the DMF for NFPLs and observed that its peak clearly depended on the magnitude, which might be playing as a proxy to duration. Damping
modification factors for high-magnitude earthquakes show a smaller peak
at 0.75s which is associated with high-frequency radiation that is very
difficult to fully capture in a model. Most importantly, they showed
that it strongly depends on the pulse period and that a sounder approach
is to regress towards $T/T_p$ rather than the oscillator period
alone. They proposed a more accurate estimator to account for this
phenomenon:

$$\frac{1}{DMF} = 3.4\frac{\xi^{1.3}}{(T/T_p)^{1.3}} + 1\qquad 0.10 \leq \xi \leq 0.50$$

and

$$\frac{1}{DMF} = 2\frac{(\xi + 0.3)^{1.5}}{(T/T_p)^{1.3}} + 1\qquad 0.50 < \xi \leq 1.00$$

which is representative down until $T/T_p=0.83$, a normalized
period where the peak in value seems to occur. Below this normalized
period, the factor is linearly reduced to 1 as required by structural
dynamics.

Pu et al.[@pu2016] pointed out the possible inaccuracy of many
building codes recommending generic estimators when the motions the
engineer is designing for are near fault with a potentially large
velocity waveform. Their findings agree with past research in that the
DMF presents significant dependence on the pulse period $T_p$
and that there is some dependence on magnitude and soil conditions.
Notably, they investigated the effect of the impulsive character of
near-fault motions on the velocity and acceleration spectra (and not
only on the displacement spectra). On this matter, they concluded that
the spectra are different enough that they must be computed individually
and cannot be derived one from another. Furthermore, they present a
statistical predictor based on 50 hand-picked pulse-like near-fault
ground motions. These pulses were selected using an analytical approach
that verifies the presence of a dominant velocity pulse. The
displacement estimator presented is:

$$\frac{1}{DMF} = 3.4\frac{\xi^{1.3}}{(T/T_p)^{1.3}} + 1\qquad 0.10 \leq \xi \leq 0.50$$

and

$$\frac{1}{DMF} = 2\frac{(\xi + 0.3)^{1.5}}{(T/T_p)^{1.3}} + 1\qquad 0.50 < \xi \leq 1.00$$

Mollaioli et al.[@mollaioli2014] studied the influence of $T_p$ on
the DMF for two sets of records: pulse-like and ordinary records. They
found that the DMF for pulse-like records usually have a pronounced peak
or valley located at a period value about one second less than the pulse
and that the ordinates are slightly higher for ordinary records than for
pulse-like records. Neglecting the pulse period can lead to a
significant overestimation for high $T/T_p$ values, and they also found that for ordinary records the influence of fault distance is
low to negligible compared to magnitude. Finally, they proposed an
estimator based on the functional form used by Stafford[@stafford2008] and
Hatzigeorgiou[@hatzigeorgiou2010]:

$$DMF = 1 - (5 - \xi)[(1 - \mathbb{I}_{\xi<5\%})(1 - c_6 T^{-0.15})] \times (1 + c_1 \ln \xi + c_2 \ln^2 \xi)(c_3 + c_4 \ln T + c_5 \ln^2 T)$$

where damping is expressed in percentages and the indicator variable
$\mathbb{I}_{\xi<5\%}$ = 1 if $\xi < 5\%$ else 0, and the coefficients depend

on the value of $T_p$. This estimator is suitable for soil types
B, C, and D, and magnitudes 5 to 7.6 and $T_p$ from 0.4 to 9s.

Rezaeian et al. (2012) developed a DMF estimator for the median and
logarithmic standard deviations of shallow crustal earthquakes with a
similar functional form as [@arias1962]. They examined the influence of the
following predictor variables on the DMF: the damping ratio, spectral
period, ground motion duration, moment magnitude, source-to-site distance, and site conditions.

They found duration to have the strongest effect on the DMF (besides
damping and period), which is captured in their model by the magnitude
and distance, yielding a total of 4 parameters. Furthermore, they showed
the strength of their predictor against others in the literature.

They mention that near fault effects such as directivity can have a
significant influence on the DMF and that these effects are for the
moment only included implicitly.

Using observations about the physical character and peculiarities
of near-fault pulse-like (NFPL) and surveying different ground motion models in the literature,

Mavroeidis and Papageorgiou[@mavroeidis2004] introduced the so-called MP-wavelets. These have a versatile form
controlled by a few parameters directly related to the physical
phenomena of the rupture, and, unlike some of the simplified pulse
models[@babak2001; @yang2010], or the cycloidal-type pulse models[@makris2000]
that were previously developed, their[@mavroeidis2003] parametric
formulation proposed is simpler and physically sound. These MP-wavelets are highly
versatile and can be used to accurately simulate the classical wavelets
such as Ricker, Morlet, or the main velocity pulse of realistic ground
motions (Figure 1) by tuning a reduced number of parameters with clear
physical meaning.

![Example of the versatility of the MP wavelet in simulating the classical wavelets such as the Gabor, Morlet, DaubechiesDb8, Ricker, Mexican hat, DaubechiesDb8, and others.](./md/media/wavelet-zoo.pdf)

Another fundamental difference between a classical wavelet and the
MP-wavelet is that the response of an elastic viscously damped
single-degree-of-freedom system to such pulse can be obtained
_analytically_[@alonso2015], which allows for simpler and more
insightful parametric studies or sensitivity analyses. This contrasts
with the classical wavelet treatment whose solution can only be obtained
numerically.

Since real ground motions close to fault with forward directivity
effects have a dominant velocity pulse, it should be possible to
accurately predict the DMF for such motions using the MP-wavelet model;
however, relatively few studies on this matter have been performed to
date. This is the main motivation for the development of this model.

On this matter, Gordó and Miranda [@gordo2018] looked at the effect of pulse
duration on the DMF and used the MP model to represent the main pulse of
the strong motion waveform of events in Spain and to predict the
response of both single and multiple-degree-of-freedom systems with high
accuracy [@alonso2015]. This shows that MP wavelets could in principle be used
to

Given the previous studies, we would like to present our contribution,
which has the following goals:

To develop a simpler model consistent with structural dynamics and
empirical observations, based solely on the spectral shape to estimate
the DMF for MP wavelets.

To prove the effectiveness of the predictor, exploring to what extent
the information on the DMF is present in the spectral ratio.

# Definition of Simplified Near-Fault Pulse Models

## Definition of an MP wavelet and closed-form damped displacement response

The velocity waveform of an MP pulse starting at time $t = 0$s consists of
a harmonic oscillation component multiplied by a bell-shaped function:

$$v_p(t) = \frac{A}{2}\cos(\omega t - \pi\gamma + \nu)\left[ 1 - \cos\frac{\omega t}{\gamma} \right]\qquad 0 \leq t \leq t_p = 2\pi\gamma/\omega.$$

In this formulation, $A$ is the pulse amplitude, which varies from
70 to 130 cm/s (Mavroeidis and Papageorgiou, 2003). The circular frequency $\omega = 2\pi f_p$ depends on the moment magnitude of the
earthquake and correlates with the faulting process parameter known as 'rise time' (Mavroeidis and Papageorgiou, 2003). Parameter $\gamma > 1$
controls the pulse modulation and fixes the pulse duration
$t_p = \gamma / f_p = 2\pi\gamma / \omega$. The phase angle $\nu$ relates to fault rupture processes and serves as a free parameter for fitting. Mavroeidis and Papageorgiou (2004) demonstrated that these pulses accurately simulate NFPL ground motion velocity waveforms. Several strategies exist for fitting the pulse to real strong motion records (Mavroeidis and Papageorgiou, 2003; Gordó and Miranda, 2018). The analytical model can adequately reproduce recorded velocity, acceleration, or displacement time histories. Alternatively, parameters can optimize response spectrum reproduction. A simultaneous time-history and spectra fit (Mavroeidis and Papageorgiou, 2003) often improves fitting accuracy.

This model focuses on intermediate-to-long period features of NFPL ground motions. Fitted pulses cannot accurately reproduce responses for ground motions with stochastic high-frequency content (Mavroeidis and Papageorgiou, 2003). When the normalized period becomes small ($T/T_p \leq 0.83$), system response primarily depends on high-frequency components that are difficult to capture (Hubbard and Mavroeidis, 2011).

Differentiating the velocity equation with respect to time yields the acceleration time history. Alonso and Miranda (2015) found an equivalent expression that avoids complex sinusoidal multiplication. The velocity waveform becomes a linear combination of three cosine pulses with distinct amplitudes, frequencies, and phases. This equivalency produces the acceleration expression:

$$a_p(t) = \frac{A\omega}{4}\left\lbrack \frac{\gamma + 1}{\gamma}\sin\left( \frac{\gamma + 1}{\gamma}\omega t - \pi\gamma + \nu \right) + \frac{\gamma - 1}{\gamma}\sin\left( \frac{\gamma - 1}{\gamma}\omega t - \pi\gamma + \nu \right) - 2\sin(\omega t - \pi\gamma + \nu) \right\rbrack$$

Using the velocity equation, Alonso and Miranda (2015) deduced the closed-form
solution for a damped oscillator with frequency $\Omega$ and critical damping level $\xi$. The exact displacement response is:

$$
u(t) = \begin{cases}
u_1(t) = e^{- \xi\Omega t}(C_1\sin\tilde{\Omega}t + C_2\cos\tilde{\Omega}t) + \sum_{i = 1}^{3}C_{3i}\sin(\omega_i t + \phi_i) + C_{4i}\cos(\omega_i t + \phi_i) & \text{if} \ \ \ 0 \leq t \leq t_p \\
u_2(t) = e^{- \xi\Omega(t - t_p)}\left( \tilde{\Omega}^{- 1}\left( \dot{u}_1(t_p) + \xi\Omega u_1(t_p) \right)\sin\tilde{\Omega}(t - t_p) + u_1(t_p)\cos\tilde{\Omega}(t - t_p) \right) & \text{if} \ \ \ t > t_p
\end{cases}
$$

where $\tilde{\Omega} = \Omega\sqrt{1 - \xi^2}$, the pulse
duration equals $t_p = 2\pi\gamma / \omega$, and the constants $C_{3i}$, $C_{4i}$ depend on the amplitude, frequency, and phase of each of
the three pulses:

$$C_{3i} = - \frac{(\Omega^2 - \omega_i^2)A_i}{\Omega^4 + \omega_i^4 + 2\omega_i^2\Omega^2(2\xi^2 - 1)}$$

$$C_{4i} = \frac{2\xi\Omega\omega_iA_i}{\Omega^4 + \omega_i^4 + 2\omega_i^2\Omega^2(2\xi^2 - 1)}$$

Finally, constants $C_2$ and $C_1$ become:

$$C_2 = \sum_{i = 1}^{3}\frac{(\Omega^4 - \omega_i^4)\sin\phi_i - 2\xi\omega_i\Omega \cos\phi_i}{\Omega^4 + \omega_i^4 + 2\omega_i^2\Omega^2(2\xi^2 - 1)}A_i$$

$$C_1 = \frac{1}{\tilde{\Omega}}\left( \xi\Omega C_2 + \sum_{i = 1}^{3}\left( - \omega_iC_{3i}\sin\phi_i + \omega_iC_{4i}\cos\phi_i \right) \right)$$

# Computation of the Damping Modification Factor

One of the original motivations for developing analytic representations
of near-fault pulses was to enable parametric studies or sensitivity
analyses. For the purposes of this work, we compute the damping
modification factor for multiple single-degree-of-freedom oscillators
and pulses. This requires obtaining the maximum absolute displacement
over the complete time-history response, plus a sufficiently long free
vibration phase. This value can occur during any peak in either the
forced or the free phases. Local and global maxima can be found by
setting the derivative of the displacement equation to zero; however the only way to compute the global
absolute maximum for non-convex functions is by evaluating those critical points and comparing them. This is
computationally equivalent to evaluating $u(t)$ at sufficiently
closely spaced intervals $t_i$ and then taking the maximum
absolute value.

This work computed the damping modification factor using the latter strategy with $T \in [0, 10]$ s divided in steps $dT = 0.01$ s:

$$DMF(T, \xi) = \frac{\max_t \mid u(t,  T,  \xi) \mid}{\max_t \mid u(t,  T,  \xi = 5\%) \mid}$$

Structural dynamics dictates that the DMF approaches 1 as the system becomes infinitely stiff or infinitely flexible, due to damping effects vanishing in the limit. The displacement amplitude becomes immaterial to the DMF because it appears in both numerator and denominator. The displacement equation shows that the response amplitude depends linearly on $A$; therefore, this parameter does not affect the DMF and is set to 1 for this study.

The fundamental frequency of the MP pulse $f_p$ scales the time axis and amplitude proportionally to $1/f_p$, skewing the spectra's abscissas and ordinates while preserving the underlying functional form. This scaling property implies that one can reconstruct an equivalent spectrum (and consequently an equivalent DMF) for a different pulse frequency by scaling a unitary frequency spectrum ($f_p = 1 = T_p$) appropriately (see Appendix B for a detailed explanation).

This study sets $f_p = 1$ for simplicity. In general, the pulse period differs from 1, and ground motion normalization should use $T/T_p$. This study takes the pulse period $T_p$ as the period at the peak of the response pseudo-velocity spectrum for $\xi = 0.05$, although more sophisticated methods based on energy or wavelet theory exist (Baker, 2007; Mollaioli and Bosi, 2012). Consequently, without loss of generality, the only explicit parameters for MP-wavelets in this work are the modulating frequency $\gamma$ and the phase shift $\nu$.

These considerations led to a parametric study of displacement damping modification factors for a set of 66 representative pulses (see Appendix A). Figure 2 presents a subset of these results.

As previously observed (Hubbard and Mavroeidis, 2011), when $\gamma$ approaches 1, DMFs plateau around $f_p$. As $\gamma$ increases, DMFs spike near $T/T_p = 1$ due to resonance. Values of $\gamma$ above 3 contain too many cycles to represent real strong near-fault ground motion records and are excluded from this study (Mavroeidis and Papageorgiou, 2004). The response in the very short period range becomes highly erratic.

For all wavelets, especially with low $\gamma$s, there are some normalized periods where the DMF
is not smooth, that is, the derivative is discontinuous (see, for
instance, first row and second column on Figure 2 at around
$T/T_p$ equal to 1 and 2.3), which indicates a qualitative
change in the behavior of the response.
Note that this is also the case for the very short period showing signs of `ringing' alternating around the value 1.

This phenomenon has been studied in shock spectra for simple pulses[@chopra2012]. The explanation is that
for the period of interest, multiple identical peaks develop
both in the forced and the free vibration phase of the response. Those
peaks do not behave equally when the period of the system is perturbed
slightly, leading to the observed loss of smoothness.

This phenomenon is not easy to capture in a DMF model.

![Table of DMFS for some selected MP pulses (parameters shown above each sub-figure), for damping levels of $\xi = 0.01, 2, 4, 6, 8, 10, 20%$. All values were computed with $f_p = T_p = 1$.](./md/media/dmf_by_damping.pdf)

# Spectral Shape Measures as Predictors for Damping Modification Factors

It is conjectured that a given response spectrum contains sufficient
information about the dynamical response of a system to accurately
predict changes in its response due to changes in damping levels, thus
making it a potentially useful and practical predictor of DMF. The complex
dependencies of seismological parameters with respect to the response of
SDOF systems, such as magnitude, fault distance, directivity are
thought to be contained within the shape and ordinate
values of the spectrum; thus, we seek measures to exploit this
information for prediction purposes. One of the first measures of
spectral shapes proposed is the so-called `SaRatio' [@miranda2020] which is
based solely on the 5% critically-damped response spectra discrete data
points. The SaRatio is defined as the 5% critically damped spectral
ordinate at the oscillator period $T$, normalized pointwise by the
geometric mean of the 5% damping ratio spectral ordinates over the
window $[aT, bT]$:

$$S_R(T,a,b) = \frac{S(T,\xi = 5\%)}{\bar{S}([aT,bT])}$$

The denominator represents a "running geometric average" with variable window:

$$\bar{S}([aT,bT]) = \left( \prod_{i = 0}^{N - 1} S\left( (a + \frac{i}{N}(b - a))T,\xi = 5\% \right) \right)^{1/N}$$

where $N$ equals the number of equally spaced ordinates. To evaluate $\bar{S}$ at period $T$, we compute the geometric average in interval $[aT, bT]$ around $T$ for all $N$ equally spaced spectrum ordinates. The limiting values become 1 as $a$ and $b$ approach 1, and the ratio of original spectral ordinates to the total geometric mean as $a = 0$ and $b \to \infty$. This work uses spectral displacement for computing $S_R$ due to numerical stability.

Alternative shape measures could use harmonic or weighted means, or signal processing techniques to exploit spectrum shape information. These possibilities remain unexplored, and the geometric mean choice lacks complete understanding.

Miranda and Miranda (2020) found that for pseudo-acceleration spectra predicting DMF for Chilean interface records, the optimum $a$ value ranges between 0.02 and 0.98 with high variability, while $b$ shows lower variability with optimum values between 1.1 and 1.4.

## Period-implicit scatter plots for all representative wavelets

This study investigates the correlation between SdRatio $S_R$ and DMF for a full suite of representative MP pulses (see Appendix A), seeking $a, b$ values that yield the best predictive model for DMF at given period and damping.

We computed damping modification factors for 14 damping levels: $\xi = 0.01 \approx 0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 15, 20, 30\%$. The period range spans 0.01 to 10s in 0.01s intervals to compute $S_R$ for high $b$ values. We chose spectral displacement as the spectral ratio function $S_R$.

We selected 30 parameter combinations from $a \in [0, 0.02, 0.25, 0.5, 0.75, 0.98] \times b \in [1.02, 1.2, 1.5, 2.0, 2.5]$. This represents a compromise between optimal limits proposed by Miranda and Miranda (2020) and a sufficiently small, well-spaced parameter space for exploration.

We plotted $(S_R, \text{DMF})$ pairs against each other for all wavelets and periods across selected $(\xi, a, b)$ combinations. Period dependency becomes implicit as all spectral ordinates appear as points.

Figure 3 reveals that some scatter plots exhibit linear or quadratic relationships.

![Comparison of different period-implicit scatter plots for different selections of $a, b$ and $\xi$ (in percentage), resulting in a wide variety of scatter forms. Note the seemingly linear and quadratic relationships, alongside interesting branching behavior, e.g., second row second column trace.](./md/media/grid-scatters-paper.pdf)

Analysis of Figure 3 shows that some $(a, b)$ combinations—top-right or bottom-left—produce traces following linear or quadratic relationships. Values of $(a, b)$ close to 1 cause $S_R$ to branch (see second-row second-column trace or third-row first-column trace), which are not useful because the window is too narrow.

The density of points near (1, 1) becomes extreme due to limiting values at both DMF ends for all wavelets. This suggests employing a weighted or robust regression predictor.

# Proposed DMF Predictor

Based on these observations, we consider a simple model to predict the DMF for _any_ MP wavelet:

$$DMF(T, \xi) = \theta(\xi) (S_R(T) - 1) + 1$$

This model captures fundamental physical facts about the DMF and its shape. It has correct limiting values: as $S_R \to 1$, $DMF \to 1$.

We performed weighted least squares regression based on observations from the previous section and Figure 2. We compared model accuracy across sample waveforms and damping levels using root-mean-squared-error (RMSE) as the measure. RMSE quantifies the dispersion of the estimator $\widehat{y}$ around the true value $y_i$:

$$RMSE = \sqrt{\mathbb{E}[(y - \widehat{y})^{2}]} \approx \sqrt{\frac{1}{N}\sum_{i = 1}^{N}(y_i - \widehat{y_i})^{2}}$$

The median RMSE across waveforms measures the median dispersion or variance for fixed $(a, b)$ levels.

We seek $(a, b)$ values that yield the lowest median RMSE with low variance. These values are independent of $T_p$, although their physical significance remains unclear.

Figure 4 shows the distribution of RMSEs across all wavelets and damping values as a boxplot for the 8 $(a, b)$ combinations with lowest median errors.

The middle line inside the box indicates the median. The box height represents the interquartile range—the difference between upper quartile (0.75) and lower quartile (0.25). The whiskers extend 1.5 times the interquartile range from the upper and lower quartiles. Outliers appear as small points and relate to damping levels close to 0.

![Boxplot for the RMSEs achieved by our model for the 8 selections of $(a, b)$ which yielded the lowest median error across all damping values. Most combinations have low median RMSEs.](./md/media/box-plot-paper.pdf)

The $(a, b)$ values yielding lowest median RMSE are $a = 0$ and $b = 2.0$. These values are also the simplest, which might indicate underlying physical significance.

Table 1 gives the regression values for the slope parameter $\theta(\xi)$ of the chosen model.

| $\xi$    | 0.01  | 0.02  | 0.03  | 0.04  | 0.06  | 0.08  | 0.10  | 0.15  | 0.20  | 0.30  |
| -------- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| $\theta$ | 0.093 | 0.062 | 0.036 | 0.016 | 0.015 | 0.045 | 0.076 | 0.156 | 0.238 | 0.404 |

: Slope values for the proposed model as a function of damping value. The maximum damping value recommended for use is 0.30. Use linear interpolation for values not listed explicitly.

**Algorithm 1** DMF estimation using spectral ratio

**Input:** 5% damped displacement spectrum, target damping ratio $\xi$, structural period $T$

**Output:** DMF value for the target damping ratio and period

1. **Compute spectral ratio:** Calculate $S_R(T)$ using the spectral ratio equation

2. **Interpolate slope parameter:** For target damping ratio $\xi$, interpolate slope parameter $\theta(\xi)$ from Table 1. Use linear interpolation for damping values not explicitly listed

3. **Calculate DMF:** Apply the DMF predictor equation:
   $$DMF(T, \xi) = 1 + \theta(\xi) \cdot (S_R(T) - 1)$$

4. **Return:** The computed DMF value

# Goodness-of-fit against MP-wavelets

Figure 5 shows linear fits to four different damping levels, colored by period.

![Linear weighted fit for 4 different damping levels colored by period](./md/media/scatter_grid.pdf)

Note that this particular shown fit was not forced to pass through (1,1) for practical purposes it naturally did for almost all dampings, which shows the adequacy of the model to the data.

## Direct comparison

Figures 6 and 7 compare the exact DMF (black) with predictions from the proposed model for sample wavelets.

![Direct comparison of the model against the DMF of sample wavelets for 0% critical damping.](./md/media/direct-0.pdf)
![Direct comparison of the model against the DMF of sample wavelets for 10% critical damping.](./md/media/direct-10.pdf)

The model closely matches the original DMF shapes, even for 0% critical damping. The main peak is captured accurately.

The loss of smoothness observed DMF discussed in section 3 partially captured in $T/T_p > 0.5$ but is not that accurate in the high-frequency regime $T/T_p \in (0,0.2)$. Errors in that `ringing' area are not too concerning since it is a small regime.

We note that it is somewhat surprising to have such a good fit for a model with only a single parameter ($\theta$) and no underlying pulse or seismological parameters.

### Analysis of residuals

Figure 8 shows residuals between predicted and true DMF as functions of SdRatio for $\xi \approx 0\%$. Many points cluster near 1, which contributes to non-constant variance in the residuals.

A wavy pattern in the plot relates to residuals at the peaks of different wavelets.

![Residuals between our predicted DMF and the true DMF as functions of SdRatio for $\xi \approx 0$](./md/media/residuals_plot.pdf)

Statistical tests on error homoscedasticity reject the null hypothesis with $p$-values near zero. Power transforms such as Box-Cox or Box-Tidwell could address heteroscedasticity, but would complicate the model unnecessarily. Removing data for $T/T_p < 0.83$ improves $p$-values, but the null hypothesis of homoscedasticity is still rejected.

### Justification of the goodness-of-fit

This section justifies the model's adequacy despite heteroscedasticity.

The model is used for prediction, not inference, so non-constant variance is less critical in this case. Mankiw (2016) notes that heteroscedasticity "has never been a reason to throw out an otherwise good model." The heteroscedasticity may reveal information about SdRatio variation at wavelet peaks.

Figures 6 and 7 provide the strongest evidence of goodness-of-fit, showing that the model faithfully captures DMF shape across all wavelets and damping levels.

The model's limiting values are physically sound, and the fit passes naturally through (1,1) without being forced, which supports the model's validity.

Perhaps unsurprisingly, the proposed model is a good predictor for
MP-wavelets, since it was developed specifically for these pulses. But a
reasonable question arises: how would the presented model perform for
other pulse-like ground motions, none of which were used in its
development? This will be discussed in the following section.

# Comparison against other narrow-band ground motions

This exploration tests our conjecture that most information required to predict the DMF resides within $S_R$. If true, the model developed using only MP-wavelets should perform well for other ground motions, even with different frequency content.

We employed Tarquis pulses for this comparison. These simple waveforms represent sinusoidal pulses corrected to become realistic ground motion representations[@tarquis1988; @arroyo2007]. Figure 9 shows the three different Tarquis pulses used in this study. The 20 and 50 second durations exceed realistic strong ground motion durations but were selected to strain the proposed model's predictive limits.

![Tarquis accelerograms for 5, 20, and 50 seconds with unit amplitude and frequency.](./md/media/tarquis-pulses.png)

Figure 10 presents four sample DMFs for different damping and pulse combinations. The proposed model captures the main resonant peak accurately, except for very low damping levels combined with high durations, where the peak becomes very sharp. This suggests that explicit duration inclusion could improve the model.

The erratic non-smooth regime of $T/T_p < 0.83$ also remains incompletely captured.

![Comparison of the true DMF for Tarquis pulses vs the proposed predictor for different critical damping levels.](./md/media/tarquis_2x2.pdf)

# Summary and Conclusions

The closed-form displacement response of a viscously-damped oscillator
to an MP-pulse was presented; this representation allows for analytic
and parametric studies of the response of SDOF systems to pulse-like
ground motions. It was noted that only the "modulation" $\gamma$ and the phase
shift $\nu$ of the pulse are required to capture the complete response
variability of a SDOF system to such wavelets. A DMF estimator based on
the spectral shape measure SaRatio $S_R$ was proposed that has a
sound physical basis, possesses the correct limiting values for short
and long period ranges, and is simpler than others found in the
literature.

We proposed a DMF estimator based on the spectral shape measure SaRatio $S_R$ that possesses sound physical basis, correct limiting values for short and long period ranges, and an elegant simplicity not found in other literature models.

The proposed estimator requires a single parameter dependent on the target damping level and uses only the 5% critically damped displacement spectrum as input. No record-specific or seismological parameters are needed.

The estimator produced low median errors and low variance for all damping ratios across MP-wavelets, including damping levels close to 0.

A predictive study using realistic narrow-band ground motions, the Tarquis pulses, demonstrated the model's simplicity and power. The model showed good predictive capability despite not being specifically developed for these narrow-band records.

This work establishes that spectral shape measures can construct simple and accurate DMF predictors for real NFPL ground motions, representing the next logical research step.

The authors are unaware of the physical explanation as to why the SdRatio is
such a good predictor despite being so simple, which implies that further research is required
to explore the reasons and limits of its predictive power.

# Acknowledgments

# Author contributions

Carlo Ruiz reviewed and compiled the relevant literature, performed the
computations, generated the figures, and typeset the paper. Mario Ordaz
provided the main research direction and guidance, proposed the
functional forms of the period-implicit predictor (equations for spectral ratio and geometric mean),
and suggested the exploration of its predictive power against
narrow-band motions.

# Financial disclosure

The first author would like to acknowledge and express his gratitude to
the Instituto de Ingeniería at UNAM, Mexico, for the financial support
given to him during his doctoral studies. He would also like to
acknowledge and express his gratitude to the SNI, CONAHCYT, Mexico, for
the financial support received during the preparation of the paper.

# Conflict of interest

The authors declare no potential conflict of interest.

# Appendix A

## Suite of wavelets used in this study

We present the set of representative wavelets used in this study (Figure 11),

As explained, $A$ and $f_p$ are immaterial to the DMF and a such only $\gamma, \nu$ need to be varied. Therefore, for simplicty a total of $11\times 6=66$ pulses were constructed from the cartesian product of

$\gamma \in [ 1, 1.2, 1.4, 1.6, 1.8, 2, 2.2, 2.4, 2.6, 2.8, 3]$ and
$\nu \in [0, 1/3 \pi, 2/3 \pi, \pi, 4/3 \pi, 5/3 \pi ]$

This way, the suite is small enough to be easily reproducible and includes much of the information content from the wavelets. For any given NFPL record, we could potentially conceive that one (or simultaneously many) of such wavelets could approximate its velocity waveform if fit appropriately.

We excluded pulses with $\gamma > 3$ as they are not representative of real near-fault pulse-like waveforms.

![Sample of the family of 66 representative wavelets used in this study. Note that higher $\gamma$ lead to more modulation and different values of $\nu$ affect the phase of the pulses. ](./md/media/pulse-suite.pdf)

# Appendix B

## Proof of $f_p$ being immaterial to the DMF of MP-wavelets

both an analytical and a geometric/visual proof.

<!-- TODO -->

# References
