data(ceosal1, package='wooldridge')

# OLS regression
lm( salary ~ roe, data=ceosal1)

# Manual regression
# b1 = cov(y)/var(x)
# b0 = E[y] - b1*E[x]
beta1_est = cov(ceosal1$salary, ceosal1$roe)/var(ceosal1$roe)
beta0_est = mean(ceosal1$salary) - beta1_est * mean(ceosal1$roe)