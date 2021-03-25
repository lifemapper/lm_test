"""Test class for lm_client"""
from random import randint, shuffle

from ot_service_wrapper.open_tree import get_ottids_from_gbifids, induced_subtree

import lm_test.base.test_base as test_base

TEST_GBIF_IDS = [
    '3032647', '3032648', '3032649', '3032651', '3032652', '3032653',
    '3032654', '3032655', '3032656', '3032658', '3032660', '3032661',
    '3032662', '3032664', '3032665', '3032666', '3032667', '3032668',
    '3032670', '3032671', '3032672', '3032673', '3032674', '3032675',
    '3032676', '3032678', '3032679', '3032680', '3032681', '3032686',
    '3032687', '3032688', '3032689', '3032690', '3752543', '3752610',
    '3753319', '3753512', '3754294', '3754395', '3754671', '3754743',
    '3755291', '3755546', '4926214', '7462054', '7516328', '7551031',
    '7554971', '7588669', '8109411', '8280496', '8365087'
]


# .............................................................................
class OpenTreeTest(test_base.LmTest):
    """Test the OpenTree services"""
    # .............................
    def __init__(self, delay_time=0, delay_interval=3600):
        test_base.LmTest.__init__(self, delay_time=delay_time)
        self.delay_interval = delay_interval

    # .............................
    def __repr__(self):
        return 'Open Tree Service Test'

    # .............................
    def run_test(self):
        """Run open tree tests."""
        self.add_new_test(OpenTreeTest(delay_time=self.delay_interval))
        test_ids = TEST_GBIF_IDS
        shuffle(test_ids)
        test_ids = test_ids[:randint(0, 20)]
        try:
            ott_ids = get_ottids_from_gbifids(test_ids)
        except Exception as err:
            raise test_base.LmTestFailure(
                'Failed to get open tree ids: {}'.format(err))
        if not ott_ids:
            raise test_base.LmTestFailure(
                'Failed to get open tree ids (no results or None)')

        try:
            tree_resp = induced_subtree(ott_ids)
        except Exception as err:
            raise tree_base.LmTestFailure(
                'Failed to induce subtree from Open tree: {}'.format(err))
        print(tree_resp)


    # .............................
    def run_layer_tests(self):
        """Run lm_client layer tests."""
        # Check that there is at least 1 layer available
        try:
            assert self.client.layer.count() > 0
        except AssertionError:
            raise test_base.LmTestFailure(
                'Count layers for {}, no parameters was zero'.format(
                    self.user_id))

        # Check that count returns zero for bad parameters
        try:
            assert self.client.layer.count(after_time='bad_value') == 0
        except AssertionError:
            raise test_base.LmTestFailure(
                'Count layers with bad parameter returned > 0')