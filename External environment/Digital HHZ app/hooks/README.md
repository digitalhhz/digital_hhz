# Information
It is assumed that you are familiar with the ionic framework. For basic information visit: https://ionicframework.com/docs/intro/tutorial/ and https://ionicframework.com/docs/v1/guide/preface.html.

For compatibility reasons, please use the following package and executable versions before trying to deploy and run the app:
- Node.js: 6.11.5
- npm: 3.10.10
- Cordova: 7.1.0
- Ionic: 3.19.0

You can find specific Node.js distros here: https://nodejs.org/dist/. You can install a specific package using the following command (and Git Bash): "npm install -g package@version". E.g. use "npm install -g cordova@7.1.0" to install Cordova version 7.1.0.

When running the app using "ionic serve", the folder "node_modules" and additional files are created. DO NOT push these into the GitHub repository as this will cause problems with synchronization. Same applies to platforms added using "ionic cordova platform add android" and "ionic cordova platform add ios". E.g. make use of gitignore to ignore these files. 