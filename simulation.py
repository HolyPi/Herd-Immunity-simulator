import random, sys
random.seed(42)
from person import Person
from logger import Logger
from virus import Virus



class Simulation(object):
    """Main class that will run the herd immunity simulation program.
    Expects initialization parameters passed as command line arguments when
    file is run.
    Simulates the spread of a virus through a given population.  The percentage
    of the
    population that are vaccinated, the size of the population, and the amount
    of initially
    infected people in a population are all variables that can be set when the
    program is run.
    """



    def __init__(self, pop_size, vacc_percentage, initial_infected, virus):
        """
        Logger object logger records all events during the simulation.
        Population represents all Persons in the population.
        The next_person_id is the next available id for all created Persons,
        and should have a unique _id value.
        The vaccination percentage represents the total percentage of
        population vaccinated at the start of the simulation.
        You will need to keep track of the number of people currently infected
        with the disease.
        The total infected people is the running total that have been infected
        since the
        simulation began, including the currently infected people who died.
        You will also need to keep track of the number of people that have die
        as a result
        of the infection.
        All arguments will be passed as command-line arguments when the file is
        run.
        HINT: Look in the if __name__ == "__main__" function at the bottom.
        """
        # TODO: Create a Logger object and bind it to self.logger.
        # Remember to call the appropriate logger method in the corresponding
        # parts of the simulation.
        # TODO: Call self._create_population() and pass in the correct
        # parameters.
        # Store the array that this method will return in the self.population
        # attribute.
        # TODO: Store each newly infected person's ID in newly_infected
        # attribute.
        # At the end of each time step, call self._infect_newly_infected()
        # and then reset .newly_infected back to an empty list.
        self.population = []
        self.pop_size = pop_size  # Int
        self.next_person_id = 0  # Int
        self.virus = virus  # Virus object
        self.initial_infected = initial_infected  # Int
        self.total_infected = 0  # Int
        self.current_infected = 0  # Int
        self.vacc_percentage = vacc_percentage  # float between 0 and 1
        self.total_dead = 0  # Int
        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(
            virus_name, pop_size, vacc_percentage, initial_infected)
        self.logger = Logger(self.file_name)  # List of Person objects
        # self.population = self.create_population(initial_infected, vacc_percentage, pop_size)
        self.newly_infected = []
        self.logger.write_metadata(self.pop_size, self.vacc_percentage, self.virus.name, self.virus.mortality_rate, self.virus.repro_rate)

    def create_population(self, initial_infected, pop_size, vacc_percentage):
        """
        This method will create the initial population.
            Args:
                initial_infected (int): The number of infected people that the
                simulation
                will begin with.
            Returns:
                list: A list of Person objects.
        """
        # TODO: Finish this method!  This method should be called when the
        # simulation
        # begins, to create the population that will be used. This method
        # should return
        # an array filled with Person objects that matches the specifications
        # of the
        # simulation (correct number of people in the population, correct
        # percentage of
        # people vaccinated, correct number of initially infected people).

        # Use the attributes created in the init method to create a population
        # that has
        # the correct intial vaccination percentage and initial infected.
        for i in range(self.pop_size):
            vaccinated = False
            vacc_chance = (random.random())
            if vacc_percentage > 0 and vacc_chance <= vacc_percentage:
                vaccinated = True
            person = Person(i, vaccinated)
            self.population.append(person)

        #tests that population is made
        print(self.pop_size)
        print(len(self.population))
        population_infected = 0

        while initial_infected > 0 and population_infected < initial_infected:
            random_infected = random.randint(0,pop_size-1)

            if (self.population[random_infected].is_vaccinated == False and self.population[random_infected].infection is None):
                self.population[random_infected].infection = self.virus
                population_infected += 1
        return self.population



        # people_infected = []
        #
        # for person in population:
        #     while person.infection and person.is_alive:
        #         people_infected.append(person)
        #
        #     return people_infected



    def _simulation_should_continue(self):
        """
        The simulation should only end if the entire population is dead
        or everyone is vaccinated.
            Returns:
                bool: True for simulation should continue, False if it should
                end.
        """
        for person in self.population:
            if person.is_alive == True and person.infection == self.virus:
                return True

        return False

            # return False






    def run(self):
        """
        This method should run the simulation until all requirements for ending
        the simulation are met.
        """
        # TODO: Finish this method.  To simplify the logic here, use the helper
        # method
        # _simulation_should_continue() to tell us whether or not we should
        # continue
        # the simulation and run at least 1 more time_step.

        # TODO: Keep track of the number of time steps that have passed.
        # HINT: You may want to call the logger's log_time_step() method at the
        # end of each time step.
        # TODO: Set this variable using a helper
        time_step_counter = 0
        self.create_population(self.initial_infected, self.pop_size, self.vacc_percentage)

        #self.population = self.create_population(self.initial_infected, self.pop_size, self.vacc_percentage)
        # print (f'checking if people exist {self.population[0]}')
        # print (f'checking if they have a virus {self.population[0].infection}')
        while self._simulation_should_continue() == True:
            self.time_step()
            time_step_counter += 1
            self.logger.log_time_step(time_step_counter)
        print(f'Simulation ended after {time_step_counter} turns')

    # TODO: for every iteration of this loop, call self.time_step() to
    # compute another
    # round of this simulation.

        # while should_continue:
        #     print('The simulation has ended after',
        #           '{time_step_counter} turns.'.format(time_step_counter))
        #
        # survived = 0
        # died = 0
        # infected = 0
        # #
        # for person in self.population:
        #     if person.is_alive:
        #         survived += 1
        # else:
        #     if person.is_alive == False:
        #         died += 1
        #     if person.infection != None:
        #         infected = 0
        # #
        # print(f'Survived: {survived} died: {died} Infected: {infected}')


    def time_step(self):
        """
        This method should contain all the logic for computing one time step
        in the simulation.
        This includes:
            1. 100 total interactions with a randon person for each infected
            person in the population
            2. If the person is dead, grab another random person from the
            population.
                Since we don't interact with dead people, this does not count
                as an interaction.
            3. Otherwise call simulation.interaction(person, random_person) and
                increment interaction counter by 1.
        """
        inf_list = []
        for infected in self.population:
            if infected.infection != None and infected.is_alive == True:
                inf_list.append(infected)

        for infected in inf_list:
            for interaction in range(100):
                rand_person_index = random.randint(0, self.pop_size-1)
                rand_person = self.population[rand_person_index]
                if rand_person.is_alive == False:
                    interaction -= 1
                else:
                    self.interaction(infected, rand_person)

        for infected in inf_list:
            did_die = not infected.did_survive_infection()
            self.logger.log_infection_survival(infected, did_die)

        self._infect_newly_infected()

        # TODO: Finish this method.


    def interaction(self, person, random_person):
        """
        This method should be called any time two living people are selected
        for an
        interaction. It assumes that only living people are passed in as
        parameters.
        Args:
            person1 (person): The initial infected person
            random_person (person): The person that person1 interacts with.
        """
        # Assert statements are included to make sure that only living people
        # are passed
        # in as params
        assert person.is_alive is True
        assert random_person.is_alive is True

        # TODO: Finish this method.
        #  The possible cases you'll need to cover are listed below:
        # random_person is vaccinated:
        #     nothing happens to random person.
        # random_person is already infected:
        #     nothing happens to random person.
        # random_person is healthy, but unvaccinated:
        #     generate a random number between 0 and 1.  If that number is
        # smaller
        #     than repro_rate, random_person's ID should be appended to
        #     Simulation object's newly_infected array, so that their .infected
        #     attribute can be changed to True at the end of the time step.
        # TODO: Call logger method during this method.
        rand_num = random.randint(0,100) / 100

        if random_person.is_vaccinated == True:
            self.logger.log_interaction(person, random_person, False, True, False)
        elif random_person.infection is not None:
            self.logger.log_interaction(person, random_person, True, False, False)
        else:
            if rand_num < person.infection.repro_rate:
                self.newly_infected.append(random_person)
                self.logger.log_interaction(person, random_person, True, False, True)









    def _infect_newly_infected(self):
        """
        This method should iterate through the list of ._id stored in
        self.newly_infected
        and update each Person object with the disease.
        """

        # TODO: Call this method at the end of every time step and infect each
        # Person.
        # TODO: Once you have iterated through the entire list of
        # self.newly_infected, remember
        # to reset self.newly_infected back to an empty list.

        for infected in self.newly_infected:
            infected.infection
        self.newly_infected = []


if __name__ == "__main__":
    params = sys.argv[1:]
    virus_name = str(params[0])
    repro_num = float(params[1])
    mortality_rate = float(params[2])

    pop_size = int(params[3])
    vacc_percentage = float(params[4])

    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1

    virus = Virus(virus_name, repro_num, mortality_rate)
    sim = Simulation(pop_size, vacc_percentage, initial_infected, virus)

    sim.run()
