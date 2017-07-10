#!/usr/bin/env python

import sys
import os
import getopt
import re
import subprocess

log_file = None
root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
current_path = os.path.dirname(os.path.abspath(__file__))
unsigned_dir = current_path + '/unsigned'
signed_dir = current_path + '/signed'
out_dir = current_path + '/out'
nonhlos_dir = current_path + '/nonhlos_dir'
original_file_list = [
    'cmnlib64.mbn',
    'cmnlib.mbn',
    'devcfg.mbn',
    'emmc_appsboot.mbn',
    'hyp.mbn',
    'keymaster.mbn',
    'NON-HLOS-UFS.bin',
    'pmic.elf',
    'prog_ufs_firehose_8996_ddr.elf',
    'rpm.mbn',
    'tz.mbn',
    'xbl.elf'
]

original_nonhlos_file_list = [
    'adsp.mbn',
    'cppf.mbn',
    'cmnlib64.mbn',
    'cmnlib.mbn',
    'gptest.mbn',
    'isdbtmm.mbn',
    'mdtp.mbn',
    'qmpsecap.mbn',
    'securemm.mbn',
    'smplap32.mbn',
    'smplap64.mbn',
    'widevine.mbn',
    'fingerprint.mbn',
    'dhsecapp.mbn',
    'qdsp6sw.mbn',
    'mba.mbn',
    'slpi.mbn',
    'venus.mbn'
]

sign_id_dict = {
        'cmnlib64.mbn':'cmnlib64',
        'cmnlib.mbn':'cmnlib',
        'devcfg.mbn':'devcfg',
        'emmc_appsboot.mbn':'appsbl',
        'hyp.mbn':'hyp',
        'keymaster.mbn':'keymaster',
        'pmic.elf':'pmic',
        'prog_ufs_firehose_8996_ddr.elf':'prog_ufs_ddr',
        'rpm.mbn':'rpm',
        'tz.mbn':'tz',
        'xbl.elf':'xbl',
        'adsp.mbn':'adsp',
        'cppf.mbn':'cppf',
        'gptest.mbn':'gptest',
        'isdbtmm.mbn':'isdbtmm',
        'mdtp.mbn':'mdtp',
        'qmpsecap.mbn':'qmpsecap',
        'securemm.mbn':'securemm',
        'smplap32.mbn':'smplap32',
        'smplap64.mbn':'smplap64',
        'widevine.mbn':'widevine',
        'fingerprint.mbn':'fingerprint',
        'dhsecapp.mbn':'dhsecapp',
        'qdsp6sw.mbn':'qdsp6sw',
        'mba.mbn':'mba',
        'slpi.mbn':'slpi',
        'venus.mbn':'venus',
        'a530_zap.elf':'gfx_microcode',
    }

def log_init(log_file_name=None):
    global log_file
    if os.path.exists(log_file_name):
        i = 1
        while os.path.exists(log_file_name + '_%.2d' % (i)):
            i += 1
        os.rename(log_file_name, log_file_name + '_%.2d' % (i))
    if log_file_name:
       log_file = open(log_file_name, 'a+' )
    else:
       log_file = None

def log_deinit():
    global log_file
    if log_file:
       log_file.close()

def log(str, log_to_stdout=True):
    global log_file
    try:
        str = str + '\n'
        if log_file:
            log_file.write(str)
            if log_to_stdout:
                sys.stdout.write(str)
    except IOError:
        print '###ERR: cannot output logs!!!'

def log_exec(cmd, shell=True, log_to_stdout=False):
    task = subprocess.Popen(cmd, shell=shell, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    c = task.stdout.read(1)
    while c:
        global log_file
        log_file.write(c)
        if log_to_stdout:
           sys.stdout.write(c)
        c = task.stdout.read(1)
    task.wait()  # Wait for the task to really complete
    if task.returncode != 0:
        log(cmd[0] + " command returned error: " + str(task.returncode))
    return task.returncode

def sign_image(sign_in, sign_out_dir, sign_id):
    global root_path
    log("------------------------------------------------------------------------")
    log("--Signing %s--" % sign_id)
    log("------------------------------------------------------------------------")
    sign_tools = root_path + '/common/sectools/sectools.py'
    sign_cfg = root_path + '/common/cmti/SecurityBoot/cmti_aione_secimage.xml'
    sign_name = os.path.basename(sign_in)
    sign_cmd = 'python ' + sign_tools + ' secimage -i ' + sign_in + ' -o ' + sign_out_dir + '/signed' + ' -g ' + sign_id + ' -c ' + sign_cfg + ' -sa'
    log(sign_cmd)
    task = log_exec(sign_cmd)

def run_cmd(cmd):
    log(cmd)
    log_exec(cmd)

def cp_original_nonhlos_files(src_dir, unsigned_dir):
    for file_name in original_nonhlos_file_list:
        if not os.path.exists(src_dir + '/' + file_name):
            print 'File: %s cannot be found!'
            sys.exit()
    for file_name in original_nonhlos_file_list:
        if os.path.exists(src_dir + '/' + file_name):
            run_cmd('cp -f ' + src_dir + '/' + file_name + ' ' + unsigned_dir + '/' + file_name)

def cp_original_files_and_rename(version_prefix, src_dir, unsigned_dir):
    for file_name in original_file_list:
        if not os.path.exists(src_dir + '/' + version_prefix + file_name):
            print 'File: %s cannot be found!'
            sys.exit()
    for file_name in original_file_list:
        if os.path.exists(src_dir + '/' + version_prefix + file_name):
            run_cmd('cp -f ' + src_dir + '/' + version_prefix + file_name + ' ' + unsigned_dir + '/' + file_name)

def get_version_prefix(src_dir):
    version_prefix = ''
    for file_name in os.listdir(src_dir):
        if re.search('.*-xbl\.elf', file_name):
            version_prefix = re.sub('xbl\.elf', '', file_name)
            break

    if not version_prefix:
        print 'File: .*-xbl.elf cannot be found!'
        sys.exit()

    return version_prefix

def offical_files_backup():
    global current_path
    global root_path
    if os.path.exists(current_path + '/bakcup'):
        #run_cmd('rm -r ' + current_path + '/bakcup')
        return
    os.mkdir(current_path + '/bakcup')
    file_name = root_path + '/contents.xml'
    if os.path.exists(file_name):
        run_cmd('cp -f ' + file_name + ' ' + current_path + '/bakcup')
    file_name = root_path + '/common/build/app/fat_creation.py'
    if os.path.exists(file_name):
        run_cmd('cp -f ' + file_name + ' ' + current_path + '/bakcup')

def offical_files_restore():
    global current_path
    global root_path
    if os.path.exists(current_path + '/bakcup/contents.xml'):
        run_cmd('cp -f ' + current_path + '/bakcup/contents.xml ' + root_path + '/contents.xml')
    if os.path.exists(current_path + '/bakcup/fat_creation.py'):
        run_cmd('cp -f ' + current_path + '/bakcup/fat_creation.py ' + root_path + '/common/build/app/fat_creation.py')
    if os.path.exists(current_path + '/bakcup'):
        run_cmd('rm -rf ' + current_path + '/bakcup')

def process():
    global current_path
    global original_file_list
    global root_path
    global unsigned_dir
    global signed_dir
    global out_dir
    global nonhlos_dir

    log_file_name = current_path + '/log'
    log_init(log_file_name)

    log('root_path = ' + root_path)
    original_files_dir = current_path + '/original_files'
    log('original_files_dir=' + original_files_dir)
    version_prefix = get_version_prefix(original_files_dir)
    log('version_prefix=' + version_prefix)

    if os.path.exists(unsigned_dir):
        run_cmd('rm -r ' + unsigned_dir)

    if os.path.exists(signed_dir):
        run_cmd('rm -r ' + signed_dir)

    if os.path.exists(out_dir):
        run_cmd('rm -r ' + out_dir)

    if os.path.exists(nonhlos_dir):
        run_cmd('rm -r ' + nonhlos_dir)

    os.mkdir(unsigned_dir)
    os.mkdir(signed_dir)
    os.mkdir(out_dir)

    cp_original_files_and_rename(version_prefix, original_files_dir, unsigned_dir)
    cp_original_nonhlos_files(original_files_dir + '/pil_split_bins', unsigned_dir)
    if os.path.exists(original_files_dir + '/pil_split_bins/a530_zap.elf'):
        run_cmd('cp -f ' + original_files_dir + '/pil_split_bins/a530_zap.elf ' + unsigned_dir)
    else:
        log('File: %s cannot be found!' % original_files_dir + '/pil_split_bins/a530_zap.elf')
        sys.exit()

    offical_files_backup()

    #--Prepare NON-HLOS.bin generating environment--#
    os.mkdir(nonhlos_dir)
    os.mkdir(nonhlos_dir + '/signed_out')
    os.mkdir(nonhlos_dir + '/mnt')
    os.mkdir(nonhlos_dir + '/ori_non_hlos_bin_files_dir')
    os.mkdir(nonhlos_dir + '/ori_non_hlos_bin_work_dir')
    run_cmd('sudo mount ' + unsigned_dir + '/NON-HLOS-UFS.bin ' + nonhlos_dir + '/mnt')
    if not os.path.exists(nonhlos_dir + '/mnt/image'):
        log('### failed to mount NON-HLOS-UFS.bin!!!')
        sys.exit()
    run_cmd('cp -rf ' + nonhlos_dir + '/mnt/* ' + nonhlos_dir + '/ori_non_hlos_bin_files_dir')
    run_cmd('cp -rf ' + nonhlos_dir + '/mnt/* ' + nonhlos_dir + '/ori_non_hlos_bin_work_dir')
    run_cmd('sudo umount ' + nonhlos_dir + '/mnt')
    #==Generate original files md5sum for verify--#
    os.chdir(nonhlos_dir + '/ori_non_hlos_bin_files_dir')
    run_cmd('find . -type f | xargs md5sum >> ../ori_non_hlos_bin_files.md5sum')
    os.chdir(current_path)

    #--Sign images--#
    for file_name in original_file_list:
        if file_name == 'NON-HLOS-UFS.bin':
            continue
        log(file_name + ': ' + sign_id_dict[file_name])
        sign_image(unsigned_dir + '/' + file_name, signed_dir, sign_id_dict[file_name])

    for file_name in original_nonhlos_file_list:
        log(file_name + ': ' + sign_id_dict[file_name])
        sign_image(unsigned_dir + '/' + file_name, signed_dir, sign_id_dict[file_name])

    #--Copy signed images--#
    for file_name in original_file_list:
        if file_name == 'NON-HLOS-UFS.bin':
            continue
        sign_id = sign_id_dict[file_name]
        file_name_tmp = signed_dir + '/signed/default/' + sign_id + '/' + file_name
        if os.path.exists(file_name_tmp):
            run_cmd('cp -f ' + file_name_tmp + ' ' + out_dir)
        else:
            log("###ERR: file %s cannot be found!" % file_name_tmp)
            sys.exit()
    
    for file_name in original_nonhlos_file_list:
        sign_id = sign_id_dict[file_name]
        if file_name == 'mba.mbn':
            file_name_tmp = signed_dir + '/signed/default/' + sign_id + '/' + file_name
            if os.path.exists(file_name_tmp):
                run_cmd('cp -f ' + file_name_tmp + ' ' + nonhlos_dir + '/signed_out')
            else:
                log("###ERR: file %s cannot be found!" % file_name_tmp)
                sys.exit()
            continue
        if file_name == "fingerprint.mbn":
            file_name_tmp = signed_dir + '/signed/default/' + sign_id + '/' + file_name
            if os.path.exists(file_name_tmp):
                run_cmd('python ' + root_path + '/common/config/pil-splitter.py ' + file_name_tmp + ' ' + nonhlos_dir + '/signed_out/fingerpr')
            continue
        file_name_tmp = signed_dir + '/signed/default/' + sign_id + '/' + os.path.splitext(file_name)[0] + '.b00'
        abspath_file_name = signed_dir + '/signed/default/' + sign_id + '/' + file_name
        if os.path.exists(file_name_tmp):
            file_name_tmp = signed_dir + '/signed/default/' + sign_id + '/' + os.path.splitext(file_name)[0] + '.b*'
            run_cmd('cp -f ' + file_name_tmp + ' ' + nonhlos_dir + '/signed_out')
            file_name_tmp = signed_dir + '/signed/default/' + sign_id + '/' + os.path.splitext(file_name)[0] + '.mdt'
            run_cmd('cp -f ' + file_name_tmp + ' ' + nonhlos_dir + '/signed_out')
        elif os.path.exists(abspath_file_name):
            if file_name == 'qdsp6sw.mbn':
                file_name = 'modem.mbn'
            run_cmd('python ' + root_path + '/common/config/pil-splitter.py ' + abspath_file_name + ' ' + nonhlos_dir + '/signed_out/' + os.path.splitext(file_name)[0])
        else:
            log("###ERR: files %s and %s cannot be found!" % (file_name_tmp, abspath_file_name))
            sys.exit()
    
    #--Generate NON-HLOS.bin--#
    if os.path.exists(nonhlos_dir + '/ori_non_hlos_bin_work_dir/image'):
        run_cmd('cp -rf ' + nonhlos_dir + '/signed_out/* ' + nonhlos_dir + '/ori_non_hlos_bin_work_dir/image')
    else:
        log('"###ERR: Target dir %s is not exist!' % nonhlos_dir + '/ori_non_hlos_bin_work_dir/image')
        sys.exit()

    for file_name in os.listdir(nonhlos_dir + '/ori_non_hlos_bin_work_dir/image'):
        abs_path_file_name = nonhlos_dir + '/ori_non_hlos_bin_work_dir/image/' + file_name
        if os.path.isfile(abs_path_file_name) and not os.path.getsize(abs_path_file_name):
            run_cmd('rm -f ' + abs_path_file_name)
    #==Generate final signed files md5sum for verify--#
    os.chdir(nonhlos_dir + '/ori_non_hlos_bin_work_dir')
    run_cmd('find . -type f | xargs md5sum >> ../ori_non_hlos_bin_work.md5sum')
    os.chdir(current_path)

    if os.path.exists(root_path + '/mdm'):
        run_cmd('rm -r ' + root_path + '/mdm')
    run_cmd('mv ' + nonhlos_dir + '/ori_non_hlos_bin_work_dir/image/mdm ' + root_path)
    if os.path.exists(root_path + '/contents.xml'):
        run_cmd('rm -f ' + root_path + '/contents.xml')
    run_cmd('cp -f ' + current_path + '/contents.xml ' + root_path)
    if os.path.exists(root_path + '/common/build/app/fat_creation.py'):
        run_cmd('rm -f ' + root_path + '/common/build/app/fat_creation.py')
    run_cmd('cp -f ' + current_path + '/fat_creation.py ' + root_path + '/common/build/app/fat_creation.py')
    os.chdir(root_path + '/common/build/')
    log('--------------------------------------------------------------------------------')
    run_cmd('python build.py --nonhlos')
    run_cmd('cp ufs/bin/asic/NON-HLOS.bin ../cmti/SecurityBoot/fih/out/NON-HLOS-UFS.bin')
    os.chdir(current_path)

    run_cmd('mv ' + root_path + '/mdm '+ nonhlos_dir + '/ori_non_hlos_bin_work_dir/image/')
    run_cmd('sudo mount ' + out_dir + '/NON-HLOS-UFS.bin ' + nonhlos_dir + '/mnt')
    #--Generate final md5sum for verify--#
    os.chdir(nonhlos_dir + '/mnt')
    run_cmd('find . -type f | xargs md5sum >> ../mnt.md5sum')
    os.chdir(current_path)
    run_cmd('sudo umount ' + nonhlos_dir + '/mnt')

    #--Change signed images name back--#
    for file_name in original_file_list:
        if os.path.exists(out_dir + '/' + file_name):
            os.rename(out_dir + '/' + file_name, out_dir + '/' + version_prefix + file_name)
        else:
            log("###ERR: file %s cannot be found!" % out_dir + '/' + file_name)
            sys.exit()

    #--Deal with special case--#
    file_name = 'a530_zap.elf'
    sign_id = sign_id_dict[file_name]
    sign_image(unsigned_dir + '/' + file_name, signed_dir, sign_id)
    file_name_tmp = signed_dir + '/signed/default/' + sign_id + '/' + os.path.splitext(file_name)[0] + '.b00'
    abspath_file_name = signed_dir + '/signed/default/' + sign_id + '/' + file_name
    if os.path.exists(abspath_file_name):
        run_cmd('cp -f ' + abspath_file_name + ' ' + out_dir)
    if os.path.exists(file_name_tmp):
        file_name_tmp = signed_dir + '/signed/default/' + sign_id + '/' + os.path.splitext(file_name)[0] + '.b*'
        run_cmd('cp -f ' + file_name_tmp + ' ' + out_dir)
        file_name_tmp = signed_dir + '/signed/default/' + sign_id + '/' + os.path.splitext(file_name)[0] + '.mdt'
        run_cmd('cp -f ' + file_name_tmp + ' ' + out_dir)
    elif os.path.exists(abspath_file_name):
        run_cmd('python ' + root_path + '/common/config/pil-splitter.py ' + abspath_file_name + ' ' + out_dir + '/' + os.path.splitext(file_name)[0])
    else:
        log("###ERR: files %s and %s cannot be found!" % (file_name_tmp, abspath_file_name))

    # In nonhlos_dir
    #   vim mnt.md5sum ori_non_hlos_bin_files.md5sum ori_non_hlos_bin_work.md5sum
    #   :sort /^[0-9a-z]*  \.\//
    # Then compare the mnt.md5sum and ori_non_hlos_bin_work.md5sum, if same, verify passes
    # and the difference between mnt.md5sum ori_non_hlos_bin_files.md5sum, are the signed images
        

    offical_files_restore()
    log_deinit()
    
def clean():
    global current_path
    global unsigned_dir
    global signed_dir
    global out_dir
    global nonhlos_dir
    log_file_name = current_path + '/log'
    log_init(log_file_name)
    if os.path.exists(unsigned_dir):
        run_cmd('rm -r ' + unsigned_dir)

    if os.path.exists(signed_dir):
        run_cmd('rm -r ' + signed_dir)

    if os.path.exists(out_dir):
        run_cmd('rm -r ' + out_dir)

    if os.path.exists(nonhlos_dir):
        run_cmd('rm -r ' + nonhlos_dir)
    run_cmd('rm -f log*')
    log_deinit()

def usage():
    print 'Usage:'
    print '    %s -h, --help              Show This page' %  sys.argv[0]
    print '    %s -c, --clean             Remove the log files and generated files and dirs' %  sys.argv[0]
    print '\nExample:'
    print '    %s' %  sys.argv[0]
    print ''

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc", ["help", "clean"])
    except getopt.GetoptError:
        usage()
        sys.exit()
 
    for op, value in opts:
        if op in ("-h", "--help"):
            usage()
            sys.exit()
        elif op in ("-c", "--clean"):
            clean()
            sys.exit()

    process()

if __name__ == '__main__':
    main()
