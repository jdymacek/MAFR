import numpy
import PIL
from PIL import Image, ImageOps


#https://timsainburg.com/python-mel-compression-inversion.html


def overlap(X, window_size, window_step):
    """
    Create an overlapped version of X
    Parameters
    ----------
    X : ndarray, shape=(n_samples,)
        Input signal to window and overlap
    window_size : int
        Size of windows to take
    window_step : int
        Step size between windows
    Returns
    -------
    X_strided : shape=(n_windows, window_size)
        2D array of overlapped X
    """
    if window_size % 2 != 0:
        raise ValueError("Window size must be even!")
    # Make sure there are an even number of windows before stridetricks
    append = numpy.zeros((window_size - len(X) % window_size))
    X = numpy.hstack((X, append))

    ws = window_size
    ss = window_step
    a = X

    valid = len(a) - ws
    nw = (valid) // ss
    out = numpy.ndarray((nw, ws), dtype=a.dtype)

    for i in numpy.arange(nw):
        # "slide" the window along the samples
        start = i * ss
        stop = start + ws
        out[i] = a[start:stop]

    return out


def stft( X, fftsize=128, step=65, mean_normalize=True, real=False, compute_onesided=True ):
    """
    Compute STFT for 1D real valued input X
    """
    if real:
        local_fft = numpy.fft.rfft
        cut = -1
    else:
        local_fft = numpy.fft.fft
        cut = None
    if compute_onesided:
        cut = fftsize // 2
    if mean_normalize:
        X -= X.mean()

    X = overlap(X, fftsize, step)

    size = fftsize
    win = 0.54 - 0.46 * numpy.cos(2 * numpy.pi * numpy.arange(size) / (size - 1))
    X = X * win[None]
    X = local_fft(X)[:, :cut]
    return X



def pretty_spectrogram(d, log=True, thresh=5, fft_size=512, step_size=64):
    """
    creates a spectrogram
    log: take the log of the spectrgram
    thresh: threshold minimum power for log spectrogram
    """
    specgram = numpy.abs( stft(d, fftsize=fft_size, step=step_size, real=False, compute_onesided=True))

    if log == True:
        specgram /= specgram.max()  # volume normalize to max 1
        specgram = numpy.log10(specgram)  # take log
        specgram[ specgram < -thresh] = -thresh  # set anything less than the threshold as the threshold
    else:
        specgram[ specgram < thresh ] = thresh  # set anything less than the threshold as the threshold

    return specgram


def mel2hz(mel):
    """Convert a value in Mels to Hertz
    :param mel: a value in Mels. This can also be a numpy array, conversion proceeds element-wise.
    :returns: a value in Hertz. If an array was passed in, an identical sized array is returned.
    """
    return 700 * (10 ** (mel / 2595.0) - 1)



def hz2mel(hz):
    """Convert a value in Hertz to Mels
    :param hz: a value in Hz. This can also be a numpy array, conversion proceeds element-wise.
    :returns: a value in Mels. If an array was passed in, an identical sized array is returned.
    """
    return 2595 * numpy.log10(1 + hz / 700.0)


def get_filterbanks(nfilt=20, nfft=512, samplerate=16000, lowfreq=0, highfreq=None):
    """Compute a Mel-filterbank. The filters are stored in the rows, the columns correspond
    to fft bins. The filters are returned as an array of size nfilt * (nfft/2 + 1)
    :param nfilt: the number of filters in the filterbank, default 20.
    :param nfft: the FFT size. Default is 512.
    :param samplerate: the samplerate of the signal we are working with. Affects mel spacing.
    :param lowfreq: lowest band edge of mel filters, default 0 Hz
    :param highfreq: highest band edge of mel filters, default samplerate/2
    :returns: A numpy array of size nfilt * (nfft/2 + 1) containing filterbank. Each row holds 1 filter.
    """
    highfreq = highfreq or samplerate / 2
    assert highfreq <= samplerate / 2, "highfreq is greater than samplerate/2"

    # compute points evenly spaced in mels
    lowmel = hz2mel(lowfreq)
    highmel = hz2mel(highfreq)
    melpoints = numpy.linspace(lowmel, highmel, nfilt + 2)
    # our points are in Hz, but we use fft bins, so we have to convert
    #  from Hz to fft bin number
    bin = numpy.floor((nfft + 1) * mel2hz(melpoints) / samplerate)

    fbank = numpy.zeros([nfilt, nfft // 2])
    for j in range(0, nfilt):
        for i in range(int(bin[j]), int(bin[j + 1])):
            fbank[j, i] = (i - bin[j]) / (bin[j + 1] - bin[j])
        for i in range(int(bin[j + 1]), int(bin[j + 2])):
            fbank[j, i] = (bin[j + 2] - i) / (bin[j + 2] - bin[j + 1])
        #HACK -- remove zero row by inserting a 1 probably should be handled better 
        if fbank[j, i] == 0:
            fbank[j, i] = 1
    return fbank



def create_mel_filter(
    fft_size, n_freq_components=64, start_freq=300, end_freq=8000, samplerate=44100
):
    """
    Creates a filter to convolve with the spectrogram to get out mels

    """
    mel_inversion_filter = get_filterbanks( 
        nfilt=n_freq_components, 
        nfft=fft_size, 
        samplerate=samplerate,
        lowfreq=start_freq,
        highfreq=end_freq,
    )

    # Normalize filter
    mel_filter = mel_inversion_filter.T / mel_inversion_filter.sum(axis=1)
    return mel_filter, mel_inversion_filter




class SPEI:
    def __init__(self, fft_size = 512,hop_size = 42, spec_thresh = 4):
        self.fft_size = fft_size
        self.step_size = hop_size
        self.spec_thresh = spec_thresh

    def mel_as_image(self,wav_data=None, mel_bands=40, start_freq=2000, end_freq=11025, sample_rate=22050):
        mel_filter, mel_inversion_filter = create_mel_filter(
            fft_size=self.fft_size,
            n_freq_components=mel_bands,
            start_freq=start_freq,
            end_freq=end_freq, samplerate=sample_rate
        )
        wav_spectrogram = pretty_spectrogram( wav_data, fft_size=self.fft_size, step_size=self.step_size, log=True, thresh=self.spec_thresh,)

        mel_spec = numpy.transpose(mel_filter).dot(numpy.transpose(wav_spectrogram))
        mel_spec = mel_spec[:, 1:-1]  # a little hacky but seemingly needed for clipping

        #Transform into a PIL image
        mel_spec = (mel_spec+self.spec_thresh)/self.spec_thresh * 255
        return ImageOps.flip(Image.fromarray(mel_spec.astype(numpy.uint8),mode="L"))

    def spec_as_image(self, wav_data=None, sample_rate=22050):
        wav_spectrogram = pretty_spectrogram(wav_data, fft_size=self.fft_size, step_size=self.step_size, log=True, thresh=self.spec_thresh)
        spec = numpy.transpose(wav_spectrogram)

        #Transform into a PIL image
        spec = (spec+self.spec_thresh)/self.spec_thresh * 255
        return ImageOps.flip(Image.fromarray(spec.astype(numpy.uint8),mode="L"))
    
