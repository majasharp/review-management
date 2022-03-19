class MorseConverter:

    def __init__(self):
        # International morse code dictionary
        self.int_morse_code = {
            "a" : ". -",
            "b" : "- . . .",
            "c" : "- . - .",
            "d" : "- . .",
            "e" : ".",
            "f" : ". . - .",
            "g" : "- - .",
            "h" : ". . . .",
            "i" : ". .",
            "j" : ". - - -",
            "k" : "- . -",
            "l" : ". - . .",
            "m" : "- -",
            "n" : "- .",
            "o" : "- - -",
            "p" : ". - - .",
            "q" : "- - . -",
            "r" : ". - .",
            "s" : ". . .",
            "t" : "-",
            "u" : ". . -",
            "v" : ". . . -",
            "w" : ". - -",
            "x" : "- . . -",
            "y" : "- . - -",
            "z" : "- - . .",
            "1" : ". - - - -",
            "2" : ". . - - -",
            "3" : ". . . - -",
            "4" : ". . . . -",
            "5" : ". . . . .",
            "6" : "- . . . .",
            "7" : "- - . . .",
            "8" : "- - - . .",
            "9" : "- - - - .",
            "0" : "- - - - -"
        }

    def to_morse(self, message):
        morse = ""
        for c in message:
            try:
                # three time units between characters
                morse = morse + "   " +  self.int_morse_code[c]
            except KeyError:
                morse = morse + "       " # seven time units for space or other unsupported characters.
        return morse

    
