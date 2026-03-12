from abc import ABC, abstractmethod
from application.application_context import ApplicationContext


class PipelineStage(ABC):
    @abstractmethod
    def run(self, application_context: ApplicationContext):
        pass
