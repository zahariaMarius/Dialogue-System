from dm import dialog_control
from dm import context_model


class DialogManager:
    dialog_context_model = context_model.DialogContextModel()
    dialog_control = dialog_control.DialogControl(dialog_context_model)

    def __init__(self) -> None:
        super().__init__()
        self.dialog_context_model()

    def user_input(self, sentence: str):
        self.dialog_context_model.process_input(sentence)

    def system_output(self):
        self.dialog_control.choose_response()
