#!/usr/bin/env python

'''
===============================================================================

 GENERAL DESCRIPTION
    This script performs task that sign the prebuilt images and prepare the
    signing environment for all builds.

===============================================================================
'''
import sys
import sys, getopt
import os
import os.path
import subprocess
import re

log_file = None
meta_root_path = ''
caf_root_path = ''

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

#-------------------------------------------------------------------------#
#--Generate secimage.xml--------------------------------------------------#
#-------------------------------------------------------------------------#
def gen_secimage_xml():
    global meta_root_path
    input_file = meta_root_path + '/common/cmti/SecurityBoot/cmti_aione_secimage.xml'
    output_file = meta_root_path + '/common/cmti/SecurityBoot/secimage.xml'
    if not os.path.exists(input_file):
        print '###ERR:Original xml file "%s" Doesn\'t exsit!' % input_file
        sys.exit()

    fb_in = open(input_file)
    input_file_content = fb_in.read()
    fb_in.close()

    if os.path.exists(output_file):
        os.remove(output_file)

    origin_content='<data_provisioning>.*\n.*<base_path>.*/sectools/resources/data_prov_assets/</base_path>.*\n.*</data_provisioning>'

    base_path = os.path.join(meta_root_path, 'common/sectools/resources/data_prov_assets/')

    replaced_content='<data_provisioning>\n        <base_path>'+ base_path +'</base_path>\n    </data_provisioning>'

    output_file_content = re.sub(origin_content, replaced_content, input_file_content)
    fb_out = open(output_file, 'w')
    fb_out.write(output_file_content)
    fb_out.close()

    log('file: "%s" is generated.' % os.path.abspath(output_file))

#-------------------------------------------------------------------------#
#--Prepare signing env-----------------------------------------------#
#-------------------------------------------------------------------------#
def prepare_env():
    global meta_root_path
    global caf_root_path
    #--adsp-----------------------------------------------#
    replace_secimage_xml_cmd = 'cp -f ' + meta_root_path + '/common/cmti/SecurityBoot/secimage.xml ' + meta_root_path + '/adsp_proc/sectools/config/integration/secimage.xml'
    log(replace_secimage_xml_cmd)
    task = log_exec(replace_secimage_xml_cmd)
    replace_secimage_xml_cmd = 'cp -f ' + meta_root_path + '/common/cmti/SecurityBoot/secimage.xml ' + meta_root_path + '/adsp_proc/tools/build/scons/sectools/config/integration/secimage.xml'
    log(replace_secimage_xml_cmd)
    task = log_exec(replace_secimage_xml_cmd)

    #--modem----------------------------------------------#
    replace_secimage_xml_cmd = 'cp -f ' + meta_root_path + '/common/cmti/SecurityBoot/secimage.xml ' + meta_root_path + '/modem_proc/tools/build/scons/sectools/config/integration/secimage.xml'
    log(replace_secimage_xml_cmd)
    task = log_exec(replace_secimage_xml_cmd)

    #--rpm------------------------------------------------#
    replace_secimage_xml_cmd = 'cp -f ' + meta_root_path + '/common/cmti/SecurityBoot/secimage.xml ' + meta_root_path + '/rpm_proc/tools/build/scons/sectools/config/integration/secimage.xml'
    log(replace_secimage_xml_cmd)
    task = log_exec(replace_secimage_xml_cmd)

    #--hlos-----------------------------------------------#
    replace_secimage_xml_cmd = 'cp -f ' + meta_root_path + '/common/cmti/SecurityBoot/secimage.xml ' + caf_root_path + '/vendor/qcom/proprietary/common/scripts/SecImage/config/integration/secimage.xml'
    log(replace_secimage_xml_cmd)
    task = log_exec(replace_secimage_xml_cmd)

    #--boot-----------------------------------------------#
    replace_secimage_xml_cmd = 'cp -f ' + meta_root_path + '/common/cmti/SecurityBoot/secimage.xml ' + meta_root_path + '/boot_images/QcomPkg/Tools/sectools/config/integration/secimage.xml'
    log(replace_secimage_xml_cmd)
    task = log_exec(replace_secimage_xml_cmd)

    #--slpi-----------------------------------------------#
    replace_secimage_xml_cmd = 'cp -f ' + meta_root_path + '/common/cmti/SecurityBoot/secimage.xml ' + meta_root_path + '/slpi_proc/tools/build/scons/sectools/config/integration/secimage.xml'
    log(replace_secimage_xml_cmd)
    task = log_exec(replace_secimage_xml_cmd)

    #--trustzone------------------------------------------#
    replace_secimage_xml_cmd = 'cp -f ' + meta_root_path + '/common/cmti/SecurityBoot/secimage.xml ' + meta_root_path + '/trustzone_images/tools/build/scons/sectools/config/integration/secimage.xml'
    log(replace_secimage_xml_cmd)
    task = log_exec(replace_secimage_xml_cmd)
    replace_secimage_xml_cmd = 'cp -f ' + meta_root_path + '/common/cmti/SecurityBoot/secimage.xml ' + meta_root_path + '/trustzone_images/apps/bsp/trustzone/qsapps/build/secimage.xml'
    log(replace_secimage_xml_cmd)
    task = log_exec(replace_secimage_xml_cmd)
    replace_secimage_xml_cmd = 'cp -f ' + meta_root_path + '/common/cmti/SecurityBoot/secimage.xml ' + meta_root_path + '/trustzone_images/core/bsp/trustzone/qsapps/build/secimage.xml'
    log(replace_secimage_xml_cmd)
    task = log_exec(replace_secimage_xml_cmd)

#-------------------------------------------------------------------------#
#--Presigning images------------------------------------------------------#
#-------------------------------------------------------------------------#

def sign_image(sign_in, sign_out_dir, sign_id, encrypted=False):
    global meta_root_path
    log("------------------------------------------------------------------------")
    log("--Signing %s--" % sign_id)
    log("------------------------------------------------------------------------")
    sign_tools = meta_root_path + '/common/sectools/sectools.py'
    sign_cfg = meta_root_path + '/common/cmti/SecurityBoot/secimage.xml'
    sign_name = os.path.basename(sign_in)
    sign_flag = ' -sa'
    sign_cmd = 'python ' + sign_tools + ' secimage -i ' + sign_in + ' -o ' + sign_out_dir + '/signed' + ' -g ' + sign_id + ' -c ' + sign_cfg + sign_flag
    log(sign_cmd)
    task = log_exec(sign_cmd)
    cp_cmd = 'cp -f ' + sign_out_dir + '/signed/default/' + sign_id + '/' + sign_name + ' ' + sign_out_dir + '/signed'
    log(cp_cmd)
    task = log_exec(cp_cmd)
    if encrypted:
        sign_flag = ' -sea'
        sign_cmd = 'python ' + sign_tools + ' secimage -i ' + sign_in + ' -o ' + sign_out_dir + '/signed_encrypted' + ' -g ' + sign_id + ' -c ' + sign_cfg + sign_flag
        log(sign_cmd)
        task = log_exec(sign_cmd)
        cp_cmd = 'cp -f ' + sign_out_dir + '/signed_encrypted/default/' + sign_id + '/' + sign_name + ' ' + sign_out_dir + '/signed_encrypted'
        log(cp_cmd)
        task = log_exec(cp_cmd)
    cp_cmd = 'cp -f ' + sign_out_dir + '/signed/' + sign_name + ' ' + sign_out_dir
    log(cp_cmd)
    task = log_exec(cp_cmd)

def sign_prebuilt_images():
    global meta_root_path
    pre_signed_image_dict = {'tz':(meta_root_path + '/trustzone_images/build/ms/bin/IADAANAA/tz.mbn',
               meta_root_path + '/trustzone_images/build/ms/bin/IADAANAA'),
         'keymaster':(meta_root_path + '/trustzone_images/build/ms/bin/IADAANAA/keymaster.mbn',
               meta_root_path + '/trustzone_images/build/ms/bin/IADAANAA'),
         'cmnlib':(meta_root_path + '/trustzone_images/build/ms/bin/IADAANAA/cmnlib.mbn',
               meta_root_path + '/trustzone_images/build/ms/bin/IADAANAA'),
         'cmnlib64':(meta_root_path + '/trustzone_images/build/ms/bin/IADAANAA/cmnlib64.mbn',
               meta_root_path + '/trustzone_images/build/ms/bin/IADAANAA'),
         'hyp':(meta_root_path + '/trustzone_images/build/ms/bin/IADAANAA/hyp.mbn',
               meta_root_path + '/trustzone_images/build/ms/bin/IADAANAA'),
         'venus':(meta_root_path + '/venus_proc/build/bsp/asic/build/PROD/mbn/reloc/venus.mbn',
               meta_root_path + '/venus_proc/build/bsp/asic/build/PROD/mbn/reloc'),
         'cppf':(meta_root_path + '/trustzone_images/build/ms/bin/IADAANAA/unsigned/cppf.mbn',
               meta_root_path + '/trustzone_images/build/ms/bin/IADAANAA'),
         'fingerprint64':(meta_root_path + '/trustzone_images/build/ms/bin/IADAANAA/unsigned/fingerprint64.mbn',
               meta_root_path + '/trustzone_images/build/ms/bin/IADAANAA'),
         'gptest':(meta_root_path + '/trustzone_images/build/ms/bin/IADAANAA/unsigned/gptest.mbn',
               meta_root_path + '/trustzone_images/build/ms/bin/IADAANAA'),
         'isdbtmm':(meta_root_path + '/trustzone_images/build/ms/bin/IADAANAA/unsigned/isdbtmm.mbn',
               meta_root_path + '/trustzone_images/build/ms/bin/IADAANAA'),
         'mdtp':(meta_root_path + '/trustzone_images/build/ms/bin/IADAANAA/unsigned/mdtp.mbn',
               meta_root_path + '/trustzone_images/build/ms/bin/IADAANAA'),
         'qmpsecap':(meta_root_path + '/trustzone_images/build/ms/bin/IADAANAA/unsigned/qmpsecap.mbn',
               meta_root_path + '/trustzone_images/build/ms/bin/IADAANAA'),
         'securemm':(meta_root_path + '/trustzone_images/build/ms/bin/IADAANAA/unsigned/securemm.mbn',
               meta_root_path + '/trustzone_images/build/ms/bin/IADAANAA'),
         'widevine':(meta_root_path + '/trustzone_images/build/ms/bin/IADAANAA/unsigned/widevine.mbn',
               meta_root_path + '/trustzone_images/build/ms/bin/IADAANAA'),
         'cmnlib':(meta_root_path + '/trustzone_images/build/ms/bin/IADAANAA/unsigned/cmnlib.mbn',
               meta_root_path + '/trustzone_images/build/ms/bin/IADAANAA'),
         'cmnlib64':(meta_root_path + '/trustzone_images/build/ms/bin/IADAANAA/unsigned/cmnlib64.mbn',
               meta_root_path + '/trustzone_images/build/ms/bin/IADAANAA'),
        }
    for sign_id in pre_signed_image_dict:
        sign_in, sign_out_dir= pre_signed_image_dict[sign_id]
        sign_image(sign_in, sign_out_dir, sign_id, True)

#-------------------------------------------------------------------------#
#--Deal with special case-------------------------------------------------#
#-------------------------------------------------------------------------#
#----Sign a530_zap.elf----------------------------------------------------#
def sign_a530():
    global meta_root_path
    global caf_root_path
    sign_in = caf_root_path + '/vendor/qcom/proprietary/prebuilt_HY11/target/product/msm8996/system/etc/firmware/a530_zap.elf'
    sign_out_dir = meta_root_path + '/common/cmti/SecurityBoot/out'
    sign_id = 'gfx_microcode'
    if not os.path.exists(sign_out_dir):
        os.mkdir(sign_out_dir)
    sign_image(sign_in, sign_out_dir, sign_id)
    sign_in_dir = os.path.dirname(sign_in)
    cp_cmd = 'cp -f ' + sign_out_dir + '/signed/default/gfx_microcode/a530_zap.*' + ' ' + sign_in_dir
    log(cp_cmd)
    task = log_exec(cp_cmd)
#----Sign mcfg_sw.mbn/mcfg_hw.mbn-----------------------------------------#
def sign_mcfg():
    global meta_root_path
    cmd = 'find ' + meta_root_path + '/modem_proc/mcfg/configs/ -name mcfg_sw.mbn -type f'
    task_sign = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    mcfg_file = task_sign.stdout.readline().strip('\n')
    while mcfg_file:
        sign_in = mcfg_file
        sign_out_dir = meta_root_path + '/common/cmti/SecurityBoot/out'
        if not os.path.exists(sign_out_dir):
            os.mkdir(sign_out_dir)
        sign_id = 'mcfg_sw'
        log(mcfg_file)
        sign_image(sign_in, sign_out_dir, sign_id)
        cp_cmd = 'cp -f ' + sign_out_dir + '/mcfg_sw.mbn' + ' ' + sign_in
        log(cp_cmd)
        task_cp = log_exec(cp_cmd)
        mcfg_file = task_sign.stdout.readline().strip('\n')

    cmd = 'find ' + meta_root_path + '/modem_proc/mcfg/configs/ -name mcfg_hw.mbn -type f'
    task_sign = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    mcfg_file = task_sign.stdout.readline().strip('\n')
    while mcfg_file:
        sign_in = mcfg_file
        sign_out_dir = meta_root_path + '/common/cmti/SecurityBoot/out'
        if not os.path.exists(sign_out_dir):
            os.mkdir(sign_out_dir)
        sign_id = 'mcfg_hw'
        log(mcfg_file)
        sign_image(sign_in, sign_out_dir, sign_id)
        cp_cmd = 'cp -f ' + sign_out_dir + '/mcfg_hw.mbn' + ' ' + sign_in
        log(cp_cmd)
        task_cp = log_exec(cp_cmd)
        mcfg_file = task_sign.stdout.readline().strip('\n')

#-------------------------------------------------------------------------#
#--Main Functions---------------------------------------------------------#
#-------------------------------------------------------------------------#
def clean():
    cmd = 'rm -f ' + meta_root_path + '/common/cmti/SecurityBoot/prepare_env_log*'
    task = subprocess.call(cmd, shell=True)
    cmd = 'rm -f ' + meta_root_path + '/common/cmti/SecurityBoot/secimage.xml'
    task = subprocess.call(cmd, shell=True)
    cmd = 'rm -rf '+ meta_root_path + '/common/cmti/SecurityBoot/out'
    task = subprocess.call(cmd, shell=True)

def usage():
    print 'Usage:'
    print '    %s -h, --help              Show This page' %  sys.argv[0]
    print '    %s -c, --clean             Remove the log files and generated files and dirs' %  sys.argv[0]
    print '    %s -s, --set_caf_path=xxx  Indicate source code path of caf build' %  sys.argv[0]
    print '\nExample:'
    print '    %s --set_caf_path=/home/user/caf_src/' %  sys.argv[0]
    print ''

def main():
    global meta_root_path
    global caf_root_path
    meta_root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    caf_root_path = meta_root_path + '/LINUX/android'
    caf_path_opt = ''

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hcs:", ["help", "clean", "set_caf_path="])
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
        elif op in ("-s", "--set_caf_path"):
            caf_path_opt = value

    if caf_path_opt:
        caf_root_path = caf_path_opt

    log_file_name = meta_root_path + '/common/cmti/SecurityBoot/prepare_env_log'
    log_init(log_file_name)

    log('meta_root_path: "%s"' % meta_root_path)
    log('caf_root_path: "%s"' % caf_root_path)

    gen_secimage_xml()
    prepare_env()
    sign_prebuilt_images()
    sign_a530()
    sign_mcfg()

    log_deinit()

main()
