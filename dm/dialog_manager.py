from dm import dialog_control
from dm import context_model
from generation import text_to_speech

"""
classe che inizializza il ControlDialog e il ControlManager
e gestisce l'output (sistema) e l'input (utente)
"""


class DialogManager:
    dialog_context_model = context_model.DialogContextModel()
    dialog_control = dialog_control.DialogControl(dialog_context_model)
    tts = text_to_speech.TextToSpeech()

    def __init__(self) -> None:
        super().__init__()
        self.dialog_context_model()

    # output da parte del systema, la frase viene scelta dal metodo choose_output()
    def system_output(self):
        return self.tts.say(self.dialog_control.choose_output())

    # input da parte dell'utente, viene analizzato dal metodo process_input()
    def user_input(self, sentence: str):
        return self.dialog_context_model.process_input(sentence)
