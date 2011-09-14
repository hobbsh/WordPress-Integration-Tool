#!/usr/bin/perl -w
use CGI;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use CGI::Session ( '-ip_match' );
use HTML::TreeBuilder;
use LWP::Simple;
use HTML::Element;
use HTML::TagParser;
use Socket;
use Unicode::Escape qw(escape unescape);
use HTML::Entities;
use MIME::Base64::URLSafe;
use URI;
use URI::Escape;
use DBI();
use strict;

#DB connect settings
my $host = "localhost";
my $database = "wp_template";
my $user = "hobbsh";
my $pw = "Myp4ssw0rd";
my $table = "sites";
my $dbh = DBI->connect("DBI:mysql:database=wp_template; host=localhost", 
			$user, $pw, {RaiseError=> 1});

		my $query = new CGI;
	
	#get domain name from form, get HTML page with get(), translate hostname to IP with IO::Socket 
	# and escape HTML to insert into DB
		my $url = $query->param('url');
		my $page = get($url) or die $!;
		#$url =~ s/^http:\/\/www.|http:\/\///gi;
		my $www = URI->new($url);
		my $host = $www->host;
		my $addr = inet_ntoa(inet_aton($host)); 			
		my $es_page = $query->escape($page);	
		my $html5 = $query->param('head');
	        my $e_addr = urlsafe_b64encode($addr);
	                $e_addr = urlsafe_b64encode($e_addr);

		my $select = $dbh->prepare("SELECT * FROM $table WHERE IP =?");
			$select->execute($addr);

		if($select->rows) ##check if IP exists already, if so update record
			{
				my $update_rows = $dbh->prepare("UPDATE $table SET domain=?,file=? WHERE IP = ?");
				$update_rows->execute($url,$es_page,$addr);
			}
		else #else insert IP, domain name, and escaped HTML code into database
			{
				my $insert = $dbh->prepare("INSERT INTO $table (IP, domain, file) VALUES (?,?,?)");
				$insert->execute($addr,$url,$es_page);
			}
	#retrieve page to parse and strip text
		my $sth = $dbh->prepare("SELECT file FROM $table WHERE IP = '$addr'");
		$sth->execute();
		my $ref = $sth->fetchrow_hashref();								
		my $file = uri_unescape("$ref->{'file'}");

		open(my $fh, "+>", "tmp/$e_addr.txt") or die $!;
		print $fh $file;
		
	#write HTML to temp file
			close($fh);
	
	#temp file to Perl object $tmp for parse
		my $tmp = "tmp/$e_addr.txt";
		
		if($html5 eq "yes"){ #HTML5 tags not recognized by parser?
			my $tree = HTML::TreeBuilder->new();
                     	$tree->parse_file($tmp);

			my $header = $tree->look_down("_tag","body","header");
			my $o_header = $header->as_HTML('<>&',"\t");
			
			my $head = $tree->look_down('_tag','head');
                        my $o_head = $head->as_HTML('<>&',"\t");

			my $update = $dbh->prepare("UPDATE $table SET head=?,top=? WHERE IP=?");
                        $update->execute($o_head, $o_header, $addr);
			
			$tree = $tree->delete;

		}
		elsif($html5 eq "no"){	
			#get Div IDs	
			my $tree = HTML::TreeBuilder->new();
	                $tree->parse_file($tmp);
                	$tree->elementify;

			my $html = HTML::TagParser->new($tmp);
			 my @list = $html->getElementsByTagName("div");
               		 #my $update = $dbh->prepare("UPDATE $table SET divs=? WHERE IP='$addr'");
               		 my @divs;
                	foreach my $elem (@list){
                         push @divs, ($elem->id(),$elem->getAttribute('class'));
                       	 }
               		 my $ids = join(";",@divs);
			my $head = $tree->look_down('_tag','head');
                        my $o_head = $head->as_HTML('<>&',"\t");

			#update file in DB with new page stripped of text content
			my $update = $dbh->prepare("UPDATE $table SET head=?,divs=? WHERE IP=?");
			$update->execute($o_head,$ids, $addr);
		$tree = $tree->delete;

		}
		else{
			print "You didn't select 'yes' or 'no' on step 1";
		}

		#re-encode IP address twice with base64
#		my $e_addr = urlsafe_b64encode($addr);
#		$e_addr = urlsafe_b64encode($e_addr);
		
		#delete tmp file, tree, and disconnect DB session to free resources
	#	unlink($tmp);		
		$dbh->disconnect();

		#redirect to step2.php passing encoded IP as QUERY STRING to essentially track session
		print $query->header(-location=>"../?id=$e_addr&html5=$html5&clicked=step2");
