# Generate acc assessment result summary figs

library(glue)
library(sf)
library(tidyverse)
library(ggthemes)

# list aoi

aois <- list("ADM", "CHP", "CYP", "NCO", "NPS", "SJF", "SJI", "SMI", "TAC")

# initialize dataframe
results <- data.frame(
  aoi = character(),
  u_water = numeric(),
  u_kelp = numeric(),
  p_water = numeric(),
  p_kelp = numeric(),
  overall_accuracy = numeric(), 
  kappa = numeric()
)

# open tables 
for (aoi in aois){
  confmat <- st_read(dsn = "../KAMaccuracy.gdb",
                       layer = glue("{aoi}_2022_ConfMatrix"))
  
  # extract values of interest
  aoi_row <- data.frame(
    aoi = aoi, 
    u_water = confmat[1,5],
    u_kelp = confmat[2,5],
    p_water = confmat[4,2],
    p_kelp = confmat[4,3],
    overall_accuracy = confmat[4,5], 
    kappa = confmat[5,6]
  )
  
  # append to dataframe
  results <- bind_rows(results, aoi_row)
}

results_long <- results %>% pivot_longer(
  cols = c("u_water", "u_kelp", "p_water", "p_kelp", "overall_accuracy", "kappa"),
  names_to = "stat_type",
  values_to = "stat_value"
)

results_long_filt <- results_long %>% filter(stat_type != "p_water" & stat_type != "u_water")
  
acc_plot <- ggplot(results_long_filt, aes(x=aoi, y=stat_value)) +
  geom_col() + 
  facet_wrap(~ stat_type, ncol = 1) +
  theme_classic()

acc_plot

acc_plot2 <- ggplot(results_long_filt, aes(x=aoi, y=stat_value, fill=stat_type)) +
  geom_col(position = "dodge")

acc_plot2