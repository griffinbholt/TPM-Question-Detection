stat_names = ['mean', 'std_dev', 'median', 'maximum', 'minimum', 'range', 'skew', 'kurtosis', 'all-pts regr. slope', 'all-pts regr. offset', 'all-pts regr. MSE', 'first-last regr. slope', 'first-last regr. offset', 'first-last regr. MSE', '%% rising slopes']
audio_options = ['full', 'last500', 'last200']
primary_audio_features = ['f0', 'sig.int.']

def generate_function_names():
    feature_names = []

    for audio_option in audio_options:
        # f0 = calculate_fundemental_frequency(audio_clip)
        # feature_vals.extend(get_stats(f0, sample_freq))

        # signal_intensity = calculate_signal_intensity(audio_clip)
        # feature_vals.extend(get_stats(signal_intensity, sample_freq))
        for primary_audio_feature in primary_audio_features:
            for stat in stat_names:
                feature_names.append('{} {} ({})'.format(primary_audio_feature, stat, audio_option))

        # jitter = calculate_jitter_of_audio_clip(audio_clip)
        #     feature_vals.append(jitter)
        feature_names.append('jitter ({})'.format(audio_option))

        # shimmer = calculate_shimmer_of_audio_clip(audio_clip)
        # feature_vals.append(shimmer)
        feature_names.append('shimmer ({})'.format(audio_option))

        # mfcc_coeff_vectors = calculate_MFCC_coefficients(audio_clip)
        # for mfcc_coeff_vector in mfcc_coeff_vectors:
        for i in range(13):
        #   feature_vals.append(np.mean(mfcc_coeff_vector))
        #   feature_vals.append(np.std(mfcc_coeff_vector))
            feature_names.append('mfcc{} mean ({})'.format(i, audio_option))
            feature_names.append('mfcc{} std_dev ({})'.format(i, audio_option))

        # rms = calculate_RMS_frame_energy(audio_clip)
        # feature_vals.append(rms)
        feature_names.append('rms ({})'.format(audio_option))

    # num_pauses, pause_durations, pause_starts, pause_total_length = calculate_pauses(audio_clip)
    # feature_vals.append(num_pauses, pause_total_length)
    feature_names.append('num. pauses (full)')
    feature_names.append('cum. pause ken (full)')

    # feature_vals.append(get_pause_stats(pause_durations, pause_starts))
    for stat in stat_names[:-1]:
        feature_names.append('pause len. {} (full)'.format(stat))

    # zcr = calculate_zero_crossing_rate(full_audio)
    # feature_vals.append(zcr)
    feature_names.append('zcr (full)')

    # spectral_balance = calculate_spectral_balance(full_audio)
    # feature_vals.append(spectral_balance)
    feature_names.append('spect. bal. (full)'.format(stat))

    # average_psd = calculate_power_spectral_density(full_audio)
    # feature_vals.append(np.argmax(average_psd))
    # feature_vals.append(np.max(average_psd))
    feature_names.append('Argmax Avg. PSD (full)')
    feature_names.append('Max Avg. PSD (full)')

    return feature_names

function_names = generate_function_names()
print(function_names)
print(len(function_names))
