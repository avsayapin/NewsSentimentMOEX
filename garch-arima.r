require(rugarch)

moex_data <- read.csv('returns.csv',sep = ",")
news_data <- read.csv('news_data.csv',sep=',')
test_data <- read.csv('test_data.csv',sep=",", header = TRUE)

# MEAN AND VARIANCE models without news data
spec <- ugarchspec(variance.model = list(model = "sGARCH", garchOrder = c(1, 1), 
submodel = 'GARCH'), 
mean.model = list(armaOrder = c(1, 1)), distribution.model = "norm")

fit <- ugarchfit(spec=spec,data=test_data['log_ret'],solver.control=list(trace=0))

print(fit)

report = ugarchroll(spec,
    data = test_data['log_ret'],
    n.start=374,
    n.ahead = 1, 
    refit.every = 1, 
    refit.window = "moving"
)
s = as.data.frame(report)
write.csv(s,'garch.csv')
print("GARCH Done")

# Models with news indices

spec <- ugarchspec(variance.model = list(model = "sGARCH", garchOrder = c(1, 1), 
submodel = 'GARCH'), 
mean.model = list(armaOrder = c(1, 1),external.regressors = matrix(test_data$prob_1)), distribution.model = "norm")


garchx.fit <- ugarchfit(spec=spec,data=test_data['log_ret'],solver.control=list(trace=0))

print(garchx.fit)

report = ugarchroll(spec,
    data = test_data,
    n.start=374,
    n.ahead = 1, 
    refit.every = 1, 
    refit.window = "moving"
)
s = as.data.frame(report)
write.csv(s,'garchx.csv')
print("GARCHX Done")
