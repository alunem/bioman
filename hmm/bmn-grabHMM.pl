#!/usr/bin/perl
use warnings;
use strict;
my $num_args = $#ARGV + 1;
if ($num_args != 1) {
  print "\nUsage: grabHMM.pl HMMdir \n";
  exit;
}


my $dir = $ARGV[0];

my @regexen;
my @kos = glob '*.ko';
for my $ko (@kos) {
    open my $DEF,   '<', $ko           or die "$ko: $!";
    open my $TOUCH, '>', "$ko.hmm" or die "$ko.hmm: $!";
    my $regex = q();
    while (<$DEF>) {
        chomp;
        $regex .= "$_|"
    }
    substr $regex, -1, 1, q();
    push @regexen, qr/$regex/;
}

# If you want the same order, uncomment the following 2 lines and comment the next 2 ones.
#
# for my $file (glob "$dir/*") {
#     $file =~ s%.*/%%;

opendir my $DIR, $dir or die "$dir: $!";
while (my $file = readdir $DIR) {
    next unless -f "$dir/$file";

    my %matching_files;
    open my $FH, '<', "$dir/$file" or die "$dir/$file: $!";
    while (my $line = <$FH>) {
        last if $. > 4;
        my @matches = map $line =~ /$_/ ? 1 : 0, @regexen;
        $matching_files{$_}++ for grep $matches[$_], 0 .. $#kos;
    }

    for my $i (keys %matching_files) {
        open my $OUT, '>>', "$kos[$i].hmm" or die "$kos[$i].hmm: $!";
        open my $IN,  '<',  "$dir/$file"        or die "$dir/$file: $!";
        print $OUT $_ while <$IN>;
        close $OUT;
    }
}
