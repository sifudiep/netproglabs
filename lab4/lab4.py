def fibonacci(n):
    previousNumber = 0
    currentNumber = 1
    while (currentNumber < n):
        yield currentNumber
        previousNumber, currentNumber = currentNumber, currentNumber + previousNumber


for i in fibonacci(1000000):
    print(i)