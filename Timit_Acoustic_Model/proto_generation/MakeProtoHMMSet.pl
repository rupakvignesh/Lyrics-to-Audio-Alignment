#!/usr/bin/perl
#
# This script can be used to produce prototype HMMSets for
# PLAINHS, TIEDHS and DISCRETEHS systems
#

# Global Variables
$nStates=0;                         # Number of active HMM states
$nStreams=0;                        # Number of streams
$vecSize=0;                         # Size of feature vector
$pKind="";                          # Parameter kind
$cKind="";                          # Covariance kind
$hsKind="";                         # System kind
$outDir="";                         # Output HMMSet directory
$configParams;                      # Global store of config parameters


#***************************** START MAIN ***********************************
$|=1; #Force buffer flush on STDOUT

if ($ARGV[0]){
    &ReadPCF();
    &SetVars();
    &TestDirEmpty();
    &WriteHSet();
}else{
    print "USAGE: MakeProtoHMMSet ConfigFile\n";
}

#******************************* END MAIN *********************************

#************************ Util Functions **********************************


#-------------------------------------
# ReadPCF: Reads the Proto Config File
#-------------------------------------
sub ReadPCF {

local($validData,$param,$val)=0;

while(<>){
    if(/\<ENDsys_setup\>/){
        $validData=0;
    }
    if($validData){
        ($param,$val)=split(/ *: */, $_);
        if (($param =~ /hmmList/)||($param =~ /outDir/)||($param =~ /parmKind/)) {
        }elsif ($param =~ /mixes/){
            @mixes=split(/ +/, $_);
        }elsif ($param =~ /sWidths/){
            @sWidths=split(/ +/, $_);
        }else{
            $val =~ tr/A-Z/a-z/;
        }
        chop($val);
        $configParams{$param}=$val;
        write;
    }
    if(/\<BEGINsys_setup\>/ || /\<BEGINtool_steps\>/){
        $validData=1;
    }
}
format STDOUT_TOP =
 Proto Config File Read
 ======================
Parameter         Value
-----------------------
.
format STDOUT=
@<<<<<<<<<<<<<<<<<<<@<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
$param,$val
.
}

#-----------------------------------------
# SetVars: Set variable from config params
#-----------------------------------------
sub SetVars {

$nStates = $configParams{"nStates"};
($nStates >= 1) || die "nStates must be >= 1";
$nStreams = $configParams{"nStreams"};
($nStreams =~ /^[1234]/) || die "nStreams must be 1,2,3 or 4";
$vecSize = $configParams{"vecSize"};
($vecSize >= 1) || die "vecSize must be >= 1";
$hsKind = $configParams{"hsKind"};
($hsKind =~ /^[pPtTdD]/) || die "hsKind must be P, T or D";
$cKind = $configParams{"covKind"};
($cKind =~ /^[dDfF]/) || die "covKind must be F or D";
$pKind = $configParams{"parmKind"};
if ($hsKind=~/^[dD]/){
 ($pKind=~/[vV]$/) || die "If hsKind is D then parmKind must have _V appended";
}
if ($hsKind=~/^[pPtT]/){
    if($pKind=~/[vV]$/){
        die "If hsKind is not D then parmKind must not have _V appended";
    }
}
$outDir = $configParams{"outDir"};
opendir(OUTDIR,$outDir) || die "Can't open $outDir";
$hmmList = $configParams{"hmmList"};
(-f $hmmList) || die "Cannot find HMM list file $hmmList";
}

#-----------------------------------------------------------------
# TestDirEmpty: Test if outDir is empty and prompt for clearing it
#-----------------------------------------------------------------
sub TestDirEmpty {
    @nFiles = grep(!/^\./, readdir(OUTDIR)); #Forget about . files
    if($nFiles[0]){
        print "\n$outDir not empty clear it Y/N?:";
        chop($ans = <STDIN>);
        if ($ans =~ /^[yY]/){
            print "\nRemoving files from $outDir\n";
            $nFiles[0] = unlink(<$outDir/*>);
            print "Removed $nFiles[0] files\n";
        }else{
            print "\nDirectory $outDir unaltered\n";
        }
    }
}

#************************ HMM Functions **********************************

#------------------------------------
# WriteGlobOpts: Write global options
#------------------------------------
sub WriteGlobOpts {
    local($fleHandle,$hmmName)=@_;

    printf($fleHandle "  ~o <VecSize> %d <$pKind> <StreamInfo> %d ",$vecSize,$nStreams);
    for ($i=1; $i<=$nStreams; $i++) {
        printf($fleHandle "%d ",$sWidths[$i]);
    }
    printf($fleHandle "\n");
    (($hsKind=~/^[tT]/)&&($fleHandle=~/MACRO/)) || printf($fleHandle "  ~h \"$hmmName\"\n");
}

#-------------------------------------------------------
# WriteDiagCMixtures: write a diagonal covariance mixture
#-------------------------------------------------------
sub WriteDiagCMixtures {
    local($streamNum)=@_;
    local($i,$j,$k,$mixWght)=0;

    $mixWght=1/$mixes[$streamNum];

    for ($i=1; $i<=$mixes[$streamNum]; $i++){
        printf(PROTO "  <Mixture> %d %1.4f\n",$i,$mixWght);
        printf(PROTO "    <Mean> %d\n",$sWidths[$streamNum]);
        printf(PROTO "      ");
        for ($j=1; $j<=$sWidths[$streamNum]; $j++){
            printf(PROTO "0.0 ");
        }
        printf(PROTO "\n");
        printf(PROTO "    <Variance> %d\n",$sWidths[$streamNum]);
        printf(PROTO "      ");
        for ($k=1; $k<=$sWidths[$streamNum]; $k++){
            printf(PROTO "1.0 ");
        }
        printf(PROTO "\n");
    }
}

#-------------------------------------------------------
# WriteFullCMixtures: write the full covariance mixtures
#-------------------------------------------------------
sub WriteFullCMixtures {
    local($streamNum)=@_;
    local($i,$j,$k,$mixWght,$tmpVecSize)=0;

    $mixWght=1/$mixes[$streamNum];
    $tmpVecSize=$sWidths[$streamNum];

    for ($i=1; $i<=$mixes[$streamNum]; $i++){
        printf(PROTO "  <Mixture> %d %1.4f\n",$i,$mixWght);
        printf(PROTO "    <Mean> %d\n",$sWidths[$streamNum]);
        printf(PROTO "      ");
        for ($j=1; $j<=$sWidths[$streamNum]; $j++){
            printf(PROTO "0.0 ");
        }
        printf(PROTO "\n");
        printf(PROTO "    <InvCovar> %d\n",$sWidths[$streamNum]);
        while ($tmpVecSize>=1){
            for ($k=1; $k<=$tmpVecSize; $k++){
                if ($k==1){
                    printf(PROTO "1.0 ");
                }else{
                    printf(PROTO "0.0 ");
                }
            }
            printf(PROTO "\n");
            $tmpVecSize--;
        }
        $tmpVecSize=$sWidths[$streamNum];
    }
}


#-----------------------------------------------
# WriteTiedMixes: Write tied mixes to macro file
#-----------------------------------------------
sub WriteTiedMixes {
    local($i,$j,$k)=0;

    if (-r $outDir."/newMacros"){
        unlink(<$outDir/newMacros>);
    }
    open(MACRO, ">>$outDir/newMacros") || die "Cannot open $outDir/newMacros for writing";
    &WriteGlobOpts(MACRO);
    for ($i=1; $i<=$nStreams; $i++){
        for ($j=1; $j<=$mixes[$i]; $j++){
            printf(MACRO "~m \"TM_${i}_${j}\"\n");
            printf(MACRO "<Mean> %d\n",$sWidths[$i]);
            for ($k=1; $k<=$sWidths[$i]; $k++){
                printf(MACRO "0.0 ");
            }
            printf(MACRO "\n");
            printf(MACRO "<Variance> %d\n",$sWidths[$i]);
            for ($k=1; $k<=$sWidths[$i]; $k++){
                printf(MACRO "1.0 ");
            }
            printf(MACRO "\n");
        }
    }
}

#----------------------------------------------
# WriteDProbs: Write the discrete probabilities
#----------------------------------------------
sub WriteDProbs {
    local($s)=@_;

    printf(PROTO "      <DProb> %d*$mixes[$s]\n",-2371.8*log(1/$mixes[$s]));
}

#-----------------------------------------------
# WriteTiedWghts: Write the tied mixture weights
#-----------------------------------------------
sub WriteTiedWghts {
    local($streamNum)=@_;

    printf(PROTO "<TMix> \"TM_${streamNum}_\"\n");
    printf(PROTO "%e*$mixes[$streamNum]\n",1/$mixes[$streamNum]);
}

#----------------------------------------------
# WriteStates: Write the contents of the states
#----------------------------------------------
sub WriteStates {
    local($i,$j)=0;

    for ($i=1; $i<=$nStates; $i++){
        printf(PROTO "  <State> %d <NumMixes> ",$i+1);
        for ($k=1; $k<=$nStreams; $k++){
            printf(PROTO "%d ",$mixes[$k]);
        }
        printf(PROTO "\n");
        for ($j=1; $j<=$nStreams; $j++){
            printf(PROTO "  <Stream> %d\n",$j);
            if ($hsKind =~ /^[Dd]/){
                &WriteDProbs($j);
            }elsif ($hsKind =~ /^[pP]/){
                if ($cKind =~ /^[dD]/){
                    &WriteDiagCMixtures($j);
                }else{
                    &WriteFullCMixtures($j);
                }
            }elsif ($hsKind =~ /^[Tt]/){
                &WriteTiedWghts($j);
            }
        }
    }
}
#-----------------------------------------------------------
# WriteTransMat: Write the contents of the transition matrix
#-----------------------------------------------------------
sub WriteTransMat {
    local($i,$j)=0;

    printf(PROTO "  <TransP> %d\n",$nStates+2);
    for ($i=1; $i<=$nStates+2; $i++){
        for ($j=1; $j<=$nStates+2; $j++){
            if (($i==1)&&($j==2)){
                printf (PROTO "   1.000e+0");
            }elsif (($i==$j)&&($i!=1)&&($i!=$nStates+2)){
                printf (PROTO "   6.000e-1");
            }elsif ($i==($j-1)){
                printf (PROTO "   4.000e-1");
            }else{
                printf (PROTO "   0.000e+0");
            }
        }
        printf (PROTO "\n");
    }
}

#----------------------------------------
# WriteHMM: Write the contents of the HMM
#----------------------------------------
sub WriteHMM {
    local($hmmName)=@_;
    local($i)=0;

    open(PROTO, ">$outDir/$hmmName") || die "Cannot open $outDir/$hmmName for writing";
    &WriteGlobOpts(PROTO,$hmmName);
    printf(PROTO "<BeginHMM>\n");
    printf(PROTO "  <NumStates> %d\n",$nStates+2);
    &WriteStates();
    &WriteTransMat();
    printf(PROTO "<EndHMM>\n");
    close(PROTO);
}

#------------------------------------------
# WriteHSet: Write the contents of the HSet
#------------------------------------------
sub WriteHSet {

    open(HMMLIST, $hmmList) || die "Cannot open $hmmList for reading";

    printf "\nWriting HMMSet\n\n";
    if ($hsKind =~ /^[tT]/){
        printf "Writing Tied Mixtures to $outDir/newMacros\n";
        &WriteTiedMixes();
        printf "\n";
    }
    while (<HMMLIST>) {
        chop($_);
        printf "Writing HMMDef to $outDir/$_\n";
        &WriteHMM($_);
    }
    close(HMMLIST);
}



