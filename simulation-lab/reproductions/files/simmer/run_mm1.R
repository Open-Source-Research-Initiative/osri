# SPDX-License-Identifier: MIT
# Executes publisher supplement blocks from Ucar, Smeets & Azcorra (2019).
# Author model is GPL>=2 simmer; supplement retrieved separately, not vendored here.
args <- commandArgs(trailingOnly=TRUE)
base <- if(length(args)) normalizePath(args[1]) else normalizePath('.')
out <- file.path(base,'outputs'); dir.create(out,showWarnings=FALSE)
supplement <- readLines(file.path(base,'sources','replication.R'),warn=FALSE)
section <- function(label,nextlabel) {
 a <- grep(paste0('^# Section ',label,'$'),supplement)
 b <- grep(paste0('^# Section ',nextlabel,'$'),supplement)
 supplement[seq(a+2,b-2)]
}
options(mc.cores=2L)
started <- proc.time()[['elapsed']]
# Model expressions, parameters, seed and horizon unchanged; plotting omitted.
s41 <- section('4.1','4.2')
s41 <- s41[seq_len(grep('library("simmer.plot")',s41,fixed=TRUE)-1)]
writeLines(s41,file.path(out,'executed-section41.R'))
eval(parse(text=s41),envir=.GlobalEnv)
resources <- get_mon_resources(mm1.env)
arrivals <- get_mon_arrivals(mm1.env)
write.csv(resources,file.path(out,'author-resource-monitor.csv'),row.names=FALSE)
write.csv(arrivals,file.path(out,'author-arrivals.csv'),row.names=FALSE)
weighted_occupancy <- function(res,horizon) {
 durations <- diff(c(res$time,horizon))
 sum(durations*(res$server+res$queue))/horizon
}
# Exact publisher section4.2 expressions, including its RNG semantics.
s42 <- section('4.2','5.1')
writeLines(s42,file.path(out,'executed-section42.R'))
eval(parse(text=s42),envir=.GlobalEnv)
author_test <- t.test(mm1.data[[2]])
capture.output(author_test,file=file.path(out,'author-t-test.txt'))
write.csv(mm1.data,file.path(out,'author-replications.csv'),row.names=FALSE)
author_means <- mm1.data[[2]]
author_result <- list(mean=mean(author_means),ci95=as.vector(author_test$conf.int),unique_replication_means=length(unique(author_means)),replications=length(author_means),time_weighted_occupancy_single_run=weighted_occupancy(resources,2000),mc_cores=2,mc_set_seed=FALSE)
# Additional validation: same model/rates/horizon but independent explicit seeds.
validation <- lapply(seq_len(100),function(i) {
 set.seed(10000+i)
 env <- simmer() %>%
  add_resource('mm1.resource',capacity=1,queue_size=Inf) %>%
  add_generator('arrival',mm1.traj,function() rexp(100,lambda)) %>%
  run(until=1000/lambda)
 a <- get_mon_arrivals(env)
 r <- get_mon_resources(env)
 data.frame(replication=i,seed=10000+i,completed_arrivals=nrow(a),mean_system_time=mean(a$end_time-a$start_time),time_weighted_occupancy=weighted_occupancy(r,1000/lambda))
})
validation <- do.call(rbind,validation)
write.csv(validation,file.path(out,'independent-replications.csv'),row.names=FALSE)
interval <- function(x,reference) {
 test <- t.test(x,conf.level=.975)
 list(mean=mean(x),standard_error=sd(x)/sqrt(length(x)),ci97p5=as.vector(test$conf.int),reference=reference,contains_reference=unname(test$conf.int[1]<=reference && test$conf.int[2]>=reference))
}
# Exact deterministic Section5.2 function, avoiding unrelated benchmark runtimes.
s52start <- grep('^# Section 5.2$',supplement)
fn_start <- grep('^test_simmer <- function',supplement)
fn_end <- fn_start + which(supplement[(fn_start+1):length(supplement)]=='}')[1]
fn <- supplement[fn_start:fn_end]
writeLines(fn,file.path(out,'executed-section52.R'))
eval(parse(text=fn),envir=.GlobalEnv)
d <- test_simmer(1000,1)
write.csv(d,file.path(out,'deterministic-arrivals.csv'),row.names=FALSE)
deterministic <- list(rows=nrow(d),all_starts_exact=identical(as.numeric(d$start_time),as.numeric(1:1000)),all_ends_exact=identical(as.numeric(d$end_time),as.numeric(2:1001)),activity_time_exact=all(d$activity_time==1),all_finished=all(d$finished))
expected <- c(.4974943,.4868269,.5081617)
observed <- c(author_result$mean,author_result$ci95)
result <- list(status='completed',paper='10.18637/jss.v090.i02',runtime=R.version.string,packages=as.list(sapply(c('simmer','Rcpp','BH','magrittr','jsonlite'),function(x)as.character(packageVersion(x)))),author=author_result,literal_paper_comparison=list(reference=expected,observed=observed,absolute_error=abs(observed-expected),tolerance=5e-8,passed=all(abs(observed-expected)<=5e-8)),independent_validation=list(system_time=interval(validation$mean_system_time,.5),system_occupancy=interval(validation$time_weighted_occupancy,1),replications=100,seeds=as.list(10001:10100),same_model_rates_horizon=TRUE,explicit_seed_change=TRUE),deterministic=deterministic,elapsed_seconds=proc.time()[['elapsed']]-started)
jsonlite::write_json(result,file.path(out,'results.json'),auto_unbox=TRUE,pretty=TRUE,digits=17)
capture.output(sessionInfo(),file=file.path(out,'sessionInfo.txt'))
print(result)
