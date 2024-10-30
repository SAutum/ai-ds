################################################################################
# Script to install all required packages for the course MV04/MS00
# 
# Instructions:
# 1. Select all code in the script
# 2. Press the "Run" button in the top right corner of the editor
################################################################################

InstallPackages <- function(pkg) {
  # Function to install package
  InstallPackage <- function(x) {
    # Check if package is already installed
    check <- NULL
    suppressWarnings(if (!require(x, character.only = TRUE)) {
      install.packages(x)
      if (!require(x, character.only = TRUE)) {
        check <- FALSE
      }
    })
    
    # Check for error
    out <- NULL
    if (!is.null(check)) {
      out <- x
    } 
  }
  
  # Install list of packages
  lop <- unlist(sapply(pkg, InstallPackage))
  
  # Output message
  if (is.null(lop)) {
    cat("\nAll packages could be installed.")
  } else {
    cat("\nThe following packages could not be installed:", paste(lop, collapse = ", "))
  }
  
  # Return
  invisible(NULL)
}

# Try to install all packages
pkg <- c(
  "AER",
  "car", 
  "effects",
  "foreign",
  "lmtest",
  "plm",
  "ivreg",
  "rio",
  "wooldridge",
  "stargazer"
  )
InstallPackages(pkg)