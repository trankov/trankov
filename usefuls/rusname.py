class RussianName:
    """
    Different forms of full Russian names (surname, name, patronymic)

    """

    def __init__(self, surname: str = "", name: str = "", patronymic: str = ""):
        self.f, self.i, self.o = surname, name, patronymic

    def surn_inits(self) -> str:
        """
        Surname and Initials letters with dots

        """
        i_ = f" {self.i[0]}." if self.i else ""
        o_ = f" {self.o[0]}." if self.o else ""
        return f"{self.f}{i_}{o_}"

    def initials(self) -> str:
        """
        First letters with dots

        """
        return (
            ".".join(char[0] for char in (self.f, self.i, self.o) if char != "") + "."
        )

    def fio(self, comma: bool = False, comma_sign: str = ",") -> str:
        """
        'Surname, Name Patronymic' or 'Surname Name Patronymic'
        depending on comma=True or comma=False

        """
        return f'{self.f}{comma and comma_sign or ""} {self.i} {self.o}'.strip()

    def full_name(self) -> str:
        """
        Name Patronymic

        """
        return f"{self.i} {self.o}".strip()

    def name_surname(self) -> str:
        return f"{self.i} {self.f}".strip()

    def surname_name(self) -> str:
        return f"{self.f} {self.i}".strip()
