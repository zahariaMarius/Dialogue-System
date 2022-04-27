import dm.dialog_manager as dm

if __name__ == '__main__':
    # crea manager e inizializza il contesto

    dialog_manager = dm.DialogManager()
    print(type(dialog_manager.dialog_context_model.context))

    sentence = 'cacca'
    dialog_manager.user_input(sentence)

    dialog_manager.system_output()
