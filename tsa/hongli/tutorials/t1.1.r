## Exercise 1

# Generate 200 observations from a bivariate normal distribution with mean 0 and
# covariance matrix (1, 0.2; 0.2, 1).

set.seed(123)
n <- 200
mu <- c(0, 0)
sigma <- matrix(c(1, 0.2, 0.2, 1), nrow = 2, ncol = 2)
x <- MASS::mvrnorm(n, mu, sigma)

# Generate a vector of standard normally distributed random errors of length 200
e <- rnorm(n)

# Create the Y variable Y = beta0 + beta1*X1 + beta2*X2 + e
# where beta0 = 2, beta1 = 0.4, and beta2 = -0.8
y <- 2 + 0.4*x[,1] - 0.8*x[,2] + e

# Fit a linear regression model to the data with OLS
fit <- lm(y ~ x)

# diagnostic plots
png("residuals.png")
par(mfrow=c(2,2))
plot(fit)
dev.off()

# print the summary of the model
print(summary(fit))
