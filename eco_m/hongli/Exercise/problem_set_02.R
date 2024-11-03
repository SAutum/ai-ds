## Task 1
data = read.csv("./Data/cars.csv", sep=";")

# plot data
plot(data$age, data$price)

# a)
reg = lm(price ~ age, data = data)

coef(reg)

# b)
age_mean = mean(data$age)
age_var = var(data$age)
price_mean = mean(data$price)
price_age_cov = cov(data$age, data$price)

Beta1 = price_age_cov/age_var
Beta0 = price_mean - Beta1 * age_mean
Beta0
Beta1

# c)
Beta0 + Beta1 * 5

# Task 2
data = read.csv('./Data/ceosalary.csv')

# a)
reg = lm(salary ~ sales, data = data)

data$salary2 = data$salary * 1e-6
data$sales2 = data$sales * 1e-6

# d)
reg_log = lm(log(salary) ~ log(sales), data = data)

coef(reg_log)

# e)
coef(lm(log(salary2) ~ log(sales2), data = data))


library(rio)