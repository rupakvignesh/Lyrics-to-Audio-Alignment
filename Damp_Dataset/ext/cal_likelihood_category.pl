

my $path_to_lab = $ARGV[0]."/*\.lab";
@filelist = `ls $path_to_lab`;
$sum_nasal=0;
$prob_nasal=0;
$sum_fric=0;
$prob_fric=0;
$sum_affric=0;
$prob_affric=0;
$sum_semi=0;
$prob_semi=0;
$sum_v=0;
$prob_v=0;
$sum_stop=0;
$prob_stop=0;
$sum=0;
$prob=0;

print "No. of files: ";
print scalar(@filelist);
foreach $file (@filelist) {
	chomp($file);
	open(FILE,"$file") || die("Not opening $file because $!");
		@lines=<FILE>;
		foreach $line (@lines) {
			$line =~ s/(^\s+|\s+$)//g;
			@cols = split('\s+',$line);
			#$nf = ($cols[1] - $cols[0])/50000;
			#$avgl = $cols[3]/$nf;
			$avgl = $cols[3];
			$sum++;
			$prob+=$avgl;	
			if ($cols[2] eq "n" || $cols[2] eq "nj" || $cols[2] eq "nx" || $cols[2] eq "nd" || $cols[2] eq "m"  || $cols[2] eq "ng" || $cols[2] eq "mq")
			{
				$sum_nasal++;
				$prob_nasal+=$avgl;
			}
			elsif ($cols[2] eq "y" || $cols[2] eq "r" || $cols[2] eq "l" || $cols[2] eq "w" || $cols[2] eq "zh" || $cols[2] eq "lx" || $cols[2] eq "rx")
			{
				$sum_semi++;
				$prob_semi+=$avgl;
			}
			elsif ($cols[2] eq "sx" || $cols[2] eq "s" || $cols[2] eq "sh" || $cols[2] eq "f" || $cols[2] eq "z")
			{
				$sum_fric++;
				$prob_fric+=$avgl;
			}
			elsif ($cols[2] eq "c" || $cols[2] eq "ch" || $cols[2] eq "jh" || $cols[2] eq "j")
                        {
                                $sum_affric++;
                                $prob_affric+=$avgl;
                        }
			elsif ($cols[2] eq "b" || $cols[2] eq "bh" || $cols[2] eq "d" || $cols[2] eq "dh" || $cols[2] eq "dx" || $cols[2] eq "dxh" || $cols[2] eq "dxhq" || $cols[2] eq "dxq" || $cols[2] eq "g" || $cols[2] eq "gh" || $cols[2] eq "gq" || $cols[2] eq "k" || $cols[2] eq "kh" || $cols[2] eq "khq" || $cols[2] eq "kq" || $cols[2] eq "p" || $cols[2] eq "t" || $cols[2] eq "th" || $cols[2] eq "tx" || $cols[2] eq "txh" || $cols[2] eq "ph" || $cols[2] eq "c")
			{
				$sum_stop++;
				$prob_stop+=$avgl;
			}
			elsif ($cols[2] eq "a" || $cols[2] eq "i" || $cols[2] eq "u" || $cols[2] eq "e" || $cols[2] eq "o"|| $cols[2] eq "ax" || $cols[2] eq "ae" || $cols[2] eq "aemq" || $cols[2] eq "amq" || $cols[2] eq "emq" || $cols[2] eq "imq" || $cols[2] eq "omq" || $cols[2] eq "umq")
			{
				$sum_v++;
				$prob_v+=$avgl;
			}
			elsif ($cols[2] eq "aa" || $cols[2] eq "ii" || $cols[2] eq "uu" || $cols[2] eq "ee" || $cols[2] eq "oo" || $cols[2] eq "aamq" || $cols[2] eq "uu" || $cols[2] eq "ee" || $cols[2] eq "oo")
			{
				$sum_v++;
				$prob_v+=$avgl;
			}	
			elsif ($cols[2] eq "ai" || $cols[2] eq "ei" || $cols[2] eq "au" || $cols[2] eq "ou" || $cols[2] eq "rq")
			{
				$sum_v++;
				$prob_v+=$avgl;
			}
		}
	close(FILE);
} 
$prob_nasal/=$sum_nasal;
$prob_fric/=$sum_fric;
$prob_affric/=$sum_affric;
$prob_semi/=$sum_semi;
$prob_stop/=$sum_stop;
$prob_v/=$sum_v;
$prob/=$sum;

print "\nLikelihood scores of HMM Segmentation: \n";
print "Semivowels: $prob_semi\n";
print "Stop Consonants: $prob_stop\n";
print "Fricatives: $prob_fric\n";
print "Affricates: $prob_affric\n";
print "Vowels: $prob_v\n";
print "Nasals: $prob_nasal\n";
print "Total: $prob\n\n";
