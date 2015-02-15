import re

surname_patterns = [
    {
        'pattern': r'^O(BR[IEYA]{2}N|BRYANT|GORMAN|FLANAGAN|HALLORAN|HARA|LOUGHLIN|SHAUGHNESSY|CONNOR|N[EAI]+LL?|CALLAG?HAN|SHEA|ROURKE|TOOLE?|GRADY|BANNON|BARR|SULLIVAN|DONOHUE|.ONN?ELL?Y?|KEEFE|DOHERTY|[KM][AE]LLE?Y|DONLEY|BAUGH|R[EI]{2}LLEY|BOYLE|.ARR.LL|DELL|HARROLL|DOUGHERTY|[CD]ON[AE]Ll?)(S?)$',
        'replace': lambda pattern: "O'" + pattern.group(1).capitalize() + pattern.group(2).lower()
    },
    {
        'pattern': r'^ST([^AEIOURY]\w+$)',
        'replace': lambda pattern: "St. " + pattern.group(1).capitalize()
    },
    {
        'pattern': r'^MC(\w+)$',
        'replace': lambda pattern: 'Mc' + pattern.group(1).capitalize()
    }
]


def recapitalize_surnames(fragment):
    for reformat in surname_patterns:
        fragment = re.sub(reformat['pattern'], reformat['replace'], fragment, flags=re.IGNORECASE)
    return fragment
