library(tidyverse)
library(stringi)
library(RcppRoll)
library(lme4)


files=dir('.',pattern='*Scores.txt', full.names=T)
files
'[1] "./highPairsContextRelevantScores.txt"        "./highPairsCosSimScores.txt"                
[3] "./incongruentPairsContextRelevantScores.txt" "./incongruentPairsCosSimScores.txt"         
[5] "./lowPairsContextRelevantScores.txt"         "./lowPairsCosSimScores.txt"                 
[7] "./singleSimScores.txt"                       "./stimWordSimScores.txt" '

HPdataCRC = read_delim('highPairsContextRelevantScores.txt', col_names = c("cue", "target", "year", "CRsim"), delim=" " ) %>% 
  mutate(category = "high-predictability", 
         cue = stri_sub(cue,from=1,to=-2))

HPdataCos = read_delim('highPairsCosSimScores.txt', col_names = c("cue", "target", "year", "cosine"), delim=" " ) %>% 
  mutate(category = "high-predictability", 
         cue = stri_sub(cue,from=1,to=-2))

LPdataCRC = read_delim('lowPairsContextRelevantScores.txt', col_names = c("cue", "target", "year", "CRsim"), delim=" " ) %>% 
  mutate(category = "low-predictability", 
         cue = stri_sub(cue,from=1,to=-2))

LPdataCos = read_delim('lowPairsCosSimScores.txt', col_names = c("cue", "target", "year", "cosine"), delim=" " ) %>% 
  mutate(category = "low-predictability", 
         cue = stri_sub(cue,from=1,to=-2))

INdataCRC = read_delim('incongruentPairsContextRelevantScores.txt', col_names = c("cue", "target", "year", "CRsim"), delim=" " ) %>% 
  mutate(category = "incongruent", 
         cue = stri_sub(cue,from=1,to=-2))

INdataCos = read_delim('incongruentPairsCosSimScores.txt', col_names = c("cue", "target", "year", "cosine"), delim=" " ) %>% 
  mutate(category = "incongruent", 
         cue = stri_sub(cue,from=1,to=-2))

dataCRC = bind_rows(HPdataCRC, LPdataCRC, INdataCRC)
dataCos = bind_rows(HPdataCos, LPdataCos, INdataCos)

data = bind_cols(dataCRC, dataCos) %>% 
  mutate(cue_check = cue == cue1,
         target_check = target==target1,
         year_check = year==year1,
         cat_check = category==category1)
data %>% summarise(mean(cue_check), mean(target_check), mean(year_check), mean(cat_check))
# A tibble: 1 x 4
'`mean(cue_check)` `mean(target_check)` `mean(year_check)` `mean(cat_check)`
<dbl>                <dbl>              <dbl>             <dbl>
  1                 1                    1                  1                 1'

# they're identical so we can ignore/drop the *1 cols

data$cue %>% unique() # some cues are not right (one bllank and one "in")
data$target %>% unique() 

good_cues = data$cue %>% unique()
good_cues = good_cues[-c(10,29)]

# Cosine Similarity -------------------------------------------------------


ggplot(data)+
  geom_histogram(aes(x=cosine))

ggplot(data)+
  geom_density(aes(x=cosine, fill=category), alpha=0.5)

ggplot(data %>% filter(year == 1990))+
  geom_density(aes(x=cosine, fill=category), alpha=0.5)

ggplot(data )+
  geom_density(aes(x=cosine, fill=category), alpha=0.5)+
  facet_wrap(~year)

ggsave("./Rgraphs/CosineSimDensityOverDecades.pdf", width = 9, height=9)

ggplot(data )+
  geom_point(aes(x=year, y=cosine, color=category, group=cue), alpha=0.2)+
  stat_summary(aes(x=year, y=cosine, color=category), geom='pointrange', fun.data='mean_cl_boot')+
  geom_smooth(aes(x=year, y=cosine, color=category))

ggplot(data %>% filter(year>=1900))+
  geom_point(aes(x=year, y=cosine, color=category, group=cue), alpha=0.2)+
  stat_summary(aes(x=year, y=cosine, color=category), geom='pointrange', fun.data='mean_cl_boot')+
  geom_smooth(aes(x=year, y=cosine, color=category))

# Stats: Cosine Similarity Stats -------------------------------------------------
data$category<-factor(data$category, levels = c("incongruent", "low-predictability","high-predictability"))
#contrasts(data$category)<-cbind(c(-0.6, 0.33, 0.33), c(0, -0.5, 0.5))
data$year_c <- scale(data$year)

m1 = lmer(cosine ~ category*year_c + (1+category*year_c|cue), data=data)
summary(m1)
'Linear mixed model fit by REML ['lmerMod']
Formula: cosine ~ category * year_c + (1 + category * year_c | cue)
   Data: data

REML criterion at convergence: -8377.9

Scaled residuals: 
    Min      1Q  Median      3Q     Max 
-4.9571 -0.5303 -0.0098  0.5593  4.7337 

Random effects:
 Groups   Name                               Variance  Std.Dev. Corr                         
 cue      (Intercept)                        0.0018284 0.04276                               
          categorylow-predictability         0.0137681 0.11734   0.06                        
          categoryhigh-predictability        0.0153043 0.12371   0.16  0.61                  
          year_c                             0.0003782 0.01945   0.36 -0.32 -0.33            
          categorylow-predictability:year_c  0.0007651 0.02766  -0.01 -0.20  0.15  0.28      
          categoryhigh-predictability:year_c 0.0007733 0.02781  -0.04 -0.12 -0.23  0.27  0.08
 Residual                                    0.0064529 0.08033                               
Number of obs: 4080, groups:  cue, 40

Fixed effects:
                                   Estimate Std. Error t value
(Intercept)                        0.039027   0.007164   5.448
categorylow-predictability         0.131267   0.018855   6.962
categoryhigh-predictability        0.186482   0.019847   9.396
year_c                             0.003766   0.003819   0.986
categorylow-predictability:year_c  0.019147   0.005434   3.524
categoryhigh-predictability:year_c 0.022890   0.005460   4.192

Correlation of Fixed Effects:
            (Intr) ctgryl- ctgryh- year_c ctgryl-:_
ctgrylw-prd  0.013                                 
ctgryhgh-pr  0.106  0.602                          
year_c       0.274 -0.253  -0.265                  
ctgrylw-p:_ -0.010 -0.157   0.121  -0.061          
ctgryhgh-:_ -0.032 -0.092  -0.184  -0.065  0.218   
convergence code: 0
Model failed to converge with max|grad| = 0.0157011 (tol = 0.002, component 1)
'

m1_allFit<-allFit(m1)
summary(m1_allFit)


m2 = lmer(cosine ~ category*year_c + (1+category*year_c|cue), data=data %>% filter(year>=1900))
summary(m2)
m2_allFit<-allFit(m2)
summary(m2_allFit)



# Context Relevant Similarity ---------------------------------------------


ggplot(data)+
  geom_histogram(aes(x=CRsim))

# major outliers in CRC
fivenum(data$CRsim)
# [1] -16.26642902   0.05737263   0.26969768   0.36918125          Inf

data1 = data %>% filter(between(CRsim, -1, 1))

ggplot(data1)+
  geom_histogram(aes(x=CRsim))

ggplot(data1)+
  geom_point(aes(x=cosine, y=CRsim))

ggplot(data1 )+
  geom_density(aes(x=CRsim, fill=category), alpha=0.5)+
  facet_wrap(~year)

ggplot(data1 )+
  geom_point(aes(x=year, y=CRsim, color=category, group=cue), alpha=0.2)+
  stat_summary(aes(x=year, y=CRsim, color=category), geom='pointrange', fun.data='mean_cl_boot')+
  geom_smooth(aes(x=year, y=CRsim, color=category))

ggplot(data1 %>% filter(year>=1900))+
  geom_point(aes(x=year, y=CRsim, color=category, group=cue), alpha=0.2)+
  stat_summary(aes(x=year, y=CRsim, color=category), geom='pointrange', fun.data='mean_cl_boot')+
  geom_smooth(aes(x=year, y=CRsim, color=category))

# Stats: Context Relevant Similarity -------------------------------------------------

m1.1 = lmer(CRsim ~ category*year_c + (1+category*year_c|cue), data=data1)
summary(m1.1)
'Linear mixed model fit by REML ['lmerMod']
Formula: CRsim ~ category * year_c + (1 + category * year_c | cue)
   Data: data1

REML criterion at convergence: -3547.7

Scaled residuals: 
    Min      1Q  Median      3Q     Max 
-7.4663 -0.4002 -0.0146  0.3946  5.6084 

Random effects:
 Groups   Name                               Variance Std.Dev. Corr                         
 cue      (Intercept)                        0.009899 0.09949                               
          categorylow-predictability         0.029456 0.17163  -0.22                        
          categoryhigh-predictability        0.024050 0.15508  -0.84 -0.34                  
          year_c                             0.001159 0.03404  -0.20  0.00  0.19            
          categorylow-predictability:year_c  0.011336 0.10647  -0.15 -0.64  0.50  0.08      
          categoryhigh-predictability:year_c 0.005990 0.07740   0.22  0.42 -0.45 -0.74 -0.73
 Residual                                    0.019900 0.14107                               
Number of obs: 3672, groups:  cue, 39

Fixed effects:
                                    Estimate Std. Error t value
(Intercept)                         0.058207   0.016823   3.460
categorylow-predictability          0.234785   0.028987   8.100
categoryhigh-predictability         0.293431   0.026089  11.247
year_c                             -0.003093   0.007202  -0.429
categorylow-predictability:year_c  -0.013363   0.018743  -0.713
categoryhigh-predictability:year_c  0.011100   0.014211   0.781

Correlation of Fixed Effects:
            (Intr) ctgryl- ctgryh- year_c ctgryl-:_
ctgrylw-prd -0.247                                 
ctgryhgh-pr -0.831 -0.306                          
year_c      -0.190  0.016   0.175                  
ctgrylw-p:_ -0.121 -0.616   0.459  -0.091          
ctgryhgh-:_  0.220  0.379  -0.426  -0.719 -0.551   
convergence code: 0
boundary (singular) fit: see ?isSingular'

m1.1_allFit<-allFit(m1.1)
summary(m1.1_allFit)


m2.1 = lmer(CRsim ~ category*year_c + (1+category*year_c|cue), data=data1 %>% filter(year>=1900))
summary(m2.1)
m1_allFit<-allFit(m1)
summary(m1_allFit$bobyqa)


# Cumulative Similarity -------------------------------------------------

# Assumes that people's language is influenced by things written in past decades (e.g., reading older books)
# weighted averaging assumes that you are less influenced by new decades as you get older

data2 = data %>% 
  group_by(cue, target) %>% 
  select(-cue1,-category1,-target1,-year1, -cue_check, -cat_check, -target_check, -year_check) %>% 
  filter(cue %in% good_cues) %>% 
  mutate(cum_avg_cosine = cummean(cosine))

ggplot(data2 )+
  stat_summary(aes(x=year, y=cum_avg_cosine, color=category), geom='pointrange', fun.data = "mean_cl_boot")

new_dat = data.frame(target=vector("character"), 
                     cue=vector("character"), 
                     year=vector("numeric"), 
                     cum_avg20yr_cosine=vector("numeric"), 
                     cum_avg80yr_cosine=vector("numeric"),
                     weighted_cum_avg20yr_cosine=vector("numeric"),
                     weighted_cum_avg80yr_cosine=vector("numeric"))

for (cues in data2$cue %>% unique()){
  cue_data = data2 %>% filter(cue==cues)
  for (targets in cue_data$target %>% unique()){
    target_data = cue_data %>% filter(target == targets)
    cum_avg20yr_cosine = roll_mean(target_data$cosine, n=2)
    cum_avg80yr_cosine = roll_mean(target_data$cosine, n=8)
    weighted_cum_avg20yr_cosine = roll_mean(target_data$cosine, n=2, weights = 1/(1:2), normalize=F )
    weighted_cum_avg80yr_cosine = roll_mean(target_data$cosine, n=8, weights = 1/(1:8), normalize=F )
    new_cols = data.frame(target=target_data$target,
                     cue=target_data$cue,
                     year=target_data$year, 
                     cum_avg20yr_cosine=c(NA,cum_avg20yr_cosine),
                     cum_avg80yr_cosine=c(rep(NA,7),cum_avg80yr_cosine),
                     weighted_cum_avg20yr_cosine=c(NA,weighted_cum_avg20yr_cosine),
                     weighted_cum_avg80yr_cosine=c(rep(NA,7),weighted_cum_avg80yr_cosine))
    new_dat = bind_rows(new_dat, new_cols)
  }
}

data3 = data2 %>%  left_join(new_dat)


ggplot(data3)+
  stat_summary(aes(x=year, y=cum_avg20yr_cosine, color=category), geom='pointrange', fun.data = "mean_cl_boot")

ggplot(data3)+
  stat_summary(aes(x=year, y=cum_avg80yr_cosine, color=category), geom='pointrange', fun.data = "mean_cl_boot")

ggplot(data3)+
  stat_summary(aes(x=year, y=weighted_cum_avg20yr_cosine, color=category), geom='pointrange', fun.data = "mean_cl_boot")

ggplot(data3)+
  stat_summary(aes(x=year, y=weighted_cum_avg80yr_cosine, color=category), geom='pointrange', fun.data = "mean_cl_boot")

ggplot(data3 %>% filter(year==1990))+
  stat_summary(aes(x=1, y=weighted_cum_avg80yr_cosine, color=category), geom='pointrange', fun.data = "mean_cl_boot")+
  stat_summary(aes(x=2, y=weighted_cum_avg20yr_cosine, color=category), geom='pointrange', fun.data = "mean_cl_boot", shape = 21)


# Stats: Cumulative Similarity -------------------------------------------------

data4 = data3 %>% 
  filter(year==1990) %>% 
  select(cue, target, category, year, starts_with("weighted")) %>% 
  pivot_longer(c(weighted_cum_avg20yr_cosine, weighted_cum_avg80yr_cosine), names_to = "age", values_to = "weighted_avg_sim") %>% 
  mutate(age=parse_number(age))

ggplot(data4)+
  stat_summary(aes(x=age, y=weighted_avg_sim, color=category), geom='pointrange', fun.data = "mean_cl_boot")

ggsave("./Rgraphs/WeightedAvgSimByAgeGroup.pdf", width = 7, height=7)

m4<-lmer(weighted_avg_sim ~ age*category + (1+age*category|cue), data= data4)
summary(m4)

## now look at the other way around? (older norms and how they would show up for YA)