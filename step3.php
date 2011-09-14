

<?php
$con = mysql_connect("localhost","hobbsh","Myp4ssw0rd");
if (!$con)
  {
  die('Could not connect: ' . mysql_error());
  }

?> 
<h3>Step 3</h3>
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
 echo "<form id=\"step3\" action=\"cgi-bin/edit.cgi\">";
echo "<input type=\"submit\" name=\"step4\" value=\"continue\"/>";
echo "<input name=\"sid\" type=\"hidden\" value=\"$IP\"/>";

echo "</form>\n";


?>

