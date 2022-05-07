import numpy as np
import pandas as pd
import dm.dialog_manager as dm
import warnings
from analysis.language_understanding import parse_sentence

warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)

if __name__ == '__main__':
    # crea manager e inizializza il contesto
    dialog_manager = dm.DialogManager()

    while True:
        print('Prima system output')
        with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.max_colwidth', None):
            print(dialog_manager.dialog_context_model.memory.get_data_frame())
        print('frame')
        print(dialog_manager.dialog_context_model.context.show_attributes())
        print()
        print("Professor Snape: " + dialog_manager.system_output())
        print()
        print('Dopo system output')
        with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.max_colwidth', None):
            print(dialog_manager.dialog_context_model.memory.get_data_frame())
        print('frame')
        print(dialog_manager.dialog_context_model.context.show_attributes())
        print()
        dialog_manager.user_input(input('Potter: '))
