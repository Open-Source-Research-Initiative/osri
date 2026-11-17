# SPDX-License-Identifier: MIT
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 3L) stop("Usage: run.R WORK_DIR OUTPUT_DIR PACKET_DIR")
work <- normalizePath(args[[1L]])
out <- normalizePath(args[[2L]])
packet <- normalizePath(args[[3L]])
stopifnot(getRversion() == "4.5.3")
expected_packages <- c(simmer = "4.3.0", Rcpp = "1.1.2", BH = "1.69.0-1",
                       magrittr = "2.0.5", jsonlite = "2.0.0", codetools = "0.2-20")
installed <- vapply(names(expected_packages), function(package) {
  packageDescription(package, fields = "Version")
}, character(1))
stopifnot(identical(installed, expected_packages))
stopifnot(identical(formals(parallel::mclapply)$mc.preschedule, TRUE))
options(mc.cores = 2L)
capture.output(sessionInfo(), file = file.path(out, "session-info.txt"))
write.csv(data.frame(package = names(installed), version = unname(installed)),
          file.path(out, "package-versions.csv"), row.names = FALSE)

# Keep the publisher's executable statements. Only Section 4.1 plotting is omitted.
source_lines <- readLines(file.path(work, "sources", "replication.R"), warn = FALSE)
section <- function(first, next_section) {
  start <- match(paste("# Section", first), source_lines)
  end <- match(paste("# Section", next_section), source_lines)
  stopifnot(!is.na(start), !is.na(end), start < end)
  source_lines[seq.int(start + 2L, end - 2L)]
}
s41 <- section("4.1", "4.2")
s41 <- s41[seq_len(match('library("simmer.plot")', s41) - 1L)]
s42 <- section("4.2", "5.1")
writeLines(s41, file.path(out, "executed-section41.R"))
writeLines(s42, file.path(out, "executed-section42.R"))
code41 <- parse(text = s41)
code42 <- parse(text = s42)
target <- jsonlite::fromJSON(file.path(packet, "targets.json"))$literal_supplement_target

literal_run <- function(kind) {
  scope <- new.env(parent = .GlobalEnv)
  RNGkind(kind, "Inversion", "Rejection")
  eval(code41, envir = scope)
  eval(code42, envir = scope)
  scope
}

run_ids <- seq_len(100L)
odd <- seq.int(1L, 99L, 2L)
even <- odd + 1L

run_monitors <- function(envs) {
  stopifnot(length(envs) == 100L)
  lapply(envs, function(env) {
    log <- simmer::get_mon_arrivals(env)
    stopifnot(nrow(log) > 0L, all(log$finished), all(log$end_time <= 500),
              all(log$end_time >= log$start_time))
    # The monitor's local replication label contributes no trajectory information.
    log$replication <- NULL
    log
  })
}

run_means <- function(logs) {
  vapply(logs, function(log) mean(log$end_time - log$start_time), numeric(1))
}

pair_table <- function(logs, means) {
  data.frame(
    pair = seq_along(odd), first_run = odd, second_run = even,
    first_completed = vapply(logs[odd], nrow, integer(1)),
    second_completed = vapply(logs[even], nrow, integer(1)),
    first_mean = means[odd], second_mean = means[even],
    exact_mean_match = means[odd] == means[even],
    exact_completed_arrival_match = vapply(seq_along(odd), function(i) {
      identical(logs[[odd[[i]]]], logs[[even[[i]]]])
    }, logical(1))
  )
}

t_summary <- function(values, level = 0.95) {
  test <- t.test(values, conf.level = level)
  list(n = length(values), mean = unname(test$estimate), lower = test$conf.int[[1L]],
       upper = test$conf.int[[2L]], width = diff(test$conf.int), confidence = level)
}

save_arm <- function(label, logs, means) {
  stopifnot(length(means) == 100L, all(is.finite(means)))
  pairs <- pair_table(logs, means)
  saveRDS(logs, file.path(out, paste0(label, "-completed-arrivals.rds")), version = 3)
  write.csv(data.frame(replication = run_ids, mean_system_time = means),
            file.path(out, paste0(label, "-replications.csv")), row.names = FALSE)
  write.csv(pairs, file.path(out, paste0(label, "-pairs.csv")), row.names = FALSE)
  list(interval = t_summary(means), distinct_means = length(unique(means)),
       paired_means = sum(pairs$exact_mean_match),
       paired_logs = sum(pairs$exact_completed_arrival_match))
}

paper <- literal_run("Mersenne-Twister")
paper_logs <- run_monitors(paper$mm1.envs)
# Use the paper's aggregate() results for all paper-value comparisons.
stopifnot(identical(as.integer(paper$mm1.data$replication), run_ids))
paper_means <- paper$mm1.data[[2L]]
stopifnot(isTRUE(all.equal(paper_means, run_means(paper_logs), tolerance = 1e-14)))
baseline <- save_arm("published-code", paper_logs, paper_means)
one_per_pair <- t_summary(paper_means[odd])
pct_wider <- 100 * (one_per_pair$width / baseline$interval$width - 1)
capture.output(t.test(paper_means), file = file.path(out, "published-code-t-test.txt"))

# This bridge holds the generator fixed for the comparison with assigned streams.
shared <- literal_run("L'Ecuyer-CMRG")
shared_logs <- run_monitors(shared$mm1.envs)
shared_means <- shared$mm1.data[[2L]]
stopifnot(isTRUE(all.equal(shared_means, run_means(shared_logs), tolerance = 1e-14)))
bridge <- save_arm("lecuyer-shared", shared_logs, shared_means)

# Reuse the publisher's function body from its parsed mclapply statement.
run_call <- Filter(function(expr) {
  is.call(expr) && identical(expr[[1L]], quote(`<-`)) &&
    identical(expr[[2L]], quote(mm1.envs))
}, as.list(code42))[[1L]][[3L]]
stopifnot(identical(run_call[[1L]], quote(mclapply)),
          identical(run_call[[2L]], quote(1:100)),
          identical(as.list(run_call)$mc.set.seed, FALSE))
simulate <- eval(run_call[[3L]], envir = shared)
RNGkind("L'Ecuyer-CMRG", "Inversion", "Rejection")
set.seed(1234)
streams <- vector("list", 100L)
streams[[1L]] <- .Random.seed
for (i in run_ids[-1L]) streams[[i]] <- parallel::nextRNGStream(streams[[i - 1L]])
stopifnot(anyDuplicated(streams) == 0L)
control_runs <- parallel::mclapply(run_ids, function(i) {
  assign(".Random.seed", streams[[i]], envir = .GlobalEnv)
  list(pid = Sys.getpid(), seed = .Random.seed, run = simulate(i))
}, mc.cores = 2L, mc.preschedule = TRUE, mc.set.seed = FALSE)
assigned <- lapply(control_runs, `[[`, "seed")
worker_pids <- vapply(control_runs, `[[`, integer(1), "pid")
stopifnot(identical(assigned, streams), length(unique(worker_pids)) == 2L,
          all(worker_pids != Sys.getpid()))
write.csv(data.frame(replication = run_ids, pid = worker_pids,
                     do.call(rbind, assigned)),
          file.path(out, "lecuyer-assigned-streams.csv"), row.names = FALSE)
control_logs <- run_monitors(lapply(control_runs, `[[`, "run"))
control <- save_arm("lecuyer-separate", control_logs, run_means(control_logs))

# Reproduce the note's separate finite-horizon experiment with integer seeds.
RNGkind("Mersenne-Twister", "Inversion", "Rejection")
distinct <- do.call(rbind, lapply(run_ids, function(i) {
  seed <- 10000L + i
  set.seed(seed)
  run <- simulate(i)
  arrivals <- simmer::get_mon_arrivals(run)
  resources <- simmer::get_mon_resources(run)
  durations <- diff(c(resources$time, 500))
  stopifnot(all(arrivals$finished), all(arrivals$end_time <= 500), all(durations >= 0))
  data.frame(replication = i, seed = seed, completed_arrivals = nrow(arrivals),
             mean_system_time = mean(arrivals$end_time - arrivals$start_time),
             time_weighted_occupancy = sum(durations * (resources$server + resources$queue)) / 500)
}))
write.csv(distinct, file.path(out, "distinct-seed-replications.csv"), row.names = FALSE)
distinct_time <- t_summary(distinct$mean_system_time, 0.975)
distinct_pop <- t_summary(distinct$time_weighted_occupancy, 0.975)

published <- c(target$mean, target$ci95)
observed <- unlist(baseline$interval[c("mean", "lower", "upper")], use.names = FALSE)
checks <- list(
  paper_printed_values = all(abs(observed - published) <= target$absolute_tolerance),
  paper_all_50_means_match = baseline$paired_means == 50L && baseline$distinct_means == 50L,
  paper_all_50_logs_match = baseline$paired_logs == 50L,
  one_per_pair_matches_note = all(abs(c(one_per_pair$lower, one_per_pair$upper) -
                                          c(0.4821378, 0.5128508)) <= 5e-8) &&
    abs(one_per_pair$mean - baseline$interval$mean) <= 1e-14 && round(pct_wider) == 44,
  shared_lecuyer_pairing_persists = bridge$paired_means == 50L && bridge$paired_logs == 50L,
  separate_lecuyer_pairing_absent = control$paired_means == 0L && control$paired_logs == 0L,
  distinct_seed_summaries_match_note = all(abs(
    unlist(c(distinct_time[c("mean", "lower", "upper")], distinct_pop[c("mean", "lower", "upper")])) -
      c(0.49806, 0.48819, 0.50793, 0.99770, 0.97466, 1.02074)
  ) <= 5e-6),
  finite_run_intervals_contain_references = distinct_time$lower <= 0.5 &&
    distinct_time$upper >= 0.5 && distinct_pop$lower <= 1 && distinct_pop$upper >= 1
)
report <- list(
  paper = "10.18637/jss.v090.i02", printed_target = published,
  literal_tolerance = target$absolute_tolerance, printed_value_errors = abs(observed - published),
  workers = 2L, preschedule = TRUE, automatic_reseeding = FALSE,
  seed = 1234L, published_code = baseline, one_per_pair = one_per_pair,
  percentage_wider = pct_wider, shared_lecuyer = bridge, separate_lecuyer = control,
  distinct_seed_time = distinct_time, distinct_seed_population = distinct_pop,
  checks = checks, passed = all(unlist(checks))
)
jsonlite::write_json(report, file.path(out, "summary.json"),
                     auto_unbox = TRUE, pretty = TRUE, digits = 17)
print(checks)
if (!report$passed) quit(status = 1L)
