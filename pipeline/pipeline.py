from pipeline.stages.pipeline_stage import PipelineStage
from application.application_context import ApplicationContext


class Pipeline:
    def __init__(self, application_context: ApplicationContext):
        self.application_context = application_context
        self.stages = []

    def add_stage(self, pipeline_stage: PipelineStage):
        if not isinstance(pipeline_stage, PipelineStage):
            raise TypeError(
                f"Expected an instance of PipelineStage or one of its subclasses,"
                f"but got {type(pipeline_stage).__name__} instead."
            )
        self.stages.append(pipeline_stage)

    def run(self):
        if len(self.stages) < 1:
            raise RuntimeError(
                "Cannot run a pipeline with no stages. Add at least one stage before running."
            )
        for stage in self.stages:
            stage.run(self.application_context)
