

- Make sure you have Python 3 installed on your system.
  
- Clone the repository to your local environment and run the following command to install the dependencies:

      pip install -r requirements.txt


# Use

- To use the tool, run the log.py script in the terminal.
  
- You will be asked to provide the following parameters:

      Log File Name: Enter the name of the log file you want to analyze.

      Type of error to look for: Specify the type of error you want to identify (critical, warning, debug).

      Output File Name: Provide the name of the output file where the report will be saved.

      After running, the tool will generate a detailed report and save it to the specified output file.

# Possible Errors

- If the specified log file is not found, the tool displays an error message.
  
- If there are no errors of the specified type in the log file, the report indicates that no errors were found.

# Future Improvements

- [ ] Improve error detection by incorporating more regular expression patterns.
- [ ] Add support for different log file formats.
- [ ] Implement a graphical interface to facilitate interaction with the tool.
- [ ] Improve code modularity for easier maintainability and extensibility.
