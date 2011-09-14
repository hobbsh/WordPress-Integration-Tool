#!/usr/bin/perl -w
use CGI;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use CGI::Session ( '-ip_match' );
use HTML::TreeBuilder;
use LWP::Simple;
use HTML::Element;
use HTML::TagParser;
use IO::Socket;
use URI::Escape;
use MIME::Base64::URLSafe;
use HTML::Entities;
use DBI();
use String::Util qw(trim);
use strict;

my $host = "localhost";
my $database = "wp_template";
my $user = "hobbsh";
my $pw = "Myp4ssw0rd";
my $table = "sites";
my $dbh = DBI->connect("DBI:mysql:database=wp_template; host=localhost", 
			$user, $pw, {RaiseError=> 1});

		my $cgi = new CGI;

	#get encoded IP from URL Query String and decode
		my $addr = $cgi->param('sid');
		my $navid = $cgi->param('nav');
			$navid = trim($navid); 
		my $decip = urlsafe_b64decode($addr);
		   $decip = urlsafe_b64decode($decip);
		my @wrapper = $cgi->param('divs');
		
		#select file that matches IP address and unescape HTML
                #my $dbout = $dbh->prepare("SELECT file FROM $table WHERE IP = '$decip'");
                #	$dbout->execute();
                #my $ref = $dbout->fetchrow_hashref();
               # my $file = uri_unescape("$ref->{'file'}");
		
		#open(my $fh, "+>", "tmp/$addr.txt") or die $!;
                #print $fh $file;
                #close($fh);
		
		my $tree = HTML::TreeBuilder->new();
		my $tmp = "tmp/$addr.txt";
                $tree->parse_file($tmp);

		my $update = $dbh->prepare("UPDATE $table SET nav=? WHERE IP = '$decip'");
		my $divnav = $tree->look_down(_tag=>'div', id=>"$navid");
			my $o_nav = $divnav->as_HTML('<>&',"\t");
			#$o_nav = $cgi->escape($o_nav);
		$update->execute($o_nav);
	
		#re-encode IP address to pass in URL as QUERY STRING and free server resources
		my $e_addr = urlsafe_b64encode($decip);
		$e_addr = urlsafe_b64encode($e_addr);		
		unlink($tmp);		
		$tree = $tree->delete;
		$dbh->disconnect();	
		
		print $cgi->header(-location=>"../?id=$e_addr&clicked=step3");

