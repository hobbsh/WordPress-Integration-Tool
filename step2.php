


<?php
$con = mysql_connect("localhost","hobbsh","Myp4ssw0rd");
if (!$con)
  {
  die('Could not connect: ' . mysql_error());
  }

?> 
<h3>Step 2</h3>
<ul> 
	<li>Here you need to tell the tool how your webpage is laid out.</li>
	<li>Select your wrapper DIV names below - this will be the outermost DIV(s) on your page</li>
	<li>They are typically named with variations of "wrapper"</li>
</ul>
<?php
	$IP = $_GET['id'];
	$d_IP = url_base64_decode($IP);
	$d_IP = url_base64_decode($d_IP);

function url_base64_decode(&$str="")
{
    return base64_decode(strtr(
            $str, 
            array(
                '.' => '+',
                '-' => '=',
                '~' => '/'
            )
        ));
}
?>
<?php 
mysql_select_db("wp_template", $con);

$result = mysql_query("SELECT * FROM sites
WHERE IP='$d_IP'");


$row = mysql_fetch_array($result);
$data = explode(";",$row['divs']);
echo "<form method=\"POST\" action=\"cgi-bin/ins.cgi\">";
echo "<p>Select your outermost div ID(s)</p>";
echo "<select name=\"divs\" title=\"Please select your wrapper DIV(s)\" width=\"400px\" multiple=\"multiple\">";
foreach($data as $key => $value){
	echo "\t\t<option>".$value."</option>\n";
}
echo "\t</select>\n";
echo "\t<select name=\"nav\" title=\"Pleas select your navigation div ID\" multiple=\"multiple\">\n";
foreach($data as $key => $values){
	echo "\t\t<option>".$values."</option>\n";
}
echo "\t</select>\n";
echo "<input name=\"sid\" type=\"hidden\" value=\"$IP\"/>";
echo "<p><input type=\"submit\" name=\"step3\" value=\">> Step 3\" /></p>\n";
echo "</form>\n";

echo "<p>IP is: ".$d_IP."</p>";

?>

