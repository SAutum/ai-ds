library(rio)

# 1)
data = import('./data/collinear.csv')

reg1 = lm(x1 ~ x2 + x3, data = data)
summary(reg1)$r.square

reg2 = lm(x2 ~ x1 + x3, data = data)
summary(reg2)$r.squared

reg1 = lm(x3 ~ x1 + x2, data = data)
summary(reg1)$r.squared

# R2 > 0.9 => VIF > 10

# 2)
data = import('./data/rental.csv')


# a)

lin_reg = lm(log(rent) ~ log(pop) + log(avginc) + pctstu, data = data)

summary(lin_reg)

# b)

n = 128
sigma = 0.1517 # Residual standard error
sd_1 = sd(log(data$pop))
r_1 = summary(lm(log(pop) ~ log(avginc) + pctstu, data = data))$r.squared
print(sd_1)
print(r_1)
print(1/(n-1)**0.5 * sigma/sd_1 * 1/(1-r_1**2)**0.5)
