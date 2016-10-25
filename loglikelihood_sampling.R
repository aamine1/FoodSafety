loglikelihood_sampling <- function(X,S,Y,Nshipments,Nsampled,Beta,Gamma,sigma,c,rho){
  n = nrow(X)
  epsilon = rnorm(n,0,1)
  delta = rnorm(n,0,1)
  if (sigma < 0 || sigma> c){
    L1= -Inf
  } else {
    G = as.matrix(X) %*% Gamma
    L1=-sum(Nshipments*(S*log(1+exp(-G+sigma*epsilon))+(1-S)*log(1+exp(G-sigma*epsilon))))/sum(Nshipments)
  }
  if (rho>1 || rho< -1){
    L2 = -Inf
  }
  else{
    B = as.matrix(X)%*%Beta
    L2=-sum(Nsampled*Y*log(1+exp(-B-rho*epsilon-sqrt(1-rho^2)*delta))+Nsampled*(1-Y)*log(1+exp(B-rho*epsilon-sqrt(1-rho^2)*delta)))/sum(Nsampled)
  }
  return (c(L1,L2))
}