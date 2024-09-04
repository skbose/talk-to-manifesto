# marathi_faq
Install gradio according to requirements.txt

# Documentation:
1) Data Preparation:
   * Conversion to 22050 Hz **(TODO: This can be eliminated/ can be changed to 16000 Hz)**
   * Denoising to remove background noise
     * Running highpass/lowpass & resample
     * Output normalized
   * Split into optimal wav files **(TODO: Change split to 10 seconds)**
2) Labelling (Speech to text)
   * DrishtiSharma/whisper-large-v2-marathi : Model used to convert speech to text
   * Still makes mistakes
   * After label generation, run chatgpt to correct the statements
   * Still makes mistakes
   * **TODO: Human Review**
3) Training
   * Find the meaning of all losses.
   * Check why its going up


Issues:
* Voice is radio type
  * TODO: Check if 16000 hz can help preprocessing
  * 10 second speech
  * Issues while conversion ()
  * Research about this issue
* Emotions lacking / Monotonous Speech:
  * Research on how this can be solved
* Model Hyperparameter tuning
  * Why is the train loss going up
  * MMS paper : VITS -> What does each thing mean?
