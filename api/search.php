<?php

$file = '../catalogue.json';
$searchfor = '20210401A';

// Prevent HTML parsing
header('Content-Type: text/plain');

// Grab file conents
$content = file_get_contents($file);

// Escape special chars
$pattern = preg_quote($searchfor, '/');

// Finalize refex, matching line
$regexPattern = "/^.*$pattern.*\$/m";

// Search and store matching occurence in $match
if (preg_match_all($regexPattern, $content, $match)) {
  $entry = implode('\n', $match[0]);

  // Delete trailing comma
  $entry = substr($entry, 0, -1);
  
  // Output search result
  echo $entry;
}

//$myJSON = json_encode($myObj);
?>
