from collections import Counter
class Simulation:
    def __init__(self, duration, noi, nos, noc, pv):
        self.duration = duration
        self.no_of_intersections = noi
        self.no_of_streets = nos
        self.no_of_cars = noc
        self.point_value = pv
        self.streets = []
        self.cars = []
        self.street_counter = Counter()
        self.intersections = []
        
    def count_streets_on_route(self):
        for car in self.cars:
            car.count_streets()
            self.street_counter += car.counter
        for street in streets:
            street.mentioned = self.street_counter[street]
            # print(street.name, street.mentioned)


    def find_intersections(self):
        for i in range(self.no_of_intersections):
            self.intersections.append(Intersection())
        for street in streets:
            self.intersections[street.start].outgoing_streets.append(street)
            self.intersections[street.end].incoming_streets.append(street)

    def get_output(self):
        output= str(self.no_of_intersections)+'\n'
        for i, intersection in enumerate(self.intersections):
            output += '{} \n{}\n'.format(i, len(intersection.incoming_streets))
            for street in intersection.incoming_streets:
                weight = (len(intersection.outgoing_streets)*0.1) +(street.duration*0.01)
                formula = max(int((4*(1/intersection.total_incoming)*street.mentioned)+weight), 1)
                if street.mentioned == 0:
                    formula = 0
                # print("{} : 6 * 1/{} * {} = {}".format(street.name, intersection.total_incoming, street.mentioned,formula))
                output += "{} {}\n".format(street.name, formula)
        return output

    def print_output(self):
        print(self.get_output())

    def file_output(self, name):
        with open(name, 'w') as fd:
            fd.write(self.get_output())

    def pre_process(self):
        self.find_intersections()
        self.count_streets_on_route()
        for intersection in self.intersections:
            intersection.weight_streets()

        

class Intersection:
    def __init__(self):
        self.outgoing_streets = []
        self.incoming_streets = []
        self.duration = 0
        self.important = False
        self.min_incoming = float("inf")
        self.total_incoming = 1

    def weight_streets(self):
        for street in self.incoming_streets:
            if street.mentioned == 0:
                print('Empty Street')
                continue
            elif street.mentioned < self.min_incoming:
                self.min_incoming = street.mentioned
            self.total_incoming += street.mentioned
            # print(self.total_incoming, ' + ', street.mentioned)
            # print(self.total_incoming)


    def add_incoming(self, street):
        self.incoming_streets.append(street)

    def add_outgoing(self, street):
        self.outgoing_streets.append(street)

class Street:
    def __init__(self, start, end, name, duration):
        self.start = start
        self.end = end
        self.name = name
        self.duration = duration
        self.mentioned = 0

class Car:
    def __init__(self, nos, streets):
        self.no_of_streets = nos
        self.streets = streets
        self.counter = ''

    def count_streets(self):
        self.counter = Counter(streets)

NAMES =['a', 'b', 'c', 'd', 'e', 'f']
# NAMES =['b']
for NAME in NAMES:
    streets = []
    cars = []
    INPUT_FILE ='{}.txt'.format(NAME)
    OUTPUT_FILE='{}_SOL.txt'.format(NAME)
    with open(INPUT_FILE) as fd:
        line = fd.readline()
        dur, noi, nos, noc, pv = line.split(' ')
        sim = Simulation(int(dur), int(noi), int(nos), int(noc), int(pv))
        for i in range(int(nos)):
            line = fd.readline()
            start, end, name, duration = line.split(' ')
            streets.append(Street(int(start), int(end), name, int(duration)))
        for i in range(int(noc)):
            line = fd.readline()
            line = line.split(' ')
            cars.append(Car(int(line[0]), line[1:]))

    sim.streets = streets
    sim.cars = cars
    sim.pre_process()
    
    # sim.print_output()
    sim.file_output(OUTPUT_FILE)
    print('{} done'.format(NAME))

