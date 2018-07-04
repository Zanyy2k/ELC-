 #load libraries
library("e1071")
library("RTextTools")
library("stringr")
library("tm")
library("SnowballC")
library("qdapDictionaries")
library("plyr")
library("RColorBrewer")
library("ggplot2")
library("wordcloud")
library("biclust")
library("cluster")
library("igraph")
library("fpc")
library("ggmap")

#functions
#pre-text processing
preprocess =  function(df) {
  
  #lower case 
  df = toupper(df)
  #remove unnecesary whitespace 
  df = trimws(df)
  #remove special characters - need stringr lib
  df = str_replace_all(df,"[^[:graph:]]", " ")
  #remove character
  df = gsub("%", " ",df)
  #remove empty rows
  df[df==""] = NA
  df = df[complete.cases(df)]
  #remove na
  df = na.omit(df)
  
  df = data.frame(df)
  return (df); 
}

JMLFollower <- read.csv("C:/Users/zyu/Desktop/SocialMedia_Analysis/JMLFollower.csv", encoding="UTF-8",na.strings = c("", "NA"))
JMLocation <- as.matrix(JMLFollower$Location)
JMLocation1 = preprocess(JMLocation)
location <- as.character(JMLocation1$df)

#Install key package helpers:
source("https://raw.githubusercontent.com/LucasPuente/geocoding/master/geocode_helpers.R")
#Install modified version of the geocode function
#(that now includes the api_key parameter):
source("https://raw.githubusercontent.com/LucasPuente/geocoding/master/modified_geocode.R")

# Generate specific geocode function:
geocode_apply<-function(x){
  geocode(x, source = "google", output = "all", api_key="AIzaSyBIKAgfMKLXZMnaY93cSRuMHDi4YjDKfe4")
}
#Apply this new function to entire list:
geocode_results<-sapply(location, geocode_apply, simplify = F)
#Look at the number of geocoded locations:
length(geocode_results)

#######
#Step 5: Clean Geocoding Results
#######
#Only keep locations with "status" = "ok"
condition_a <- sapply(geocode_results, function(x) x["status"]=="OK")
geocode_results<-geocode_results[condition_a]
#Only keep locations with one match:
condition_b <- lapply(geocode_results, lapply, length)
condition_b2<-sapply(condition_b, function(x) x["results"]=="1")
geocode_results<-geocode_results[condition_b2]
#Look at the number of *successfully* geocoded locations:
length(geocode_results)
#Address formatting issues:
source("https://raw.githubusercontent.com/LucasPuente/geocoding/master/cleaning_geocoded_results.R")
#Turn list into a data.frame:
results_b<-lapply(geocode_results, as.data.frame)
results_c<-lapply(results_b,function(x) subset(x, select=c("results.formatted_address", "results.geometry.location")))
#Format thes new data frames:
results_d<-lapply(results_c,function(x) data.frame(Location=x[1,"results.formatted_address"],
                                                   lat=x[1,"results.geometry.location"],
                                                   lng=x[2,"results.geometry.location"]))
#Bind these data frames together:
results_e<-rbindlist(results_d)
#Add info on the original (i.e. user-provided) location string:
results_f<-results_e[,Original_Location:=names(results_d)]

#######
# Step 6: Map the Geocoded Results
#######
#Load Relevant Packages:
ipak <- function(pkg){
  new.pkg <- pkg[!(pkg %in% installed.packages()[, "Package"])]
  if (length(new.pkg)) 
    install.packages(new.pkg, dependencies = TRUE)
  sapply(pkg, require, character.only = TRUE)
}
packages <- c("maps", "mapproj", "splancs")
ipak(packages)
#Generate a blank map:
zd_proj<-map("world", proj="albers", param=c(39, 45), col="#999999", fill=FALSE, bg=NA, lwd=0.2, add=FALSE, resolution=1)
#Add points to it:
points(mapproject(result_f$lng, results_f$lat), col=NA, bg="#00000030", pch=21, cex=1.0)
#Add a title:
mtext("The Geography of JML Followers", side = 3, line = -3.5, outer = T, cex=1.5, font=3)
#For more on mapping, see: http://flowingdata.com/2014/03/25/how-to-make-smoothed-density-maps-in-r/.

write.csv(results_f, file = "C:\\Users\\zyu\\Desktop\\Twitter\\JMLOCATION.csv", row.names = FALSE)


