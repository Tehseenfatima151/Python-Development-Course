# Day 8 – Functions with Inputs & Caesar Cipher

## 📌 Overview
Is session mein humne **functions with inputs** ka detailed concept seekha — function parameters kaise pass hote hain, positional vs keyword arguments mein farq, aur functions ko chain kar ke complex logic kaise banate hain. Iske baad humne ye sab concepts use kar ke ek classic encryption technique — **Caesar Cipher** — implement ki.

---

## 1️⃣ Functions with Inputs (Recap + Detail)

Function mein input dene ka matlab hai usse **parameters** dena, taake function har baar different data pe kaam kar sake.

```python
def greet(name):
    print(f"Hello, {name}!")

greet("Ali")
```

### Positional Arguments
Values order ke hisaab se parameters mein assign hoti hain.

```python
def describe_pet(animal, name):
    print(f"I have a {animal} named {name}.")

describe_pet("dog", "Rex")
# Output: I have a dog named Rex.
```

### Keyword Arguments
Hum parameter ka naam likh kar bhi value pass kar sakte hain — order matter nahi karta.

```python
describe_pet(name="Rex", animal="dog")
# Output: I have a dog named Rex.
```

### Default Parameters
Agar value na di jaye to default use hoti hai.

```python
def describe_pet(animal, name="Unknown"):
    print(f"I have a {animal} named {name}.")

describe_pet("cat")
# Output: I have a cat named Unknown.
```

### Multiple Parameters with Return

```python
def calculate_bmi(weight, height):
    bmi = weight / (height ** 2)
    return round(bmi, 2)

result = calculate_bmi(70, 1.75)
print(f"Your BMI is: {result}")
```

### Functions Calling Other Functions

Ek function ke andar dusra function bhi call ho sakta hai — is se complex logic ko chote reusable parts mein tor sakte hain.

```python
def square(n):
    return n * n

def sum_of_squares(a, b):
    return square(a) + square(b)

print(sum_of_squares(3, 4))   # Output: 25  (9 + 16)
```

---

## 2️⃣ What is Caesar Cipher?

Caesar Cipher ek purani aur simple **encryption technique** hai jisme har letter ko alphabet mein aik fixed number of positions **shift** kar diya jata hai.

**Example:** Shift = 3
```
Original:  a  b  c  d  e  f  ...
Shifted:   d  e  f  g  h  i  ...
```

Agar hum "hello" ko shift 3 se encrypt karein:
```
h -> k
e -> h
l -> o
l -> o
o -> r
```
Result: `"khoor"`

Decrypt karne ke liye ulta shift karte hain (yani letters ko peeche move karte hain).

---

## 3️⃣ Building the Caesar Cipher – Step by Step

### Step 1: Alphabet List Banana

```python
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
```

### Step 2: Encryption Function

```python
def encrypt(plain_text, shift_amount):
    encrypted_text = ""

    for letter in plain_text:
        if letter in alphabet:
            position = alphabet.index(letter)
            new_position = (position + shift_amount) % 26
            encrypted_text += alphabet[new_position]
        else:
            encrypted_text += letter   # spaces, punctuation waisay hi rahenge

    return encrypted_text
```

**Explanation:**
- Har letter ka current `position` alphabet list mein `.index()` se nikalte hain
- `shift_amount` add kar ke `new_position` nikalte hain
- `% 26` use karte hain taake agar position 26 se aage nikal jaye to wapis "z" ke baad "a" pe loop ho jaye (wraparound)
- Agar character alphabet mein nahi hai (jaise space `" "` ya punctuation), usse waisay hi add kar dete hain

### Step 3: Decryption Function

Decryption bilkul encryption jaisa hai, bas shift **minus (-)** karte hain instead of plus.

```python
def decrypt(encrypted_text, shift_amount):
    decrypted_text = ""

    for letter in encrypted_text:
        if letter in alphabet:
            position = alphabet.index(letter)
            new_position = (position - shift_amount) % 26
            decrypted_text += alphabet[new_position]
        else:
            decrypted_text += letter

    return decrypted_text
```

### Step 4: Combining into One Reusable Function

Ek hi function banaya ja sakta hai jo `direction` parameter se decide kare ke encrypt karna hai ya decrypt.

```python
def caesar(start_text, shift_amount, cipher_direction):
    output_text = ""

    if cipher_direction == "decode":
        shift_amount *= -1

    for letter in start_text:
        if letter in alphabet:
            position = alphabet.index(letter)
            new_position = (position + shift_amount) % 26
            output_text += alphabet[new_position]
        else:
            output_text += letter

    return output_text
```

**Explanation:**
- Agar direction `"decode"` ho, to shift ko negative kar dete hain (`shift_amount *= -1`)
- Isse encrypt aur decrypt dono ka logic same code mein handle ho jata hai — code repeat nahi karna parta (DRY principle)

---

## 4️⃣ Full Program with User Input

```python
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def caesar(start_text, shift_amount, cipher_direction):
    output_text = ""

    if cipher_direction == "decode":
        shift_amount *= -1

    for letter in start_text:
        if letter in alphabet:
            position = alphabet.index(letter)
            new_position = (position + shift_amount) % 26
            output_text += alphabet[new_position]
        else:
            output_text += letter

    return output_text


should_continue = True

while should_continue:
    direction = input("Type 'encode' to encrypt, 'decode' to decrypt:\n").lower()
    text = input("Type your message:\n").lower()
    shift = int(input("Type the shift number:\n"))

    result = caesar(start_text=text, shift_amount=shift, cipher_direction=direction)
    print(f"Here is the result: {result}")

    restart = input("Type 'yes' if you want to go again. Otherwise type 'no':\n").lower()
    if restart == "no":
        should_continue = False
        print("Goodbye!")
```

---

## 5️⃣ Example Run

```
Type 'encode' to encrypt, 'decode' to decrypt: encode
Type your message: hello world
Type the shift number: 3
Here is the result: khoor zruog
```

```
Type 'encode' to encrypt, 'decode' to decrypt: decode
Type your message: khoor zruog
Type the shift number: 3
Here is the result: hello world
```

---

## ✅ Key Takeaways
- Functions ko parameters ke through data diya jata hai — positional, keyword, ya default values ke through
- Functions ek dusre ko call kar sakte hain, jisse code chota aur organized rehta hai
- Caesar Cipher letters ko fixed shift ke sath alphabet mein move karta hai
- `.index()` se letter ki position nikalna aur `% 26` se wraparound handle karna cipher ka core logic hai
- Encode aur decode ka logic same function mein combine kiya ja sakta hai sirf shift ka sign (+/-) change kar ke
- `while` loop se program ko baar baar chalaya ja sakta hai jab tak user khud exit na kare

---

## 🔗 Practice Task
- Caesar Cipher ko modify karo taake uppercase letters bhi handle ho sakein
- Ek "brute force" function banao jo shift number pata na hone pe 1 se 25 tak har shift try kar ke result dikhaye
- User se validation lo taake agar shift 26 se zyada ho to error message aaye
