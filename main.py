import numpy as np
import pandas as pd
import torch
import dm.dialog_manager as dm
import warnings
from dm.context_model import Intent
from analysis import speech_recognizer

warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)
warnings.filterwarnings(action='ignore', category=torch.jit.TracerWarning)  # suppress TracerWarning
warnings.warn('User provided device_type of \'cuda\', but CUDA is not available. Disabling')

if __name__ == '__main__':
    # crea manager e inizializza il contesto
    dialog_manager = dm.DialogManager()
    stop = True

    while (stop):
        # print('Prima system output')
        # with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.max_colwidth', None):
        #     print(dialog_manager.dialog_context_model.memory.get_data_frame())
        # print('frame')
        # print(dialog_manager.dialog_context_model.context.show_attributes())
        # print()
        dialog_manager.system_output()
        stop = dialog_manager.dialog_context_model.memory.get_data_frame()['intent'].values[-1] != Intent.EVALUATION
        if stop:
            # print()
            # print('Dopo system output')
            # with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.max_colwidth', None):
            #     print(dialog_manager.dialog_context_model.memory.get_data_frame())
            # print('frame')
            # print(dialog_manager.dialog_context_model.context.show_attributes())
            # print()
            #audio = speech_recognizer.recognizer()
            dialog_manager.user_input(input('Potter: '))
