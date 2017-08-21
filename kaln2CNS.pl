#! /usr/bin/perl -w
use strict;

die "must provide kaln file\nusage: \$kaln2CNS.pl *.kaln <# of alignments in gap> > *.CNS.fa\n" unless($ARGV[0]);
open(ALN,"$ARGV[0]");
my $outFile='out.cs.fa';
if($ARGV[0]=~ /(\S+)\.kaln/){
    $outFile=$1 . '.cs.fa';
}

my $select=2 unless($select=$ARGV[1]);

open(OUT,">$outFile");
my %aln;
my $space=0;
my $c=0;
my $header=<ALN>;
while(<ALN>){
    chomp;
    if($_=~ /\S+/){
	$space=1;
    }
    else{
	$space=0;
	$c=0;
    }
    if($space==1){
	$_=~ /^(\S+)\s+(\S+)/;
	my($id,$seq)=($1,$2);
	$c++;
	$aln{$c}=$seq unless($aln{$c}.=$seq);
    }
}
close ALN; 

my %cs;
foreach my $id(keys %aln){
    my @seq=split(//,$aln{$id});
    my $sqC=@seq;

    for(my $x=0;$x<@seq;$x++){
	$cs{$x}{$seq[$x]}=1 unless($cs{$x}{$seq[$x]}++);
    }
}
my $csSeq;
foreach my $base(sort{$a<=>$b}keys %cs){
    my @sortOrder=sort{$cs{$base}{$b}<=>$cs{$base}{$a}}keys %{$cs{$base}};
    my $sN=@sortOrder;
    if($sortOrder[0] eq '-'){
	if($sN>1){
	    if($cs{$base}{$sortOrder[1]} > $select){ 
		$csSeq.=$sortOrder[1];
	    }
	}
    }
    else{
	$csSeq.=$sortOrder[0];
    }
}
print OUT ">$outFile\n$csSeq\n";
close OUT;
