data {
  int polls; // number of polls
  int T; // number of days
  matrix[T, polls] Y; // polls
  matrix[T, polls] sigma; // polls standard deviations
  real initial_prior;
  real rw_sd; //standard deviation (really? not var?) of random walk
}
parameters {
  vector[T] mu; // the mean of the polls
  real<lower = 0> tau; // the standard deviation of the random effects
  matrix[T, polls] shrunken_polls;
}
model {
  // prior on initial difference
  mu[1] ~ normal(initial_prior, 1);
  tau ~ student_t(4, 0, 5);
  // state model
  for(t in 2:T) {
    mu[t] ~ normal(mu[t-1], rw_sd);
  }

  // measurement model
  for(t in 1:T) {
    for(p in 1:polls) {
      if(Y[t, p] > 0) {
        Y[t,p]~ normal(shrunken_polls[t, p], sigma[t,p]);
        shrunken_polls[t, p] ~ normal(mu[t], tau);
      } else {
        shrunken_polls[t, p] ~ normal(50, 5);
      }
    }
  }
}
