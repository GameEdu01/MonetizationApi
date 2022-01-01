class Manager:

    def __init__(self):

        self.allowedLetters = "qwertyuiopasdfghjklzxcvbnm1234567890"
        self.phoneNumberAllowedLetters = "1234567890+ "

    def check_spelling(self, text, email=False, phone_number=False):

        accurate = True

        if text == "":
            accurate = False

        if not phone_number:
            for letter in text:
                if not letter in self.allowedLetters:
                    if email:
                        if letter == "@":
                            continue
                    accurate = False
        else:
            for letter in text:
                if not letter in self.phoneNumberAllowedLetters:
                    accurate = False

        return accurate
