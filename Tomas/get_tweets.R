library(rtweet)
library(tidyverse)
temp <- search_tweets("immediate effect",retryonratelimit = T)
df <- temp
#write_csv (df,"test.csv")
write_as_csv(temp, "tweet_data.csv", prepend_ids = TRUE, na = "", fileEncoding = "UTF-8")