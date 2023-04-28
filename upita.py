# CONSTANTS -------------------------------------------------------------------------------------------------

DIGITS = "0123456789"

# TOKENS DECLARATION -----------------------------------------------------------------------------------------

TOKEN_INT = "INT"  # Entiers
TOKEN_FLOAT = "FLOAT"  # Décimaux
TOKEN_PLUS = "PLUS"  # Addition
TOKEN_MINUS = "MINUS"  # Soustraction
TOKEN_MUL = "MUL"  # Multiplication
TOKEN_DIV = "DIV"  # Division
TOKEN_LPAREN = "LPAREN"  # Parenthèse gauche
TOKEN_RPAREN = "RPAREN"  # Parenthèse droite
TOKEN_EOF = "EOF"  # Fin de fichier (EndOfFile)

# TOKENS ----------------------------------------------------------------------------------------------------


class Token:

    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):  # Renvoie en string le type et la valeur (si y'en a) du token.
        if self.value:
            return f'{self.type}:{self.value}'
        else:
            return f'{self.type}'


# POSITION --------------------------------------------------------------------------------------------------


class Position:

    def __init__(self, index, col, line, filename, filetext):
        self.index = index
        self.col = col
        self.line = line
        self.filename = filename
        self.filetext = filetext

    def advance(self, current_char=None):  # Augmente l'index et la colonne de 1
        self.index += 1
        self.col += 1
        if current_char == "\n":  # Si changement de ligne, on incrémente la ligne et met la colonne à 0
            self.line += 1
            self.col += 1

    def copy(self):  # Copie toutes les valeurs de init
        return Position(self.index, self.col, self.line, self.filename, self.filetext)


# LEXER -----------------------------------------------------------------------------------------------------


class Lexer:

    def __init__(self, filename, text):
        self.filename = filename
        self.text = text
        self.pos = Position(-1, 0, -1, filename, text)  # Crée une instance de Position pour mettre le curseur
        self.current_char = None
        self.advance()

    def advance(self):  # Avance de 1 le caractère si y'a quelque chose
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.index] if self.pos.index < len(self.text) else None

    def get_tokens(self):  # Récupère le texte et, pour chaque caractère, renvoie le token.
        tokens = []
        while self.current_char is not None:
            if self.current_char == " \t":
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(Token(self.get_number()))  # Ici il faut get_number()
                self.advance()
            elif self.current_char == "+":
                tokens.append(Token(TOKEN_PLUS))
                self.advance()
            elif self.current_char == "-":
                tokens.append(Token(TOKEN_MINUS))
                self.advance()
            elif self.current_char == "*":
                tokens.append(Token(TOKEN_MUL))
                self.advance()
            elif self.current_char == "/":
                tokens.append(Token(TOKEN_DIV))
                self.advance()
            elif self.current_char == "(":
                tokens.append(Token(TOKEN_LPAREN))
                self.advance()
            elif self.current_char == ")":
                tokens.append(Token(TOKEN_RPAREN))
                self.advance()
            else:
                return []
        tokens.append(Token(TOKEN_EOF))
        return tokens, None

    def get_number(self):  #
        num_str = ""
        dot_count = 0
        while self.current_char in DIGITS + ".":
            if self.current_char == ".":
                if dot_count >= 1:  # Si il y a plus d'une virgule, renvoie une erreur.
                    start_pos = self.pos.index
                    return [], IllegalFloatingPointError(start_pos, end_pos=None, details="Two floating points in a same float")
                else:
                    dot_count += 1
                    num_str += "."
            else:
                num_str += self.current_char
                self.advance()
        if dot_count == 0:  # Renvoie le bon token en fonction du nombre de virgules
            return Token(TOKEN_INT, int(num_str))
        else:
            return Token(TOKEN_FLOAT, float(num_str))

# ERRORS ----------------------------------------------------------------------------------------------------


class Error:

    def __init__(self, start_pos, end_pos, error_name, details):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.error_name = error_name
        self.details = details

    def as_string(self):  # Renvoie, en chaîne de caractères, l'erreur
        result = f'{self.error_name}: {self.details}'
        result += f'File {self.start_pos.filename}, at line {self.start_pos.line + 1}'
        return result


class IllegalCharError(Error):  # Erreur quand le lexer trouve un caractère non supporté

    def __init__(self, start_pos, end_pos, details):
        super().__init__(start_pos, end_pos, 'IllegalCharacterError', details)


class IllegalFloatingPointError(Error):  # Erreur quand le lexer trouve deux virgules dans un float

    def __init__(self, start_pos, end_pos, details):
        super().__init__(start_pos, end_pos, 'IllegalFloatingPointError', details)

# RUN ---------------------------------------------------------------------------------------------------

def run(filename, text):  # Run le shell et transforme l'entrée en tokens grâce au lexer
    lexer = Lexer(filename, text)
    tokens, error = lexer.get_tokens()
    return tokens, error
