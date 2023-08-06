from random import choice

__version__ = '1.0.0'

fact_list = [
    f'the {choice(["fall", "spring"])} equinox',
    f'the {choice(["winter", "summer"])} {choice(["solstice", "olympics"])}',
    f'the {choice(["earliest", "latest"])} {choice(["sunrise", "sunset"])}',
    f'daylight {choice(["saving", "savings"])} time',
    f'leap {choice(["day", "year"])}',
    f'easter',
    f'the {choice(["harvest", "super", "blood"])} moon',
    f'toyota truck month',
    f'shark week',
]

occurrence_3_list = [
    'sun',
    'moon',
    'zodiac',
    f'{choice(["gregorian", "mayan", "lunar", "iphone"])} calendar',
    'atomic clock in colorado',
]

occurrence_list = [
    f'happens {choice(["earlier", "later", "at the wrong time"])} every year',
    f'drifts out of sync with the {choice(occurrence_3_list)}',
    f'might {choice(["not happen", "happen twice"])} this year',
]

cause_3_list_1 = [
    'precession',
    'liberation',
    'nutation',
    'libation',
    'eccentricity',
    'obliquity',
]

cause_3_list_2 = [
    'moon',
    'sun',
    'earth\'s axis',
    'equator',
    'prime meridian',
    f'{choice(["international date", "mason-dixon"])} line'
]

cause_list = [
    f'the zone legislation in {choice(["indiana", "arizona", "russia"])}',
    f'a decree by the pope in the 1500s',
    f'{choice(cause_3_list_1)} of the {choice(cause_3_list_2)}',
    f'magnetic field reversal',
    f'an arbitrary decision by {choice(["benjamin franklin", "isaac newton", "fdr"])}',
]

effect_5_list = [
    'will never happen',
    'actually makes things worse',
    'is stalled in congress',
    'might be unconstitutional',
]

effect_list = [
    'it causes a predictable increase in car accidents',
    'that\'s why we have leap seconds',
    'scientists are really worried',
    f'it was even more extreme during the {choice(["bronze age", "ice age", "cretaceous", "1990s"])}',
    f'there\'s a proposal to fix it, but it {choice(effect_5_list)}',
    'it\'s getting worse and no one knows why',
]


def get_fact():
    return f'Did you know that {choice(fact_list)} {choice(occurrence_list)} because of {choice(cause_list)}? ' \
           f'apparently {choice(effect_list)}.'


def run():
    print(get_fact())


if __name__ == '__main__':
    run()
