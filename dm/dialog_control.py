from dm.context_model import DialogContextModel
from generation.response_generation import *


class DialogControl:

    def __init__(self, dialog_context_model: DialogContextModel) -> None:
        super().__init__()
        self._dialog_context_model = dialog_context_model
        self._response_generator = ResponseGenerator()

    def choose_response(self):
        mem = self._dialog_context_model.memory.get_data_frame()
        right = mem['right'].values[-1]
        wrong = mem['wrong'].values[-1]
        complete= mem['complete'].values[-1]

        #sta parlando di tutt'altro
        if right == 0 and wrong == 0:
            self._response_generator.refusal()
        elif complete == 100:
            self._response_generator.approval()
        else:
            self._response_generator.clarify()

