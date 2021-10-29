def next_prime(n):
    #Finds the next prime number after n
    #Check numbers after n until one is found with factors 1 and itself
    has_factor = True
    
    while has_factor:
        n += 1
        has_factor = False
        for i in range(2, n):
            if n % i == 0:
                has_factor = True

    return n


def prime_factors(n):
    #Divide by first prime
    #Keep dividing until division isn't an integer
    #Repeat for next primes until original number is 1
    #Returns list of factors of n (or n rounded down)
    n = int(n//1)
    factors = []
    curr_prime = 2

    while n > 1:
        while n % curr_prime == 0:
            n /= curr_prime
            factors.append(curr_prime)
        curr_prime = next_prime(curr_prime)

    return factors


def prime_factors_string(n):
    #Formats output as string
    factors = prime_factors(n)
    unique_factors = []
    for x in factors:
        if x not in unique_factors:
            unique_factors.append(x)

    string = ""
    exponent = 1
    for x in factors:
        if x in unique_factors:
            if exponent != 1:
                string += ("^" + str(exponent))
            if x != factors[0]:
                string += (" * " + str(x))
            else:
                string += str(x)
            exponent = 1
            unique_factors.remove(x)
        else:
            exponent += 1
        print(string)

    if exponent != 1:
        string += ("^" + str(exponent))

    return string


print(prime_factors(10080))
print(prime_factors_string(10080))

