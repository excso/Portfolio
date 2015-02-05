#-------------------------------------------------------------------------------
# Name:        Graph.R
# Purpose:     Uses csv outputs from ArcGIS/Python script to make png graphs.
#
# Author:      Brian
#
# Created:     04/02/2015
# Copyright:   (c) Brian 2015
# Licence:     MIT
#-------------------------------------------------------------------------------

folder = "../tabular"
files<-list.files(folder, full.names=TRUE, pattern='.csv')
  
make_graph<-function(file){  
  plot.new()
  xs_df <- read.csv(file, header=TRUE, sep=",")
  xs_df_sorted<-xs_df[order(xs_df$StationFtFromLeftPoint),]
  x <- xs_df_sorted$StationFtFromLeftPoint
  y <- xs_df_sorted$ElevationFt 
  cl <- xs_df_sorted$StationFtFromCL
  
  filename <- paste(strsplit(file, ".csv"), ".png", sep="")
  
  png(filename, height=1100, width=1100, units="px", bg="white")
  
  plot(x,y,type="b",col="blue",lty=3,asp=1, xlab="", ylab="")
  # Label points with elevations above line
  with(xs_df_sorted[,], text(x,y, labels = formatC(y, digits=2, format="f"), pos=3, offset=3, srt=90)) 
  # Label points with distance from centerline
  with(xs_df_sorted[,], text(x,y, labels = formatC(cl, digits=2, format="f"), pos=3, offset=-3, srt=90)) 
  
  axis(1, at=seq(0,250,by=25), lab=as.character(seq(0, 250, by=25)))
  z_min <- (min(y)%/%100)*100
  axis(2, at=seq(0,250,by=50), lab=as.character(seq(z_min, z_min+250, by=50)))
  
  title_r <- strsplit(file, ".csv")[[1]]     # Strips right side
  title_l <- strsplit(title_r, "/")[[1]]  # Strips left side
  
  title(main=title_l[length(title_l)], col.main="blue", font.main=4)
  
  title(xlab= "Station", col.lab=rgb(0,0.5,0))
  title(ylab= "Elevation", col.lab=rgb(0,0.5,0))
  dev.off()
}

for(file in files){
  make_graph(file)
}