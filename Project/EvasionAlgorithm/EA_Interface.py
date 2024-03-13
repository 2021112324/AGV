from abc import abstractmethod, ABCMeta
class EA_Interface(metaclass=ABCMeta):
    @abstractmethod
    def UpdateMap(self,map):
        pass

    @abstractmethod
    def UpdateRobot(self,robot):
        pass

    @abstractmethod
    def DeleteRobot(self,robot):
        pass

    @abstractmethod
    def EvasionAlgorithm(self,robot):
        pass