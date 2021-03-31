# import xml.etree.ElementTree as ET
from lxml import etree
import os
import os.path
import time
import re
import collections

file_name = input('Enter the file name: ')
tree = etree.parse(file_name)
root = tree.getroot()
lst = []
new_lst = []
name_lst = []


def search_file(xlm):
    cur_dir = os.getcwd()
    while True:
        file_list = os.listdir(cur_dir)
        print(f'Searching for {xlm} in {cur_dir}\n')
        if xlm in file_list:
            os.system('cls')
            print(f'Successfully found {xlm}. Opening...')
            # time.sleep(2)
            resource_search(xlm)
            break
        else:
            print(f"File {xlm} was not found")
            break


def resource_search(xml):
    data = []

    for node in tree.xpath('./Resource'):
        data.append(node.get('name'))

    user_input = input('Enter the resource name: ')
    fuzzy_finder(user_input, data)


def fuzzy_finder(user_input, data):
    suggestions = []
    pattern = '.*'.join(user_input)
    regex = re.compile(pattern)
    for item in data:
        match = regex.search(item)
        if match:
            suggestions.append((match.start(), item))
    for number, name in enumerate([x for _, x in sorted(suggestions)]):
        print(number, name)

    print()
    answer = list(map(int, input('Choose a number to see name properties: ').split()))

    if len(answer) > 1:
        for num in answer:
            multiple_info_by_names(sorted(suggestions)[num][1])
    else:
        strings = [str(integer) for integer in answer]
        a_string = " ".join(strings)
        one = int(a_string)
        info_by_name(sorted(suggestions)[one][1])

    # answer = int(input('Choose a number to see name properties: '))
    # info_by_name(sorted(suggestions)[answer][1])


def info_by_name(name):
    global info
    os.system('cls')

    for child in root.findall(f"./Resource[@name='{name}']"):
        info = child.attrib
    for key, value in info.items():
        print(key, ' : ', value)

    property = input('Choose a property to change: ')
    change_property(name, property)


def multiple_info_by_names(names):
    global infos

    for child in root.findall(f"./Resource[@name='{names}']"):
        infos = child.attrib

    while True:
        if names:
            for tags in infos:
                lst.append(tags)
            break
        else:
            break
    final_lst = [''.join(x) for x in lst]
    super = ' '.join(final_lst)
    # compare_final_lst = ([item for item, count in collections.Counter(final_lst).items() if count > 1])
    # print(super)

    words = super.split(" ")
    for i in range(0, len(words)):
        count = 1
        for j in range(i + 1, len(words)):
            if words[i] == (words[j]):
                count = count + 1
                words[j] = '0'

                # Displays the duplicate word if count is greater than 1
        if count > 1 and words[i] != "0":
            new_lst.append(words[i])

    print('Same parameters for chosen resources: ')
    choose_multiple_properties(new_lst, infos)


def change_property(name, property):
    new_property = input(f'Type a new value for the {property} variable: ')

    for find in tree.xpath(f"./Resource[@name='{name}']"):
        find.attrib[property] = new_property

    entry = etree.ElementTree(root)
    entry.write('output.xml', pretty_print=True, xml_declaration=True, encoding='utf-8')


def choose_multiple_properties(lst_names, infos):
    final_lst = [''.join(x) for x in lst_names]
    column = ' '.join(final_lst)
    print()
    print(*column.split(), sep='\n')

    names_lst = []
    names_lst.append(infos.get('name'))

    change_multiple_properties(names_lst)


def change_multiple_properties(names_lst, ):
    print(names_lst)


if __name__ == '__main__':
    search_file(file_name)
