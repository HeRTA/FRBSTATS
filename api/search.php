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
if (preg_match_all($pattern, $contents, $matches)) {
  $entry = implode('\n', $matches[0]);
  echo $entry
  $myObj = str_replace('\\', '', $entry);
}

$myJSON = json_encode($myObj);

echo $myJSON;
?>
