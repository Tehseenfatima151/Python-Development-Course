def primechecker(number):
    if number <= 1:
        print("number is not prime")
        return
    else:
        is_prime = True
    for i in range(2, number):
        if number % i == 0:
            is_prime = False
    
    if is_prime:
        print("number is prime")
    else:
        print("number is not prime")
primechecker(1)