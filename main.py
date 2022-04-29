import dm.dialog_manager as dm

if __name__ == '__main__':
    #crea manager e inizializza il contesto
    dialog_manager = dm.DialogManager()

    while True:
        print(dialog_manager.dialog_context_model.memory.get_data_frame())
        print()
        print("Professor Snape: " + dialog_manager.system_output())
        print()
        print(dialog_manager.dialog_context_model.memory.get_data_frame()['expected'])
        print()
        dialog_manager.user_input(input('Potter: '))

