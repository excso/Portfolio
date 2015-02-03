f = "<path to>BoatRampLevee_MaxWatersideHeight.csv"
xs_df <- read.csv(f, header=TRUE, sep=",")

x <- xs_df$StationFt
y <- xs_df$ElevationFt 

filename <- paste(strsplit(f, ".csv"), ".png", sep="")

png(filename, height=1100, width=1100, units="px", bg="white")

plot(x,y,type="b",col="blue",lty=3,asp=1, xlab="", ylab="")
with(xs_df[,], text(x,y, labels = formatC(y, digits=2, format="f"), pos=3, offset=1))
axis(1, at=seq(0,250,by=25), lab=as.character(seq(0, 250, by=25)))
z_min <- (min(y)%/%100)*100
axis(2, at=seq(0,250,by=50), lab=as.character(seq(z_min, z_min+250, by=50)))

title_r <- strsplit(f, ".csv")[[1]]     # Strips right side
title_l <- strsplit(title_r, "/")[[1]]  # Strips left side

title(main=title_l[length(title_l)], col.main="blue", font.main=4)

title(xlab= "Station", col.lab=rgb(0,0.5,0))
title(ylab= "Elevation", col.lab=rgb(0,0.5,0))
dev.off()