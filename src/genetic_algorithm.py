# src/genetic_algorithm.py

from typing import List
from src.genome import Genome
import random
from src.agent_parts.creature import Creature


class GeneticAlgorithm:
    def __init__(
        self,
        population_size: int,
        initial_creature: Creature,
        creature_data: dict,
        speciation_threshold: float = 3.0
    ):
        """
        Initialize the Genetic Algorithm with a given population size and initial creature.

        Args:
            population_size (int): Number of genomes in the population.
            initial_creature (Creature): The initial creature to determine inputs and outputs.
            speciation_threshold (float): Threshold for speciation.
        """
        self.population_size = population_size
        self.initial_creature = initial_creature
        self.speciation_threshold = speciation_threshold
        self.speciation = {}  # species_id -> List[Genome]
        self.species_representatives = {}  # species_id -> Genome
        self.population: List[Genome] = []
        self.innovation = None
        self.genome_id_counter = 0
        self.creature_data = creature_data
        
        

        # Determine number of inputs and outputs based on initial creature
        self.num_inputs, self.num_outputs = self.determine_io()

        # Initialize the population
        self.population = self.initialize_population()

        # Assign genomes to species
        self.assign_species_to_population()

    def determine_io(self) -> (int, int):
        """
        Determine the number of inputs and outputs based on the initial creature.

        Returns:
            Tuple[int, int]: Number of inputs and outputs.
        """
        # Example based on your initial code
        # Inputs:
        # - Vision data: 4
        # - Joint rates: number of joints
        # - Limb positions: number of limbs * 2
        amount_of_joints = self.initial_creature.get_amount_of_joints()
        amount_of_limb = self.initial_creature.get_amount_of_limb()
        num_inputs = 4 + amount_of_joints + (amount_of_limb * 2)
        num_outputs = amount_of_joints  # Assuming each joint has one output

        return num_inputs, num_outputs

    def initialize_population(self) -> List[Genome]:
        """Initialize a population of genomes."""
        population = []
        for _ in range(self.population_size):
            genome = Genome(
                genome_id=self.genome_id_counter,
                num_inputs=self.num_inputs,
                num_outputs=self.num_outputs,
            )
            population.append(genome)
            self.genome_id_counter += 1
        return population

    def assign_species_to_population(self):
        """Assign genomes in the population to species."""
        self.speciation.clear()
        self.species_representatives.clear()
        for genome in self.population:
            self.assign_to_species(genome)

    def assign_to_species(self, genome: Genome):
        """Assign a genome to an existing species or create a new species if none match."""
        species_id = self.determine_species(genome)

        # If the species ID is new, initialize its entry
        if species_id not in self.speciation:
            self.speciation[species_id] = []

        # Add the genome to the determined species
        self.speciation[species_id].append(genome)
        genome.species = species_id

    def determine_species(self, genome: Genome) -> int:
        """Determine the species ID for a given genome."""
        for species_id, representative in self.species_representatives.items():
            distance = genome.compute_compatibility_distance(representative)
            if distance < self.speciation_threshold:
                return species_id

        # If no existing species matches, create a new species
        new_species_id = len(self.species_representatives) + 1
        self.species_representatives[new_species_id] = genome
        return new_species_id

    def reassign_species(self):
        """Reassign genomes to species after a generation."""
        self.speciation.clear()
        self.species_representatives.clear()
        for genome in self.population:
            self.assign_to_species(genome)

    def evaluate_population(self, evaluate_function) -> float:
        """
        Evaluate the entire population's fitness.

        Parameters:
            evaluate_function (callable): Function to evaluate fitness of a genome.

        Returns:
            float: The average fitness of the population.
        """
        total_fitness = 0.0
        for genome in self.population:
            genome.fitness = evaluate_function(genome, self.creature_data)
            total_fitness += genome.fitness
        average_fitness = total_fitness / len(self.population) if self.population else 0
        return average_fitness

    def adjust_fitness(self):
        """Adjust the fitness of each genome based on species size."""
        for species_id, members in self.speciation.items():
            species_size = len(members)
            for genome in members:
                genome.adjusted_fitness = genome.fitness / species_size

    def tournament_selection(
        self, members: List[Genome], tournament_size: int = 3
    ) -> Genome:
        """Select a parent genome using tournament selection."""
        tournament = random.sample(members, min(tournament_size, len(members)))
        tournament.sort(key=lambda g: g.fitness, reverse=True)
        return tournament[0]

    def reproduce(self):
        """Create a new generation through reproduction."""
        new_population = []
        total_adjusted_fitness = sum(
            genome.adjusted_fitness for genome in self.population
        )

        if total_adjusted_fitness == 0:
            total_adjusted_fitness = 1  # Prevent division by zero

        # Calculate offspring counts for each species
        offspring_counts = {}
        for species_id, members in self.speciation.items():
            species_adjusted_fitness = sum(
                genome.adjusted_fitness for genome in members
            )
            offspring_count = int(
                (species_adjusted_fitness / total_adjusted_fitness)
                * self.population_size
            )
            offspring_counts[species_id] = offspring_count

        # Generate offspring for each species
        for species_id, members in self.speciation.items():
            offspring_count = offspring_counts.get(species_id, 0)
            if offspring_count == 0:
                continue

            # Sort members by fitness in descending order
            members.sort(key=lambda g: g.fitness, reverse=True)

            # Elitism: Keep the best genome
            best_genome = members[0].copy()
            best_genome.id = self.genome_id_counter
            self.genome_id_counter += 1
            new_population.append(best_genome)

            for _ in range(offspring_count - 1):
                parent1 = self.tournament_selection(members)
                if random.random() < 0.25:
                    # Mutation without crossover
                    child = parent1.copy()
                    child.mutate()
                else:
                    parent2 = self.tournament_selection(members)
                    # Ensure the more fit parent is parent1
                    if parent2.fitness > parent1.fitness:
                        parent1, parent2 = parent2, parent1

                    # Perform crossover
                    child = parent1.crossover(parent2)
                    child.mutate()

                # Assign a new genome ID
                child.id = self.genome_id_counter
                self.genome_id_counter += 1
                new_population.append(child)

        # If the new population is smaller due to rounding, fill it up
        while len(new_population) < self.population_size:
            parent = random.choice(self.population)
            child = parent.copy()
            child.mutate()
            child.id = self.genome_id_counter
            self.genome_id_counter += 1
            new_population.append(child)

        # Update the population
        self.population = new_population

    def evolve(self, generations: int, evaluate_function):
        """Run the evolution process for a specified number of generations."""
        for generation in range(generations):
            print(f"Generation {generation + 1}")
            average_fitness = self.evaluate_population(evaluate_function)
            print(f"Average Fitness: {average_fitness}")
            self.adjust_fitness()
            self.reassign_species()
            self.reproduce()
