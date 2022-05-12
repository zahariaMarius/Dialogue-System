import pyttsx3


class TextToSpeech:

    def __init__(self) -> None:
        super().__init__()
        self._engine = pyttsx3.init()
        self._voices = self._engine.getProperty('voices')
        self._engine.setProperty('voice', self._voices[7].id)

    def say(self, sentence):
        if isinstance(sentence, list):
            print('Professor Snape: {}'.format(' '.join(sentence)))
            for i, elem in enumerate(sentence):
                if i == (len(sentence) - 1):
                    self._engine.setProperty('rate', 260)
                self._engine.say(elem)
        else:
            print('Professor Snape: {}'.format(sentence))
            self._engine.say(sentence)
        self._engine.runAndWait()
