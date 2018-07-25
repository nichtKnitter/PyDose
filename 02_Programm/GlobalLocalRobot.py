import time

from transitions import Machine


class VDummyKlasse(object):
    def schalten1(self):
        print("Geschaltet 1")

    def schalten2(self):
        print("Geschaltet 2")

    def say_hello(self): print("hello, new state!")

    def say_goodbye(self): print("goodbye, old state!")


class robotStateMachine(object):
    states = ['start', 'start_messung', 'segmentpruefung', 'messen', 'schalten', 'warten']
    # segTime = 0
    # tacktzeit = 0
    Messkarte = VDummyKlasse()

    def __init__(self, startparameter1):

        self.name = startparameter1
        self.kittens_rescued = 0

        self.num = 0
        self.segTime = time.time()
        self.tacktzeit = time.time()

        # Initialize the state machine
        self.machine = Machine(model=self, states=robotStateMachine.states, initial='start')
        # self.machine = Machine(
        #     model=self.Messkarte,
        #     states=self.states,
        #     initial='start'
        # )

        self.machine.add_transition(  # regel 1
            source='start',
            dest='start_messung',
            trigger='tock',
            after=['printTransition', 'resetTacktTimer']
        )
        self.machine.add_transition(  # regel 2
            source='start_messung',
            dest='segmentpruefung',
            trigger='tock',
            after=['printTransition']
            # ,            conditions=[self.testTimeisUp]
        )
        self.machine.add_transition(  # regel 3
            source='segmentpruefung',
            dest='messen',
            trigger='tock',
            after=['printTransition']
        )
        self.machine.add_transition(  # regel 3
            source='messen',
            dest='schalten',
            trigger='tock',
            after=['printTransition', 'VentileSchalten']
            # ,            conditions=[self.testTimeisUp]
        )
        self.machine.add_transition(  # regel 3
            source='schalten',
            dest='warten',
            trigger='tock',
            after=['printTransition']
            # ,            conditions=[self.testTimeisUp]
        )
        self.machine.add_transition(  # regel 3
            source='warten',
            dest='start',
            trigger='tock',
            after=['printTransition'],
            conditions=[self.testTacktTimer]
        )

    def testTacktTimer(self):
        self.num = self.num + 1
        if self.num == 100:
            print('.', end='', flush=True)
            self.num = 0
        # result = True if  else False
        if (time.time() - self.tacktzeit > 5):
            result = True
            print()
        else:
            result = False

        return result

    def resetTacktTimer(self):
        self.tacktzeit = time.time()
        # print ('nextState')
        # self.tock()

    def printTransition(self):
        print("state gewechselt zu:\t", self.state)

    def VentileSchalten(self):
        self.Messkarte.schalten1()


class globalRobot():
    batman = robotStateMachine("Batman")  # achtung! hier wird batman gleich wieder zerstört

    def run(self):
        while True:
            time.sleep(0.001)
            self.batman.tock()


blubb = globalRobot()
blubb.run()
