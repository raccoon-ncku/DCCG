import timeit

regular_time = timeit.timeit(
    stmt="for i in range(1000): is_prime(i)",
    setup="from prime_numbers import is_prime",
    number=100
)

optimised_time = timeit.timeit(
    stmt="for i in range(1000): is_prime_optimized(i)",
    setup="from prime_numbers import is_prime_optimized",
    number=100
)

print("Regular Time: ", regular_time)
print("Optimised Time: ", optimised_time)
print("Optimised is faster than regular by: {} times.".format(round(regular_time/optimised_time, 2)))