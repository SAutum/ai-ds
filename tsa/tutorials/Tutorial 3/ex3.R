#increase font size
set.seed(12124)
setwd("C:\\Users\\DICE\\Dropbox\\PC (2)\\Desktop\\Time Series\\Tutorial_WS23-24\\Tutorial 3")

#1. 
rho1 = 0.7/(1+0.7^2)
#all higher lags are zero

#simulate data from ma(1)
#sd refers to the white noise
ma1 <- 10 + arima.sim(n=120, list(ma = c(0.7)),sd = 1)
ts.plot(ma1); abline(h=mean(ma1), col="blue")

#keep in mind, data is random/simulated, so not perfect
par(mfrow=c(1,2))
forecast::Acf(ma1)
pacf(ma1)
par(mfrow=c(1,1))

#2
rho1 = (0.5 + 0.5*0.3)/(1+0.5^2 +0.3^2)
rho2 = (0.3)/(1+0.5^2 +0.3^2)

ma2 <- 10 + arima.sim(n=150, list(ma = c(0.5,0.3)),sd = 1)
ts.plot(ma2); abline(h=mean(ma2), col="blue")

par(mfrow=c(1,2))
forecast::Acf(ma2)
pacf(ma2)
par(mfrow=c(1,1))

#3
#load the data
quakes <- scan("quakes.dat")
quakes <- ts(quakes)
plot(quakes, type="o")
abline(h=mean(quakes), col="blue")

#acf and pacf
par(mfrow=c(1,2))
forecast::Acf(quakes)
pacf(quakes)
par(mfrow=c(1,1))

#4
fb <- read.csv("FB.csv")
fb <- ts(fb$Adj.Close)

#plot the series and ACF, PACF
ts.plot(fb)

par(mfrow=c(1,2))
forecast::Acf(fb)
pacf(fb)
par(mfrow=c(1,1))

#looks like a random walk
ts.plot(diff(fb))

#first differences a random walk produces white noise: y_t = y_(t-1) + e => FD => y_t - y_(t-1) = e
#no significant dependence structures in the autocorrelation plots
par(mfrow=c(1,2))
forecast::Acf(diff(fb,1))
pacf(diff(fb,1))