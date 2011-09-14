<!doctype html>
<!--[if lt IE 7 ]> <html class="no-js ie6" lang="en"> <![endif]-->
<!--[if IE 7 ]>    <html class="no-js ie7" lang="en"> <![endif]-->
<!--[if IE 8 ]>    <html class="no-js ie8" lang="en"> <![endif]-->
<!--[if (gte IE 9)|!(IE)]><!--> <html class="no-js" lang="en"> <!--<![endif]-->
<head>
  <meta charset="utf-8">

  <title>Wordpress Integration Tool beta</title>
  <meta name="description" content="">

  <link rel="stylesheet" href="css/style.css">
  <script src="js/libs/modernizr-1.7.min.js"></script>
<script type="text/javascript" src="http://code.jquery.com/jquery-latest.js"></script>
<script type="text/javascript" src="http://view.jquery.com/trunk/plugins/validate/jquery.validate.js"></script> 
<script src="asmselect/asmselect/jquery.asmselect.js" type="text/javascript"></script>
<link href="asmselect/asmselect/jquery.asmselect.css" rel="stylesheet" />

  <script type="text/javascript">
    $(document).ready(function() {
      $("#getParse").validate();
    });
  </script>
  
  <script type="text/javascript">

	$(document).ready(function() {
		$("select[multiple]").asmSelect({
			addItemTarget: 'bottom',
			highlight: true
		});
		
	}); 

</script>
</head>

<body>

  <div id="container">
    <header>
    	<div id="heading">
		<h2 id="title">Wordpress Integration Tool <!-- <span class="smaller">beta</span> --> </h2><br>
		<p>What you need to add a blog to your existing site</p>
		</div>
    </header>
    <div id="main" role="main">
    	
    	<div id = "content">

		<?php 
		$client_ip = $_SERVER['REMOTE_ADDR'];
				$clicked = $_GET['clicked'];
				if(!$clicked){
					include("step1.php");
				}
				else if($clicked == "step2"){
						include("step2.php");
				}else if($clicked == "step3"){
						include("step3.php");
				}else if($clicked == "step4"){
						include("step4.php");
				}
				?>
				</div>
		<div id = "process">
    		<h3>The Integration Process:</h3><br>
			<ul>
			<li><b>This tool is meant to be used by website admins or editors who know how to read HTML/PHP</b></li>
			<li>Enter the URL of the page you wish to be emulated</li>
			<li>If you use HTML5 tags, you might click Yes on option 2</li>
			<li>On Step 2, you must select the appropriate HTML structure elements on your site</li>
			<li>On Step 3 you will be able to download your files</li>
			</ul>
		</div>
    </div>
    <footer>
		<div id="client_ip">
			<p> Your IP Address is: <?php echo $client_ip;?></p>
		</div>

    </footer>
  </div> <!-- eo #container -->


</body>
</html>
