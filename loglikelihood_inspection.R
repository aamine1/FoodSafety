loglikelihood_inspection <- function(X,S,Y,Beta,Gamma,sigma,c,rho){ 
  n = nrow(X)
  epsilon = rnorm(n,0,1)
  delta = rnorm(n,0,1)
  if (sigma < 0 || sigma> c){
    L1= -Inf
  } else {
    G = as.matrix(X) %*% Gamma
    L1=-sum(S*log(1+exp(-G+sigma*epsilon))+(1-S)*log(1+exp(G-sigma*epsilon)))
  }
  if (rho>1 || rho< -1){
    L2 = -Inf
  }
  else{
    B = as.matrix(X)%*%Beta
    L2=-sum(Y*log(1+exp(-B-rho*epsilon-sqrt(1-rho^2)*delta))+(1-Y)*log(1+exp(B-rho*epsilon-sqrt(1-rho^2)*delta)))
  }
  return (c(L1,L2))
}
