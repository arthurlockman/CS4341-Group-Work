from node import Node
from prior import Prior


def main():
    graph = compose_graph()
    print(propogate_graph(graph))


def propogate_graph(graph):
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

    return [humidity_state, temperature_state, day_state, icy_state, snow_state, cloudy_state, exams_state, stress_state]


def compose_graph():
    humidity = Node(
        ['LOW', 'MEDIUM', 'HIGH'],  # States
        [],  # No parents
        {
            Prior([None]): {'LOW': 0.2, 'MEDIUM': 0.5, 'HIGH': 0.3}
        }
    )

    temperature = Node(
        ['WARM', 'MILD', 'COLD'],  # States
        [],  # No parents
        {
            Prior([None]): {'WARM': 0.1, 'MILD': 0.4, 'COLD': 0.5}
        }
    )

    icy = Node(
        ['ICY', 'NOT_ICY'],  # States
        [humidity, temperature],  # Parents
        {
            Prior(['LOW', 'WARM']): {'ICY': 0.001, 'NOT_ICY': 0.999},
            Prior(['LOW', 'MILD']): {'ICY': 0.01, 'NOT_ICY': 0.99},
            Prior(['LOW', 'COLD']): {'ICY': 0.05, 'NOT_ICY': 0.95},
            Prior(['MEDIUM', 'WARM']): {'ICY': 0.001, 'NOT_ICY': 0.999},
            Prior(['MEDIUM', 'MILD']): {'ICY': 0.03, 'NOT_ICY': 0.97},
            Prior(['MEDIUM', 'COLD']): {'ICY': 0.2, 'NOT_ICY': 0.8},
            Prior(['HIGH', 'WARM']): {'ICY': 0.005, 'NOT_ICY': 0.995},
            Prior(['HIGH', 'MILD']): {'ICY': 0.01, 'NOT_ICY': 0.99},
            Prior(['HIGH', 'COLD']): {'ICY': 0.35, 'NOT_ICY': 0.65}
        }
    )

    snow = Node(
        ['SNOW', 'NOT_SNOW'],  # States
        [humidity, temperature],  # Parents
        {
            Prior(['LOW', 'WARM']): {'SNOW': 0.00001, 'NOT_SNOW': 0.99999},
            Prior(['LOW', 'MILD']): {'SNOW': 0.001, 'NOT_SNOW': 0.999},
            Prior(['LOW', 'COLD']): {'SNOW': 0.1, 'NOT_SNOW': 0.9},
            Prior(['MEDIUM', 'WARM']): {'SNOW': 0.00001, 'NOT_SNOW': 0.99999},
            Prior(['MEDIUM', 'MILD']): {'SNOW': 0.0001, 'NOT_SNOW': 0.9999},
            Prior(['MEDIUM', 'COLD']): {'SNOW': 0.25, 'NOT_SNOW': 0.75},
            Prior(['HIGH', 'WARM']): {'SNOW': 0.0001, 'NOT_SNOW': 0.9999},
            Prior(['HIGH', 'MILD']): {'SNOW': 0.001, 'NOT_SNOW': 0.999},
            Prior(['HIGH', 'COLD']): {'SNOW': 0.4, 'NOT_SNOW': 0.6}
        }
    )

    day = Node(
        ['WEEKEND', 'WEEKDAY'],  # States
        [],  # No parents
        {
            Prior([None]): {'WEEKEND': 0.2, 'WEEKDAY': 0.8}
        }
    )

    cloudy = Node(
        ['CLOUDY', 'NOT_CLOUDY'],
        [snow],
        {
            Prior(['NOT_SNOW']): {'CLOUDY': 0.3, 'NOT_CLOUDY': 0.7},
            Prior(['SNOW']): {'CLOUDY': 0.9, 'NOT_CLOUDY': 0.1}
        }
    )

    exams = Node(
        ['EXAMS', 'NOT_EXAMS'],  # States
        [snow, day],  # Parents
        {
            Prior(['NOT_SNOW', 'WEEKEND']): {'EXAMS': 0.001, 'NOT_EXAMS': 0.999},
            Prior(['NOT_SNOW', 'WEEKDAY']): {'EXAMS': 0.1, 'NOT_EXAMS': 0.9},
            Prior(['SNOW', 'WEEKEND']): {'EXAMS': 0.0001, 'NOT_EXAMS': 0.9999},
            Prior(['SNOW', 'WEEKDAY']): {'EXAMS': 0.3, 'NOT_EXAMS': 0.7}
        }
    )

    stress = Node(
        ['HIGH_STRESS', 'LOW_STRESS'],  # States
        [snow, exams],  # Parents
        {
            Prior(['NOT_SNOW', 'NOT_EXAMS']): {'HIGH_STRESS': 0.01, 'LOW_STRESS': 0.99},
            Prior(['NOT_SNOW', 'EXAMS']): {'HIGH_STRESS': 0.2, 'LOW_STRESS': 0.8},
            Prior(['SNOW', 'NOT_EXAMS']): {'HIGH_STRESS': 0.1, 'LOW_STRESS': 0.9},
            Prior(['SNOW', 'EXAMS']): {'HIGH_STRESS': 0.5, 'LOW_STRESS': 0.5}
        }
    )

    return [humidity, temperature, day, icy, snow, cloudy, exams, stress]


if __name__ == '__main__':
    main()
