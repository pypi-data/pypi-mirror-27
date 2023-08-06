from __future__ import print_function
from .audio_classes import Track, Source, Target
from os import path as op
from six.moves import map
import multiprocessing
import soundfile as sf
import collections
import numpy as np
import functools
import signal
import yaml
import glob
import tqdm
import os
import musdb


class DB(object):
    """
    The musdb DB Object

    Parameters
    ----------
    root_dir : str, optional
        musdb Root path. If set to `None` it will be read
        from the `MUSDB_PATH` environment variable

    subsets : str or list, optional
        select a _musdb_ subset `train` or `test` (defaults to both)

    is_wav : boolean, optional
        expect subfolder with wav files for each source instead stems,
        defaults to stems


    Attributes
    ----------
    setup_file : str
        path to yaml file. default: `setup.yaml`
    root_dir : str
        musdb Root path. Default is `MUSDB_PATH` env
    sources_dir : str
        path to Sources directory
    sources_names : list[str]
        list of names of sources
    targets_names : list[str]
        list of names of targets
    setup : Dict
        loaded yaml configuration

    Methods
    -------
    load_mus_tracks()
        Iterates through the musdb folder structure and
        returns ``Track`` objects
    test(user_function)
        Test the musdb processing
    run(user_function=None, estimates_dir=None)
        Run the musdb processing and saving the estimates

    """
    def __init__(
        self,
        root_dir=None,
        setup_file=None,
        is_wav=False
    ):
        if root_dir is None:
            if "MUSDB_PATH" in os.environ:
                self.root_dir = os.environ["MUSDB_PATH"]
            else:
                raise RuntimeError("Variable `MUSDB_PATH` has not been set.")
        else:
            self.root_dir = root_dir

        if setup_file is not None:
            setup_path = op.join(self.root_dir, setup_file)
        else:
            setup_path = os.path.join(
                musdb.__path__[0], 'configs', 'mus.yaml'
            )

        with open(setup_path, 'r') as f:
            self.setup = yaml.load(f)

        self.sources_names = list(self.setup['sources'].keys())
        self.targets_names = list(self.setup['targets'].keys())
        self.is_wav = is_wav

    def load_mus_tracks(self, subsets=None):
        """Parses the musdb folder structure, returns list of `Track` objects

        Parameters
        ==========
        subsets : list[str], optional
            select a _musdb_ subset `Dev` or `Test`. Defaults to both

        Returns
        -------
        list[Track]
            return a list of ``Track`` Objects
        """

        if subsets is not None:
            if isinstance(subsets, str):
                subsets = [subsets]
            else:
                subsets = subsets
        else:
            subsets = ['train', 'test']

        tracks = []
        for subset in subsets:

            subset_folder = op.join(self.root_dir, subset)

            for _, track_folders, track_names in os.walk(subset_folder):
                if self.is_wav:
                    # parse pcm tracks
                    for track_filename in sorted(track_folders):
                        # create new mus track
                        track = Track(
                            name=track_filename,
                            path=op.join(
                                op.join(subset_folder, track_filename),
                                self.setup['mixture']
                            ),
                            subset=subset
                        )

                        # add sources to track
                        sources = {}
                        for src, source_file in list(
                            self.setup['sources'].items()
                        ):
                            # create source object
                            abs_path = op.join(
                                subset_folder,
                                source_file
                            )
                            if os.path.exists(abs_path):
                                sources[src] = Source(
                                    name=src,
                                    path=abs_path
                                )
                        track.sources = sources

                        # add targets to track
                        targets = collections.OrderedDict()
                        for name, target_srcs in list(
                            self.setup['targets'].items()
                        ):
                            # add a list of target sources
                            target_sources = []
                            for source, gain in list(target_srcs.items()):
                                if source in list(track.sources.keys()):
                                    # add gain to source tracks
                                    track.sources[source].gain = float(gain)
                                    # add tracks to components
                                    target_sources.append(sources[source])
                            # add sources to target
                            if target_sources:
                                targets[name] = Target(sources=target_sources)
                        # add targets to track
                        track.targets = targets

                        # add track to list of tracks
                        tracks.append(track)
                else:
                    # parse stem files
                    for track_name in sorted(track_names):
                        if 'stem' in track_name and track_name.endswith(
                            '.mp4'
                        ):
                            # create new mus track
                            track = Track(
                                name=track_name,
                                path=op.join(subset_folder, track_name),
                                subset=subset,
                                stem_id=self.setup['stem_ids']['mixture']
                            )
                            # add sources to track
                            sources = {}
                            for src, source_file in list(
                                self.setup['sources'].items()
                            ):
                                # create source object
                                abs_path = op.join(
                                    subset_folder,
                                    track_name
                                )
                                if os.path.exists(abs_path):
                                    sources[src] = Source(
                                        name=src,
                                        path=abs_path,
                                        stem_id=self.setup['stem_ids'][src]
                                    )
                            track.sources = sources

                            # add targets to track
                            targets = collections.OrderedDict()
                            for name, target_srcs in list(
                                self.setup['targets'].items()
                            ):
                                # add a list of target sources
                                target_sources = []
                                for source, gain in list(target_srcs.items()):
                                    if source in list(track.sources.keys()):
                                        # add gain to source tracks
                                        track.sources[source].gain = float(
                                            gain
                                        )
                                        # add tracks to components
                                        target_sources.append(sources[source])
                                # add sources to target
                                if target_sources:
                                    targets[name] = Target(
                                        sources=target_sources
                                    )
                            # add targets to track
                            track.targets = targets

                            # add track to list of tracks
                            tracks.append(track)

        return tracks

    def _save_estimates(self, user_estimates, track, estimates_dir):
        track_estimate_dir = op.join(
            estimates_dir, track.subset, track.name
        )
        if not os.path.exists(track_estimate_dir):
            os.makedirs(track_estimate_dir)

        # write out tracks to disk
        for target, estimate in list(user_estimates.items()):
            target_path = op.join(track_estimate_dir, target + '.wav')
            sf.write(target_path, estimate, track.rate)
        pass

    def test(self, user_function):
        """Test the musdb processing

        Parameters
        ----------
        user_function : callable, optional
            function which separates the mixture into estimates.

        Raises
        ------
        TypeError
            If the provided function handle is not callable.

        ValueError
            If the output is not compliant to the bsseval methods

        See Also
        --------
        run : Process the musdb
        """
        if not hasattr(user_function, '__call__'):
            raise TypeError("Please provide a function.")

        test_track = Track(name="test - test")
        signal = np.random.random((66000, 2))
        test_track.audio = signal
        test_track.rate = 44100

        user_results = user_function(test_track)

        if isinstance(user_results, dict):
            for target, audio in list(user_results.items()):
                if target not in self.targets_names:
                    raise ValueError("Target '%s' not supported!" % target)

                d = audio.dtype
                if not np.issubdtype(d, float):
                    raise ValueError(
                        "Estimate is not of type numpy.float_"
                    )

                if audio.shape != signal.shape:
                    raise ValueError(
                        "Shape of estimate does not match input shape"
                    )

        else:
            raise ValueError("output needs to be a dict")

        return True

    def _process_function(self, track, user_function, estimates_dir):
        # load estimates from disk instead of processing
        if user_function is None:
            track_estimate_dir = op.join(
                estimates_dir,
                track.subset,
                track.name
            )
            user_results = {}
            for target_path in glob.glob(track_estimate_dir + '/*.wav'):
                target_name = op.splitext(
                    os.path.basename(target_path)
                )[0]
                try:
                    target_audio, rate = sf.read(
                        target_path,
                        always_2d=True
                    )
                    user_results[target_name] = target_audio
                except RuntimeError:
                    pass
        else:
            # call the user provided function
            user_results = user_function(track)
        if estimates_dir and user_function is not None:
            self._save_estimates(user_results, track, estimates_dir)

    def run(
        self,
        user_function,
        tracks=None,
        estimates_dir=None,
        subsets=None,
        parallel=False,
        cpus=4
    ):
        """Run the musdb processing

        Parameters
        ----------
        user_function : callable
            function which separates the mixture into estimates.
        tracks : list[Track], optional
            select a list of tracks
        subsets : list[str], optional
            select a _musdb_ subset `Dev` or `Test`. Defaults to both
        estimates_dir : str, optional
            path to the user provided estimates. Directory will be
            created if it does not exist. Default is `none` which means that
            the results are not saved.
        parallel: bool, optional
            activate multiprocessing
        cpus: int, optional
            set number of cores if `parallel` mode is active, defaults to 4

        Raises
        ------
        RuntimeError
            If the provided function handle is not callable.

        See Also
        --------
        test : Test the user provided function
        """

        if user_function is None and estimates_dir:
            raise RuntimeError("Provide a function!")

        # list of tracks to be processed
        if tracks is None:
            tracks = self.load_mus_tracks(subsets=subsets)

        success = False
        if parallel:
            pool = multiprocessing.Pool(cpus, initializer=init_worker)
            success = list(
                tqdm.tqdm(
                    pool.imap_unordered(
                        func=functools.partial(
                            process_function_alias,
                            self,
                            user_function=user_function,
                            estimates_dir=estimates_dir
                        ),
                        iterable=tracks,
                        chunksize=1
                    ),
                    total=len(tracks)
                )
            )

            pool.close()
            pool.join()

        else:
            success = list(
                tqdm.tqdm(
                    map(
                        lambda x: self._process_function(
                            x,
                            user_function,
                            estimates_dir
                        ),
                        tracks
                    ),
                    total=len(tracks)
                )
            )
        return success


def process_function_alias(obj, *args, **kwargs):
    return obj._process_function(*args, **kwargs)


def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)
