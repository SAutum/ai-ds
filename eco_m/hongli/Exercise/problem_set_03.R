library("rio")

# task 1
house_prices_data = import("./Data/houseprices81NA.csv")

# a)
simple_l_reg = lm(price ~ rooms, data = house_prices_data)
coef(simple_l_reg)

# b)
multi_l_reg = lm(price ~ rooms + area, data = house_prices_data)
coef(multi_l_reg)

# c) e) f)
summary(simple_l_reg)
summary(multi_l_reg)

# d)
# here I forgot to check the missing values in dependent variable y
room_missing_idx = c(which(is.na(house_prices_data$rooms)))
area_missing_idx = c(which(is.na(house_prices_data$area)))
print(house_prices_data[room_missing_idx, ])
print(house_prices_data[area_missing_idx, ])

# g)
cleaned_data = house_prices_data[-c(room_missing_idx, area_missing_idx), ]
X <- cleaned_data[c("rooms", "area")]
# add constant column for intercept calculation
X <- cbind(1, X)
y <- cleaned_data[["price"]]

beta_hat <- solve(t(X) %*% X) %*% t(X) 
beta_hat <- beta_hat %*% y

y_hat = X %*% beta_hat

R_2 = var(y_hat)/var(y)
print(R_2)

# task 2
# log() explains the percentage of percentage
# Winston is not right!!
# 1.makes only sense to compare models based on their R2 value that
# have the same dependent variables (e.g. model 1 and 3)

# R2 = var(y_hat)/var(y), same denominator is require

# 2.by construction, the R2 cannot decrease when we add more independent
# variables (e.g. model 1 and 2)

# R2(model 2) will always >= R(model 2)
# solution -> adjusted R2
