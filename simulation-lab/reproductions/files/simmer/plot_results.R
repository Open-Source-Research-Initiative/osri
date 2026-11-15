# SPDX-License-Identifier: MIT
args <- commandArgs(trailingOnly=TRUE)
base <- if(length(args)) normalizePath(args[1]) else normalizePath('.')
r <- read.csv(file.path(base,'outputs','author-resource-monitor.csv'))
t <- r$time
n <- r$server+r$queue
cumulative <- cumsum(c(0,diff(t))*c(0,head(n,-1)))/t
plot_result <- function() {
 par(mfrow=c(1,2),mar=c(4.5,4.5,1,1))
 plot(t,n,type='s',xlim=c(0,15),ylim=c(0,5),xlab='Simulation time',ylab='Customers in system',col='#134e6f',lwd=1)
 plot(t[is.finite(cumulative)],cumulative[is.finite(cumulative)],type='l',xlab='Simulation time',ylab='Time-averaged customers',col='#134e6f',lwd=1,ylim=c(0,1.3))
 abline(h=1,lty=2,col='#b55a30')
}
png(file.path(base,'outputs','mm1-paper-comparison.png'),width=1400,height=550,res=140)
plot_result();dev.off()
svg(file.path(base,'outputs','mm1-paper-comparison.svg'),width=10,height=4)
plot_result();dev.off()
