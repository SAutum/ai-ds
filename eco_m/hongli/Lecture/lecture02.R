# random numbers:
x <- runif(100)
y <- rnorm(100)

# average:
mean(y)

# linear regression
lm(y ~ x)

# manual linear regression
beta1_estimator <- cov(x, y)/var(x)
beta0_estimator <- mean(y) - beta1_estimator * mean(x)