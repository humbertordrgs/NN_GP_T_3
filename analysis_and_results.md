# 1) Des Chiffres et des Lettres (Variation)

## Problem
French television programme where two contestants compete against one another, this game consists of different rounds each having a set of rules and objectives for each player (numbers round, letters round, duels, final sprint and lets mots de la fin). 

For this project we will focus on the numbers round. This round has the goal of arriving to a chosen number using arithmetic operations (+, -, *, /) applied to randomly selected numbers. The players have limited time to provide a combination of operations over the randomly selected numbers to arrive at the goal number.

As an optional objective, make sure that there is no duplicate numbers. Each number must appear only once in a tree.

## Solution
In general terms our solution for this problem can be expressed as the set of different parameters that configure the `GeneticProgram` instance. Specifically we used populations of `1000` individuals.

Regarding the terminals and non_terminals, we used the natural approach of using the given numbers and defined custom functions that represent the most basic arithmethic operations (`+`,`-`,`*`,`/`) respectively. Our goal number is established and used inside the created fitness method. For this exercise we used `459` as target and [25,7,8,100,4,2] as the input values.

Our library was built based on a minimization approach this means that a lower fitness value is better. Due to this, the respective fitness method built for this problem can be interpreted as the absolute value of the difference between our goal number and the one obtained evaluating the current tree.

Our end criteria is based off our fitness value, if the fitness value of an individual is `0` then our goal has been reached and the end criteria met.

In this variation of the original problem we are allowed to use the same terminal number  multiple times, because of this the max deepness of the individuals that is used is (`4`). Normally changing this value can help the engine to find better solutions faster.

An important side note is that the custom version of the division operation is returning `1` in all the cases where the denominator is `0`.


(fitness definition and why it is defined this way, individual composition and population generation)

## Results
fitness charts, chart labels,axis, title and others explanation

## Conclusion

# 2) Derivative Expression
## Problem
The objective of this task is to find a function described by a set of given points, specifically we will be estimating the derivative expression of a function.
## Solution
The first step to solve this problem is to define the function we desire to calculate its derivative expression, also we need to define the set of given points to test our results with them.

Regarding the function definition we used `sympy` symbols to be able to create the expression we want to work with. After that, we define our `ground_truth` using the `diff` method in sympy which will calculate the correct derivative expression for the function we defined before.

The Expression used was: `x**2 - 6*x + 1`

Now we need the set of points to be used for the evaluation, this is done using a python `range` defining a discret interval from [-1.0,1.0,0.1](30 points).

In terms of the terminals to be used we defined a set with all the integers between `0` and `9` inclusive.

An important difference with the previous solved problem is that in this case we actually need to use the `variable` attribute of our engine which add an additional set of terminals, in this case the `x` value only with a `variable_prob` of `0.7`. This probility can be interpreted as the probability a terminal has to be `x`. It was estimated through different experiments and it is also a hyper parameter of this approach.

Regarding the population size we used `100`, a smaller amount compared with the previous exercise. This is because the fitness calculation for this problem is more complex and it takes longer in time due to the size of the elected interval (can be modified to run quicly or to get estimations of the derivative expression and not necesarilly the exact one).

To help the engine with the convergence to better solutions we reduced `max_tree_deepness` to `2`

As we showed before We will be comparing in our charts the behaviour of the `fitness` depending of which selection method is used.









## Results

## Conclusion
