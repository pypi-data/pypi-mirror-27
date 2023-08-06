import os, sys, platform, socket
import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer
from subprocess import Popen

server_port = 9000


def run_remote_imperas(name, port):
    root = '/opt/imgtec/Hardware Support/Simulators/MIPS-IASim'
    library_location = os.path.join(root, 'bin', 'Linux64')
    env = os.environ
    env['IMPERAS_MDI_PORT'] = str(port)
    env['IMPERAS_HOME'] = os.path.join(root, )
    env['IMPERAS_VLNV'] = os.path.join(root, 'lib', 'Linux64', 'ImperasLib')
    env['IMPERAS_RUNTIME'] = 'OVPsimMIPS'
    env['LD_LIBRARY_PATH'] = os.path.pathsep.join([env.get('LD_LIBRARY_PATH', ''), library_location])
    env['PATH'] = os.path.pathsep.join([env.get('PATH', ''), library_location])

    name, endian = name.split('-')

    sim_executable = os.path.join(root, 'bin', 'Linux64', 'mips-iasim')
    sim_command = [sim_executable, name, endian]

    print sim_command
    return Popen(sim_command, env=env)


def run_meta_simulator(name, port):
    root = '/opt/imgtec/Hardware Support/Simulators'
    env = os.environ
    env['METACCONFIG'] = os.path.join(root, name, 'metac-sim.metaconfig')

    sim_executable = os.path.join(root, name, 'metac-sim')
    sim_command = [sim_executable, '-sap-comms=%s' % port]

    print sim_command
    return Popen(sim_command, env=env)


class Server(object):
    def __init__(self, starting_port=9001):
        self.port_count = starting_port
        self.running_simulators = {}

    def start_simulator(self, name, type):
        hostname = socket.getfqdn()
        if type == "Meta":
            simulator = run_meta_simulator(name, self.port_count)
            remote_name = 'RemoteSimulator %s:%s' % (hostname, self.port_count)

        elif type == "Mips":
            simulator = run_remote_imperas(name, self.port_count)
            remote_name = 'RemoteImperas %s:%s' % (hostname, self.port_count)

        else:
            valid_simulators = ', '.join(self.list_simulators())
            raise ValueError('Unknown Simulator: %s\nValid Simulators: %s' % (name, valid_simulators))

        self.running_simulators[remote_name] = simulator
        self.port_count += 1
        print "Made new simulator: {0} {1} and its address is {2}".format(name, type, remote_name)
        return remote_name

    def kill_simulator(self, name):
        print "Killing {0}".format(name)
        self.running_simulators[name].terminate()
        del self.running_simulators[name]

    def ping(self):
        return True

if __name__ == "__main__":
    server_instance = Server(starting_port=9001)
    server = SimpleXMLRPCServer(("", server_port), allow_none=True)
    server.register_instance(server_instance)
    server.serve_forever()

