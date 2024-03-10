# set directory to the location of the data
setwd("/home/hongli/MyApps/aids/tsa/tutorials/Tutorial 5")

# Load the hotel.csv dataset
hotel <- read.csv("hotel.csv")
hotel_price <- ts(hotel$x,start=2001,frequency = 12)

# Plot the time series
ts.plot(hotel_price)
# There is a clear trend and seasonality in the data.
# The seasonality is already very clear, but we can still check for it.
monthplot(hotel_price)

# Check the ACF and PACF plots
par(mfrow=c(1,2))
forecast::Acf(hotel_price)
forecast::Pacf(hotel_price)
# The ACF and PACF plots show that the data is not stationary

# Take the first difference of the data
hotel_price_diff <- diff(hotel_price);
ts.plot(hotel_price_diff)

# Use arima with seasonal differencing
model1 <- forecast::Arima(hotel_price,order = c(0,1,1), seasonal = list(order = c(0,1,1), period = 12))
print(summary(model1))

# Plot the residuals
ts.plot(model1$residuals)
# forecast::Acf(model1$residuals)

# adf
aTSA::adf.test(hotel_price)
# kpss
tseries::kpss.test(hotel_price)
