# set directory to the location of the data
setwd("/home/hongli/MyApps/aids/tsa/tutorials/Tutorial 3")

# Load the quakes.dat dataset using scan
quakes <- scan("quakes.dat")
print(quakes)

# creat a timeseirs plot and add a mean line
quakes_ts <- ts(quakes, start=1900)
plot.ts(quakes_ts, type="o")
abline(h=mean(quakes_ts), col="blue")

# ACF function
forecast::Acf(quakes_ts)

#creat a lag-1plot using base R or the astsa package
lag.plot(quakes_ts, lags=1, do.lines=FALSE, cex=1.1, diag=TRUE)
astsa::lag1.plot(quakes_ts, 1)

#create a linear regression model between lag-1 and quake
quakes_df <- cbind(quakes_ts, lag(quakes_ts, -1))
ar1model <- lm(quakes_df[,1] ~ quakes_df[,2])
print(summary(ar1model))

print(coefficients(ar1model))

# PACF function
forecast::Pacf(quakes_ts)
# forecast::Acf(quakes_ts)

# Load teh FB.csv dataset using read.csv
fb <- read.csv("FB.csv")
