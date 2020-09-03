library(reticulate)
library(shiny)
library(ggplot2)
library(DT)
use_python("python3")
# py_install(c("requests","pandas","datetime","json"))
# reticulate::virtualenv_create(envname = 'python3_env')
# reticulate::virtualenv_install('python3_env', packages = c("requests","pandas","datetime","json"), ignore_installed = T)
# reticulate::use_virtualenv('python3_env', required = T)

source_python("cb.py")

server <- function(input, output, session){
  output$tableDT <- DT::renderDataTable({datatable(data[,1:23]) %>% 
      formatPercentage("溢价率", 2)},
                                        options = list(paging=T),
                                        rownames=F)
}

ui <- fluidPage(
  DT::dataTableOutput("tableDT")
)

shinyApp(ui, server)