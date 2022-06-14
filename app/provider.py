from abc import ABC, abstractmethod


class Provider(ABC):
    @abstractmethod
    def send_mail(self):
        pass
