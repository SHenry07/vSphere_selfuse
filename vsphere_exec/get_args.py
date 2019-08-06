from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vim
import atexit
import argparse
import getpass
import logging ; logging.basicConfig(level=logging.INFO)



def get_args():

    parser = argparse.ArgumentParser(
        description='Arguments for talking to vCenter')

    parser.add_argument('-s', '--host',
                        required=True,
                        action='store',
                        help='vSpehre service to connect to')

    parser.add_argument('-o', '--port',
                        type=int,
                        default=443,
                        action='store',
                        help='Port to connect on')

    parser.add_argument('-u', '--user',
                        required=True,
                        action='store',
                        help='User name to use')

    parser.add_argument('-p', '--password',
                        required=False,
                        action='store',
                        help='Password to use')

    parser.add_argument('-v', '--vm-name',
                        required=False,
                        action='store',
                        help='name of the vm')

    parser.add_argument('--uuid',
                        required=False,
                        action='store',
                        help='vmuuid of vm')

    parser.add_argument('--disk-type',
                        required=False,
                        action='store',
                        default='thin',
                        choices=['thick', 'thin'],
                        help='thick or thin')

    parser.add_argument('--disk-size',
                        required=False,
                        action='store',)

    parser.add_argument('--template',
                        required=False,
                        #required=True,
                        action='store',
                        help='Name of the template/VM \
                            you are cloning from')

    parser.add_argument('--datacenter-name',
                        required=False,
                        action='store',
                        default=None,
                        help='Name of the Datacenter you\
                            wish to use. If omitted, the first\
                            datacenter will be used.')

    parser.add_argument('--vm-folder',
                        required=False,
                        action='store',
                        default=None,
                        help='Name of the VMFolder you wish\
                            the VM to be dumped in. If left blank\
                            The datacenter VM folder will be used')

    parser.add_argument('--datastore-name',
                        required=False,
                        action='store',
                        default=None,
                        help='Datastore you wish the VM to end up on\
                            If left blank, VM will be put on the same \
                            datastore as the template')

    parser.add_argument('--datastorecluster-name',
                        required=False,
                        action='store',
                        default=None,
                        help='Datastorecluster (DRS Storagepod) you wish the VM to end up on \
                            Will override the datastore-name parameter.')

    parser.add_argument('--cluster-name',
                        required=False,
                        action='store',
                        default=None,
                        help='Name of the cluster you wish the VM to\
                            end up on. If left blank the first cluster found\
                            will be used')

    parser.add_argument('--resource-pool',
                        required=False,
                        action='store',
                        default=None,
                        help='Resource Pool to use. If left blank the first\
                            resource pool found will be used')

    parser.add_argument('--power-on',
                        dest='power_on',
                        action='store_true',
                        help='power on the VM after creation')

    parser.add_argument('--opaque-network',
                        required=False,
                        help='Name of the opaque network to add to the VM')

    args = parser.parse_args()
    
    if not args.password:
            args.password = getpass.getpass(
                            prompt='Enter password for host %s and user %s: ' %
                   (args.host, args.user))   

    return args


def service_con(host,user,pwd):

    si = None
    si = SmartConnectNoSSL( host=host,
                      user=user,
                        pwd=pwd,
                        )

    atexit.register(Disconnect,si)

    return si
def get_obj(content, vimtype, name):
    obj = None
    container = content.viewManager.CreateContainerView(
        content.rootFolder, vimtype, True)
    for c in container.view:
        if c.name == name:
            obj = c
            break
    return obj

def Get_Vm(si,vm_name=None,vm_ip=None,vm_uuid=None):
    """
    支持按ip查询，名字查询，uuid查询
    """
    search_index = si.content.searchIndex

    # without exception find managed objects using durable identifiers that the
    # search index can find easily. This is much better than caching information
    # that is non-durable and potentially buggy.

    vm = None
    if vm_uuid:
        vm = search_index.FindByUuid(None, vm_uuid, True, True)
        logging.info("被检查的VM是:{}".format(vm_uuid))
    elif vm_ip:
        vm = search_index.FindByIp(None, vm_ip, True)
        logging.info("被检查的VM是:{}".format(vm_ip))
    elif vm_name:
        content = si.RetrieveContent()
        vm = get_obj(content, [vim.VirtualMachine], vm_name)
        logging.info("被检查的VM是:{}".format(vm_name))

    if not vm:
        return(u"Could not find a virtual machine to examine.")

    return vm 