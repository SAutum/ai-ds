library(vars)
library(urca)
library(dplyr)

## Preliminary analysis
# (a) Load the data stroed in the file
metals <- read.csv("tsa/hongli/metals.csv")

# (b) Create he logarithm of the data
metals$log_rmp <- log(metals$rmp)
metals$log_ipac <- log(metals$ipac)
metals$log_ipcn <- log(metals$ipcn)
metals$log_oil <- log(metals$oil)
metals$log_euro <- log(metals$euro)

# (c) Define the series as time series objects and plot them
ts_log_rmp <- ts(metals$log_rmp, start=1995, frequency=4)
ts_log_ipac <- ts(metals$log_ipac, start=1995, frequency=4)
ts_log_ipcn <- ts(metals$log_ipcn, start=1995, frequency=4)
ts_log_oil <- ts(metals$log_oil, start=1995, frequency=4)
ts_log_euro <- ts(metals$log_euro, start=1995, frequency=4)

png("ts_log_rmp.png")
plot(ts_log_rmp, main="Log of RMP")
dev.off()
png("ts_log_ipac.png")
plot(ts_log_ipac, main="Log of IPAC")
dev.off()
png("ts_log_ipcn.png")
plot(ts_log_ipcn, main="Log of IPCN")
dev.off()
png("ts_log_oil.png")
plot(ts_log_oil, main="Log of Oil")
dev.off()
png("ts_log_euro.png")
plot(ts_log_euro, main="Log of Euro")
dev.off()

# Decompose the time series
    # rmp shows a clear trend
plot(decompose(ts_log_rmp))
plot(acf(ts_log_rmp))
plot(pacf(ts_log_rmp))
    # ipac shows a clear trend
plot(decompose(ts_log_ipac))
plot(acf(ts_log_ipac))
plot(pacf(ts_log_ipac))
    # ipcn has a clear deterministic trend with no clear seasonality
plot(decompose(ts_log_ipcn))
plot(acf(ts_log_ipcn))
plot(pacf(ts_log_ipcn))
    # oil shows a clear trend
plot(decompose(ts_log_oil))
plot(acf(ts_log_oil))
plot(pacf(ts_log_oil))
    # euro shows a clear trend
plot(decompose(ts_log_euro))
plot(acf(ts_log_euro))
plot(pacf(ts_log_euro))
# There are no significant spikes in the acf and pacf plots of the time series.
# The seasonality in the time series is trivial.

## Stationarity
# (a) Test for stationarity at 5% significance level
# Augmented Dickey-Fuller test
adf_rmp <- aTSA::adf.test(ts_log_rmp) # cannot reject H_0 of non-stationarity
adf_ipac <- aTSA::adf.test(ts_log_ipac) # cannot reject H_0 of non-stationarity
adf_ipcn <- aTSA::adf.test(ts_log_ipcn) # cannot reject H_0 of non-stationarity
adf_oil <- aTSA::adf.test(ts_log_oil) # cannot reject H_0 of non-stationarity
adf_euro <- aTSA::adf.test(ts_log_euro) # cannot reject H_0 of non-stationarity
# None of the time series is stationary at 5% significance level.

# Test for trend stationarity at 5% significance level
# KPSS test
tseries::kpss.test(ts_log_rmp, null="T") # reject H_0 of trend stationarity
tseries::kpss.test(ts_log_ipac, null="T") # reject H_0 of trend stationarity
tseries::kpss.test(ts_log_ipcn, null="T") # reject H_0 of trend stationarity
tseries::kpss.test(ts_log_oil, null="T") # accept H_0 of trend stationarity
tseries::kpss.test(ts_log_euro, null="T") # reject H_0 of trend stationarity

# (b) Reasons: The ADF test can be used to test the stationarity in general with
# 3 types, while the kpss test can be used to test the trend stationarity and
# is a method completely different from the ADF test.

# (c) Create the first differences of the time series
ts_log_rmp_diff <- diff(ts_log_rmp)
ts_log_ipac_diff <- diff(ts_log_ipac)
ts_log_ipcn_diff <- diff(ts_log_ipcn)
ts_log_oil_diff <- diff(ts_log_oil)
ts_log_euro_diff <- diff(ts_log_euro)

# (d) Run the appropriate tests to determine the order of integration
# rmp
aTSA::adf.test(ts_log_rmp_diff) # reject H_0 of non-stationarity
aTSA::pp.test(ts_log_rmp_diff) # reject H_0 of non-stationarity
# rmp has an order of integration of 1

# ipac
aTSA::adf.test(ts_log_ipac_diff) # reject H_0 of non-stationarity
aTSA::pp.test(ts_log_ipac_diff) # reject H_0 of non-stationarity
# ipac has an order of integration of 1

# ipcn
aTSA::adf.test(ts_log_ipcn_diff) # cannot reject H_0 of non-stationarity
aTSA::pp.test(ts_log_ipcn_diff) # cannot reject H_0 of non-stationarity
 # further differencing is needed
ts_log_ipcn_diff2 <- diff(ts_log_ipcn_diff)
aTSA::adf.test(ts_log_ipcn_diff2) # reject H_0 of non-stationarity
aTSA::pp.test(ts_log_ipcn_diff2) # reject H_0 of non-stationarity
# ipcn has an order of integration of 2

# oil
aTSA::adf.test(ts_log_oil_diff) # reject H_0 of non-stationarity
aTSA::pp.test(ts_log_oil_diff) # reject H_0 of non-stationarity
# oil has an order of integration of 1

# euro
aTSA::adf.test(ts_log_euro_diff) # reject H_0 of non-stationarity
aTSA::pp.test(ts_log_euro_diff) # reject H_0 of non-stationarity
# euro has an order of integration of 1

## Cointegration & ECM
# Here we consider the linear regression of log(rmp) on an I(1) variables and
# a time trend.
# (a) The order of intergration of log(rmp) of the resulting residual
# is tested using the ADF and PP tests.
residual_rmp <- lm(ts_log_rmp ~ ts_log_ipac + ts_log_oil + ts_log_euro + time(ts_log_rmp))
residual_rmp <- residuals(residual_rmp)
aTSA::adf.test(residual_rmp) # cannot reject H_0 of non-stationarity
aTSA::pp.test(residual_rmp) # cannot reject H_0 of non-stationarity
residual_rmp_diff <- diff(residual_rmp)
aTSA::adf.test(residual_rmp_diff) # reject H_0 of non-stationarity
aTSA::pp.test(residual_rmp_diff) # reject H_0 of non-stationarity
# The order of integration of the residual of the linear regression of log(rmp)
# on an I(1) variables and a time trend is 1.

# The regression is spurious
