#! /usr/bin/env python
from subprocess import call,Popen, PIPE
import sys, os, shutil

cloud_repl_password = 'password'
mysql_root_password = 'PaSSw0rd1234'
savedHome = os.getcwd()


def setUp():
        call(["rpm","-Uvh", "http://mirror.pnl.gov/epel/6/x86_64/epel-release-6-8.noarch.rpm"], shell=False)
        call(["yum","install", "wget", "-y"], shell=False)
        call(["yum","install", "python-setuptools", "-y"], shell=False)
        call(["yum","install", "ansible", "-y"], shell=False)
        call(["yum","install", "nodejs", "-y"], shell=False)
        call(["yum","install", "npm", "-y"], shell=False)
        call(["npm","update"], shell=False)
        call(["npm","install", "forever", "-g"], shell=False)
        call(["service","iptables", "stop"], shell=False)
        call(["chkconfig","iptables", "off"], shell=False)

def getRPMS(repo):
        # Download rpm packages from remote repository
        os.chdir(savedHome + '/public')
        call(["wget","--no-parent", "-r", "--reject", "index.html*", "http://cloudstack.apt-get.eu/rhel/%s/" % repo], shell=False)
        os.chdir(savedHome)

def getSystemtemplate(repo):
        # Download rpm packages from remote repository
        if repo == '4.3':
                os.chdir(savedHome + '/public/templates/4.3/')
                call(["wget","http://download.cloud.com/templates/4.3/systemvm64template-2014-01-14-master-kvm.qcow2.bz2"], shell=False)
                #call(["wget","http://download.cloud.com/templates/4.3/systemvm64template-2014-01-14-master-xen.vhd.bz2"], shell=False)
                #call(["wget","http://download.cloud.com/templates/4.3/systemvm64template-2014-01-14-master-vmware.ova"], shell=False)
                os.chdir(savedHome)
        if repo == '4.2':
                os.chdir(savedHome + '/public/templates/4.2/')
                os.chdir('public/template/4.2/')
                call(["wget","http://download.cloud.com/templates/4.2/systemvmtemplate-2013-06-12-master-kvm.qcow2.bz2"], shell=False)
                os.chdir(savedHome)

def startnode():
        # Check if webserver is already running. If so, kill and restart new process
        chkprog = Popen(['node_modules/forever/bin/forever', 'list'], stdout=PIPE)
        stdout, stderr = chkprog.communicate()
        a = stdout.split('\n')
        if len(a) > 2:
                for l in a: 
                        try:
                                id = l.split(' ')[4][1:-1]
                                Popen(['node_modules/forever/bin/forever', 'stop', '%s' % id], stderr=PIPE)
                        except: pass
        print('Starting webserver........')
        print ""
        prog = Popen(['node_modules/forever/bin/forever', 'start', 'app.js'], stderr=PIPE)
        errdata = prog.communicate()[1]
        if len(errdata) != 0:
                print errdata.strip("\n")
        if len(errdata) == 0: 
                pass
        
def stopnode():
        # Check if webserver is already running. If so, kill and restart new process
        chkprog = Popen(['node_modules/forever/bin/forever', 'list'], stdout=PIPE)
        stdout, stderr = chkprog.communicate()
        a = stdout.split('\n')
        if len(a) > 2:
                for l in a: 
                        try:
                                id = l.split(' ')[4][1:-1]
                                Popen(['node_modules/forever/bin/forever', 'stop', '%s' % id], stderr=PIPE)
                        except: pass
                print('Stopped webserver........')
        else:
                print('No webservers found........')
        print('')

def startall():
        # ansible-playbook -i ./ansible/hosts ./ansible/run-all.yml -k
        start_now = Popen(['ansible-playbook', '-i', './ansible/hosts', './ansible/play-books/run-all.yml', '-k'], stderr=PIPE)
        errdata = start_now.communicate()[1]
        if len(errdata) != 0:
                print errdata.strip("\n")

def startall_in_one():
        # ansible-playbook -i ./ansible/hosts ./ansible/run-all.yml -k
        start_now = Popen(['ansible-playbook', '-i', './ansible/hosts', './ansible/play-books/all-in-one.yml', '-k'], stderr=PIPE)
        errdata = start_now.communicate()[1]
        if len(errdata) != 0:
                print errdata.strip("\n")
def runfileupdates():
        # ansible-playbook -i ./ansible/hosts ./ansible/run-all.yml -k
        start_now = Popen(['ansible-playbook', '-i', './ansible/hosts', './ansible/play-books/cldstk-files-update.yml', '-k'], stderr=PIPE)
        errdata = start_now.communicate()[1]
        if len(errdata) != 0:
                print errdata.strip("\n")

def kvm_agent_Install():
        # ansible-playbook -i ./ansible/hosts ./ansible/run-all.yml -k
        start_now = Popen(['ansible-playbook', '-i', './ansible/hosts', './ansible/play-books/cldstk-agent_deploy.yml', '-k'], stderr=PIPE)
        errdata = start_now.communicate()[1]
        if len(errdata) != 0:
                print errdata.strip("\n")

def management_Install():
        # ansible-playbook -i ./ansible/hosts ./ansible/run-all.yml -k
        start_now = Popen(['ansible-playbook', '-i', './ansible/hosts', './ansible/play-books/cldstk-mgmt_deploy.yml', '-k'], stderr=PIPE)
        errdata = start_now.communicate()[1]
        if len(errdata) != 0:
                print errdata.strip("\n")

def db_Install():
        # ansible-playbook -i ./ansible/hosts ./ansible/run-all.yml -k
        start_now = Popen(['ansible-playbook', '-i', './ansible/hosts', './ansible/play-books/mysql-server-install.yml', '-k'], stderr=PIPE)
        errdata = start_now.communicate()[1]
        if len(errdata) != 0:
                print errdata.strip("\n")

def db_replication_Install():
        # ansible-playbook -i ./ansible/hosts ./ansible/run-all.yml -k
        start_now = Popen(['ansible-playbook', '-i', './ansible/hosts', './ansible/play-books/mysql-replication-setup.yml', '-k'], stderr=PIPE)
        errdata = start_now.communicate()[1]
        if len(errdata) != 0:
                print errdata.strip("\n")

def systemtemplate_Install():
        # ansible-playbook -i ./ansible/hosts ./ansible/run-all.yml -k
        start_now = Popen(['ansible-playbook', '-i', './ansible/hosts', './ansible/play-books/cldstk-preseed-kvm-systmpl.yml', '-k'], stderr=PIPE)
        errdata = start_now.communicate()[1]
        if len(errdata) != 0:
                print errdata.strip("\n")

def main():
        print ""
        print "Cloudstack Deployment: Answer the questions below...."
        print ""
        installmysql = raw_input('Install MySQL?[Y/n]: ')

        if installmysql.lower() == 'y':
                db_master = raw_input('Db Server[dns/ip]: ')
        else:
                db_master = ''

        if installmysql.lower() == 'n':
                mgmt_master = raw_input('Whats the current DB Server?[dns/ip]: ')
        else:
                mgmt_master = ''

        installmysqlreplica = raw_input('Install MySQL Replica?[Y/n]: ')

        if installmysqlreplica.lower() == 'y':
                db_slave = raw_input('Db Replica Server[dns/ip]: ')
        else:
                db_slave = ''

        installmgmtsrv = raw_input('Install Management Server?[Y/n]: ')

        if installmgmtsrv.lower() == 'y':
                cldstk_mgmt = raw_input('Server[dns/ip]: ')
        else:
                cldstk_mgmt = ''

        installwebsrv = raw_input('Install additional Management servers?[Y/n]: ')

        if installwebsrv.lower() == 'y':
                cldstk_web = raw_input('Comma separated list: ')
        else:
                cldstk_web = ''

        installkvmhost = raw_input('Install KVM Hosts?[Y/n]: ')

        if installkvmhost.lower() == 'y':
                cldstk_kvmhost = raw_input('Comma separated list: ')
        else:
                cldstk_kvmhost = ''

        preseedtemplates = raw_input('Install System Templates?[Y/n]: ')

        if preseedtemplates.lower() == 'y':
                nfs_server = raw_input('NFS Server[dns/ip]: ')
        else:
                nfs_server = ''

        if preseedtemplates.lower() == 'y':
                nfs_path = raw_input('NFS Path[/nfsdirpath]: ')
        else:
                nfs_path = ''


        # Write the /etc/ansible/hosts file
        if len(db_master) != 0:
                hostsfile = open('./ansible/hosts','w')
                hostsfile.write('[localhost]\n127.0.0.1\n\n')
                hostsfile.write('[db_master]\n%s\n' % db_master)

                if len(db_slave) != 0:
                        hostsfile.write('\n[db_slave]\n%s\n' % db_slave)

                hostsfile.write('\n[mysql_servers]\n%s\n' % db_master)
                if len(db_slave) != 0:
                        hostsfile.write('%s\n' % db_slave)

                if len(cldstk_mgmt) != 0:
                        hostsfile.write('\n[cldstk_mgmt]\n')
                        cldstk_mgmt = cldstk_mgmt.split(',')[0]
                        hostsfile.write('%s\n' % cldstk_mgmt)

                if len(cldstk_web) != 0:
                        hostsfile.write('\n[cldstk_web]\n')
                        cldstk_web = cldstk_web.split(',')
                        for w in cldstk_web:
                                hostsfile.write('%s\n' % w.strip())

                if len(cldstk_kvmhost) != 0:
                        hostsfile.write('\n[cldstk_kvm]\n')
                        cldstk_kvmhost = cldstk_kvmhost.split(',')
                        for k in cldstk_kvmhost:
                                hostsfile.write('%s\n' % k.strip())

                hostsfile.close()
                print('ansible hosts file successfully writing to disk.....')

                # Write the vars_file.yml file
                if len(db_master) != 0:
                        vars_file = open('./ansible/vars_file.yml','w')
                        vars_file.write('mgmt_primary: %s\n' % cldstk_mgmt)
                        vars_file.write('master: %s\n' % db_master)
                        vars_file.write('slave: %s\n' % db_slave)
                        vars_file.write('cloud_repl_password: %s\n' % cloud_repl_password)
                        vars_file.write('mysql_root_password: %s\n' % mysql_root_password)
                        vars_file.write('nfs_server: %s\n' % nfs_server)
                        vars_file.write('nfs_path: %s\n' % nfs_path)
                        vars_file.write('repotype: Internet\n')
                        vars_file.write('repoversion: 4.3\n')
                        vars_file.write('systemtemplate: \n')
                        vars_file.close()
                else:
                        vars_file = open('./ansible/vars_file.yml','w')
                        vars_file.write('mgmt_primary: %s\n' % cldstk_mgmt)
                        vars_file.write('master: %s\n' % mgmt_master)
                        vars_file.write('slave: %s\n' % db_slave)
                        vars_file.write('cloud_repl_password: %s\n' % cloud_repl_password)
                        vars_file.write('mysql_root_password: %s\n' % mysql_root_password)
                        vars_file.write('nfs_server: %s\n' % nfs_server)
                        vars_file.write('nfs_path: %s\n' % nfs_path)
                        vars_file.write('repotype: Internet\n')
                        vars_file.write('repoversion: 4.3\n')
                        vars_file.write('systemtemplate: \n')
                        vars_file.close()

                print('vars_file successfully writing to disk.....')
                
                startinstallation = raw_input('Start installation now?[Y/n]: ')

                if startinstallation.lower() == 'y':
                        startall()
                else:
                        print('Exiting program......')
                        sys.exit()

        else:
                print('You must provide the Master Database Server...')
                main()

if __name__ == '__main__':
        if len(sys.argv) == 2 and sys.argv[1] == '-s':
                startnode()
                print('')
                print('Started webserver........')
                print('Browse to: http://localhost:3000')
                print('')
                sys.exit()
        elif len(sys.argv) == 2 and sys.argv[1] == '-S':
                stopnode()
                sys.exit()
        elif len(sys.argv) == 3 and sys.argv[1] == 'get':
                if sys.argv[2].split('=')[0] == 'rpmversion' and len(sys.argv[2].split('=')[1]) != 0:
                        getRPMS('%s' % sys.argv[2].split('=')[1])
                elif sys.argv[2].split('=')[0] == 'systemtemplate' and len(sys.argv[2].split('=')[1]) != 0:
                        getSystemtemplate('%s' % sys.argv[2].split('=')[1])
                else:
                        print('Wrong Syntax.....')
        elif len(sys.argv) == 3 and sys.argv[1] == 'setup':
                if sys.argv[2] == 'all':
                        setUp()
                else:
                        print('Wrong Syntax.....')
        elif len(sys.argv) == 3 and sys.argv[1] == 'install':
                startnode()
                print('')
                print('Started webserver........')
                print('Browse to: http://localhost:3000')
                print('')
                if sys.argv[2] == 'all':
                        startall()
                elif sys.argv[2] == 'all-in-one':
                        startall_in_one()
                elif sys.argv[2] == 'kvm-agent':
                        runfileupdates()
                        kvm_agent_Install()
                elif sys.argv[2] == 'management':
                        runfileupdates()
                        management_Install()
                elif sys.argv[2] == 'db':
                        runfileupdates()
                        db_Install()
                elif sys.argv[2] == 'db-replication':
                        runfileupdates()
                        db_replication_Install()
                elif sys.argv[2] == 'systemtemplate':
                        systemtemplate_Install()
                sys.exit()
        else:
                main()