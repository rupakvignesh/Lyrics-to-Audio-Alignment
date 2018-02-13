# Lyrics-to-Audio-Alignment
This project aims at creating an automatic alignment between the textual lyrics and monophonic singing vocals (audio). This system shall be very useful in a setting where a karoake performer would want to keep in sync with the background track. Traditional Hidden Markov Models are used for phoneme modelling and an interesting structural segmentation approach has been explored to break the audio (usually of length 4-5 minutes) to smaller chunks that are structurallly meaningful (Intro, Verse, Chorus, etc) without any implicit assumptions.

## Watch the Demo
[![Video link](https://github.com/rupakvignesh/Lyrics-to-Audio-Alignment/blob/master/Damp_Dataset/misc_items/demo_l2a.png)](https://www.youtube.com/watch?v=w-6tgVNj1go)

## Pre-requisites

* [HTK tool-kit] (http://htk.eng.cam.ac.uk/download.shtml)
* [sph2pipe] (https://www.ldc.upenn.edu/language-resources/tools/sphere-conversion-tools)
* [Flite] (http://www.speech.cs.cmu.edu/flite/download.html)
* [MSAF] (https://github.com/urinieto/msaf/releases)

## Training Steps

### Training Acoustic models

### TIMIT
* Create initial hmm models (isolated phoneme training)
```
tcsh scripts/model_gen.sh <phonelist> <proto_file>
```
* Create connected HMM models (embedded re-estimation)
```
tcsh script/embedded_reestimation.sh <iterations>
```

### Damp
* Align Damp dataset with the generated HMM Models using forced Viterbi alignment
* Perform embedded reestimation using the Damp Dataset to refine the phoneme models.

### Structural Segmentation
* Use MSAF library to segment Damp training data into structural segments
```
python scripts/msaf_segmentation.py <wav_in_dir> <wav_out_dir>
```
* Create MLF files corresponding to the segmented audio
```
python scripts/msaf_to_mlf.py <labfile_list>
```
* Perform embedded reestimation within these segments to get the final phoneme models

## Testing
* To test any model do the forced Viterbi alignment
```
sh scripts/force_align.sh
``` 
Set the parameters such as model, features, mlf, dictionary, etc inside the file

## Authors

* **Phoneme Acoustic Modelling** - [Rupak Vignesh](https://github.com/rupakvignesh)
* **Structural Segmentation with MSAF** - [Benjamin Genchel](https://github.com/bgenchel)

## Acknowledgments

* Thanks to [Alex Lerch](https://github.com/alexanderlerch) for his guidance
* S Aswin Shanmugham's hybrid segmentation framework
* Stanford's DAMP dataset.
