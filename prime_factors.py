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
    factors = []
    curr_prime = 2

    while n % curr_prime == 0:
        n /= curr_prime
        factors.append(curr_prime)

    return factors


print(prime_factors(8))
print(next_prime(1))
