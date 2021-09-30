#!/usr/bin/perl
#
#
use Data::Dumper;
#use IO::File;
#use File::Basename;
#use Date::Manip;
#use File::stat;
use File::Basename;
use Text::CSV;
#use Tie::IxHash;

if ( $#ARGV < 0 ) {
        print "Usage: $0 filename\n";
        exit;
} else {
        $oldfile=$ARGV[0];
}

($file,$dir,$ext) = fileparse($oldfile, qr/\.csv/);
$tmpfile = "${file}.tmp";
$newfile = "${file}fixed.csv";

my %month = ( JAN=>'01', FEB=>'02', MAR=>'03',
              APR=>'04', MAY=>'05', JUN=>'06',
              JUL=>'07', AUG=>'08', SEP=>'09',
              OCT=>'10', NOV=>'11', DEC=>'12' );

print "Converting Month to number\n";
open(FILE, "$oldfile") || die "Can not open $oldfile"; #read in a file
open (NEWFILE, ">$tmpfile") or print "Die" and die;
      while(<FILE>) {
          chop($_);
          next if /^#/;
          $_=~ s/\/(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\//\/$month{uc $1}\//g;
          $_=~ s/(,|;)[a-z]+\.*[a-z]*(,|;)/$torc\.ai/g;
          print NEWFILE "$_\n";
      }

close(FILE);
close (NEWFILE);
#unlink($tmpfile);

open(FILE, "$tmpfile") || die "Can not open $tmpfile"; #read in a file
open (NEWFILE, ">$newfile") or print "Die" and die;
while(<FILE>) {
        chop($_);
        next if /^#/;
        #       Issue key,Summary,Issue Type,Status,Priority,Assignee,Reporter,Creator,Created,Updated,Last Viewed,Description,Watchers,Watchers,Watchers,Watchers,Custom field (ITSM Issue Type),Custom field (Request Type),Comment,Comment,Comment,Comment,Comment,Comment,Comment,Comment,Comment,Comment,Comment,Comment,Comment

        if ( $_ =~/^IT-/) {
            ($isskey,$summary,$isstype,$status,$priority,$assignee,$reporter,$creator,$created,$updated,$lastviewed,$description,$watcher1,$watcher2,$watcher3,$watcher4,$itsm,$requestype,$comm1,$comm2,$comm3,$comm4,$comm5,$comm6,$comm7,$comm8,$comm8,$comm9,$comm10,$comm11,$comm12,$comm13) = split(/,/, $_);
            #    print "$isskey\n";
           print "description is $description\n";
           $assignee=~ s/$/\@torc\.ai/;
            $reporter=~ s/$/\@torc\.ai/;
            $creator=~ s/$/\@torc\.ai/;
            $watcher1=~ s/$/\@torc\.ai/i;
            $watcher2=~ s/$/\@torc\.ai/i;
            $watcher3=~ s/$/\@torc\.ai/i;
            $watcher4=~ s/$/\@torc\.ai/i;
            print NEWFILE "$isskey,$summary,$isstype,$status,$priority,$assignee,$reporter,$creator,$created,$updated,$lastviewed,$description,$watcher1,$watcher2,$watcher3,$watcher4,$itsm,$requestype,$comm1,$comm2,$comm3,$comm4,$comm5,$comm6,$comm7,$comm8,$comm8,$comm9,$comm10,$comm11,$comm12,$comm13\n";
    } else {
            print NEWFILE "$_\n";
    }
}
close(FILE);
close (NEWFILE);
unlink($tmpfile);
