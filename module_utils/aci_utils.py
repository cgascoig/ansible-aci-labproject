import re

def parse_interface(interface_spec):
    output_format="topology/pod-{}/paths-{}/{}pathep-[eth{}/{}]"
    pod=1
    leaf_int_re = r'^\s*(pod-(?P<pod>\d+)/)?leaf-(?P<leaf>\d+)/e(t(h(e(r(n(e(t?)?)?)?)?)?)?)?((?P<fex>\d+)/)?(?P<mod>\d+)/(?P<port>\d+)'
    m = re.match(r'^\s*'+leaf_int_re, interface_spec)
    if m:
        group_dict = m.groupdict()
        leaf=group_dict['leaf']
        mod=group_dict['mod']
        port=group_dict['port']
        fex = 'extpaths-{}/'.format(group_dict['fex']) if 'fex' in group_dict and group_dict['fex'] is not None else ''
        if 'pod' in group_dict and group_dict['pod'] is not None:
            pod=group_dict['pod']
        return output_format.format(pod, leaf, fex, mod, port)
        
        
    return None
    
