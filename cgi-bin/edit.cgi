#!/usr/bin/perl -w
use CGI;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use CGI::Session ( '-ip_match' );
use HTML::TreeBuilder;
use LWP::Simple;
use HTML::Element;
use HTML::TagParser;
use Socket;
use URI::Escape;
use HTML::Entities;
use MIME::Base64::URLSafe;
use URI;
use DBI();
use Encode;
use strict;

 
#DB connect settings
my $host = "localhost";
my $database = "wp_template";
my $user = "hobbsh";
my $pw = "Myp4ssw0rd";
my $table = "sites";
my $dbh = DBI->connect("DBI:mysql:database=wp_template; host=localhost", 
			$user, $pw, {RaiseError=> 1});

		my $cgi = new CGI;

		my $addr = $cgi->param('sid');
		my $decip = urlsafe_b64decode($addr);
		  	 $decip = urlsafe_b64decode($decip);
#		print "$decip";
my $sth = $dbh->prepare("SELECT nav FROM $table WHERE IP = '$decip'");
		$sth->execute();
		my $ref = $sth->fetchrow_hashref();
		my $myNav = uri_unescape($ref->{'nav'});

my $dir = "../templ_files/";
opendir(BIN, $dir) or die "Can't open $dir: $!";
my @array = grep { -T "$dir/$_" } readdir BIN;
my $ins_nav = "insertnavhere";
my $file = "header.php";


	my $tree = HTML::TreeBuilder->new();
	$tree->parse_file("$dir"."$file");
	$tree->pos($ins_nav);
	my $output = $tree->push_content($myNav);
	$output = $output->as_HTML('<>&',"\t");
	
my $select = $dbh->prepare("SELECT * FROM output WHERE IP =?");
			$select->execute($decip);
if($select->rows){
	my $update = $dbh->prepare("UPDATE output SET header=? WHERE IP = ?");
	$update->execute($output,$decip);
}
else{
	my $insert  = $dbh->prepare("INSERT INTO output (IP,header) VALUES (?,?)");
	$insert->execute($decip,$output);
}


	
	my $e_addr = urlsafe_b64encode($decip);
	$decip = urlsafe_b64encode($e_addr);
	
	$tree = $tree->delete;
	$dbh->disconnect();

	print $cgi->header(-location=>"../?id=$e_addr&clicked=step4");
