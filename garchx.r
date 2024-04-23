require(rugarch)

moex_data <- read.csv('returns.csv',sep = ",")
news_data <- read.csv('news_data.csv',sep=',')
test_data <- read.csv('test_data.csv',sep=",")


# MEAN AND VARIANCE models without news data
spec <- ugarchspec(
mean.model = list(armaOrder = c(1, 1),include.mean = FALSE))

garch.res <- ugarchfit(spec=spec,data=moex_data['return'],solver.control=list(trace=0))

print(garch.res)

# MEAN AND VARIANCE models without news data
spec <- ugarchspec(variance.model = list(model = "sGARCH", garchOrder = c(1, 1), 
submodel = 'GARCH', variance.targeting = TRUE), 
mean.model = list(armaOrder = c(1, 1)))

garch.res <- ugarchfit(spec=spec,data=test_data['return'],solver.control=list(trace=0))

print(garch.res)

# Models with news indices

spec <- ugarchspec(variance.model = list(model = "sGARCH", garchOrder = c(1, 1), 
submodel = 'GARCH', external.regressors = matrix(test_data$prob_0), variance.targeting = TRUE), 
mean.model = list(armaOrder = c(1, 1), external.regressors = matrix(test_data$prob_0)))


garchx.res <- ugarchfit(spec=spec,data=test_data['return'],solver.control=list(trace=0))

print(garchx.res)