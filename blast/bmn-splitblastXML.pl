#!/usr/bin/env perl

undef $/;
$_ = <>;
$n = 0;

for $match (split(/(?=\<\?xml )/)) {
      open(O, '>blastXML.p' . ++$n);
      print O $match;
      close(O);
}
