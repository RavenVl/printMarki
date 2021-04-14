from pprint import pprint

from dbfread import DBF


class Group:
    def __init__(self, name, subgroup, order_sort, prevgroup=None):
        self.name = name
        self.subgroup = subgroup
        self.prevgroup = prevgroup
        self.order_sort = order_sort

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


def print_result(rez):
    for id_, el in sorted(rez.items(), key=lambda el: el[1].order_sort):
        print(el.name)
        if el.subgroup:
            for el_sub in el.subgroup:
                print('  ', el_sub.name)
                if el_sub.subgroup:
                    for el_sub2 in el_sub.subgroup:
                        print('      ', el_sub2.name)


def printMarki(marki_path='marki.dbf'):
    marki_arr = []
    # transferring dbf to dict for easier handling
    for i, record in enumerate(DBF(marki_path, lowernames=True)):
        temp_marka = change_kodur(record['kodur'], record['group'])
        marki_arr.append({
            'group': record['group'],
            'naim': record['naim'],
            'kodur': temp_marka['kodur'],
            'prevgroup': temp_marka['prevgroup'],
            'order_sort': i,
        })

    rez = dict()
    # обработка групп с подгруппами
    for record in marki_arr:
        if record['group']:
            if record['prevgroup'] is None:
                rez[record['kodur'].strip()] = Group(name=record['naim'], subgroup=[], order_sort=record['order_sort'])
            else:
                rez[record['kodur'].strip()] = Group(name=record['naim'],
                                                     subgroup=[],
                                                     order_sort=record['order_sort'],
                                                     prevgroup=record['prevgroup'])
    # обработка подгрупп
    for record in marki_arr:
        if record['group'] is None:
            index = record['kodur'].strip().split()[0]

            rez_temp_kodur = rez.get(index)

            if rez_temp_kodur:
                rez_temp_kodur.subgroup.append(Group(name=record['naim'], subgroup=[], order_sort=record['order_sort']))
            else:
                rez[record['kodur'].strip()] = Group(name=record['naim'], subgroup=[], order_sort=record['order_sort'])

    # добавление вложенных подгрупп
    del_arr = []
    for id_, record in rez.items():
        if record.prevgroup is not None:
            rez[record.prevgroup].subgroup.append(rez[id_])
            del_arr.append(id_)
    for el in del_arr:
        del rez[el]

    print_result(rez)




if __name__ == '__main__':
    printMarki()
