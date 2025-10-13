# Compute fuzzy error matrix

# Set env
library(sf)

# Load data
sample_points <- st_read(dsn = "../KAMaccuracy.gdb",
                         layer = "TAC_2022_SamplePoints_Method2_Fuzzy")

c

# Compute matrix 
m <- table(Prediction = sample_points$Classified, 
              Reference = sample_points$GrndTruth)

print(m)
# Values in col "2" are acceptably kelp or water

# Compute accuracy stats

# Overall accuracy = correctly classed points / total points
overall_accuracy <- sum(diag(m)) / sum(m)

# Producers
fuzzy_prod_kelp <- (m[2,2] + m[1,3])/ (m[2,2] + m[1,3] + m[1,2])
det_prod_kelp <- (m[2,2])/ (m[2,2] + m[1,3] + m[1,2])

fuzzy_prod_water <- (m[1,1] + m[2,3]) / (m[1,1] + m[2,3] + m[2,1])
det_prod_water <- (m[1,1]) / (m[1,1] + m[2,3] + m[2,1])

# Users
fuzzy_u_kelp <- (m[2,2] + m[2,3])/ (m[2,1] + m[2,2] + m[2,3])
det_u_kelp <- (m[2,2])/ (m[2,1] + m[2,2] + m[2,3])

fuzzy_u_water <- (m[1,1] + m[1,3]) / (m[1,1] + m[1,2] + m[1,3])
det_u_water <- (m[1,1] + m[1,3]) / (m[1,1] + m[1,2] + m[1,3])

# Compute deterministic kappa

# prepare "deterministic' matrix where all fuzzy acceptables are treated as incorrect
m_det <- m[, -3]
m_det[1,2] <- m[1,2] + m[1,3]
m_det[2,1] <- m[2,1] + m[2,3]
print(m_det)

  
Po <- sum(diag(m_det))/sum(m_det)
Pe <- sum(rowSums(m_det) * colSums(m_det)) / (sum(m_det))^2

kappa_det <- (Po - Pe) / (1 - Pe)

# Compute fuzzy kappa
# prepare "fuzzy" matrix where all fuzzy acceptables are treated as correct
m_fuzz <- m[, -3]
m_fuzz[1,1] <- m[1,1] + m[1,3]
m_fuzz[2,2] <- m[2,2] + m[2,3]
print(m_fuzz)

Po <- sum(diag(m_fuzz))/sum(m_fuzz)
Pe <- sum(rowSums(m_fuzz) * colSums(m_fuzz)) / (sum(m_fuzz))^2

kappa_fuzz <- (Po - Pe) / (1 - Pe)

# Write results to a table 

