import time


class VDummyKlasse(object):
    def schalten1(self):
        print("1")

    def schalten2(self):
        print("2")

    def say_hello(self): print("hello, new state!")

    def say_goodbye(self): print("goodbye, old state!")


from transitions import Machine

#########################################
####### Local Robot
########################################
class localRobot():
    # class localRobot(Segmentart='halten', pSoll=0, TSoll=20, TimeMax=5):

    Messkarte = VDummyKlasse()
    states = ['s1', 's2', 'gas', 'plasma']
    transitions = [
        {'trigger': 'schalten_hoch', 'source': 's1', 'dest': 's2'},
        {'trigger': 'schalten_runter', 'source': 's2', 'dest': 's1'},
        {'trigger': 'sublimate', 'source': 's1', 'dest': 's2'},
        {'trigger': 'ionize', 'source': 's2', 'dest': 's1'}
    ]
    machine = Machine(model=Messkarte, states=states, transitions=transitions, initial='s1')
    # machine.add_transition('schalten_hoch', 's1', 's2')
    # machine.add_transition('schalten_runter', 's2', 's1')
    # Lump now has state!
    print('Messkarte.state:\t', Messkarte.state)
    print('Messkarte.is_plasma()\t',
          Messkarte.is_plasma())  ## Wichtig! So kann ich auf die Statemethoden zugreifen, wird nicht im autocomplete angezeigt!!!!
    Messkarte.to_plasma()
    Messkarte.say_goodbye()

    def schalten_hoch(self):
        self.Messkarte.schalten1()
        self.Messkarte.state = 's2'
        print('Messkarte1:\t', self.Messkarte.state)

    def schalten_2(self):
        self.Messkarte.schalten2()
        self.Messkarte.state = 's1'
        print('Messkarte2:\t', self.Messkarte.state)

    def schalten_3(self):
        self.Messkarte.schalten2()
        print('is plasma: ', self.Messkarte.is_plasma())




#########################################
####### Global Robot
########################################

class GlobalRobot():
    states = ['THochIsobar', 'TRunterIsobar', 'pHochIsotherm', 'gemischt', 'pRunterIsotherm', 'Ausheizen','NA']
    currentState = ['NA']
    localRobotObj = localRobot()
    timestart = time.time()
    def los(self):
        while time.time() - self.timestart < 5:
            ### hier aussen die warteschleife implementieren?
            # 0. Messen
            # 1. segmentstate mit segmentsollstate abgleichen
            # bei Änderung vsoll, timeSoll, wunschstate,
            # 2. in jeweilige regelstrategie gehen
            #       jeweilige stellparameter berechnen
            #       schalten

            # assert machine.get_state(hero.state).is_busy  # We are at home and busy
            # assert hero.state == 'away'  # Impatient superhero already left the building
            # assert machine.get_state(hero.state).is_home is False  # Yupp, not at home anymore
            print('1 Robot.Messkarte.state\t', localRobot.Messkarte.state)
            # Robot.Messkarte.schalten2()
            # Robot.Messkarte.schalten1()
            print('2 Robot.Messkarte.state\t', self.localRobotObj.Messkarte.state)
            self.localRobotObj.Messkarte.schalten2()

            #
            # localRobotObj.schalten_hoch()
            # localRobotObj.schalten_runter()

            self.localRobotObj.Messkarte.to_plasma()
            print(self.localRobotObj.Messkarte.state)  ### Achtung! Variable wird nicht in pycharm angezeigt.
            self.localRobotObj.Messkarte.to_s2()
            print(self.localRobotObj.Messkarte.state)  ### Achtung! Variable wird nicht in pycharm angezeigt.

            self.localRobotObj.Messkarte.schalten2()
            print(self.localRobotObj.Messkarte.state)  ### Achtung! Variable wird nicht in pycharm angezeigt.

            self.localRobotObj.Messkarte.to_s1()
            print(self.localRobotObj.Messkarte.state)  ### Achtung! Variable wird nicht in pycharm angezeigt.

            time.sleep(1)



Hauptrechner = GlobalRobot()
Hauptrechner.los()
