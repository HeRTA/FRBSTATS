<?php

$catalogue = '../catalogue.json';

$searchfor = $_GET['frb'];

// Neglect 'FRB' prefix, underscores and spaces
$searchfor = str_ireplace(["frb", " ", "_"], "", $searchfor);

// Prevent HTML parsing
header('Content-type: application/json');

// Grab file conents
$content = json_decode(file_get_contents($catalogue), true);

// Escape special chars
$pattern = preg_quote($searchfor, '/');

// Finalize refex, matching line
$regexPattern = "/^.*$pattern.*\$/m";

$return_array = [];

// Search and store matching occurence in $match
foreach($content as $key){
  if(str_contains($key['frb'],$pattern)){
    $return_array[] = $key;
  }
}

echo json_encode($return_array);

?>
