age_token = lambda age_to: (
    (age_to in range(5, 20)) and 'лет' or
    (1 in (age_to, (diglast := age_to % 10))) and 'год' or
    ({age_to, diglast} & {2, 3, 4}) and 'года' or 'лет')

test = [f'{x} {age_token(x)}' for x in range(30)]
