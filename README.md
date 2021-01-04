# Genetic Program library
This project contains a basic implementation of the Genetic Programming operations along with examples of how they can be used to solve specific computational problems.

There are two main components of this library, the `GeneticProgram` and `Tree` classes. In this section we will show the operations provided step by step.

* ## Tree class

    This class is a recursive `'rootless'` abstraction of a `binary tree`. This means that a `Tree` is composed by a `value` and two other `Tree` the `left` and the `right`. It is probably the most natural representation of this data structure and it is also easy to read.

    Along with the data representation the class also provides the most basic operations for the `Genetic programming` paradigm
    which are `copy`, `print`, `evaluate`.

    Creating and Printing a Tree:

    ```python
        from Tree import Tree

        left = Tree(1,is_leaf=True)
        right = Tree(2,is_leaf=True)
        my_first_tree = Tree("+",is_leaf=False,size=3,left=left,right=right)
        my_first_tree.print()
    ```

    The result will be:

    ![](https://raw.githubusercontent.com/humbertordrgs/NN_GP_T_3/develop/assets/init.png)
    
    In this example we created our first `Tree` instance and there are a few important things to mention:

    *   Every instance has a `is_leaf` attribute which is important for the correct behavior of the methods in the class.

    *   Every `Tree` has a size attribute which needs to be consistent and should be **left.size + right.size + 1**. This is achieved modifying the instance using the functions provided in this class and not in a direct way, always that the `size` is involved.

    Copying a Tree:

    This is one of the most basic operations of the genetic algorithm implementation of this project.

    ```python
        my_copied_tree = my_first_tree.copy()
        my_first_tree.value = "-"
        my_copied_tree.print()
    ```
    
    The result in this case should be exactly the same as before due to the copy method not keeping any reference to the original instance.

    Evaluating a Tree: There are two methods provided by this library to do this `eval_in_order` and `eval_post_order` both of them returns a `string` with an executable `python` statement.     

    *   eval_in_order: This methods apply extract an in order representation of the `Tree`(<left_subtree> <current_value> <right_subtree>) it is ideal when the information inside the `Tree` contains only constants values. It will use the `__str__` of each node in the instance.

    *    eval_post_order: This methods works under the assumptiom that every not leaf value in the `Tree` is a python function with exactly two arguments. The result will have the following pattern: `<not_leaf_value>(<left_subtree,right_subtree>)`

    Example: 
    
    ```python
        def custom_div(x, y):
            if y == 0:
                return 1init
            return x / y

        custom_div.__str__ = lambda : "/"

        left = Tree(1,is_leaf=True)
        right = Tree(0,is_leaf=True)
        evaluable_tree = Tree(custom_div,is_leaf=False,size=3,left=left,right=right)
    ```

    ```python
        evaluable_tree.eval_in_order()
        #Output  '1/0'

        evaluable_tree.eval_post_order()
        #Output 'custom_div(1, 0)'
    ```

    It is important to notice the difference in the results.

    The idea is that the results of this functions should be setted in the appropiate context in case using variables and then execute it using python `eval` built in method.

    ## Indexing subtrees: 
    Every `Tree` instance is indexed in specific way which follows the next pattern:

    current_node = i
    left_subtree = i +init 1
    right_subtree = i + 1 + left_subtree.sizeinit

    ```python
        for i in range(0,tree.size)
    ```

    These indexes are used to retrieve and update specific subtrees

    ## Updating Subtree:
    This functions replace the desired subtree.

    ```python
        left = Tree(1,is_leaf=True)
        right = Tree(2,is_leaf=True)
        updatable_tree = Tree("+",is_leaf=False,size=3,left=left,right=right)

        n_left = Tree(3,is_leaf=True)
        n_right = Tree(4,is_leaf=True)
        replacement_tree = Tree("*",is_leaf=False,size=3,left=n_left,right=n_right)

        updatable_tree.update_sub_tree(2,replacement_tree)
        updatable_tree.print()
    ```
    
    Resulting in:
    
    ![](https://raw.githubusercontent.com/humbertordrgs/NN_GP_T_3/develop/assets/updated.png)

* ## GeneticProgram class

    This is the second component of our library in which we configure all the enviroment needed for our experiments.

    When creating an instance of this class We need to define several mandatory things as follows:

    *   Population Size: Exact number of individuals inside a population

    *   Terminals: Array of values that will be used as terminals (tree leafs only)

    *   Non-Terminals: Array of values (mostly operations) that will  appear in the non-leaf subtrees.

    *   Generate_individual: A mandatory function with the following sign:

        ```python
        def generate_tree(max_tree_deepness, terminals, non_terminals, variables, variables_prob)
        ```
        that should return an instance of the `Tree` class 
    
    *   Fitness: A mandatory function which receives an instance of the `Tree` class as the only parameter and returns an scalar with the result of evaluating the tree in the right context.

    *   Selection: A string with the values `tournament` or `roulette`.

    *   Reproduction: A string with the values `crossover` or `variant`.
    *   End Criteria: A mandatory function which returns a boolean value, if True is received by the engine end criteria has been achieved.

    *   Variables: An optional array of values that will be also be considered as terminals.

    *    Variables prob: An optional scalar wich indicates the probability that a terminal is a variable or not.

    *   Max tree deepness: An optional integer with the maximum desired deepness for the instances of the `Tree` class.

    ```python
        # This method can have more parameters than the ones specified but not less
        def generate_tree(max_tree_deepness, terminals, non_terminals, variables, variables_prob):

            # Dummy use of the terminals just for the example
            left = Tree(terminals[0],is_leaf=True)
            right = Tree(terminals[-1],is_leaf=True)
            fixed_tree = Tree(non_terminals[0],is_leaf=False,size=3,left=left,right=right)
            return fixed_tree

        def custom_sum(x, y):
            return x + y

        custom_sum.__str__ = lambda : "+"

        def fitness(tree):
            return abs(20 - eval(tree.eval_post_order()))

        end_criteria = lambda x: x == 0
        terminals = [1,2,3,5,7]
        non_terminals = [custom_sum] 

        my_engine = GeneticProgram(
            10,
            terminals,
            non_terminals,
            generate_tree,
            fitness,
            "roulette",
            "crossover",
            end_criteria,
            max_tree_deepness=2
        )
        best, b_fitness =  my_engine.run(1)
        best.print()
    ```

    Resulting in:

    ![](https://raw.githubusercontent.com/humbertordrgs/NN_GP_T_3/develop/assets/dummy.png)
