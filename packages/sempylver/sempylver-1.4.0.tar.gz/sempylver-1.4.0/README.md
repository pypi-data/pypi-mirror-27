# sempylver
Simple semantic versioning in Python. A CLI tool.

## How to use this package:
1. Install Cygwin and **make sure to include the git package when installing**
2. Add Cygwin's bin directory to your path
3. Copy your .ssh folder to cygwin/home/USERNAME/.ssh
4. *pip install git+ssh://git@github.com/jeffrey-cochran/sempylver.git*
5. *sempylver config --author YOURNAME*
6. *sempylver config --email YOUREMAIL*
7. *sempylver config --working-directory DIR-CONTAINING-GIT-REPOS*
8. *sempylver track NAME-OF-GIT-REPO -s*
   This creates a version file named *__version__* with format X.X.X  
   **If you do not want to modify your setup file** to retrieve the version number from the version file, omit *-s* from the above command  
9. Whenever committing a tracked repo...
   Sempylver will automatically increment (+=1) the Y in the version number X.X.Y  
   Including '-m' **in the commit message** will increment (+=) the Y in the version number X.Y.Z and set Z==0  
   Including '-M' **in the commit message** will increment (+=) the Y in the version number Y.Z.Z and set Z==0  
   Including '-s' **in the commit message** will skip version incrementation, and keep the current version
   Including '-t' **in the commit message** will tag the commit with the version number