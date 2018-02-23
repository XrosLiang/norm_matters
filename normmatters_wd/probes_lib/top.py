import pandas as pd


class ProbesManager:
    def __init__(self):
        self.per_epoch_stats = None
        self.probes_of = {}
        self.probes = {}
        self.training = True
        self.return_predictions_data = {"test": False, "train": False}

    def _add_probe_to_loc(self, probe, probe_loc):
        if probe_loc not in self.probes_of.keys():
            self.probes_of[probe_loc] = []
        self.probes_of[probe_loc].append(probe)

    def add_probe(self, probe, probe_name, probe_locs):
        for loc in probe_locs:
            self._add_probe_to_loc(probe, loc)
        if probe_name in self.probes.keys():
            print("Probe name " + str(probe_name) + " already exists!")
            raise KeyError
        self.probes[probe_name] = probe
        self.update_return_predictions_data(probe)

    def update_return_predictions_data(self, probe):
        if hasattr(probe, "return_predictions_data"):
            if "test" in probe.return_predictions_data.keys():
                self.return_predictions_data["test"] = (probe.return_predictions_data["test"] or
                                                        self.return_predictions_data["test"])
            if "train" in probe.return_predictions_data.keys():
                self.return_predictions_data["train"] = (probe.return_predictions_data["train"] or
                                                         self.return_predictions_data["train"])

    def add_data(self, probe_loc, **kwargs):
        if not probe_loc or probe_loc not in self.probes_of.keys():
            return
        for probe in self.probes_of[probe_loc]:
            probe.add_data(training=self.training, **kwargs)

    def epoch_prologue(self):
        for probe in self.probes.values():
            probe.epoch_prologue()

    def epoch_epilogue(self):
        for probe in self.probes.values():
            probe.epoch_epilogue()

    def pickle_prologue(self):
        for probe in self.probes.values():
            probe.pickle_prologue()

    def pickle_epilogue(self):
        for probe in self.probes.values():
            probe.pickle_epilogue()

    def calc_epoch_stats(self):
        last_epoch_stats = {}
        for probe_name in self.probes.keys():
            probe = self.probes[probe_name]
            probe_last_epoch_stats = probe.get_last_epoch_stats()
            for key in probe_last_epoch_stats.keys():
                last_epoch_stats[probe_name + "_" + key] = probe_last_epoch_stats[key]

        df = pd.DataFrame([last_epoch_stats.values()], columns=last_epoch_stats.keys())
        if self.per_epoch_stats is None:
            self.per_epoch_stats = df
        else:
            self.per_epoch_stats = self.per_epoch_stats.append(df, ignore_index=True)

    def train(self):
        self.training = True

    def eval(self):
        self.training = False


class StatsProbe:
    def __init__(self, **kwargs):
        return

    def add_data(self, **kwargs):
        raise NotImplementedError

    def epoch_epilogue(self):
        return

    def epoch_prologue(self):
        return

    def pickle_prologue(self):
        return

    def pickle_epilogue(self):
        return

    def get_last_epoch_stats(self):
        raise NotImplementedError
