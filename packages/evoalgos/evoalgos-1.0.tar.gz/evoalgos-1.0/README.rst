
evoalgos has been tested with Python 2.7 and 3.6. The recommended version is
Python 3.x, because compatibility is reached by avoiding usage of xrange. So,
the code has a higher memory consumption under Python 2.

Everything in this package is pure Python. For a description of the contents
see DESCRIPTION.rst.


Changes
=======

1.0
---
* Corrected documentation for NearestBetterSorting.
* Added two functions calc_contributions and calc_contributions_2d in
  HyperVolumeIndicator to be able to assess exclusive hypervolume contributions
  directly there.
* Simplified HyperVolumeContributionSorting by using the functionality now
  available in HyperVolumeIndicator.
* Implemented greedy forward selection in HyperVolumeContributionSelection.
* Made the `already_chosen` argument functional in
  HyperVolumeContributionSelection and TruncationSelection.
* Added an archive as an attribute to EvolutionaryAlgorithm, which is then
  passed as the already_chosen argument to selection.

0.9
---
* Added a random permutation of the population before the survivor selection, to
  break ties randomly (in the following stable sorting).
* Replaced SBXIndividual with ESIndividual in the SMS-EMOA example in the
  documentation.
* Adapted the parallelization example in the documentation to the interface
  changes in optproblems 1.1.
* Added a convenience class CMSAES with a function minimize that mimics the
  SciPy interface to all optimization algorithms.
* Changed order of arguments num_offspring and max_age in EA constructors.

0.8
---
* Added performance measures PeakRatio, PeakDistance, PeakInaccuracy, and
  AveragedHausdorffDistance for multi-local optimization.
* Applied the template function design pattern to recombination just as in
  mutation. Now, method _recombine must be overridden in individuals.
* Implemented CMSAIndividual with covariance matrix self-adaptation. This
  induces a dependency on NumPy.
* Made it possible to call individual.recombine with num_parents == 1 in
  ESReproduction. This is also supported by a few individuals.

0.7
---
* Added FixedSizeSetIndividual to evoalgos.individual. It can be used to evolve
  sets of fixed size and bitstrings with a fixed number of ones.
* evoalgos.reproduction.ESReproduction got a new argument
  "redetermine_first_parent".
* Added a function connected_components to
  evoalgos.niching.NearestBetterClustering.
* Added forgotten documentation for RankSumSorting.

0.6
---
* Gave distance function argument a default for NearestBetterSorting and
  NearestBetterSelection.
* Changed the provided distance for NearestBetterSorting and
  NearestBetterSelection from squared Euclidean distance to Euclidean distance.
* Added a module evoalgos.niching with the two basin identification methods
  TopographicalSelection and NearestBetterClustering.
* Moved the inner class NearestBetterSorting.DistMatrixFunction to its own
  module. New place: evoalgos.distance.DistMatrixFunction.

0.5
---
* Simplified the code in the sorting module.
* Added sorting component RankSumSorting for many-objective optimization.
* Added a multiobjective mode of operation to NearestBetterSorting and
  NearestBetterSelection.

0.4
---
* LexicographicSorting can now also sort when objective values are just scalars.
* Implemented NearestBetterSorting and NearestBetterSelection.
* identify_groups() and identify_best_group() of CrowdingDistanceSorting and
  HyperVolumeContributionSorting now also consider the respective secondary
  criteria (before: only dominance relation).
* Added documentation about parallelization.

0.3
---
* Added BinaryIndividual for optimization in binary search spaces.
* Added convenience classes CommaEA and PlusEA, which are special cases of
  EvolutionaryAlgorithm. By default, they are intended for single-objective
  optimization.

0.2
---
* Implemented the NSGA2b (NSGA2 with extensions).
* Fixed bug when individuals with identical objective values should be sorted
  by HyperVolumeContributionSorting (led to "unorderable types" exception
  under Python 3).
* Changed default setting for parameter "prefer_boundary_points" of SMSEMOA
  to True.

0.1
---
* Initial version containing the SMS-EMOA.
