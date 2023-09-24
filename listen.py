# Empty List
empty_list = []

print(empty_list)

# Filled list

filled_list = ['Hello World', 'Mettbrötchen']

print(filled_list)


# Objecte zu Liste hinzufügen

object_list = []

basic_string = "Hello world"

object_list.append(basic_string)

print(object_list)


# Listen auslesen mit for loops

for x in filled_list:
    print(x)


# Einzelne Objecte aus Listen auslesen

random_list = []
for x in range(20):
    random_list.append(x)

print(random_list[2:16])

# Python fuctions useful on lists

#lenght on an tuple (amount)
print(len(random_list))


##############


# Empty Tuple

empty_tuple = ()

print(empty_tuple)

# Filled Tuple

filled_tuple = (1, 20)

print(filled_tuple)


#################

# Dict

empty_dict = {}

# filled dict

filled_dict = {
    '0': "Hello World",
    'eins': "Mettbrötchen",
}

# access values via key

print(filled_dict['eins'])