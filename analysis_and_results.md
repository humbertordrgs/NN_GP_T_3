# 1) Des Chiffres et des Lettres (Variation)

## Problem
French television programme where two contestants compete against one another, this game consists of different rounds each having a set of rules and objectives for each player (numbers round, letters round, duels, final sprint and lets mots de la fin). 

For this project we will focus on the numbers round. This round has the goal of arriving to a chosen number using arithmetic operations (+, -, *, /) applied to randomly selected numbers. The players have limited time to provide a combination of operations over the randomly selected numbers to arrive at the goal number.

As an optional objective, make sure that there is no duplicate numbers. Each number must appear only once in a tree.

## Solution
In general terms our solution for this problem can be expressed as the set of different parameters that configure the `GeneticProgram` instance. Specifically we used populations of `1000` individuals.

Regarding the terminals and non_terminals, we used the natural approach of using the given numbers and defined custom functions that represent the most basic arithmethic operations (`+`,`-`,`*`,`/`) respectively. Our goal number is established and used inside the created fitness method. For this exercise we used `459` as target and [25,7,8,100,4,2] as the input values.

Our library was built based on a minimization approach this means that a lower fitness value is better. Due to this, the respective fitness method built for this problem can be interpreted as the absolute value of the difference between our goal number and the one obtained evaluating the current tree. For practical reasons and to have a more stable computational version of these experiments, we estabished the maximum fitness value for an individual as the goal number itself.

Our end criteria is based off our fitness value, if the fitness value of an individual is `0` then our goal has been reached and the end criteria met.

In this variation of the original problem we are allowed to use the same terminal number  multiple times, because of this the max deepness of the individuals that is used is (`4`). Normally changing this value can help the engine to find better solutions faster.

An important side note is that the custom version of the division operation is returning `1` in all the cases where the denominator is `0`.

Regarding the generation of individuals (`Tree`) we used a `pre-order` oriented function that will be adding subtrees and navigating it. In each step we calculate the probability of this node being a leaf, taking into account the relation between `current_level` and the `max_tree_deepness`.

Finally the number of generations used in the `run` method was `10`.

## Results
We will be showing in this section charts of the form `Generation` Vs `Fitness`, the idea is to observe how the fitness changes along generations and what is the impact of the selection method used, in the convergence to better solutions. 

*   Avg Fitness value using Roulette:

    ![](https://raw.githubusercontent.com/humbertordrgs/NN_GP_T_3/develop/assets/avg_roulette_task1.PNG)

*   Avg Fitness value using Torunament:

    ![](https://raw.githubusercontent.com/humbertordrgs/NN_GP_T_3/develop/assets/avg_tournament_task1.PNG)


*   Min Fitness value using Roulette:

    ![](https://raw.githubusercontent.com/humbertordrgs/NN_GP_T_3/develop/assets/min_roulette_task1.PNG)

*   Min Fitness value using Torunament:

    ![](https://raw.githubusercontent.com/humbertordrgs/NN_GP_T_3/develop/assets/min_tournament_task1.PNG)

The first thing to notice is that the tournament charts are not reaching Generation `10`, they are converging to a solution faster than roulette. As we mention, for this problem, the maximum `fitness` value is never higher than the goal number.

## Conclusion
As we can observe in the previous charts, there is a clear tendency of the tournament algorithm being able to find good solutions in less generations than when using the roulette algorithm. Even though, in some cases when the calculation of the fitness for an individual is expensive, it is possible for a roulette strategy combined with a bigger population size to outperform a tournament approach. In problems where the possibility of being stuck in a local minimum exists, a tournament approach is still a valid option combined with a higher mutation rate.

# 2) Derivative Expression
## Problem
The objective of this task is to find a function described by a set of given points, specifically we will be estimating the derivative expression of a function in an specific discretized interval.
## Solution
The first step to solve this problem is to define the function we desire to calculate it's derivative expression. We also need to define the set of given points that we will use to test our results.

Regarding the function definition, we used `sympy` symbols to be able to create the expression we want to work with. After that, we define our `ground_truth` using the `diff` method in `sympy` which will calculate the correct derivative expression for the function we defined before.

The Expression used was:  `x**2 - 6*x + 1`

Now we need the set of points to be used for the evaluation, this is done using a python `range` defining a discretized interval from [-1.0,1.0,0.1](30 points in total).

For the terminals to be used, we defined a set with all the integers between `0` and `9` inclusive.

An important difference with the previous solved problem is that in this case we actually need to use the `variable` attribute of our engine which adds an additional set of terminals, in this case the `x` value only, with a `variable_prob` of `0.7`. This probility can be interpreted as the chance a terminal has to be the `x` variable. The value of `variable_prob` was estimated through different experiments and it is also a hyper parameter of this approach.

Regarding the population size we used `100`, a smaller amount compared with the previous task. As this problem is more complex the fitness calculation takes longer, mainly due to the size of the selected interval (this interval can be modified depending of the desired result, more points implies a better estimation).

The fitness function for this task evaluates the expression obtained from the current individual in each element of the discretized interval. The result of this is compared to the evaluation using the `ground_truth` and the absolute difference is accumulated. Once the whole interval has been processed the fitness value will be the sum of all the stored differences.

The end criteria for this task is met, once the fitness value (accumulated error across the interval) is less than `0.1`.

To help the engine with the convergence to better solutions we reduced `max_tree_deepness` to `2`.

Another important difference with the first task is we used `variant crossover` as the reproduction method.

We tested with a maximum of `20` generations in this task.

## Results
As we showed before We will be comparing in our charts the behaviour of the `fitness` based on which selection method is used. As we did in the first task we also added a maximum value for the maximum fitness of `1000`.

*   Avg Fitness value using Roulette:

    ![](https://raw.githubusercontent.com/humbertordrgs/NN_GP_T_3/develop/assets/avg_roulette_task2.PNG)

*   Avg Fitness value using Torunament:

    ![](https://raw.githubusercontent.com/humbertordrgs/NN_GP_T_3/develop/assets/avg_tournament_task2.PNG)


*   Min Fitness value using Roulette:

    ![](https://raw.githubusercontent.com/humbertordrgs/NN_GP_T_3/develop/assets/min_roulette_task2.PNG)

*   Min Fitness value using Torunament:

    ![](https://raw.githubusercontent.com/humbertordrgs/NN_GP_T_3/develop/assets/min_tournament_task2.PNG)


## Conclusion

We can observe on the charts generated in the previous section that even though we used a different reproduction strategy the tendency we observed on task 1 of tournament converging faster than roulette are still present.

# Global Notes:

All the experiments used the same `generate_tree` function.

The data used to generate the studied charts were all generated by running the exact same engine configuration `3` times and averaging the results for each generation.

The detailed information, code and interactive charts are available [here](https://colab.research.google.com/drive/1xppHvwZkNOJSmGPmyPFRcnr7V9xllsIg?usp=sharing).