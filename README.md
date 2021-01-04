# Genetic Program library
This work contains a basic implementation of the Genetic Programming operations along with examples of how can be use to solve specific computational problems.

There are two main components of this library the `GeneticProgram` and the `Tree` classes. In this section we will show the operations provided step by step.

* ## Tree class

    This class is a recursive `'rootless'` abstraction of a `binary tree`. This means that a `Tree` is composed by a `value` and two other `Tree` the `left` and the `right`. It is probable the most natural representation of this data structure and it is easier to read.

    Along with the data representation the class also provides the most basic operations for the `Genetic programming` paradigm
    which are `copy`, `print`, `evaluate`.

    Creating a Tree:

    ```python
        from Tree import Tree

    ```




