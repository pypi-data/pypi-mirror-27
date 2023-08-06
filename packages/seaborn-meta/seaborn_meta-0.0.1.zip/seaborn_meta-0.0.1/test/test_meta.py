from seaborn.meta import *

def smoke_test():
    assert class_name_to_instant_name('ParentEndpoint_ChildEndpoint') == 'parent_endpoint.child_endpoint'
    assert instant_name_to_class_name('parent_endpoint.child_endpoint') == 'ParentEndpoint_ChildEndpoint'


if __name__ == '__main__':
    smoke_test()
