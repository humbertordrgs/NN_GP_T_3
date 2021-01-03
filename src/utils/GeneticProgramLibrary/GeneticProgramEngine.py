import numpy as np
from random import randint, random

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
    - Change to mutate an individual
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

  def generate_initial_population(self):
    res = []
    for i in range(self.population_size):
      res.append(self.generate_individual(0,self.max_tree_deepness,self.terminals,self.non_terminals,self.variables,self.variables_prob))
    return res
  
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

  def roulette_selection(self):
    parent_idxs = []
    for i in range(0, 2):
        parent_idxs.append(self.gen_rand_with_memory(parent_idxs))
    return [self.population[idx] for idx in parent_idxs] 

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

  def crossover(self, parents):

    # Copy of first parent
    c_p1 = parents[0].copy()
    # Copy of seconmd parent
    c_p2 = parents[1].copy()

    # Caculate indexes of sub trees to be merged
    idx_sub_tree_to_be_replaced = randint(0,c_p1.size - 1)
    sub_tree_level, sub_tree_to_be_replaced = c_p1.get_sub_tree(0,0,idx_sub_tree_to_be_replaced)
    
    # Get all the possible candidates inside c_p2 taking in account the max deepness
    valid_sub_tree_options = c_p2.get_sub_trees_by_level(0,0,(self.max_tree_deepness-sub_tree_level), self.max_tree_deepness)

    if len(valid_sub_tree_options) > 1:
      replacement_tree = valid_sub_tree_options[randint(0, len(valid_sub_tree_options) - 1)][1]
    else:
      replacement_tree = valid_sub_tree_options[0][1]

    if idx_sub_tree_to_be_replaced > 0:
      c_p1.update_sub_tree(0,idx_sub_tree_to_be_replaced,replacement_tree)
    else:
      c_p1 = replacement_tree.copy()

    # Returns a list with a single new element
    return [ c_p1 ]
  
  def variant_crossover(self, parents):
    # Copy of first parent
    c_p1 = parents[0].copy()
    # Copy of seconmd parent
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
      elif len(valid_sub_tree_options) > 1:
        replacement_tree = valid_sub_tree_options[randint(0, len(valid_sub_tree_options) - 1)]
      else:
        replacement_tree = valid_sub_tree_options[0]

    if idx_sub_tree_to_be_replaced > 0:
      c_p1.update_sub_tree(0,idx_sub_tree_to_be_replaced,replacement_tree[1])
    else:
      c_p1 = replacement_tree[1].copy()
  
    if replacement_tree[0] > 0:
      c_p2.update_sub_tree(0,replacement_tree[0],sub_tree_to_be_replaced)
    else:
      c_p2 = sub_tree_to_be_replaced.copy()

    # Returns a list with two new elements
    return [ c_p1, c_p2 ]

  def mutate(self, individual):
    # Caculate indexes of sub trees to be merged
    idx_sub_tree_to_be_replaced = randint(0,individual.size - 1)
    sub_tree_level, sub_tree_to_be_replaced = individual.get_sub_tree(0,0,idx_sub_tree_to_be_replaced)
    replacement_tree = self.generate_individual(0,max(self.max_tree_deepness-sub_tree_level,0),self.terminals,self.non_terminals,self.variables,self.variables_prob)

    if idx_sub_tree_to_be_replaced > 0:
      individual.update_sub_tree(0,idx_sub_tree_to_be_replaced,replacement_tree)
    else:
      individual = replacement_tree.copy()
    return individual

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

  def run(self, generations):
    # Initialize metrics
    self.historic_min_metric = []
    self.historic_mean_metric = []
    self.historic_max_metric = []
    self.best = None

    for g in range(0,generations):
      print(f"Generation: {g+1}")

      print("Evaluation")
      # Evaluate fitness of current population
      current_results = self.eval_population()
      
      print(current_results)
      # Verify an acceptable individual has been found
      if self.end_criteria(current_results[0][1]):
        print("Criteria met")
        return self.population[current_results[0][0]], current_results[0][1]

      # Apply selection and reproduction methods
      self.select_and_reproduction()
    print("Criteria not met returning the best found")
    return self.best, np.max(self.historic_max_metric)
  '''
    Parameters:
    - Population size
    - Terminal Values (Leaf Nodes)
    - Allowed Operations (Operator Nodes)
    - Function of fitness to be used
    - Specify the selection method to be used
    - Specify the reproduction method to be used
    - Method to recognize when end criteria is met
    - Max deepness of trees handled in the engine
    - Change to mutate an individual
  '''
  def __init__(
    self,
    population_size,
    terminals,
    operations,
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
    self.operations = operations
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

  def generate_initial_population(self):
    res = []
    for i in range(self.population_size):
      res.append(generate_tree(0,self.max_tree_deepness,self.terminals,self.operations,self.variables,self.variables_prob))
    return res
  
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

  def roulette_selection(self):
    parent_idxs = []
    for i in range(0, 2):
        parent_idxs.append(self.gen_rand_with_memory(parent_idxs))
    return [self.population[idx] for idx in parent_idxs] 

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

    if len(valid_sub_tree_options) > 1:
      replacement_tree = valid_sub_tree_options[randint(0, len(valid_sub_tree_options) - 1)][1]
    else:
      replacement_tree = valid_sub_tree_options[0][1]

    if idx_sub_tree_to_be_replaced > 0:
      c_p1.update_sub_tree(0,idx_sub_tree_to_be_replaced,replacement_tree)
    else:
      c_p1 = replacement_tree.copy()

    # Returns a list with a single new element
    return [ c_p1 ]
  
  def variant_crossover(self, parents):
    # Copy of first parent
    c_p1 = parents[0].copy()
    # Copy of seconmd parent
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
      elif len(valid_sub_tree_options) > 1:
        replacement_tree = valid_sub_tree_options[randint(0, len(valid_sub_tree_options) - 1)]
      else:
        replacement_tree = valid_sub_tree_options[0]

    if idx_sub_tree_to_be_replaced > 0:
      c_p1.update_sub_tree(0,idx_sub_tree_to_be_replaced,replacement_tree[1])
    else:
      c_p1 = replacement_tree[1].copy()
  
    if replacement_tree[0] > 0:
      c_p2.update_sub_tree(0,replacement_tree[0],sub_tree_to_be_replaced)
    else:
      c_p2 = sub_tree_to_be_replaced.copy()

    # Returns a list with two new elements
    return [ c_p1, c_p2 ]

  def mutate(self, individual):
    # Caculate indexes of sub trees to be merged
    idx_sub_tree_to_be_replaced = randint(0,individual.size - 1)
    sub_tree_level, sub_tree_to_be_replaced = individual.get_sub_tree(0,0,idx_sub_tree_to_be_replaced)
    replacement_tree = generate_tree(0,max(self.max_tree_deepness-sub_tree_level,0),self.terminals,self.operations,self.variables,self.variables_prob)

    if idx_sub_tree_to_be_replaced > 0:
      individual.update_sub_tree(0,idx_sub_tree_to_be_replaced,replacement_tree)
    else:
      individual = replacement_tree.copy()
    return individual

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

  def run(self, generations):
    # Initialize metrics
    self.historic_min_metric = []
    self.historic_mean_metric = []
    self.historic_max_metric = []
    self.best = None

    for g in range(0,generations):
      print(f"Generation: {g+1}")

      print("Evaluation")
      # Evaluate fitness of current population
      current_results = self.eval_population()
      
      print(current_results)
      # Verify an acceptable individual has been found
      if self.end_criteria(current_results[0][1]):
        print("Criteria met")
        return self.population[current_results[0][0]], current_results[0][1]

      # Apply selection and reproduction methods
      self.select_and_reproduction()
    print("Criteria not met returning the best found")
    return self.best, np.max(self.historic_max_metric)