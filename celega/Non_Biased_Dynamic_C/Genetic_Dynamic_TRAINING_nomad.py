import numpy as np
import ray
from Worm_Env.trained_connectome import WormConnectome
from graphing import graph,graph_comparison
from Worm_Env.weight_dict import dict
import PyNomad
from tqdm import tqdm
import csv

values_list = []

muscles = ['MVU', 'MVL', 'MDL', 'MVR', 'MDR']
muscleList = ['MDL07', 'MDL08', 'MDL09', 'MDL10', 'MDL11', 'MDL12', 'MDL13', 'MDL14', 'MDL15', 'MDL16', 'MDL17', 'MDL18', 'MDL19', 'MDL20', 'MDL21', 'MDL22', 'MDL23', 'MVL07', 'MVL08', 'MVL09', 'MVL10', 'MVL11', 'MVL12', 'MVL13', 'MVL14', 'MVL15', 'MVL16', 'MVL17', 'MVL18', 'MVL19', 'MVL20', 'MVL21', 'MVL22', 'MVL23', 'MDR07', 'MDR08', 'MDR09', 'MDR10', 'MDR11', 'MDR12', 'MDR13', 'MDR14', 'MDR15', 'MDR16', 'MDR17', 'MDR18', 'MDR19', 'MDR20', 'MDL21', 'MDR22', 'MDR23', 'MVR07', 'MVR08', 'MVR09', 'MVR10', 'MVR11', 'MVR12', 'MVR13', 'MVR14', 'MVR15', 'MVR16', 'MVR17', 'MVR18', 'MVR19', 'MVR20', 'MVL21', 'MVR22', 'MVR23']

mLeft = ['MDL07', 'MDL08', 'MDL09', 'MDL10', 'MDL11', 'MDL12', 'MDL13', 'MDL14', 'MDL15', 'MDL16', 'MDL17', 'MDL18', 'MDL19', 'MDL20', 'MDL21', 'MDL22', 'MDL23', 'MVL07', 'MVL08', 'MVL09', 'MVL10', 'MVL11', 'MVL12', 'MVL13', 'MVL14', 'MVL15', 'MVL16', 'MVL17', 'MVL18', 'MVL19', 'MVL20', 'MVL21', 'MVL22', 'MVL23']
mRight = ['MDR07', 'MDR08', 'MDR09', 'MDR10', 'MDR11', 'MDR12', 'MDR13', 'MDR14', 'MDR15', 'MDR16', 'MDR17', 'MDR18', 'MDR19', 'MDR20', 'MDL21', 'MDR22', 'MDR23', 'MVR07', 'MVR08', 'MVR09', 'MVR10', 'MVR11', 'MVR12', 'MVR13', 'MVR14', 'MVR15', 'MVR16', 'MVR17', 'MVR18', 'MVR19', 'MVR20', 'MVL21', 'MVR22', 'MVR23']
# Used to accumulate muscle weighted values in body muscles 07-23 = worm locomotion

all_neuron_names = [
    'ADAL', 'ADAR', 'ADEL', 'ADER', 'ADFL', 'ADFR', 'ADLL', 'ADLR', 'AFDL', 'AFDR',
    'AIAL', 'AIAR', 'AIBL', 'AIBR', 'AIML', 'AIMR', 'AINL', 'AINR', 'AIYL', 'AIYR',
    'AIZL', 'AIZR', 'ALA', 'ALML', 'ALMR', 'ALNL', 'ALNR', 'AQR', 'AS1', 'AS10', 'AS11',
    'AS2', 'AS3', 'AS4', 'AS5', 'AS6', 'AS7', 'AS8', 'AS9', 'ASEL', 'ASER', 'ASGL', 'ASGR',
    'ASHL', 'ASHR', 'ASIL', 'ASIR', 'ASJL', 'ASJR', 'ASKL', 'ASKR', 'AUAL', 'AUAR', 'AVAL',
    'AVAR', 'AVBL', 'AVBR', 'AVDL', 'AVDR', 'AVEL', 'AVER', 'AVFL', 'AVFR', 'AVG', 'AVHL',
    'AVHR', 'AVJL', 'AVJR', 'AVKL', 'AVKR', 'AVL', 'AVM', 'AWAL', 'AWAR', 'AWBL', 'AWBR',
    'AWCL', 'AWCR', 'BAGL', 'BAGR', 'BDUL', 'BDUR', 'CEPDL', 'CEPDR', 'CEPVL', 'CEPVR', 'DA1',
    'DA2', 'DA3', 'DA4', 'DA5', 'DA6', 'DA7', 'DA8', 'DA9', 'DB1', 'DB2', 'DB3', 'DB4', 'DB5',
    'DB6', 'DB7', 'DD1', 'DD2', 'DD3', 'DD4', 'DD5', 'DD6', 'DVA', 'DVB', 'DVC', 'FLPL', 'FLPR',
    'HSNL', 'HSNR', 'I1L', 'I1R', 'I2L', 'I2R', 'I3', 'I4', 'I5', 'I6', 'IL1DL', 'IL1DR', 'IL1L',
    'IL1R', 'IL1VL', 'IL1VR', 'IL2L', 'IL2R', 'IL2DL', 'IL2DR', 'IL2VL', 'IL2VR', 'LUAL', 'LUAR',
    'M1', 'M2L', 'M2R', 'M3L', 'M3R', 'M4', 'M5',  'MCL', 'MCR', 'MDL01', 'MDL02', 'MDL03',
    'MDL04', 'MDL05', 'MDL06', 'MDL07', 'MDL08', 'MDL09', 'MDL10', 'MDL11', 'MDL12', 'MDL13', 'MDL14',
    'MDL15', 'MDL16', 'MDL17', 'MDL18', 'MDL19', 'MDL20', 'MDL21', 'MDL22', 'MDL23', 'MDL24', 'MDR01',
    'MDR02', 'MDR03', 'MDR04', 'MDR05', 'MDR06', 'MDR07', 'MDR08', 'MDR09', 'MDR10', 'MDR11', 'MDR12',
    'MDR13', 'MDR14', 'MDR15', 'MDR16', 'MDR17', 'MDR18', 'MDR19', 'MDR20', 'MDR21', 'MDR22', 'MDR23',
    'MDR24', 'MI', 'MVL01', 'MVL02', 'MVL03', 'MVL04', 'MVL05', 'MVL06', 'MVL07', 'MVL08', 'MVL09',
    'MVL10', 'MVL11', 'MVL12', 'MVL13', 'MVL14', 'MVL15', 'MVL16', 'MVL17', 'MVL18', 'MVL19', 'MVL20',
    'MVL21', 'MVL22', 'MVL23', 'MVR01', 'MVR02', 'MVR03', 'MVR04', 'MVR05', 'MVR06', 'MVR07', 'MVR08',
    'MVR09', 'MVR10', 'MVR11', 'MVR12', 'MVR13', 'MVR14', 'MVR15', 'MVR16', 'MVR17', 'MVR18', 'MVR19',
    'MVR20', 'MVR21', 'MVR22', 'MVR23', 'MVR24', 'MVULVA', 'NSML', 'NSMR', 'OLLL', 'OLLR', 'OLQDL',
    'OLQDR', 'OLQVL', 'OLQVR', 'PDA', 'PDB', 'PDEL', 'PDER', 'PHAL', 'PHAR', 'PHBL', 'PHBR', 'PHCL',
    'PHCR', 'PLML', 'PLMR', 'PLNL', 'PLNR', 'PQR', 'PVCL', 'PVCR', 'PVDL', 'PVDR', 'PVM', 'PVNL', 'PVNR',
    'PVPL', 'PVPR', 'PVQL', 'PVQR', 'PVR', 'PVT', 'PVWL', 'PVWR', 'RIAL', 'RIAR', 'RIBL', 'RIBR', 'RICL',
    'RICR', 'RID', 'RIFL', 'RIFR', 'RIGL', 'RIGR', 'RIH', 'RIML', 'RIMR', 'RIPL', 'RIPR', 'RIR', 'RIS',
    'RIVL', 'RIVR', 'RMDDL', 'RMDDR', 'RMDL', 'RMDR', 'RMDVL', 'RMDVR', 'RMED', 'RMEL', 'RMER', 'RMEV',
    'RMFL', 'RMFR', 'RMGL', 'RMGR', 'RMHL', 'RMHR', 'SAADL', 'SAADR', 'SAAVL', 'SAAVR', 'SABD', 'SABVL',
    'SABVR', 'SDQL', 'SDQR', 'SIADL', 'SIADR', 'SIAVL', 'SIAVR', 'SIBDL', 'SIBDR', 'SIBVL', 'SIBVR',
    'SMBDL', 'SMBDR', 'SMBVL', 'SMBVR', 'SMDDL', 'SMDDR', 'SMDVL', 'SMDVR', 'URADL', 'URADR', 'URAVL',
    'URAVR', 'URBL', 'URBR', 'URXL', 'URXR', 'URYDL', 'URYDR', 'URYVL', 'URYVR', 'VA1', 'VA10', 'VA11',
    'VA12', 'VA2', 'VA3', 'VA4', 'VA5', 'VA6', 'VA7', 'VA8', 'VA9', 'VB1', 'VB10', 'VB11', 'VB2', 'VB3',
    'VB4', 'VB5', 'VB6', 'VB7', 'VB8', 'VB9', 'VC1', 'VC2', 'VC3', 'VC4', 'VC5', 'VC6', 'VD1', 'VD10',
    'VD11', 'VD12', 'VD13', 'VD2', 'VD3', 'VD4', 'VD5', 'VD6', 'VD7', 'VD8', 'VD9'
]


class Genetic_Dyn_Algorithm:
    def __init__(self, population_size,pattern= [5],  total_episodes=10, training_interval=25, genome=None,matrix_shape= 3689,):
        self.population_size = population_size
        self.matrix_shape = matrix_shape
        self.total_episodes = total_episodes
        self.training_interval = training_interval
        self.original_genome = genome
        self.food_patterns = pattern
        self.population = self.initialize_population(genome)

    def initialize_population(self, genome=None):
        population = []
        population.append(WormConnectome(weight_matrix=np.array(genome, dtype=float), all_neuron_names=all_neuron_names))
        for _ in range(self.population_size-1):
                population.append(WormConnectome(weight_matrix=np.random.uniform(low=-20, high=20, size=self.matrix_shape).astype(np.float32), all_neuron_names=all_neuron_names))
        return population

    def evaluate_fitness(self, candidate, worm_num, env, prob_type):
        cumulative_rewards = []
        for a in prob_type:
            env.reset(a)
            for _ in range(self.total_episodes):
                observation = env._get_observations()
                for _ in range(self.training_interval):
                    movement = candidate.move(observation[worm_num][0], env.worms[worm_num].sees_food, mLeft, mRight, muscleList, muscles)
                    next_observation, reward, _ = env.step(movement, worm_num, candidate)
                    #env.render(worm_num)
                    observation = next_observation
                    cumulative_rewards.append(reward)
        return np.sum(cumulative_rewards)

    def select_parents(self, fitnesses, num_parents):
        parents = np.argsort(fitnesses)[-num_parents:]
    
        return [self.population[i] for i in parents]
###fix the corssover function so that for each theers a crossvoer
    def crossover(self, parents, fitnesses, num_offspring):
        offspring = []
        parent_fitnesses = np.array([fitnesses[i] for i in np.argsort(fitnesses)[-len(parents):]])
        fitness_probs = parent_fitnesses / np.sum(parent_fitnesses)

        for _ in range(num_offspring):
            parent1 = np.random.choice(parents, p=fitness_probs)
            parent2 = np.random.choice(parents, p=fitness_probs)
            crossover_prob = (fitness_probs[parents.index(parent1)] / (fitness_probs[parents.index(parent1)] + fitness_probs[parents.index(parent2)]))**1.2
            prob_array = (np.random.rand(self.matrix_shape) < crossover_prob).astype(int)
            final_array = np.where(prob_array, parent1.weight_matrix, parent2.weight_matrix)
            offspring.append(WormConnectome(weight_matrix=final_array,all_neuron_names=all_neuron_names))
        return offspring

    def mutate(self, offspring, n=5):
        for child in offspring:
                indices_to_mutate = np.random.choice(self.matrix_shape, size=n, replace=False)
                new_values = np.random.uniform(low=-20, high=20, size=n)
                child.weight_matrix[indices_to_mutate] = new_values
        return offspring

    @staticmethod
    @ray.remote
    def evaluate_fitness_ray_evo(candidate_weights,nur_name, worm_num, env, prob_type, mLeft, mRight, muscleList, muscles,interval,episodes):
        
        sum_rewards = 0
        for a in prob_type:
            candidate = WormConnectome(weight_matrix=candidate_weights,all_neuron_names=nur_name)
            env.reset(a)
            for _ in range(episodes):  # total_episodes
                observation = env._get_observations()
                for _ in range(interval):  # training_interval
                    movement = candidate.move(observation[worm_num][0], env.worms[worm_num].sees_food, mLeft, mRight, muscleList, muscles)
                    next_observation, reward, _ = env.step(movement, worm_num, candidate)
                    #env.render(worm_num)
                    observation = next_observation
                    sum_rewards+=reward
        return sum_rewards

    def run(self, env, generations=50, batch_size=32):
        last_best = self.original_genome
        ray.init(
            ignore_reinit_error=True,
            object_store_memory=15 * 1024 * 1024 * 1024,
            num_cpus=16,
        )
        
        try:
            for generation in tqdm(range(generations), desc="Generations"):
                population_batches = [self.population[i:i+batch_size] for i in range(0, len(self.population), batch_size)]
                fitnesses = []
                nomad_res=[]
                futures = []
                for batch in population_batches:
                    for worm_num, candidate in enumerate(batch):
                        ind = len(np.where(candidate.weight_matrix != self.original_genome)[0])
                        if (ind < 50) and (ind > 0):
                            # Submit task to Ray and collect future
                            futures.append(self.evaluate_fitness_nomad.remote(
                                self.original_genome,
                                candidate.weight_matrix,
                                all_neuron_names,
                                worm_num,
                                env,
                                self.food_patterns,
                                mLeft,
                                mRight,
                                muscleList,
                                muscles,
                                self.training_interval,
                                self.total_episodes
                            ))
                        else:
                            # Submit task to Ray and collect future
                            futures.append(self.evaluate_fitness_ray_evo.remote(
                                candidate.weight_matrix,
                                all_neuron_names,
                                worm_num,
                                env,
                                self.food_patterns,
                                mLeft,
                                mRight,
                                muscleList,
                                muscles,
                                self.training_interval,
                                self.total_episodes
                            ))

                # Retrieve results from all futures
                results = ray.get(futures)

                # Process results
                fitnesses = []
                for result in results:
                    # If `result` is a tuple, extract the relevant part. Modify as needed.
                    if isinstance(result, tuple):
                        fitnesses.append(result[1])
                    else:
                        fitnesses.append(result)

                #print(fitnesses)
                # Evaluate fitness using NOMAD in parallel
             
                
                best_index = np.argmax(fitnesses)  # Use np.argmin for minimization
                best_fitness = fitnesses[best_index]
                best_candidate = self.population[best_index]
                print(f"Generation {generation + 1} best fitness: {best_fitness}")
                
                # Select parents from the entire population
                self.population = self.select_parents(fitnesses, self.population_size // 2)
                
                # Generate offspring through crossover and mutation
                offspring = self.crossover(self.population, fitnesses, self.population_size - len(self.population) - 1)
                offspring = self.mutate(offspring)
                self.population.extend(offspring)
                self.population.append(best_candidate)
                
                if not np.array_equal(last_best, best_candidate.weight_matrix):
                    last_best = best_candidate.weight_matrix
                    print("Update")
                    with open('arrays.csv', 'a', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(best_candidate.weight_matrix.flatten().tolist())
            
            return best_candidate.weight_matrix
        
        finally:
            ray.shutdown()

    @staticmethod
    @ray.remote
    def evaluate_fitness_nomad(ori, candidate_weights, nur_name, worm_num, env, prob_type, mLeft, mRight, muscleList, muscles, interval, episodes):
        # Example of using NOMAD for fitness evaluation
        candidate_weights = np.array(candidate_weights)

        candidate_weights[0] = candidate_weights[0] - 1
        candidate_weights[1] = candidate_weights[1] + 1

        ind= np.where(candidate_weights != ori)[0]  # Get indices where the candidate weights differ from the original
        print(ind)
        assert ind != []
        # Define initial point and bounds only for differing values
        x0 = np.array(candidate_weights[ind])
        lower_bounds = (x0 - 1).tolist()
        upper_bounds = (x0 + 1).tolist()
        x0 = x0.tolist()
        
        params = [
            'DISPLAY_DEGREE 0', 
            'DISPLAY_STATS BBE BLK_SIZE OBJ', 
            'BB_MAX_BLOCK_SIZE 4',
            'MAX_BB_EVAL 100'
        ]
        wrapper = BlackboxWrapper(env, prob_type, mLeft, mRight, muscleList, muscles, interval, episodes,ind,ori)
        result = PyNomad.optimize(wrapper.blackbox_block, x0, lower_bounds, upper_bounds,params)
        # Use NOMAD's minimize function with blackbox_block and pass additional args
        
        # Reconstruct the full candidate weights with optimized values
        #optimized_weights[ind] = result.x
        candidate_weights[ind] = result['x_best']
        return candidate_weights,-result['f_best']

class BlackboxWrapper:
    def __init__(self, env, prob_type, mLeft, mRight, muscleList, muscles, interval, episodes,index,ori):
        self.env = env
        self.prob_type = prob_type
        self.mLeft = mLeft
        self.mRight = mRight
        self.muscleList = muscleList
        self.muscles = muscles
        self.interval = interval
        self.episodes = episodes
        self.ind = index
        self.old_worm = ori

    def blackbox(self, eval_point):
            candidate_edit = []
            candidate_weights = np.copy(self.old_worm)
            for a in range(len(self.ind)):
                candidate_edit.append(eval_point.get_coord(a))
            candidate_weights[self.ind] = candidate_edit
            eval_value = evaluate_fitness_ray(
                candidate_weights, all_neuron_names, 0, self.env, self.prob_type, 
                self.mLeft, self.mRight, self.muscleList, self.muscles, self.interval, self.episodes
            )
            eval_point.setBBO(str(eval_value).encode('utf-8'))
            return True

    def blackbox_block(self, eval_block):
        eval_state = []
        for index in range(eval_block.size()):
            eval_point = eval_block.get_x(index)
            eval_state.append(self.blackbox(eval_point))
        return eval_state


def evaluate_fitness_ray(candidate_weights, nur_name, worm_num, env, prob_type, mLeft, mRight, muscleList, muscles, interval, episodes):
        sum_rewards = 0
        for a in prob_type:
            candidate = WormConnectome(weight_matrix=candidate_weights, all_neuron_names=nur_name)
            env.reset(a)
            for _ in range(episodes):
                observation = env._get_observations()
                for _ in range(interval):
                    movement = candidate.move(observation[worm_num][0], env.worms[worm_num].sees_food, mLeft, mRight, muscleList, muscles)
                    next_observation, reward, _ = env.step(movement, worm_num, candidate)
                    observation = next_observation
                    sum_rewards += reward
        return float(-(sum_rewards))  # Minimize negative rewards

