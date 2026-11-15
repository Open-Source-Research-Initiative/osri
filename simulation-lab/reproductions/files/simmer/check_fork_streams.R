# SPDX-License-Identifier: MIT
# Exploratory diagnosis of the publisher's mc.set.seed=FALSE configuration.
args <- commandArgs(trailingOnly=TRUE)
base <- if(length(args)) normalizePath(args[1]) else normalizePath('.')
eval(parse(file=file.path(base,'outputs','executed-section41.R')),envir=.GlobalEnv)
library(parallel)
options(mc.cores=2L)
set.seed(1234)
envs <- mclapply(1:2,function(i) {
 simmer() %>% add_resource('mm1.resource',capacity=1,queue_size=Inf) %>%
 add_generator('arrival',mm1.traj,function() rexp(100,lambda)) %>%
 run(until=1000/lambda) %>% wrap()
},mc.set.seed=FALSE)
a <- get_mon_arrivals(envs[[1]])
b <- get_mon_arrivals(envs[[2]])
result <- list(scope='Exploratory diagnosis, not a prespecified scientific target',replications=2,mc_cores=2,mc_set_seed=FALSE,first_completed_arrivals=nrow(a),second_completed_arrivals=nrow(b),complete_arrival_monitors_identical=identical(a,b),comparison='All dataframe columns compared with identical()')
jsonlite::write_json(result,file.path(base,'outputs','duplicate-stream-check.json'),pretty=TRUE,auto_unbox=TRUE)
print(result)
