#################################################
library(animint2)
library(gert)

path_name <- '~/Downloads/temp_name.csv'
plotmode<- '' #select the plot model: 'Overall': plot four in one graph, 
#other: plot in 4 separate graphs

path <- '~/Downloads/temp.csv'

path_origin <- '~/Downloads/temp-origin.csv'
path_overlapped <- '~/Downloads/temp-overlapped.csv'
path_heatmap <- '~/Downloads/temp-heatmap.csv'
path_colormap <- '~/Downloads/temp-colormap.csv'

title_animint <- 'Animated2Grad: CAM-COVID-19-chest-X-rays-ViT-
visualization-140px-696cases' #the title of your plot
source_url <- 'https://github.com/TyBruceChen/Animinted2GradCAM' 

#the source of your related code URL, just for increasing reproductivity.
github_push <- TRUE  #set TRUE to upload this to your github repository
github_repo <- 'Animated2GradCAM-COVID19-Chest-X-ray-ViT-V5-140px-609Case-animated2pages'
#the name of github repository you want to upload

#######################################################
#* This is part tutorial is from https://github.com/animint/animint2
#If you are first try to upload github repository:
#A GitHub token is required to create and push to a new repository. 
#To create a GitHub token, follow these steps:
  #1. Go to https://github.com/settings/tokens/new?scopes=repo&description=animint2pages
#2. Confirm your password if prompted.
#3. Ensure that the 'repo' scope is checked.
#4. Click 'Generate token' at the bottom of the page.
#5. Copy the generated token.
#After creating the token, you can set it up in your R environment by running: 
  #Sys.setenv(GITHUB_PAT="yourGithubPAT") 
#gert::git_config_global_set("user.name", "yourUserName") 
#gert::git_config_global_set("user.email", "yourEmail")

git_token <- '' #bind the generated toekn
Sys.setenv(GITHUB_PAT= git_token) 
gert::git_config_global_set("user.name", "username") 
gert::git_config_global_set("user.email","bonded email")

########################################################

##########################################
name_df <- read.csv(path_name)
if (plotmode == 'Overall'){
  img_df <- read.csv(path)
}else{
  df_origin <-read.csv(path_origin)
  df_overlapped <-read.csv(path_overlapped)
  df_heatmap <-read.csv(path_heatmap)
  df_colormap <- read.csv(path_colormap)
}

ImageTypeLabeller <- function(type){
  paste("Type: ",type)
}

plot_img_itr <- ggplot(name_df) +
  facet_grid(.~img_type, 
             labeller = as_labeller(ImageTypeLabeller), #self-defined labeller, so that I can have own title for the facet type
             scales = "free",
             space = 'free')+ 
  #theme(legend.position="none") +
  theme_animint(width=1650, height=400)+
  geom_point(aes(Index,Confidence....,color = Type)) +
  geom_tallrect(aes(xmin = Index- 0.5, 
                    xmax = Index + 0.5, 
                    fill = Type)
                , alpha = 0.5
                , clickSelects = "img_index") +
  scale_x_continuous("Image Index") +
  labs(x = "Image Index",y = "Confidence (%)", title = "Test Set")

if (plotmode == 'Overall'){
  plot <- ggplot() +
    theme(legend.position="none") +
    scale_fill_identity() + 
    geom_tile(aes(y = img_df$row.height.
                  , x = img_df$column.width.
                  , fill = img_df$color.hex.
                  ,color = img_df$color.hex.)  #fill the white gap between tiles
              ,showSelected = "img_index",
              data = img_df,
              color = NA) +
    coord_equal() + 
    theme_bw() +
    theme(axis.ticks = element_blank(),
          axis.title.x = element_blank(),
          axis.title.y = element_blank())+
    theme_animint(width=600, height=600) +
    labs(x = "Origin/Processed",y = "", title = "Animinted2GradCAM: Origin(top left)/Overlapped Grad-CAM(top right)/Heatmap(bottom left)/Colormap(bottom left)")
  ##############################
  animint_post = animint(title = title_animint,
                         plot_img_itr, plot,
                         source = source_url)
  
  animint_post  #display and create anmint plot
  
}else{
  plot_origin <- ggplot() +
    theme(legend.position="none") +
    scale_fill_identity() + 
    geom_tile(aes(y = df_origin$row.height.
                  , x = df_origin$column.width.
                  , fill = df_origin$color.hex.
                  ,color = df_origin$color.hex.)
              ,showSelected = "img_index",
              data = df_origin,
              color = NA) +
    coord_equal() + 
    theme_bw() +
    theme(axis.ticks = element_blank(),
          axis.title.x = element_blank(),
          axis.title.y = element_blank())+
    theme_animint(width=350, height=350) +
    labs(x = "", y = "",title = "Origin")
  
  plot_overlapped <- ggplot() +
    theme(legend.position="none") +
    scale_fill_identity() + 
    geom_tile(aes(y = df_overlapped$row.height.
                  , x = df_overlapped$column.width.
                  , fill = df_overlapped$color.hex.
                  ,color = df_overlapped$color.hex.)
              ,showSelected = "img_index",
              data = df_overlapped,
              color = NA) +
    coord_equal() + 
    theme_bw() +
    theme(axis.ticks = element_blank(),
          axis.title.x = element_blank(),
          axis.title.y = element_blank())+
    theme_animint(width=350, height=350) +
    labs(x = "", y = "",title = "Overlapped Grad-CAM")
  
  plot_heatmap <- ggplot() +
    theme(legend.position="none") +
    scale_fill_identity() + 
    geom_tile(aes(y = df_heatmap$row.height.
                  , x = df_heatmap$column.width.
                  , fill = df_heatmap$color.hex.
                  ,color = df_heatmap$color.hex.)
              ,showSelected = "img_index",
              data = df_heatmap,
              color = NA) +
    coord_equal() + 
    theme_bw() +
    theme(axis.ticks = element_blank(),
          axis.title.x = element_blank(),
          axis.title.y = element_blank())+
    theme_animint(width=350, height=350) +
    labs(x = "", y = "",title = "Heatmap")
  
  plot_colormap <- ggplot() +
    theme(legend.position="none") +
    scale_fill_identity() + 
    geom_tile(aes(y = df_colormap$row.height.
                  , x = df_colormap$column.width.
                  , fill = df_colormap$color.hex.
                  ,color = df_colormap$color.hex.)
              ,showSelected = "img_index",
              data = df_colormap,
              color = NA) +
    coord_equal() + 
    theme_bw() +
    theme(axis.ticks = element_blank(),
          axis.title.x = element_blank(),
          axis.title.y = element_blank())+
    theme_animint(width=350, height=350) +
    labs(x = "", y = "",title = "Colormap")
  
  animint_post = animint(
          title = title_animint,
          controller = plot_img_itr,
          origin = plot_origin,
          overlapped = plot_overlapped,
          colormap = plot_heatmap,plot_colormap,
          source = source_url)
  
  animint_post  #display and create anmint plot
}

animint_post = animint(
  title = title_animint,
  plot = ggplot(),
  source = source_url)

if (github_push == TRUE){
  animint2pages(animint_post,
                github_repo = github_repo, #push to newly specified repository
                commit_message = "This is pushed by animint2pages.")
}

#########################################


