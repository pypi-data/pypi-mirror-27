

def _require_networkx():

    pass

class BaseNetwork(object):

    pass


class OneToOne(BaseNetwork):
    """Object to apply one-to-one matching.
    """

    def __init__(self, method='greedy'):
        super(OneToOne, self).__init__(method='greedy')

        self.method = method

    def compute(self, links, weigths=None):
        """Compute the one-to-one matching.
        """

        if self.method == 'greedy':
            links_sorted = links.sort_values()

            deduplicated = x
        else:
            raise ValueError("unknown matching method {}".format(self.method))

        return deduplicated


class ConnectedComponents(BaseNetwork):
    """Object to get connected components."""

    def __init__(self):
        super(ConnectedComponents, self).__init__()

    def compute(self, links):
        """Compute the one-to-one matching.
        """

        if self.method == 'greedy':
            links_sorted = links.sort_values()

            deduplicated = x
        else:
            raise ValueError("unknown matching method {}".format(self.method))

        return deduplicated
