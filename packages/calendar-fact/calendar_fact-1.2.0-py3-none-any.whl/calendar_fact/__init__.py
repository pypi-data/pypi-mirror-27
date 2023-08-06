from random import choice

__version__ = '1.2.0'

event_list = [
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

recurrence_3_list = [
    'sun',
    'moon',
    'zodiac',
    f'{choice(["gregorian", "mayan", "lunar", "iphone"])} calendar',
    'atomic clock in colorado',
]

recurrence_list = [
    f'happens {choice(["earlier", "later", "at the wrong time"])} every year',
    f'drifts out of sync with the {choice(recurrence_3_list)}',
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

trivia_list = [
    'causes huge headaches for software developers',
    'is taken advantage of by high-speed traders',
    'triggered the 2003 Northeast Blackout',
    'has to be corrected for by GPS satellites',
    'is now recognized as a major cause of World War I',
]


def get_fact(separator=' '):
    parts = [
        f'Did you know that {choice(event_list)} {choice(recurrence_list)} because of {choice(cause_list)}?',
        f'apparently {choice(effect_list)}.',
        f'While it may seem like trivia, it {choice(trivia_list)}.',
    ]
    return separator.join(parts)


def run(separator=' '):
    print(get_fact(separator))


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser(description='Print a calendar fact from https://xkcd.com/1930/')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--separator', type=str,
                       help='A separator between sections, default: a space (" ")', default=' ')
    group.add_argument('-n', '--new-line', action='store_true', help='Separate sections with a new line')
    args = parser.parse_args()

    separator = args.separator
    if args.new_line:
        separator = '\n'

    run(separator)
