$OUTDIR = test_lab_word_timit_model
$MODEL = timit_4s_4m/hmmdefs
$MLF = test_lyrics.mlf
$FEATS = lists/test.mfclist
$DICT = words_to_phone_dict
$PHONELIST = lists/cmu_phones.txt

HVite -l $OUTDIR -C Configs/config-hvite -a -H $MODEL -y lab -o MN -I $MLF -S $FEATS $DICT $PHONELIST
