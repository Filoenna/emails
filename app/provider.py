from abc import ABC, abstractmethod


class Provider(ABC):
    @abstractmethod
    async def send_mail(self):
        pass

    @abstractmethod
    def prepare_message(self):
        pass
