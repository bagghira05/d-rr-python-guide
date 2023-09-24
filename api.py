import requests

# LINK = "https://catfact.ninja/fact"

# response = requests.get(LINK)

# if response.status_code == 200:
#     print("success!")
# elif response.status_code == 404:
#     print("not found!")

# print(response.json())

# json = response.json()

# print(json['fact'])

# facts_liste = []

# for x in range(5):
#     response = requests.get(LINK)
#     json = response.json()
#     facts_liste.append(json['fact'])

# for y in facts_liste:
#     print(y)



# LINK = "http://ntfy.timschyrocki.de/coffee"

# LINK2 = "https://catfact.ninja/fact"

# response = requests.get(LINK2)

# x = response.json()

# response = requests.post(data=x['fact'].encode(encoding='utf-8'), url=LINK)

# response.status_code

# if response.status_code == 200:
#     print("Success!")
# elif response.status_code == 404:
#     print("not found!")


# Fahrenheit = float(input("Gib die Temperatur in Fahrenheit an: ") )

# Celsius = round((Fahrenheit - 32) * (5 / 9))

# print("Die Temperatur beträgt ", Celsius, "Grad")


def grad_Converter(input):
    if input[-1] == 'C':
        Fahrenheit = round(int(input[:-1]) * 1.8 + 32)
        return str(Fahrenheit) + " F"
    elif input[-1] == 'F':
        Celsius = round((int(input[:-1]) - 32) * (5 / 9))
        return str(Celsius) + " C"
    
input = str(input("Gib deine Temperatur ein: "))

x = grad_Converter(input)

print(x)
















