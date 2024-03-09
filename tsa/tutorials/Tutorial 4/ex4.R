##increase font size
setwd("C:\\Users\\DICE\\Dropbox\\PC (2)\\Desktop\\Time Series\\Tutorial_WS23-24\\Tutorial 4")
copper <- read.csv("copper_prices.csv")
copper_price <- ts(copper$price,start=1960,frequency = 12)

ts.plot(copper_price)

copper_price <- log(copper_price)
ts.plot(copper_price)
copper_price_diff <- diff(copper_price); ts.plot(copper_price_diff)

#Check for seasonality.
monthplot(copper_price)

#Check the ACF and PACF plots
par(mfrow=c(1,2))
forecast::Acf(copper_price_diff)
forecast::Pacf(copper_price_diff)
par(mfrow=c(1,2))

#estimate our preferred model
model1 <- forecast::Arima(copper_price,order = c(0,1,1))
print(summary(model1))
model2 <- forecast::Arima(copper_price,order = c(2,0,0))
print(summary(model2))
model3 <- forecast::Arima(copper_price,order = c(2,0,1))
print(summary(model3))


#coefficient testing
lmtest::coeftest(model1)

t = 0.3756/0.0385
pval = 2*(1-pt(t, length(copper_price)-3))
cat(model1$coef,pval)

#check residuals
forecast::Acf(model1$residuals)

#Ljung-Box test of residuals
Box.test(model1$residuals,lag=12,type="Ljung-Box",fitdf = 2)

automated_model <- forecast::auto.arima(copper_price)
print(summary(automated_model))

setwd("C:\\Users\\DICE\\Dropbox\\PC (2)\\Desktop\\Time Series\\Tutorial_WS23-24\\Tutorial 2")
#Bonus: Earthquake data
quakes = scan("quakes.dat")
quakes = ts(quakes)

par(mfrow=c(1,2))
forecast::Acf(quakes)
forecast::Pacf(quakes)
par(mfrow=c(1,1))

model1 <- forecast::Arima(quakes, order = c(1,0,0))
model2 <- forecast::auto.arima(quakes)
print(summary(model2))
model3 <- forecast::Arima(quakes, order = c(1,0,1))
print(summary(model3))

lmtest::coeftest(model2)

cat("model1 AICc:",model1$aicc,"model2 AICc:",model2$aicc)