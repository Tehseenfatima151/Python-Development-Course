logo = r'''
                                                                                                                                  
    mmmm                                                                  mmmm      ##               mm                           
  ##""""#                                                               ##""""#     ""               ##                           
 ##"        m#####m   m####m   mm#####m   m#####m   ##m####            ##"        ####     ##m###m   ##m####m   m####m    ##m####
 ##         " mmm##  ##mmmm##  ##mmmm "   " mmm##   ##"                ##           ##     ##"  "##  ##"   ##  ##mmmm##   ##"
 ##m       m##"""##  ##""""""   """"##m  m##"""##   ##                 ##m          ##     ##    ##  ##    ##  ##""""""   ##
  ##mmmm#  ##mmm###  "##mmmm#  #mmmmm##  ##mmm###   ##                  ##mmmm#  mmm##mmm  ###mm##"  ##    ##  "##mmmm#   ##
    """"    """" ""    """""    """"""    """" ""   ""                    """"   """"""""  ## """    ""    ""    """""    ""
                                                                                           ##
                                                                                           ""
'''
print(logo)
# two seperate functions for ceaser cipher
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
             'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
             'a', 'b', 'c', 'd','e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
             'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
def caesar(text, shift, direction):
    cipher_text = ""
    for letter in text:
        if letter in alphabet:
            position = alphabet.index(letter)
            if direction == "encode":
                new_position = position + shift
            elif direction == "decode":
                new_position = position - shift
            cipher_text += alphabet[new_position]
        else:
            cipher_text += letter  # Non-alphabet characters are added unchanged
    print(f"The {direction}d text is {cipher_text}")

should_continue = True
while should_continue:

    direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n")
    text = input("Type your message:\n").lower()
    shift = int(input("Type the shift number:\n"))
    shift = shift % 26
    caesar(text, shift, direction)
    result = input("Type 'yes' if you want to go again. Otherwise type 'no'.\n").lower()

    if result == "no":
        should_continue = False
        print("Goodbye")

# def encrypt(text, shift):
#     cipher_text = ""
#     for letter in text:
#         position = alphabet.index(letter)
#         new_position = position + shift
#         cipher_text += alphabet[new_position]
#     print(f"The encoded text is {cipher_text}")

# def decrypt(text, shift):
#     cipher_text = ""
#     for letter in text:
#         position = alphabet.index(letter)
#         new_position = position - shift
#         cipher_text += alphabet[new_position]
#     print(f"The decoded text is {cipher_text}")

# if direction == "encode":
#     encrypt(text, shift)
# elif direction == "decode":
#     decrypt(text, shift)
# else:
#     print("Invalid input. Please type 'encode' or 'decode'.")

# single function
   