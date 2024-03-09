setwd("C:\\Users\\DICE\\Dropbox\\PC (2)\\Desktop\\Time Series\\Tutorial_WS23-24\\Tutorial 2")

#load the dataset
quake <- scan("quakes.dat")

#transform into time series object
quake <- ts(quake, start = 1900)

plot.ts(quake,type="o")
abline(h=mean(quake), col="blue")

#acf function
forecast::Acf(quake)

#create a lag-1-plot using base R or the astsa package
lag.plot(quake, lags = 1, do.lines = F, cex = 1.1, diag = T)
astsa::lag1.plot(quake, 1)

#create a data.frame with quake, lagged quake
quakes_df <- cbind(quake,lag(quake,-1))

#estimate a linear model with OLS
ar1model <- lm(quakes_df[,1] ~ quakes_df[,2])
print(summary(ar1model))

 #print first autocorrelation coefficient w/o a graph
forecast::Acf(quake,plot = F)["1"]
forecast::Acf(quake,plot = F)["2"]

#in AR(1), impulse response function/dynamic multiplier for lag s = phi^s
coef(ar1model)[2]^3

#plot residuals
plot(ar1model$residuals)
par(mfrow=c(2,2))
plot(ar1model,cex=1.5)

par(mfrow=c(1,1))

forecast::Acf(ar1model$residuals)