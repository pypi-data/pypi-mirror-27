
from capsul.attributes.completion_engine import ProcessCompletionEngine, \
    PathCompletionEngine, ProcessCompletionEngineFactory
from capsul.attributes.completion_engine_iteration \
    import ProcessCompletionEngineIteration
from capsul.attributes.fom_completion_engine \
    import FomProcessCompletionEngine, FomPathCompletionEngine, \
    FomProcessCompletionEngineIteration
from capsul.pipeline.process_iteration import ProcessIteration


class BuiltinProcessCompletionEngineFactory(ProcessCompletionEngineFactory):
    '''
    '''
    factory_id = 'builtin'

    def get_completion_engine(self, process, name=None):
        '''
        Factory for ProcessCompletionEngine: get an ProcessCompletionEngine
        instance for a process in the context of a given StudyConfig.

        The study_config should specify which completion system(s) is (are)
        used (FOM, ...)
        If nothing is configured, a ProcessCompletionEngine base instance will
        be returned. It will not be able to perform completion at all, but will
        conform to the API.
        '''
        if hasattr(process, 'completion_engine'):
            return process.completion_engine

        study_config = process.get_study_config()

        # FOM
        if 'FomConfig' in study_config.modules and study_config.use_fom:
            try:
                pfom = FomProcessCompletionEngine(process, name)
                if pfom is not None:
                    pfom.create_attributes_with_fom()
                    return pfom
            except KeyError:
                # process not in FOM
                pass

        # iteration
        if isinstance(process, ProcessIteration):
            if isinstance(
                    ProcessCompletionEngine.get_completion_engine(
                        process.process),
                    FomProcessCompletionEngine):
                return FomProcessCompletionEngineIteration(process, name)
            else:
                return ProcessCompletionEngineIteration(process, name)

        # standard ProcessCompletionEngine
        return ProcessCompletionEngine(process, name)

