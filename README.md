# Genetic Program library
This work contains a basic implementation of the Genetic Programming operations along with examples of how can be use to solve specific computational problems.

There are two main components of this library the `GeneticProgram` and the `Tree` classes. In this section we will show the operations provided step by step.

* ## Tree class

    This class is a recursive `'rootless'` abstraction of a `binary tree`. This means that a `Tree` is composed by a `value` and two other `Tree` the `left` and the `right`. It is probable the most natural representation of this data structure and it is easier to read.

    Along with the data representation the class also provides the most basic operations for the `Genetic programming` paradigm
    which are `copy`, `print`, `evaluate`.

    Creating and Printing a Tree:

    ```python
        from Tree import Tree

        left = Tree("1",is_leaf=True)
        right = Tree("2",is_leaf=True)
        my_first_tree = Tree("0",is_leaf=False,size=3,left=left,right=right)
        my_first_tree.print()
    ```

    The result will be:

    ![](https://raw.githubusercontent.com/humbertordrgs/NN_GP_T_3/develop/assets/init.png)
    
    In this example we created our first `Tree` instance and there few important things to mention:

    *   Every instance has a `is_leaf` attribute which is important for the right behavior of the methods in the class.

    *   Every `Tree` has a size attribute which needs to be consistent and should be **left.size + right.size + 1**. This is achieved modifying the instance using the functions provided in this class and not in a direct way always that the `size` is envolved.

    Copying a Tree:

    This operation is the base of the main Genetic operations and it is pretty simple to use.

    ```python
        my_copied_tree = my_first_tree.copy()
        my_first_tree.value = "a"
        my_copied_tree.print()
    ```
    
    The result in this case should be exactly the same as before due to the copy method does not keep any reference to the original instance

    Evaluating a Tree:

    ```python
        

    ```
