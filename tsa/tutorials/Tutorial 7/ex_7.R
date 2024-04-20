setwd("/home/hongli/MyApps/aids/tsa/tutorials/Tutorial 7")

library(vars)
library(urca)

#load the data and plot the yield curves and the spread
yield_rates <- read.csv("yields.csv")
yield_rates$spread <- yield_rates$y10 - yield_rates$m3
yield_rates <- ts(yield_rates,start=c(1962,1),frequency = 4)
print(summary(yield_rates))
zoo::autoplot.zoo(yield_rates,facets = NULL)

# engle-granger procedure
# y10 and m3 are cleary non-stationary, but we can test (Normal critical values)
aTSA::adf.test(yield_rates[,"y10"])
aTSA::adf.test(yield_rates[,"m3"])

# theory suggests that u = y10 - m3, i.e. beta_hat = 1, but we can also estimate their relationship
coint_eq <- lm(y10 ~ m3, data = yield_rates)
summary(coint_eq)

# test the residuals for stationarity (-> cointegration)
VARselect(coint_eq$residuals, lag.max = 5, type="const")
aTSA::adf.test(coint_eq$residuals)
# with N = 1, T=204 for 5%: −2.86154 - −2.8903/204 −4.234/(204^2) = -2.88
# -2.88 > -3.48 -> reject H0 of unit root: cointegration

test<-ur.df(coint_eq$residuals, type = c("drift"), lags = 2)
summary(test)

#theory + test suggests cointegration at <1% level, with beta_hat = 0.81
# -> estimate ECM (VAR in differences + residuals(t-1) from cointegration equation)
# transform residuals into time series
u_spread <- ts(coint_eq$residuals,start=c(1962,1), frequency = 4)
ts.plot(u_spread)
u_spread_lagged <- head(stats::lag(u_spread,-1),-1) #lag and remove last element

#select lag order in levels
VARselect(yield_rates[,c("y10","m3")])
VARselect(diff(yield_rates[,c("y10","m3")]), exogen = cbind(u_spread_lagged = c(u_spread_lagged)))

# ECM (add lagged residuals as exogenous variable), lag order can be adjusted based on residual plots
# We choose p=3 since higher lag order requires too many parameters. captured most correlation before lag=7 anyway
#and we have quarterly data
var1 <- VAR(diff(yield_rates[,c("y10","m3")]), p = 3,
            exogen = cbind(u_spread_lagged = c(u_spread_lagged)),
            type = "const")
summary(var1)

#alpha_y10 = ~ -0.088
par(mfcol=c(2,1))
plot(irf(var1,ortho = T,impulse = "y10"))

VARselect(yield_rates[,c("y10","m3")])
vec_jo <- ca.jo(yield_rates[,c("y10","m3")],K = 4,
                ecdet = "const",type="trace")
summary(vec_jo) #r = 0 can be rejected at 5%-level (28.19 > 19.96)
#johansen test finds that r=1 (cointegration)
  #Cointegration relationship (beta) + loading matrix (alpha=speed)

#transform ca.jo into VAR object (in levels)
var_ca <- vec2var(vec_jo, r=1)
var_ca
plot(irf(var_ca, ortho = F,impulse = "y10",runs = 500)) #IRFs
