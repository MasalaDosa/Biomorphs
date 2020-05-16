import random

# This class represents a 'gene'
# A gene has minimum and maximum values and a number of discrete values it is allowed to take.
# e.g. a gene with a minimum value of 0, and a maximum of 10, with 6 discrete values could take the values
# 0, 2, 4, 6, 8, 10
# A gene has methods to randomise this value, and to access it.
# Additionally there are methods to increment and decrement the value (wrapping around if needed).
class Gene:
    def __init__(self, name, minimum, maximum, num_discrete_values):
        self.name = name
        if minimum >= maximum:
            raise ValueError("minimum must be less than maximum")
        if num_discrete_values <= 1:
            raise ValueError("num_discrete_values should be greater than 1.")

        self.min = minimum
        self.max = maximum
        self.delta = (maximum - minimum) / (num_discrete_values - 1)
        self.num_discrete_values = num_discrete_values
        self.underlying_value = 0

    def __str__(self):
        return '%s: minimum=%6.3f, maximum=%6.3f steps=%s (delta=%6.3f) value=%6.3f' % (self.name, self.min, self.max, self.num_discrete_values, self.delta, self.value())

    def short_str(self):
        return '%s: %6.3f' % (self.name, self.value())

    # Returns the gene's current value
    def value(self):
        return self.min + self.underlying_value * self.delta

    # Randomise the gene's current value
    def randomise(self):
        self.underlying_value = random.randint(0, self.num_discrete_values)

    # Increment the value
    def increment(self):
        if self.underlying_value < self.num_discrete_values - 1:
            self.underlying_value += 1
        else:
            self.underlying_value = 0

    # Decrement the value
    def decrement(self):
        if self.underlying_value > 0:
            self.underlying_value -= 1
        else:
            self.underlying_value = self.num_discrete_values - 1
