from node import Node
from prior import Prior
from sys import *
import math
import time


def current_milli_time():
    return int(round(time.time() * 1000))


def main():
    if len(argv) < 3:
        print('usage: python3 sample.py [query node=condition] [number of iterations] [observed node=condition] ...')
        print('humidity=[LOW, HIGH], temperature=[WARM, MILD, COLD], icy=[TRUE, FALSE], snow=[TRUE, FALSE]')
        print('day=[WEEKEND, WEEKDAY], cloudy=[TRUE, FALSE], exams=[TRUE, FALSE], stress=[HIGH, LOW]')
        exit()

    desired_state = str.upper(argv[1].split('=')[1]) + '_' + str.upper(argv[1].split('=')[0])
    num_trials = int(argv[2])
    given_states = []
    for arg in argv[3:]:
        _state = str.upper(arg.split('=')[1]) + '_' + str.upper(arg.split('=')[0])
        given_states.append(_state)
    graph = compose_graph()

    accepted_simulations = []

    start_time = current_milli_time()

    # Simulate the graph num_trials times and reject bad samples
    for i in range(num_trials):

        # Simulate the graph
        simulated_states = propagate_graph(graph)

        # Assume the simulation is acceptable
        acceptable = True

        # Reject the simulation if it doesn't match
        for state in given_states:
            if state not in simulated_states:
                acceptable = False

        if acceptable is True:
            accepted_simulations.append(simulated_states)

    sample_size = len(accepted_simulations)
    # print('Collected ' + str(num_trials) + ' samples')
    # print('Accepted ' + str(sample_size) + ' samples')
    num_true = 0

    # Find the probability of the desired state in the accepted_simulations
    for simulation in accepted_simulations:
        if desired_state in simulation:
            num_true += 1

    if sample_size == 0:
        print('No samples succeeded.')
        exit()

    average = num_true / sample_size
    # print('Estimated probability: ' + str(average))

    # Calculate the confidence interval
    # Based on the Binomial Proportion Confidence Interval
    # https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval

    # Calculate confidence interval
    z = 1.96  # This corresponds to a 95% confidence
    confidence_interval = z * math.sqrt((1 / sample_size) * average * (1 - average))

    total_time_ms = current_milli_time() - start_time
    # print('95% confidence interval: ' + str(average) + ' +- ' + str(confidence_interval))
    print(str(total_time_ms)+' :: '+str(average) + ' +- ' + str(confidence_interval))


def propagate_graph(graph):
    [humidity, temperature, day, icy, snow, cloudy, exams, stress] = graph

    # Independent states
    humidity_state = humidity.determine_state(Prior([None]))
    temperature_state = temperature.determine_state(Prior([None]))
    day_state = day.determine_state(Prior([None]))

    # Dependent states
    icy_state = icy.determine_state(Prior([humidity_state, temperature_state]))
    snow_state = snow.determine_state(Prior([humidity_state, temperature_state]))
    cloudy_state = cloudy.determine_state(Prior([snow_state]))
    exams_state = exams.determine_state(Prior([snow_state, day_state]))
    stress_state = stress.determine_state(Prior([exams_state, snow_state]))

    return [humidity_state, temperature_state, day_state, icy_state, snow_state, cloudy_state, exams_state,
            stress_state]


def compose_graph():
    humidity = Node(
        ['LOW_HUMIDITY', 'MEDIUM_HUMIDITY', 'HIGH_HUMIDITY'],  # States
        [],  # No parents
        {
            Prior([None]): {'LOW_HUMIDITY': 0.2, 'MEDIUM_HUMIDITY': 0.5, 'HIGH_HUMIDITY': 0.3}
        }
    )

    temperature = Node(
        ['WARM_TEMPERATURE', 'MILD_TEMPERATURE', 'COLD_TEMPERATURE'],  # States
        [],  # No parents
        {
            Prior([None]): {'WARM_TEMPERATURE': 0.1, 'MILD_TEMPERATURE': 0.4, 'COLD_TEMPERATURE': 0.5}
        }
    )

    icy = Node(
        ['TRUE_ICY', 'FALSE_ICY'],  # States
        [humidity, temperature],  # Parents
        {
            Prior(['LOW_HUMIDITY', 'WARM_TEMPERATURE']): {'TRUE_ICY': 0.001, 'FALSE_ICY': 0.999},
            Prior(['LOW_HUMIDITY', 'MILD_TEMPERATURE']): {'TRUE_ICY': 0.01, 'FALSE_ICY': 0.99},
            Prior(['LOW_HUMIDITY', 'COLD_TEMPERATURE']): {'TRUE_ICY': 0.05, 'FALSE_ICY': 0.95},
            Prior(['MEDIUM_HUMIDITY', 'WARM_TEMPERATURE']): {'TRUE_ICY': 0.001, 'FALSE_ICY': 0.999},
            Prior(['MEDIUM_HUMIDITY', 'MILD_TEMPERATURE']): {'TRUE_ICY': 0.03, 'FALSE_ICY': 0.97},
            Prior(['MEDIUM_HUMIDITY', 'COLD_TEMPERATURE']): {'TRUE_ICY': 0.2, 'FALSE_ICY': 0.8},
            Prior(['HIGH_HUMIDITY', 'WARM_TEMPERATURE']): {'TRUE_ICY': 0.005, 'FALSE_ICY': 0.995},
            Prior(['HIGH_HUMIDITY', 'MILD_TEMPERATURE']): {'TRUE_ICY': 0.01, 'FALSE_ICY': 0.99},
            Prior(['HIGH_HUMIDITY', 'COLD_TEMPERATURE']): {'TRUE_ICY': 0.35, 'FALSE_ICY': 0.65}
        }
    )

    snow = Node(
        ['TRUE_SNOW', 'FALSE_SNOW'],  # States
        [humidity, temperature],  # Parents
        {
            Prior(['LOW_HUMIDITY', 'WARM_TEMPERATURE']): {'TRUE_SNOW': 0.0001, 'FALSE_SNOW': 0.9999},
            Prior(['LOW_HUMIDITY', 'MILD_TEMPERATURE']): {'TRUE_SNOW': 0.001, 'FALSE_SNOW': 0.999},
            Prior(['LOW_HUMIDITY', 'COLD_TEMPERATURE']): {'TRUE_SNOW': 0.1, 'FALSE_SNOW': 0.9},
            Prior(['MEDIUM_HUMIDITY', 'WARM_TEMPERATURE']): {'TRUE_SNOW': 0.0001, 'FALSE_SNOW': 0.9999},
            Prior(['MEDIUM_HUMIDITY', 'MILD_TEMPERATURE']): {'TRUE_SNOW': 0.0001, 'FALSE_SNOW': 0.9999},
            Prior(['MEDIUM_HUMIDITY', 'COLD_TEMPERATURE']): {'TRUE_SNOW': 0.25, 'FALSE_SNOW': 0.75},
            Prior(['HIGH_HUMIDITY', 'WARM_TEMPERATURE']): {'TRUE_SNOW': 0.0001, 'FALSE_SNOW': 0.9999},
            Prior(['HIGH_HUMIDITY', 'MILD_TEMPERATURE']): {'TRUE_SNOW': 0.001, 'FALSE_SNOW': 0.999},
            Prior(['HIGH_HUMIDITY', 'COLD_TEMPERATURE']): {'TRUE_SNOW': 0.4, 'FALSE_SNOW': 0.6}
        }
    )

    day = Node(
        ['WEEKEND_DAY', 'WEEKDAY_DAY'],  # States
        [],  # No parents
        {
            Prior([None]): {'WEEKEND_DAY': 0.2, 'WEEKDAY_DAY': 0.8}
        }
    )

    cloudy = Node(
        ['TRUE_CLOUDY', 'FALSE_CLOUDY'],
        [snow],
        {
            Prior(['FALSE_SNOW']): {'TRUE_CLOUDY': 0.3, 'FALSE_CLOUDY': 0.7},
            Prior(['TRUE_SNOW']): {'TRUE_CLOUDY': 0.9, 'FALSE_CLOUDY': 0.1}
        }
    )

    exams = Node(
        ['TRUE_EXAMS', 'FALSE_EXAMS'],  # States
        [snow, day],  # Parents
        {
            Prior(['FALSE_SNOW', 'WEEKEND_DAY']): {'TRUE_EXAMS': 0.001, 'FALSE_EXAMS': 0.999},
            Prior(['FALSE_SNOW', 'WEEKDAY_DAY']): {'TRUE_EXAMS': 0.1, 'FALSE_EXAMS': 0.9},
            Prior(['TRUE_SNOW', 'WEEKEND_DAY']): {'TRUE_EXAMS': 0.0001, 'FALSE_EXAMS': 0.9999},
            Prior(['TRUE_SNOW', 'WEEKDAY_DAY']): {'TRUE_EXAMS': 0.3, 'FALSE_EXAMS': 0.7}
        }
    )

    stress = Node(
        ['HIGH_STRESS', 'LOW_STRESS'],  # States
        [snow, exams],  # Parents
        {
            Prior(['FALSE_SNOW', 'FALSE_EXAMS']): {'HIGH_STRESS': 0.01, 'LOW_STRESS': 0.99},
            Prior(['FALSE_SNOW', 'TRUE_EXAMS']): {'HIGH_STRESS': 0.2, 'LOW_STRESS': 0.8},
            Prior(['TRUE_SNOW', 'FALSE_EXAMS']): {'HIGH_STRESS': 0.1, 'LOW_STRESS': 0.9},
            Prior(['TRUE_SNOW', 'TRUE_EXAMS']): {'HIGH_STRESS': 0.5, 'LOW_STRESS': 0.5}
        }
    )

    return [humidity, temperature, day, icy, snow, cloudy, exams, stress]


if __name__ == '__main__':
    main()
