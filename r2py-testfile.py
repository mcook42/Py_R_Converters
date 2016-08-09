# David Millar - July 17, 2016
# dave.millar@uwyo.edu

# NOTES: - ggplot code at the end is just used for evaluation and plotting, and can be omitted 
#          or commented out when integrating this module into TREES_Py_R
#        - Non-linear least squares regression are currently used to determine empirical model
#          parameter estimates.  

#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#
#                                                                                  #
# Module for  estimating the Gs_ref parameter using stomatal conductance           #  
# and vapor pressure deficit data.                                                 #
#                                                                                  #
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::;;:::::::#


# clear everything out of memory
#rm(list=ls())

# call to ggplot package
library(ggplot2)

#-----------------------------------------------------------------------------------------------------
# set the current working directory - make sure to change this as needed
#

# read in the vapor pressure deficit (VPD) and non-water-stressed, non-photosynthesis-limited 
# canopy conductance (Gs) calculated from sap flux measurements.

# D = atmospheric vapor pressure deficit (kPa)
# Gs = non-water-stressed, non-photosynthesis-limited stomatal conductance (mol m^-2 s^-1)

Gs_data  =  read.csv("PICO_atm_demand_data.csv")
names(Gs_data)=c("number","D_obs", "Gs_obs")

D_obs  = Gs_data["D_obs"]
Gs_obs  =  Gs_data["Gs_obs"]


#-----------------------------------------------------------------------------------------------------

#::::::::::::::::::::::::::::::::#
#   Gs_ref estimation function   #
#::::::::::::::::::::::::::::::::#

def Gs_ref_func(D_obs,Gs_obs):  
  # fit Gs_ref parameter to observed Gs and D data
  
  Gs_ref.fit  =  nls(Gs_obs ~ Gs_ref - (0.6*Gs_ref)*log(D_obs), start = list(Gs_ref = 0.1))
  Gs_ref.paras  =  coef(Gs_ref.fit)
  Gs_ref  =  Gs_ref.paras[1]
  
  return(Gs_ref)
  


#-----------------------------------------------------------------------------------------------------

#::::::::::::::::::::::::::::::::::::::::::::::::#
#   create timeseries plot of obs and sim sfd    #
#::::::::::::::::::::::::::::::::::::::::::::::::#
# 
# Gs_ref <- Gs_ref_func(D_obs,Gs_obs)
# 
# # simulate Gs in absence of water supply and/or photosynthetic limitation
# Gs_sim <- Gs_ref - (0.6*Gs_ref)*log(D_obs)
# 
# Gs_obs <- Gs_obs
# D_obs <- D_obs
# 
# #calculate R^2
# eval = summary(lm(Gs_sim~Gs_obs))
# R2 <- eval$r.squared
# R2
# 
# ggdata <- cbind.data.frame(D_obs,Gs_sim,Gs_obs)
# 
# Gs_test_plot <- ggplot(ggdata) + 
#   geom_point(aes(x=D_obs, y=Gs_obs, shape ='observed', linetype = 'observed', color ='observed',size ='observed')) + 
#   geom_line(aes(x=D_obs, y=Gs_sim, shape ='simulated', linetype = 'simulated', color ='simulated',size ='simulated')) +
#   scale_shape_manual(values=c(19, NA)) + 
#   scale_linetype_manual(values=c(0, 1)) +
#   scale_size_manual(values=c(4,1.5)) +
#   scale_color_manual(values=c("blue","springgreen3")) +
#   xlab("vapor pressure deficit (kPa)") + 
#   ylab("canopy conductance") +
#   ylab(expression(paste("canopy conductance (mol ", m^-2," ",s^-1,")"))) +
#   ggtitle(expression(paste("fitting ", Gs[ref]))) +
#   theme(axis.text=element_text(size=18),
#         strip.text=element_text(size=18),
#         title=element_text(size=18),
#         text=element_text(size=18),
#         legend.text=element_text(size=18),
#         legend.title=element_blank(),
#         legend.key = element_blank())
# 
# Gs_test_plot
# 
# #-----------#
# # save plot #
# #-----------#
# 
# #ggsave("CP_sf_decline_obs_and_sim_timeseries.png",width=10,height=4,units='in',dpi=500)
# #dev.off()
# 
# 
