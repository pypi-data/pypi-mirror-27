import logging
from typing import List, Dict

import os

from pydmt.api.builder import Builder
from pydmt.core.cache import Cache
from pydmt.core.utils import sha1_file, copy_mkdir


class BuildProcessStats:
    def __init__(self):
        self.builder_fail = []
        self.builder_ok = []
        self.copy_missing = []
        self.copy_sha1 = []
        self.nop = []

    def add_copy_missing(self, filename: str, object_name: str):
        self.copy_missing.append((filename, object_name))

    def get_copy_missing(self):
        return len(self.copy_missing)

    def add_copy_sha1(self, filename: str, object_name: str):
        self.copy_sha1.append((filename, object_name))

    def add_nop(self, filename: str, object_name: str):
        self.nop.append((filename, object_name))

    def get_nop(self):
        return len(self.nop)

    def add_builder_ok(self, builder: Builder):
        self.builder_ok.append(builder)

    def add_builder_fail(self, builder: Builder, e: Exception):
        self.builder_fail.append((builder, e))

    def get_builder_ok(self):
        return len(self.builder_ok)

    def get_builder_fail(self):
        return len(self.builder_fail)


class PyDMT:
    def __init__(self):
        self.builders = []  # type: List[Builder]
        self.target_to_builder = {}  # type: Dict[str, Builder]
        self.cache = Cache()

    def build_by_builder(self, builder: Builder, stats: BuildProcessStats):
        """ run one builder, return statistics about the run """
        logger = logging.getLogger(__name__)
        target_signature = builder.get_signature()
        assert target_signature is not None, "builder signature is None"
        if self.cache.list_sig_ok(target_signature):
            logger.info("verifying [{}]".format(builder.get_name()))
            file_bad = 0
            file_correct = 0
            file_missing = 0
            file_total = 0
            list_filename = self.cache.get_list_filename(target_signature)
            for object_name, signature in Cache.iterate_objects(list_filename):
                filename = self.cache.get_object_filename(signature)
                if os.path.isfile(object_name):
                    object_name_signature = sha1_file(object_name)
                    if object_name_signature != signature:
                        # logger.info("file [{}] is incorrect. Getting from cache.".format(object_name))
                        copy_mkdir(filename, object_name)
                        stats.add_copy_sha1(filename, object_name)
                        file_bad += 1
                    else:
                        # logger.info("file [{}] is up to date".format(object_name))
                        stats.add_nop(filename, object_name)
                        file_correct += 1
                else:
                    # logger.info("file [{}] is missing. Getting from cache.".format(object_name))
                    copy_mkdir(filename, object_name)
                    stats.add_copy_missing(filename, object_name)
                    file_missing += 1
                file_total += 1
            if file_bad > 0 or file_missing > 0:
                logger.info("Retrieved {} files from cache (bad/correct/missing = {}/{}/{}".format(
                    file_total, file_bad, file_correct, file_missing))
            else:
                logger.info("ok [{}]".format(builder.get_name()))
        else:
            # this is one of the rare cases in which really want to catch all exceptions.
            # noinspection PyBroadException
            try:
                logger.info("running [{}]".format(builder.get_name()))
                builder.build()
                logger.info("ok [{}]".format(builder.get_name()))
                stats.add_builder_ok(builder)
                # first lets build a list of what was constructed
                targets = builder.get_targets()
                targets.extend(builder.get_targets_post_build())
                content = ""
                for target in targets:
                    signature = sha1_file(target)
                    content += target + " " + signature + "\n"
                    self.cache.save_object_by_signature(signature, target)
                self.cache.save_list_by_signature(target_signature, content)
            except Exception as e:
                logger.info("failed [{}]".format(builder.get_name()))
                logger.info("exception [{}]".format(e))
                stats.add_builder_fail(builder, e)

    def build_by_target(self, target: str, stats: BuildProcessStats) -> None:
        b = self.target_to_builder[target]
        self.build_by_builder(b, stats)

    def build_by_targets(self, targets: List[str], stats: BuildProcessStats) -> None:
        for target in targets:
            self.build_by_target(target, stats)

    def build_all(self) -> BuildProcessStats:
        """
        Build all the targets, very high level method
        :return:
        """
        stats = BuildProcessStats()
        for builder in self.builders:
            self.build_by_builder(
                builder=builder,
                stats=stats,
            )
        return stats

    def add_builder(self, b: Builder) -> None:
        self.builders.append(b)
        targets = b.get_targets()
        if targets:
            for target in targets:
                self.target_to_builder[target] = b
