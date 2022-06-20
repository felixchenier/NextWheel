//download.h
const char DOWNLOAD_HTML_TEMPLATE[] PROGMEM = R"====(
<!DOCTYPE HTML>
<html>
<head>
    <title>NextWheel SDCard Browser</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
    <h2>File Reader
    <br>
    <br> %URLLINK%
    <br>
    <br>
    <a href=/index.htm >Main Menu</a></h2><br>
</body>
</html>
)====";