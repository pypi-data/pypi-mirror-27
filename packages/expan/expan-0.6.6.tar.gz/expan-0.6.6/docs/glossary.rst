==========
Glossary
==========


Assumptions used in analysis
------------------------------------

1. Sample-size estimation

  * Treatment does not affect variance
  * Variance in treatment and control is identical
  * Mean of delta is normally distributed

2. Welch t-test

  * Mean of means is t-distributed (or normally distributed) 

3. In general

  * Sample represents underlying population
  * Entities are independent


Per-entity ratio vs. ratio of totals
------------------------------------

There are two different definitions of a ratio metric (think of e.g. conversion rate, which is the ratio between the number of orders and the number of visits): 1) one that is based on the entity level or 2) ratio between the total sums, and **ExpAn** supports both of them.

In a nutshell, one can reweight the individual **per-entity ratio** to calculate the **ratio of totals**. This enables to use the existing ``statistics.delta()`` function to calculate both ratio statistics (either using normal assumtion or bootstraping).

Calculating conversion rate
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As an example let's look at how to calculate the conversion rate, which might be typically defined per-entity as the average ratio between the number of orders and the number of visits:

.. math::

	\overline{CR}^{(pe)} = \frac{1}{n} \sum_{i=1}^n CR_i = \frac{1}{n} \sum_{i=1}^n \frac{O_i}{V_i}

The ratio of totals is a reweighted version of :math:`CR_i` to reflect not the entities' contributions (e.g. contribution per custormer) but overall equal contributions to the conversion rate, which can be formulated as:

.. math::

	CR^{(rt)} = \frac{\sum_{i=1}^n O_i}{\sum_{i=1}^n V_i}

Overall as Reweighted Individual
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

One can calculate the :math:`CR^{(rt)}` from the :math:`\overline{CR}^{(pe)}` using the following weighting factor (easily proved by paper and pencile):

.. math::

	CR^{(rt)} = \frac{1}{n} \sum_{i=1}^n \alpha_i \frac{O_i}{V_i}

with

.. math::

	\alpha_i = n \frac{V_i}{\sum_{i=1}^n V_i}

Weighted delta function
^^^^^^^^^^^^^^^^^^^^^^^

To have such functionality as a more generic approach in **ExpAn**, we can introduce a *weighted delta* function. Its input are

- The per-entity metric, e.g. :math:`O_i/V_i`
- A reference metric, on which the weighting factor is based, e.g. :math:`V_i`

With this input it calculates :math:`\alpha` as described above and outputs the result of ``statistics.delta()``.


Early stopping
------------------------------------

Given samples x from treatment group, samples y from control group, we want to know whether there is a significant difference between the means :math:`\delta=\mu(y)−\mu(x)`.
To save the cost of long-running experiments, we want to stop the test early if we are already certain that there is a statistically significant result.

You can find links to our detailed documentations for
`concept of early stopping <https://github.com/shansfolder/AB-Test-Early-Stopping/blob/master/docs/EarlyStoppingConcept/EarlyStoppingConcept.pdf>`_ and
`early stopping methods we investigated <https://github.com/shansfolder/AB-Test-Early-Stopping/blob/master/docs/EvaluateEarlyStopping/EvaluatingEarlyStopping.pdf>`_.


Subgroup analysis
------------------------------------
Subgroup analysis in ExaAn will select subgroup (which is a segment of data) based on the input argument, and then perform a regular delta analysis per subgroup as described before. 

That is to say, we don't compare between subgroups, but compare treatment with control within each subgroup.


Multiple testing problem
------------------------------------
ToDo