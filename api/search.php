<?php

$file = '../catalogue.json';
$searchfor = '20210401A';

// the following line prevents the browser from parsing this as HTML.
header('Content-Type: text/plain');

// get the file contents, assuming the file to be readable (and exist)
$contents = file_get_contents($file);

// escape special characters in the query
$pattern = preg_quote($searchfor, '/');

// finalise the regular expression, matching the whole line
$pattern = "/^.*$pattern.*\$/m";

// search, and store all matching occurences in $matches
if(preg_match_all($pattern, $contents, $matches)){
  $myObj = implode("\n", $matches[0]);
}
else{
  echo "No matches found";
}

$myJSON = json_encode($myObj);

echo $myJSON;
?>
//{"l": "177.63", "snr": "15.58", "frb": "FRB 20210321A", "width": "-", "dec": "+26:11:24", "telescope": "CHIME", "utc": "2021-03-21 1:12:23", "ra": "5:07:50", "mjd": "59294.05027", "fluence": "-", "frequency": "600", "ref": "https://www.wis-tns.org/object/20210321a", "flux": "-", "dm": "412.46", "b": "-8.49"}
