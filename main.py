from dbfread import DBF


class Group:
    def __init__(self, name, subgroup, prevgroup=None):
        self.name = name
        self.subgroup = subgroup
        self.prevgroup = prevgroup

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'{self.name} - {self.subgroup}'


def change_kodur(kodur, group):
    rez = {
        'kodur': '',
        'prevgroup': None
    }
    temp_arr = kodur.strip().split()
    if len(temp_arr) == 1:
        rez['kodur'] = str(temp_arr[0])
    elif group is None:
        rez['kodur'] = ''.join(kodur.strip().split()[:-1])
    else:
        rez['kodur'] = ''.join(kodur.strip().split())
        rez['prevgroup'] = temp_arr[0]
    return rez


def printMarki(marki_path='marki.dbf'):
    marki_arr = []
    for record in DBF(marki_path, lowernames=True):
        temp_marka = change_kodur(record['kodur'], record['group'])
        marki_arr.append({
            'group': record['group'],
            'naim': record['naim'],
            'kodur': temp_marka['kodur'],
            'prevgroup': temp_marka['prevgroup']
        })

    rez = dict()

    for record in marki_arr:
        if record['group']:
            if record['prevgroup'] is None:
                rez[record['kodur'].strip()] = Group(name=record['naim'], subgroup=[])
            else:
                rez[record['kodur'].strip()] = Group(name=record['naim'], subgroup=[], prevgroup=record['prevgroup'])

    for record in marki_arr:
        if record['group'] is None:
            index = record['kodur'].strip().split()[0]

            rez_temp_kodur = rez.get(index)

            if rez_temp_kodur:
                rez_temp_kodur.subgroup.append(Group(name=record['naim'], subgroup=[]))
            else:
                rez[record['kodur'].strip()] = Group(name=record['naim'], subgroup=[])
    del_arr = []
    for id, record in rez.items():
        if record.prevgroup is not None:
            rez[record.prevgroup].subgroup.append(rez[id])
            del_arr.append(id)
    for el in del_arr:
        del rez[el]

    for id, el in rez.items():
        print(el.name)
        if el.subgroup:
            for el_sub in el.subgroup:
                print('  ', el_sub.name)
                if el_sub.subgroup:
                    for el_sub2 in el_sub.subgroup:
                        print('      ', el_sub2.name)


if __name__ == '__main__':
    printMarki()
