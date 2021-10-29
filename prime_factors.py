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
