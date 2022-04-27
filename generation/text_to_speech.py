import pyttsx3


class TextToSpeech:
    
    def __init__(self) -> None:
        super().__init__()
        self._engine = pyttsx3.init()
        self._voices = self._engine.getProperty('voices')
        self._rate = self._engine.getProperty('rate')
        self._engine.setProperty('voice', self._voices[1].id)
        self._engine.setProperty('rate', 125) 
        
    def say(self, sentence):    
        self._engine.say(sentence)
        self._engine.runAndWait()
        self._engine.stop()
