import random

def jailbreak():
    print("You have picked up a JAILBREAK card!")
    US = input("Would you like to use or store this card? U/S ").upper()

    while US != "U" and US != "S":
        US = input("Please select an option correctly. U/S ").upper()
    
    if US == "U":
        print("You have now been realesed early from jail due to chance! ")

    if US == "S":
        print("You have now stored the JAILBREAK card! ")


C_cards = ["jailbreak", "gotogo", "moveup", "movedown", "paydebt"]

random_C_card = random.choice(C_cards)
print(random_C_card)

if random_C_card == "jailbreak":
    jailbreak()