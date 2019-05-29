from pyVim.connect import SmartConnectNoSSL, Disconnect
import atexit
import argparse
import getpass



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
