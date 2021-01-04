import numpy as np
from random import randint, random


'''
  This is the main file of the library it contains the GeneticProgram class
  Which is a basic implementation of the Genetic Programming operations

  In order to set a custom probability for a specific terminal subset we use the 
  parameters `variables` and `variables_prob`, these can also be interpreted as a 
  hyper parameter of the model.
'''
class GeneticProgram():
  '''
    Parameters:
    - Population size
    - Terminal Values (Leaf Nodes)
    - Allowed non_terminals (Operator Nodes)
    - Function used to generate a new individual (Tree class)
    - Function of fitness to be used
    - Specify the selection method to be used
    - Specify the reproduction method to be used
    - Method to recognize when end criteria is met
    - Max deepness of trees handled in the engine
    - Chance to mutate an individual
    - Variable list, is used also as terminals
    - Probability that a terminal is a `variable` or common 
  '''
  def __init__(
    self,
    population_size,
    terminals,
    non_terminals,
    generate_individual,
    fitness,
    selection,
    reproduction,
    end_criteria,
    max_tree_deepness=4,
    mutation_prob=0.25,
    variables=[],
    variables_prob = 0.0
  ):
    self.population_size = population_size
    self.terminals = terminals
    self.non_terminals = non_terminals
    self.generate_individual = generate_individual
    self.fitness = fitness
    self.selection = self.tournament_selection if selection == "tournament" else self.roulette_selection
    self.reproduction = self.crossover if reproduction == "crossover" else self.variant_crossover
    self.end_criteria = end_criteria
    self.max_tree_deepness = max_tree_deepness
    self.mutation_prob = mutation_prob
    self.variables = variables
    self.variables_prob = variables_prob

    # Generate initial population
    self.population = self.generate_initial_population()

  '''
    This Method will generate the initial population calling the mandatory `generate` method provided
  '''
  def generate_initial_population(self):
    res = []
    for i in range(self.population_size):
      res.append(self.generate_individual(self.max_tree_deepness,self.terminals,self.non_terminals,self.variables,self.variables_prob))
    return res
  
  '''
    Auxiliar method to extract `parents` avoiding duplicates
  '''
  def gen_rand_with_memory(self, prev_idxs):
    while (True):
      new_rand = randint(0, self.population_size - 1)
      flag = True
      for idx in prev_idxs:
        if (new_rand == idx):
          flag = False
          break
      if (flag):
          return new_rand

  '''
    Implementation of the roulette selection method
  '''
  def roulette_selection(self):
    parent_idxs = []
    for i in range(0, 2):
        parent_idxs.append(self.gen_rand_with_memory(parent_idxs))
    return [self.population[idx] for idx in parent_idxs] 

  '''
    Implementation of the torunament selection method
  '''
  def tournament_selection(self):
    parent_idxs = []
    for i in range(0,2):
      prospect_idxs = []
      fit_vals = []
      for i in range(0,min(5,len(self.population)) - len(parent_idxs) ):
        prospect_idxs.append(self.gen_rand_with_memory(prospect_idxs + parent_idxs))
        fit_vals.append(self.fitness(self.population[prospect_idxs[-1]]))
      parent_idxs.append(prospect_idxs[np.argmin(fit_vals)])
    return [self.population[idx] for idx in parent_idxs]

  '''
    Implementation of the crossover reproduction method
    The result will be always a tree with deepness less or equal than `max_tree_deepness`
  '''
  def crossover(self, parents):

    # Copy of first parent
    c_p1 = parents[0].copy()
    # Copy of second parent
    c_p2 = parents[1].copy()

    # Caculate indexes of sub trees to be merged
    idx_sub_tree_to_be_replaced = randint(0,c_p1.size - 1)
    sub_tree_level, sub_tree_to_be_replaced = c_p1.get_sub_tree(0,0,idx_sub_tree_to_be_replaced)
    
    # Get all the possible candidates inside c_p2 taking in account the max deepness
    valid_sub_tree_options = c_p2.get_sub_trees_by_level(0,0,(self.max_tree_deepness-sub_tree_level), self.max_tree_deepness)

    # Extracting the candidate tree
    if len(valid_sub_tree_options) > 1:
      replacement_tree = valid_sub_tree_options[randint(0, len(valid_sub_tree_options) - 1)][1]
    else:
      replacement_tree = valid_sub_tree_options[0][1]

    # Replacing the subtree
    if idx_sub_tree_to_be_replaced > 0:
      c_p1.update_sub_tree(idx_sub_tree_to_be_replaced,replacement_tree)
    else:
      c_p1 = replacement_tree.copy()

    # Returns a list with a single new element
    return [ c_p1 ]
  
  '''
    Implementation of the crossover reproduction method
    `c_p1` will be always a tree with deepness less or equal than `max_tree_deepness`.
    `c_p2` can be bigger because c_p1 is the one used as an anchor in this implementation.

    TODO: Evalutate a different approach or use a doble anchor which is not the original behaviour of the variant  
  '''
  def variant_crossover(self, parents):
    # Copy of first parent
    c_p1 = parents[0].copy()
    # Copy of second parent
    c_p2 = parents[1].copy()

    # Caculate indexes of sub trees to be merged
    idx_sub_tree_to_be_replaced = randint(0,c_p1.size - 1)
    sub_tree_level, sub_tree_to_be_replaced = c_p1.get_sub_tree(0,0,idx_sub_tree_to_be_replaced)

    valid_sub_tree_options = []
    replacement_tree = None

    while valid_sub_tree_options == []:
      # Get all the possible candidates inside c_p2 taking in account the max deepness
      valid_sub_tree_options = c_p2.get_sub_trees_by_level(0,0,max(0,self.max_tree_deepness-sub_tree_level), self.max_tree_deepness)
      if not valid_sub_tree_options:
        continue
      # Extracting the candidate tree
      elif len(valid_sub_tree_options) > 1:
        replacement_tree = valid_sub_tree_options[randint(0, len(valid_sub_tree_options) - 1)]
      else:
        replacement_tree = valid_sub_tree_options[0]

    # Replacing the subtree in c_p1
    if idx_sub_tree_to_be_replaced > 0:
      c_p1.update_sub_tree(idx_sub_tree_to_be_replaced,replacement_tree[1])
    else:
      c_p1 = replacement_tree[1].copy()
  
    # Replacing the subtree in c_p2
    if replacement_tree[0] > 0:
      c_p2.update_sub_tree(replacement_tree[0],sub_tree_to_be_replaced)
    else:
      c_p2 = sub_tree_to_be_replaced.copy()

    # Returns a list with two new elements
    return [ c_p1, c_p2 ]

  '''
    Implementation of the mutation method
    General behaviour:
      - Estimate a subtree to be mutated and extract his level.
      - Generate a new individual(subtree) with a deepness that takes 
      into account the level of the subtree which is being mutated and 
      the `max_tree_deepness`
      - Replace the old subtree with the new 'mutated' subtree into the 
      corresponding idx of the individual and return it
  '''
  def mutate(self, individual):
    # Caculate indexes of sub trees to be mutated
    idx_sub_tree_to_be_replaced = randint(0,individual.size - 1)
    sub_tree_level, sub_tree_to_be_replaced = individual.get_sub_tree(0,0,idx_sub_tree_to_be_replaced)

    # Generate a tree that will be the mutated result
    replacement_tree = self.generate_individual(max(self.max_tree_deepness-sub_tree_level,0),self.terminals,self.non_terminals,self.variables,self.variables_prob)

    # Replacing the old subtree with the mutated onew
    if idx_sub_tree_to_be_replaced > 0:
      individual.update_sub_tree(idx_sub_tree_to_be_replaced,replacement_tree)
    else:
      individual = replacement_tree.copy()
    return individual

  '''
    This method is in charge of generating the new population each generation
    General behaviour:
      - Create a new empty population
      - Select individuals to be reproduced
      - Apply reproduction method with the selected individuals
      - The candidate(s) are evaluated for possible mutations
      - The candidates are added to the new population
      - If the new population has the desired size then replace the old population
  '''
  def select_and_reproduction(self):
    new_population = []
    print("\t- Selection,Reproduction & Mutation")
    while (len(new_population) < self.population_size):
      new_individuals = self.reproduction(self.selection())
      for indv in new_individuals:
        if random() < self.mutation_prob:
          new_population.append(self.mutate(indv))
        else:
          new_population.append(indv)

    self.population = new_population

  '''
    This method is in charge of estimating the fitness value for a population
    and storing the data for generating charts. This function calculates
    the individual with the lowest, avg and highest value in each generation.
  '''
  def eval_population(self):
    fitness = []
    for individual in self.population:
      fitness.append(self.fitness(individual))
    
    # Calculate Metrics
    idx_min = np.argmin(fitness)
    c_mean = np.mean(fitness)
    idx_max = np.argmax(fitness)

    # Store metrics
    self.historic_min_metric.append(fitness[idx_min])
    self.historic_mean_metric.append(c_mean)
    self.historic_max_metric.append(fitness[idx_max])

    # Assuming Minimization approach 
    if self.best is None or np.min(self.historic_min_metric) > fitness[idx_min]:
      self.best = self.population[idx_min]

    return [ (idx_min,fitness[idx_min]) , (-1,c_mean), (idx_max,fitness[idx_max]) ]

  '''
    The executable run(<generations>) method follows the next life cycle:
    - Evaluate Fitness of the current population and store data for charts
    - If there is an individual that pass the end criteria return it and stop
    - Generate a new population based on the selection and reproduction methods
    - Each candidate for the new population is considered for possible mutations
    - Add the individual(s) to the new population pool
    - If the number of generation is reached, return the individual found with the
    best(lowest) fitness value (across the generations)
  '''
  def run(self, generations):
    # Initialize metrics
    self.historic_min_metric = []
    self.historic_mean_metric = []
    self.historic_max_metric = []
    self.best = None

    for g in range(0,generations):
      print(f"Generation: {g+1}")

      print("\t-Evaluation")
      # Evaluate fitness of current population
      current_results = self.eval_population()
      
      print(f"\t-Fitness results:\n\t\tlowest: {current_results[0][1]:.3e}\n\t\tAvg: {current_results[1][1]:.3e}\n\t\thighest: {current_results[2][1]:.3e}")
      # Verify an acceptable individual has been found
      if self.end_criteria(current_results[0][1]):
        print("Criteria met finishing")
        return self.population[current_results[0][0]], current_results[0][1]

      # Apply selection and reproduction methods
      self.select_and_reproduction()
    print("Criteria not met returning the best found")
    return self.best, np.min(self.historic_min_metric)
