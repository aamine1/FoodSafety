#install.packages('caTools')
#install.packages('ROCR')

library(caTools)
library(ROCR)

source('~/loglikelihood_inspection.R')

#define auxiliary function

Scaled_BetaPDF <- function(y, a, b, p, q){
  return ((y-p)^(a-1) * (q - y)^(b-1)) / ((q - p)^(a+b-1) * beta(a,b))
}

#Load file

raw_features = read.csv('~/features.csv',stringsAsFactors = F)

#adding country features

features = subset(raw_features, raw_features$specific.country!="other")
features$Thailand = ifelse(features$specific.country == "Thailand",1,0)
features$Indonesia = ifelse(features$specific.country == "Indonesia",1,0)
features$India = ifelse(features$specific.country == "India",1,0)
features$Vietnam = ifelse(features$specific.country == "Vietnam",1,0)
features$China = ifelse(features$specific.country == "China",1,0)
features$Malaysia = ifelse(features$specific.country == "Malaysia",1,0)
features$Bangladesh = ifelse(features$specific.country == "Bangladesh",1,0)

#Input features

#features = read.csv('~/features.csv')

input_X = readline('Enter the indices of the feature columns, separated by comma: ') #4,6,7,12,13,15,16,21,22,23,24,25,26,27
input_S = readline('Enter the index of the inspection status column: ')#18
input_Y = readline('Enter the index of the inspection outcome column: ')#19
input_burnin = readline('Enter the burnin paramater (number of pre-iterations in MCMC loop): ')
input_nsamples = readline('Enter the nsamples paramater (number of iterations in MCMC loop): ')

input_X = eval(parse(text=paste('list(',input_X,')')))

X=features[,as.numeric(input_X)]
ones=rep(1,nrow(X))
X=cbind(ones,X)
S=ifelse(features[,as.numeric(input_S)]>0,1,0)
Y=ifelse(features[,as.numeric(input_Y)]>0,1,0)

ind=c()
for (row in 1:nrow(X)){
  for (col in 1:ncol(X)){
    if (X[row,col]=="NaN"){
      ind = c(ind,row)
    }
  }
}
if (length(ind)>0){
  X=X[-ind,]
  S=S[-ind]
  Y=Y[-ind]
}

#model paramters

nsamples = as.numeric(input_nsamples)
burnin = as.numeric(input_burnin)
a = 1; b = 1 #hyperprior of beta distribution for sigma (if a=b=1, uniform distribution)
c = 1; d = 1 #hyperprior of scaled beta distribution for rho (if c=d=1, uniform distribution)
mu = 0; sigma = 100  #hyperpriors of normal prior for all of the beta's and gamma's
hyperpriors = c(a,b,c,d,mu,sigma)

nfeatures = ncol(X)
ndata = nrow(X)
n = nsamples + burnin
Beta_old = rnorm(nfeatures,0,1)
Gamma_old = rnorm(nfeatures,0,1)
rho_old = runif(1,-1,1)
sigma_old = runif(1,0,c)
Samples = matrix(0, nrow = n , ncol = 2*nfeatures+2) #initialize samples array
Samples[1,] = c(sigma_old,rho_old,Beta_old,Gamma_old)  #input the first sample
params_old = Samples[1,]

step_beta = 0.1  #st. dev. for beta proposals
step_gamma = 0.1 #st. dev. for gamma proposals
step_rho = 0.1   #st. dev for rho proposals
step_sigma = 0.1

X_S = X[S>0,]
S_S = S[S>0]
Y_S = Y[S>0]

# in sample mcmc loop

print ("In Sample Analysis")

for (i in 2:n){
  sigma_old = params_old[1]
  Gamma_old = params_old[(nfeatures+3):length(params_old)]
  # sample sigma
  sigma_new = sigma_old+rnorm(1,0,1)*step_sigma  #proposal
  l_old = loglikelihood_inspection(X,S,Y,Beta_old,Gamma_old,sigma_old,hyperpriors[1],rho_old)[1]
  l_new = loglikelihood_inspection(X,S,Y,Beta_old,Gamma_old,sigma_new,hyperpriors[1],rho_old)[1]
  ll_old = l_old+log(dbeta(sigma_old/hyperpriors[1],hyperpriors[1],hyperpriors[2]))
  ll_new = l_new+log(dbeta(sigma_new/hyperpriors[1],hyperpriors[1],hyperpriors[2]))
  u = log(runif(1,0,1))
  w = ll_new-ll_old
  if (w>u | is.na(w)){
    sigma_old = sigma_new
    params_old[1]= sigma_new
  }
  
  for (f in 1:nfeatures){
  # sample gamma_f
  Gamma_new = Gamma_old
  Gamma_new[f] = Gamma_old[f]+rnorm(1,0,1)*step_gamma
  l_old = loglikelihood_inspection(X,S,Y,Beta_old,Gamma_old,sigma_old,hyperpriors[1],rho_old)[1]
  l_new = loglikelihood_inspection(X,S,Y,Beta_old,Gamma_new,sigma_old,hyperpriors[1],rho_old)[1]
  ll_old = l_old -(Gamma_old[f]-hyperpriors[5])^2/2/hyperpriors[6]^2
  ll_new = l_new -(Gamma_new[f]-hyperpriors[5])^2/2/hyperpriors[6]^2
  u = log(runif(1,0,1))
  w = ll_new-ll_old
  if (w>u | is.na(w)){
    Gamma_old[f] = Gamma_new[f]
    params_old[(nfeatures+f+2)]= Gamma_new[f]
  }
  Samples[i,1] = params_old[1]
  Samples[i,(nfeatures+3):ncol(Samples)] = params_old[(nfeatures+3):length(params_old)]
  }
  if (i %% 1000==0){
    print (paste("Iteration",as.character(i)))
  }
}

for (i in 2:n){
  rho_old = params_old[2]
  Beta_old = params_old[3:(nfeatures+2)]
  # sample rho
  rho_new = rho_old+rnorm(1,0,1)*step_rho  #proposal
  l_old = loglikelihood_inspection(X_S,S_S,Y_S,Beta_old,Gamma_old,sigma_old,hyperpriors[1],rho_old)[2]
  l_new = loglikelihood_inspection(X_S,S_S,Y_S,Beta_old,Gamma_old,sigma_old,hyperpriors[1],rho_new)[2]
  ll_old = l_old+log(Scaled_BetaPDF(rho_old,hyperpriors[3],hyperpriors[4],-1,1)) 
  ll_new = l_new+log(Scaled_BetaPDF(rho_new,hyperpriors[3],hyperpriors[4],-1,1))
  u = log(runif(1,0,1))
  w = ll_new-ll_old
  if (w>u | is.na(w)){
    rho_old = rho_new
    params_old[2]= rho_new
  }
  
  for (f in 1:nfeatures){
    # sample beta_f
    Beta_new = Beta_old
    Beta_new[f] = Beta_old[f]+rnorm(1,0,1)*step_beta
    l_old = loglikelihood_inspection(X_S,S_S,Y_S,Beta_old,Gamma_old,sigma_old,hyperpriors[1],rho_old)[2]
    l_new = loglikelihood_inspection(X_S,S_S,Y_S,Beta_new,Gamma_old,sigma_old,hyperpriors[1],rho_old)[2]
    ll_old = l_old -(Beta_old[f]-hyperpriors[5])^2/2/hyperpriors[6]^2
    ll_new = l_new -(Beta_new[f]-hyperpriors[5])^2/2/hyperpriors[6]^2
    u = log(runif(1,0,1))
    w = ll_new-ll_old
    if (w>u | is.na(w)){
      Beta_old[f] = Beta_new[f]
      params_old[(f+2)]= Beta_new[f]
    }
    Samples[i,2] = params_old[2]
    Samples[i,3:(nfeatures+2)] = params_old[3:(nfeatures+2)]
  }
  if (i %% 1000==0){
    print (paste("Iteration",as.character(burnin+nsamples+i)))
  }
}

# in-sample significant features

q_significant_features=data.frame(inspection_model=c("significant feature","sign"))
p_significant_features=data.frame(inspection_model=c("significant feature","sign"))
for (i in 2:length(X)){
  if (quantile(Samples[burnin+1:ncol(Samples),(2+i)],0.025)*quantile(Samples[burnin+1:ncol(Samples),(2+i)],0.975)>0){
    p_significant_features=cbind(p_significant_features,data.frame(feature=c(colnames(X)[i],sign(quantile(Samples[,(2+i)],0.05)))))
  }
  if (quantile(Samples[burnin+1:ncol(Samples),(2+nfeatures+i)],0.025)*quantile(Samples[burnin+1:ncol(Samples),(2+nfeatures+i)],0.975)>0){
    q_significant_features=cbind(q_significant_features,data.frame(feature=c(colnames(X)[i],sign(quantile(Samples[,(2+nfeatures+i)],0.05)))))
  }
}

# Out of sample analysis

Mat = data.frame(X,S,Y)
set.seed(123)
split = sample.split(S,0.5)
train = subset(Mat,split=TRUE)
test = subset(Mat,split=FALSE)
X = train[,1:(ncol(Mat)-2)]
S = train[,(ncol(Mat)-1)]
Y = train[,ncol(Mat)]
nfeatures = ncol(X)
ndata = nrow(X)

Beta_old = rnorm(nfeatures,0,1)
Gamma_old = rnorm(nfeatures,0,1)
rho_old = runif(1,-1,1)
sigma_old = runif(1,0,c)
Samples = matrix(0, nrow = n , ncol = 2*nfeatures+2) #initialize samples array
Samples[1,] = c(sigma_old,rho_old,Beta_old,Gamma_old)  #input the first sample
params_old = Samples[1,]

X_S = X[S>0,]
S_S = S[S>0]
Y_S = Y[S>0]

print ("Out Of Sample Analysis")

for (i in 2:n){
  sigma_old = params_old[1]
  Gamma_old = params_old[(nfeatures+3):length(params_old)]
  # sample sigma
  sigma_new = sigma_old+rnorm(1,0,1)*step_sigma  #proposal
  l_old = loglikelihood_inspection(X,S,Y,Beta_old,Gamma_old,sigma_old,hyperpriors[1],rho_old)[1]
  l_new = loglikelihood_inspection(X,S,Y,Beta_old,Gamma_old,sigma_new,hyperpriors[1],rho_old)[1]
  ll_old = l_old+log(dbeta(sigma_old/hyperpriors[1],hyperpriors[1],hyperpriors[2]))
  ll_new = l_new+log(dbeta(sigma_new/hyperpriors[1],hyperpriors[1],hyperpriors[2]))
  u = log(runif(1,0,1))
  w = ll_new-ll_old
  if (w>u | is.na(w)){
    sigma_old = sigma_new
    params_old[1]= sigma_new
  }
  
  for (f in 1:nfeatures){
    # sample gamma_f
    Gamma_new = Gamma_old
    Gamma_new[f] = Gamma_old[f]+rnorm(1,0,1)*step_gamma
    l_old = loglikelihood_inspection(X,S,Y,Beta_old,Gamma_old,sigma_old,hyperpriors[1],rho_old)[1]
    l_new = loglikelihood_inspection(X,S,Y,Beta_old,Gamma_new,sigma_old,hyperpriors[1],rho_old)[1]
    ll_old = l_old -(Gamma_old[f]-hyperpriors[5])^2/2/hyperpriors[6]^2
    ll_new = l_new -(Gamma_new[f]-hyperpriors[5])^2/2/hyperpriors[6]^2
    u = log(runif(1,0,1))
    w = ll_new-ll_old
    if (w>u | is.na(w)){
      Gamma_old[f] = Gamma_new[f]
      params_old[(nfeatures+f+2)]= Gamma_new[f]
    }
    Samples[i,1] = params_old[1]
    Samples[i,(nfeatures+3):ncol(Samples)] = params_old[(nfeatures+3):length(params_old)]
  }
  if (i %% 1000==0){
    print (paste("Iteration",as.character(i)))
  }
}

for (i in 2:n){
  rho_old = params_old[2]
  Beta_old = params_old[3:(nfeatures+2)]
  # sample rho
  rho_new = rho_old+rnorm(1,0,1)*step_rho  #proposal
  l_old = loglikelihood_inspection(X_S,S_S,Y_S,Beta_old,Gamma_old,sigma_old,hyperpriors[1],rho_old)[2]
  l_new = loglikelihood_inspection(X_S,S_S,Y_S,Beta_old,Gamma_old,sigma_old,hyperpriors[1],rho_new)[2]
  ll_old = l_old+log(Scaled_BetaPDF(rho_old,hyperpriors[3],hyperpriors[4],-1,1)) 
  ll_new = l_new+log(Scaled_BetaPDF(rho_new,hyperpriors[3],hyperpriors[4],-1,1))
  u = log(runif(1,0,1))
  w = ll_new-ll_old
  if (w>u | is.na(w)){
    rho_old = rho_new
    params_old[2]= rho_new
  }
  
  for (f in 1:nfeatures){
    # sample beta_f
    Beta_new = Beta_old
    Beta_new[f] = Beta_old[f]+rnorm(1,0,1)*step_beta
    l_old = loglikelihood_inspection(X_S,S_S,Y_S,Beta_old,Gamma_old,sigma_old,hyperpriors[1],rho_old)[2]
    l_new = loglikelihood_inspection(X_S,S_S,Y_S,Beta_new,Gamma_old,sigma_old,hyperpriors[1],rho_old)[2]
    ll_old = l_old -(Beta_old[f]-hyperpriors[5])^2/2/hyperpriors[6]^2
    ll_new = l_new -(Beta_new[f]-hyperpriors[5])^2/2/hyperpriors[6]^2
    u = log(runif(1,0,1))
    w = ll_new-ll_old
    if (w>u | is.na(w)){
      Beta_old[f] = Beta_new[f]
      params_old[(f+2)]= Beta_new[f]
    }
    Samples[i,2] = params_old[2]
    Samples[i,3:(nfeatures+2)] = params_old[3:(nfeatures+2)]
  }
  if (i %% 1000==0){
    print (paste("Iteration",as.character(burnin+nsamples+i)))
  }
}

# Inspection out-of-sample prediction

X = test[,1:(ncol(Mat)-2)]
S = test[,(ncol(Mat)-1)]
q = matrix(0,nrow=nrow(X),ncol=nsamples)
for (i in 1:nrow(X)){
  x_c = X[i,]
  x = as.matrix(Samples[(burnin+1):nrow(Samples),(nfeatures+3):ncol(Samples)])%*%t(as.matrix(x_c))
  q[i,] = 1/(1+exp(-x))
}

qmean = rep(0,nrow(X))
for (i in 1:nrow(X)){
  qmean[i]=mean(q[i,])
}

plot(sort(qmean))

#sampling out of sample ROC
pred_s = prediction(qmean,S)
perf_s <- performance( pred_s, "tpr", "fpr" )
plot( perf_s, colorize = TRUE)
q_AUC = as.numeric(performance(pred_s,"auc")@y.values)

#Inspection outcome out-of-sample prediction

Y = test[,ncol(Mat)]
p = matrix(0,nrow=nrow(X),ncol=nsamples)
for (i in 1:nrow(X)){
  x_c = X[i,]
  x = as.matrix(Samples[(burnin+1):nrow(Samples),3:(nfeatures+2)])%*%t(as.matrix(x_c))
  p[i,] = 1/(1+exp(-x))
}

pmean = rep(0,nrow(X))
for (i in 1:nrow(X)){
  pmean[i]=mean(p[i,])
}

plot(sort(pmean))

pred = prediction(pmean,Y)
perf <- performance( pred, "tpr", "fpr" )
plot( perf, colorize = TRUE)

p_AUC = as.numeric(performance(pred,"auc")@y.values)

# plotting inspection and inspection outcome ROC

plot( perf_s, colorize = TRUE)
plot( perf, add = T, colorize = TRUE)

#computing risk scores

X=features[,as.numeric(input_X)]
ones=rep(1,nrow(X))
X=cbind(ones,X)
S=features[,as.numeric(input_S)]
Y=features[,as.numeric(input_Y)]
if (length(ind)>0){
  X=X[-ind,]
  S=S[-ind]
  Y=Y[-ind]
  Nshipments=Nshipments[-ind]
  Nsampled=Nsampled[-ind]
}

q = matrix(0,nrow=nrow(X),ncol=nsamples)
for (i in 1:nrow(X)){
  x_c = X[i,]
  x = as.matrix(Samples[(burnin+1):nrow(Samples),(nfeatures+3):ncol(Samples)])%*%t(as.matrix(x_c))
  q[i,] = 1/(1+exp(-x))
}

q_mean = rep(0,nrow(X))
for (i in 1:nrow(X)){
  q_mean[i]=mean(q[i,])
}

p = matrix(0,nrow=nrow(X),ncol=nsamples)
for (i in 1:nrow(X)){
  x_c = X[i,]
  x = as.matrix(Samples[(burnin+1):nrow(Samples),3:(nfeatures+2)])%*%t(as.matrix(x_c))
  p[i,] = 1/(1+exp(-x))
}

p_mean = rep(0,nrow(X))
for (i in 1:nrow(X)){
  p_mean[i]=mean(p[i,])
}

#saving files
features = features[-ind,]
write.csv(Samples[(burnin+1):nrow(Samples),],'posterior samples.csv')
write.csv(q_significant_features,'significant features for inspection.csv')
write.csv(p_significant_features,'significant features for inpection outcome.csv')
features_table=features;
features_table$inspection_score=q_mean;
features_table$risk_score=p_mean;
write.csv(features_table,'inspection_features_scores.csv')

