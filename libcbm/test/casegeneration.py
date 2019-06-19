import math
import numpy as np
import libcbm.configuration.cbm_defaults as cbm_defaults
def get_classifier_name(id):
    return str(id)


def get_random_sigmoid_func():
    x_0 = np.random.rand(1)[0] * 100
    L = np.random.rand(1)[0] * 400
    k=0.1 
    def sigmoid(x):
        return L/(1+math.exp(-k*(x-x_0)))
    return sigmoid

#return a step of value y for the range minx to maxX
def get_step_func():
    y = np.random.rand(1)[0] * 500
    minX = np.random.randint(low=1, high=200)
    def step(x):
        if x == 0:
            return 0
        if x>=minX:
            return y
        else:
            return 0
    return step


def get_ramp_func():
    rate = np.random.rand(1)[0] * 5
    def ramp(x):
        return x*rate
    return ramp


def get_expCurve_func():
    yMax = np.random.rand(1)[0] * 500
    def expCurve(x):
        return yMax - math.exp(-x) * yMax
    return expCurve


def create_scenario(id, age, area, delay, unfccc_land_class, admin_boundary,
                    eco_boundary, historic_disturbance, last_pass_disturbance,
                    components, events):
    return {
        "id":id,
        "age": age,
        "area": area,
        "delay": delay,
        "unfccc_land_class": unfccc_land_class,
        "admin_boundary": admin_boundary,
        "eco_boundary": eco_boundary,
        "historic_disturbance": historic_disturbance,
        "last_pass_disturbance": last_pass_disturbance,
        "components": components,
        "events": events
    }


def choose_random_yield_func(func_factories=[
            get_random_sigmoid_func,
            get_step_func,
            get_ramp_func,
            get_expCurve_func]):
    return np.random.choice(func_factories,1)[0]()


def generate_scenarios(random_seed, num_cases, dbpath, n_steps,
    max_disturbances, max_components, growth_generator, n_growth_digits,
    age_interval, max_age):

    np.random.seed(random_seed)

    species_ref = cbm_defaults.load_species_reference(dbpath, "en-CA")
    species = [
        k for k,v in species_ref.items() 
        if len(k)<50 and v["forest_type_id"] in [1,3]
        ] #exclude species names that are too long for the CBM-CFS3 project database schema
    
    spatial_units = cbm_defaults.get_spatial_unit_ids_by_admin_eco_name(dbpath, "en-CA")
    random_spus = np.random.choice([",".join(x) for x in spatial_units.keys()], num_cases)

    disturbance_types = cbm_defaults.get_disturbance_type_ids_by_name(dbpath, "en-CA")

    cases = []
    for i in range(num_cases):
        num_components = np.random.randint(1,max_components) if max_components > 1 else 1
        random_species = np.random.choice(list(species), num_components)
        spu = random_spus[i].split(',')
        components = []
        for c in range(num_components):
            growth_func = choose_random_yield_func()
            components.append({
                "species": random_species[c],
                "age_volume_pairs": [(x, round(growth_func(x),n_growth_digits))
                                     for x in range(0,max_age,age_interval)]
            })

        disturbance_events = []
        if max_disturbances>0:
            num_disturbances = np.random.randint(0,max_disturbances)
            random_dist_types = np.random.choice(list(disturbance_types), num_disturbances)

            min_timestep = 0
            for d in range(num_disturbances):

                disturbance_events.append({
                "disturbance_type": random_dist_types[d],
                "time_step": np.random.randint(min_timestep, n_steps)
                })

        cases.append(create_scenario(
            id = i+1,
            age = 0,
            area = 1.0,
            delay = 0,
            unfccc_land_class = 0,
            admin_boundary = spu[0],
            eco_boundary = spu[1],
            historic_disturbance="Wildfire",
            last_pass_disturbance="Wildfire",
            components = components,
            events = disturbance_events))
    return cases