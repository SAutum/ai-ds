# set directory to the location of the data
setwd("/home/hongli/MyApps/aids/tsa/tutorials/Tutorial 4")

# load the data copper_prices.csv
copper <- read.csv("copper_prices.csv")

# create the time series object
ts_copper_prices <- ts(copper_prices$price, start=1960, frequency=12)

# plot the time series
ts.plot(ts_copper_prices)

# box-cox transformation
ts_copper_prices <- log(ts_copper_prices)
ts.plot(ts_copper_prices)

# arima model with first difference
ts_copper_prices_diff <- diff(ts_copper_prices, 1)
ts.plot(ts_copper_prices_diff)

# check for seasonality
monthplot(ts_copper_prices)

# acf and pacf plots
par(mfrow=c(1,2))
forecast::Acf(ts_copper_prices_diff)
forecast::Pacf(ts_copper_prices_diff)

# estimate the preferred model
model1 <- forecast::Arima(ts_copper_prices, order=c(0,1,1))
model2 <- forecast::Arima(ts_copper_prices, order=c(2,0,0))
model3 <- forecast::Arima(ts_copper_prices, order=c(2,0,1))

# coefficient testing
lmtest::coeftest(model1)
t = 0.3756/0.0385
pval = 2*(1-pt(t, length(ts_copper_prices)-3))
cat(model1$coef,pval)

# Ljung-Box test of residuals
Box.test(model1$residuals, lag=12, type="Ljung-Box", fitdf=2)

# automated model
automated_model <- forecast::auto.arima(ts_copper_prices)
print(summary(automated_model))
par(mfrow=c(1,1))
plot(automated_model$residuals)
