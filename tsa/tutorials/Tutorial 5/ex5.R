library(forecast)
library(tseries)
setwd("/home/hongli/MyApps/aids/tsa/tutorials/Tutorial 5")
#load the data and transform into ts
hotel <- read.csv("hotel.csv")
hotel <- ts(hotel,start = 2001, frequency = 12)

#hotel <- window(hotel,start=2001,end=c(2018,12))

tsdisplay(hotel)
monthplot(hotel)

#seasonal diff with s=12
hotel_sadj <- diff(hotel,12)
tsdisplay(hotel_sadj)
monthplot(hotel_sadj)
#we have removed most of the seasonality

#does the time series need further regular differencing?
tseries::kpss.test(hotel_sadj,null = "L") #reject H_0 of stationarity
# aTSA::adf.test(hotel_sadj) #can NOT reject H_0 of non-stationarity
# aTSA::pp.test(hotel_sadj) #can NOT reject H_0 of non-stationarity
#both tests point toward non-stat/unit root

hotel_sadj_fd <- diff(hotel_sadj)
ts.plot(hotel_sadj_fd)
tsdisplay(hotel_sadj_fd)

tseries::kpss.test(hotel_sadj_fd,null = "L")
aTSA::pp.test(hotel_sadj_fd)

#identify lag order, first non-seasonal
#two small spikes in ACF and PACF, could be AR(2) or MA(2)
#look at seasonal spikes: 1 in ACF, one in PACF: try sMA(1) or sAR(1)

model1 <- Arima(hotel,order = c(2,1,0), seasonal = c(0,1,1))
model2 <- Arima(hotel,order = c(2,1,0), seasonal = c(1,1,0))
model3 <- Arima(hotel,order = c(0,1,2), seasonal = c(1,1,0))
model4 <- Arima(hotel,order = c(0,1,2), seasonal = c(0,1,1))

cat(model1$aicc,model2$aicc,model3$aicc,model4$aicc)
cat(model1$bic,model2$bic,model3$bic,model4$bic)

#look at residuals and test for independence
tsdisplay(model1$residuals)
Box.test(model1$residuals,lag = 24,fitdf = 3,type = "L")

#model1 has both lower AICc and BIC, choose model1
#what does auto.arima think?
#stepwise, approximation both F gives a full search of all models up to max.order = 5 (default)
model_aa <- auto.arima(hotel,seasonal = T,stepwise = F,approximation = F,max.order = 7)
print(summary(model_aa))
#pretty close: (2,1,0)(1,1,1)
