import sys
from imageSynthesis import createFolderTest
import main
from main import main_function
print sys.argv[1],sys.argv[2]
folderNumber = createFolderTest([sys.argv[1],sys.argv[2]])
print folderNumber
main_function(testCaseNumber=folderNumber)