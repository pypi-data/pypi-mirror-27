import abc
from typing import List


class Builder(metaclass=abc.ABCMeta):
    """
    A Builder is what really builds things in the system.
    A builder knows on which inputs it relies and what
    outputs it generates (sometimes before build and sometimes
    after).
    """
    __metaclass__ = abc.ABCMeta

    def get_name(self) -> str:
        return self.__class__.__name__+" "+",".join(self.get_sources())+"->"+",".join(self.get_targets())

    @abc.abstractmethod
    def __init__(self):
        """ initialize your builder here """
        pass

    @abc.abstractmethod
    def build(self):
        """ this method actually does the building """
        pass

    @abc.abstractmethod
    def get_sources(self) -> List[str]:
        return []

    def get_targets(self) -> List[str]:
        """ return the names of the files that you are sure you produce. If you do not know them,
        you must implement the get_results_names_post_build method and return None here."""
        return []

    def get_targets_post_build(self) -> List[str]:
        """ find out the names of the files that you produced.
        If you implemented the get_results_names and there you return all the results
        that you created then you don't need to implement anything here """
        return []

    @abc.abstractmethod
    def get_signature(self) -> str:
        """ return the sha1 of anything that identifies the build """
        pass
