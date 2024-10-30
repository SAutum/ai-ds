a = c(1, 2, 3, 4)
b = 7:19
print(a)
print(b)

c = rep(1, 10)
print(c)
print(b[2:5])

print(length(a))

# Task: Calculate with R
v1 = 1:6
print(length(v1))
print(sum(v1))

n = 100
print(sum((1:n)^3 + (1:n)^2)/n)

# Matrix operations
m1 = matrix(1:6, nrow=2, ncol=3, byrow=TRUE)
print(m1)

m2 = diag(8, 5)
print(m2)

m3 = t(m1)
print(m3)

# Task2: Matrix operations
m1 = matrix(c(2, 3, 1, 1), nrow=2, ncol=2, byrow=TRUE)
m2 = matrix(c(7, 2, 5, 1), nrow=2, ncol=2, byrow=TRUE)
print(m1 %*% m2)

print(7* m1)

print(det(m1))

print(solve(m1))

# Random numbers
n = 100
print(rnorm(n, 15, 1))
print(runif(n, 100, 115))

x=1:100
print(sample(x, 10, replace=FALSE))
print(sample(x, 100, replace = TRUE))

# Task3: Random numbers
n = 100
x = (1:n)/n
eps = rnorm(n, 0, 1)
beta1 = 5; beta2 = 7
y = beta1*x + beta2*x^2 + eps
print(x)
print(y)

# Plot
plot(x, y, type = "l", col="red")
lines(x, y+x, col="blue")


# Task4: Plot
n = 100
x = (-5*n:5*n)/n
g = sin(x)
plot(x, g, type="o", col="red")
lines(x,g)

n = 100
x = runif(n, 0, 1)
y = runif(n, 0, 1)
plot(x, y, type = "p", col="blue")

# Use external R-scripts

# Loop/if else
for (i in 1:100){
    check = 1
    for (j in 2:(i%/%2)){
        if (i%%j == 0){
            check = 0
            break
        }
    }
    if (check==1){
        print(i)
    }
}

# List

x = list(number = 5, text = "hallo", datapoints = c(1,2,3,4))
print(x[[2]])
print(x$number)
print(x$datapoints)

# Task5: Read
x = read.csv("sl/hongli/test.csv", sep=";", dec=",")
print(names(x))
print(x[1, ])
print(x[1:20, ])
print(x[1:20, 5])
print(x$ARZTBES)
