import random
from past.builtins import range
import numpy as np
from GeneticAlgorithm.Fixed import Fixed
from GeneticAlgorithm.Population import Population
from GeneticAlgorithm.Tournament import Tournament
from GeneticAlgorithm.CycleCrossover import CycleCrossover
from GeneticAlgorithm.Candidate import Candidate
random.seed()

class Sudoku(object):
    """ Solves a given Sudoku puzzle using a genetic algorithm. """

    def __init__(self, Nd, sqrtVal, input, puzzle):
        self.given = None
        self.Nd = Nd
        self.sqrtVal = sqrtVal
        self.input = input
        self.puzzle = puzzle
        return

    def load(self, p):
        #values = np.array(list(p.replace(".","0"))).reshape((Nd, Nd)).astype(int)
        self.given = Fixed(p, self.Nd, self.sqrtVal)
        return

    def solve(self):
        Nc = 100  # Number of candidates (i.e. population size).
        Ne = int(0.05 * Nc)  # Number of elites.
        Ng = 10000  # Number of generations.
        Nm = 0  # Number of mutations.

        # Mutation parameters.
        phi = 0
        sigma = 1
        mutation_rate = 0.06

        # Check given one first
        if self.given.no_duplicates(self.Nd) == False:
            return (-1, 1)

        # Create an initial population.
        self.population = Population(self.Nd, self.sqrtVal, self.input, self.puzzle)
        print("Below are the population created for each generation.")
        print("Note that some of them will be not correct Answer!!")
        if self.population.seed(Nc, self.given) ==  1:
            pass
        else:
            return (-1, 1)

        # For up to 10000 generations...
        stale = 0
        for generation in range(0, Ng):
            # Check for a solution.
            best_fitness = 0.0
            #best_fitness_population_values = self.population.candidates[0].values
            for c in range(0, Nc):
                fitness = self.population.candidates[c].fitness
                if (fitness == 1):
                    print("=========================================")
                    print("Solution found at generation %d!" % generation)
                    print("=========================================")
                    return (generation, self.population.candidates[c])

                # Find the best fitness and corresponding chromosome
                if (fitness > best_fitness):
                    best_fitness = fitness
                    #best_fitness_population_values = self.population.candidates[c].values
            print("Generation:", generation, " Best fitness:", best_fitness)
            #print(best_fitness_population_values)

            # Create the next population.
            next_population = []

            # Select elites (the fittest candidates) and preserve them for the next generation.
            self.population.sort()
            elites = []
            for e in range(0, Ne):
                elite = Candidate(self.Nd, self.sqrtVal)
                elite.values = np.copy(self.population.candidates[e].values)
                elites.append(elite)

            # Create the rest of the candidates.
            for count in range(Ne, Nc, 2):
                # Select parents from population via a tournament.
                t = Tournament()
                parent1 = t.compete(self.population.candidates)
                parent2 = t.compete(self.population.candidates)

                ## Cross-over.
                cc = CycleCrossover(self.Nd, self.sqrtVal)
                child1, child2 = cc.crossover(parent1, parent2, crossover_rate=1.0)

                # Mutate child1.
                child1.update_fitness()
                old_fitness = child1.fitness
                success = child1.mutate(mutation_rate, self.given)
                child1.update_fitness()
                if (success):
                    Nm += 1
                    if (child1.fitness > old_fitness):  # Used to calculate the relative success rate of mutations.
                        phi = phi + 1

                # Mutate child2.
                child2.update_fitness()
                old_fitness = child2.fitness
                success = child2.mutate(mutation_rate, self.given)
                child2.update_fitness()
                if (success):
                    Nm += 1
                    if (child2.fitness > old_fitness):  # Used to calculate the relative success rate of mutations.
                        phi = phi + 1

                # Add children to new population.
                next_population.append(child1)
                next_population.append(child2)

            # Append elites onto the end of the population. These will not have been affected by crossover or mutation.
            for e in range(0, Ne):
                next_population.append(elites[e])

            # Select next generation.
            self.population.candidates = next_population
            self.population.update_fitness()

            # Calculate new adaptive mutation rate (based on Rechenberg's 1/5 success rule).
            # This is to stop too much mutation as the fitness progresses towards unity.
            if (Nm == 0):
                phi = 0  # Avoid divide by zero.
            else:
                phi = phi / Nm

            if (phi > 0.2):
                sigma = sigma / 0.998
            elif (phi < 0.2):
                sigma = sigma * 0.998

            mutation_rate = abs(np.random.normal(loc=0.0, scale=sigma, size=None))

            # Check for stale population.
            self.population.sort()
            if (self.population.candidates[0].fitness != self.population.candidates[1].fitness):
                stale = 0
            else:
                stale += 1

            # Re-seed the population if 100 generations have passed
            # with the fittest two candidates always having the same fitness.
            if (stale >= 100):
                print("The population has gone stale. Re-seeding...")
                self.population.seed(Nc, self.given)
                stale = 0
                sigma = 1
                phi = 0
                mutation_rate = 0.06

        print("No solution found.")
        return (-2, 1)