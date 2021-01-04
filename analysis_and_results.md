# 1) Des Chiffres et des Lettres (Variation)

## Problem
French television programme where two contestants compete against one another, this game consists of different rounds each having a set of rules and objectives for each player (numbers round, letters round, duels, final sprint and lets mots de la fin). For this project we will focus on the numbers round, which 

## Solution
In general terms our solution for this problem can be expressed as the set of different parameters that configure the `GeneticProgram` instance. Specifically we used populations of `1000` individuals.

Regarding the terminals and non_terminals, we used the natural approach of using the given numbers and defined custom functions that represent the most basic arithmethic operations (`+`,`-`,`*`,`/`) respectively.

In this terms our goal number is established and used inside the created fitness method.

Our library was built based on a minimization approach this means that a lower fitness value is better. Due to this, the respective fitness method built for this problem can be interpreted as the absolute value of the difference between our goal number and the one obtained evaluating the current tree.

In terms of the end criteria based on our fitness value is trivial then to define that if the fitness value for an individual is `0` then our goal has been reached.

We did several tests changing the selection and reproduction method but and we selected `tournament` and normal `crossover` respectively.

In this variation of the original problem we are allowed to use multiple times the same terminal number, is because of this that the max deepness of the individuals is the default (`4`). Normally changing this value can help the engine to find better solutions faster.

An important side note is that the custom version of the division operation is returning `1` in all the cases the denominator is `0`.








(fitness definition and why it is defined this way, individual composition and population generation)

## Results
fitness charts, chart labels,axis, title and others explanation

## Conclusion

# 2) Derivative Expression
## Problem

## Solution

## Results

## Conclusion
