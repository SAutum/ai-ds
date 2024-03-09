# set directory to the location of the data
setwd("/home/hongli/MyApps/aids/tsa/tutorials/Tutorial 3")

# simulate n = 120 sample values with the MA(1) model:
# y_t = 10 + e_t + 0.7e_{t-1}
# where e_t is a white noise process with mean 0 and variance 1
set.seed(123)
n <- 120
e <- rnorm(n, mean=0, sd=1)
y <- numeric(n)
y[1] <- 10 + e[1]
for (t in 2:n) {
  y[t] <- 10 + e[t] + 0.7*e[t-1]
}

# create a time series object
y_ts <- ts(y, start=1, frequency=1)

# plot the time series
plot(y_ts, main="MA(1) Time Series")

# plot the ACF
acf(y_ts)


# simulate n =150 sample values with the MA(2) model:
# y_t = 10 + e_t + 0.5e_{t-1} + 0.3e_{t-2}
# where e_t is a white noise process with mean 0 and variance 1
set.seed(123)
n <- 150
e <- rnorm(n, mean=0, sd=1)
y <- numeric(n)
y[1] <- 10 + e[1]
y[2] <- 10 + e[2] + 0.5*e[1]
for (t in 3:n) {
  y[t] <- 10 + e[t] + 0.5*e[t-1] + 0.3*e[t-2]
}

# create a time series object
y_ts <- ts(y, start=1, frequency=1)

# plot the time series
plot(y_ts, main="MA(2) Time Series")

# plot the ACF
acf(y_ts)

# Load teh FB.csv dataset using read.csv
fb <- read.csv("FB.csv")
# create a time series object
fb_ts <- ts(fb$Adj.Close, start=c(2012, 5), frequency=365)

# plot the time series
plot(fb_ts, main="Facebook Stock Price")

# plot the ACF
acf(fb_ts)
pacf(fb_ts)

# first differences
fb_diff <- diff(fb_ts, 1)
plot(fb_diff, main="First Differences of Facebook Stock Price")

# plot the ACF
acf(fb_diff)
# pacf(fb_diff)
