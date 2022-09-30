age_token = lambda age_to: (
    (age_to in range(5, 20)) and 'лет' or
    (1 in (age_to, (diglast := age_to % 10))) and 'год' or
    ({age_to, diglast} & {2, 3, 4}) and 'года' or 'лет')

test = [f'{x} {age_token(x)}' for x in range(30)]

# OR

def inflate(
    number: int,
    nominative_singular: str,
    genetive_singular: str,
    nominative_plural: str
) -> str:
    """
      >>> number = 20
      >>> inflate(number, "год", "года", "лет")
      >>> 'лет'

    """
    return (
        (number in range(5, 20)) and nominative_plural or
        (1 in (number, (diglast := number % 10))) and nominative_singular or
        ({number, diglast} & {2, 3, 4}) and genetive_singular or nominative_plural
    ) # type: ignore
