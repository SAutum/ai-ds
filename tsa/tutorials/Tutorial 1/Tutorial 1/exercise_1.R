set.seed(112233)
N = 200

cov_matrix <- matrix(c(1,0.2,0.2,1),ncol=2)

X <- MASS::mvrnorm(N,c(0,0),cov_matrix)

#Run OLS with normal errors 
e <- rnorm(N) #normal errors
Y = 2 + 0.4*X[,1] -0.8*X[,2] + e

model2 <- lm(Y ~ X[,1] + X[,2])
print(summary(model2))
plot(model2$residuals)

par(mfrow=c(2,2))
plot(model2)

#Repeated with uniform errors
e2 <- runif(N) #uniform errors
Y = 2 + 0.4*X[,1] -0.8*X[,2] + e2

model2 <- lm(Y ~ X[,1] + X[,2])
print(summary(model2))
plot(model2$residuals)

par(mfrow=c(2,2))
plot(model2)